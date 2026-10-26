"""Shared pipeline code for UtilityRAG.

ingest.py, ask.py and evaluate.py all import from here, so the indexing,
retrieval, and prompt settings stay identical between the scripts.
The notebook UtilityRAG.ipynb walks through the same steps one at a time.
"""

import os
import re
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

# ---------------------------------------------------------------- settings
ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
CHROMA_DIR = ROOT / "chroma_db"
EVAL_FILE = ROOT / "eval" / "questions.json"
RESULTS_DIR = ROOT / "results"

COLLECTION = "utilityrag"
LLM_MODEL = "claude-haiku-5-5"
EMBED_MODEL = "voyage-3.5-lite"
TOP_K = 4
ABSTAIN_PHRASE = "not in the docs"

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]


# ---------------------------------------------------------------- keys
def load_keys():
    """Load API keys from .env, falling back to the *_api_key.txt files."""
    load_dotenv(ROOT / ".env")
    fallbacks = {
        "ANTHROPIC_API_KEY": "anthropic_api_key.txt",
        "VOYAGE_API_KEY": "voyage_ai_api_key.txt",
        "LANGCHAIN_API_KEY": "langchain_api_key.txt",
    }
    for var, fname in fallbacks.items():
        path = ROOT / fname
        if not os.getenv(var) and path.exists():
            os.environ[var] = path.read_text(encoding="utf-8").strip()
    return {var: bool(os.getenv(var)) for var in fallbacks}


# ---------------------------------------------------------------- models
def get_llm():
    from langchain_anthropic import ChatAnthropic

    # No temperature: the Claude API rejects sampling parameters as of 2026-10-21.
    return ChatAnthropic(model=LLM_MODEL, max_tokens=4096)


def get_embeddings():
    import time

    import voyageai.error
    from langchain_voyageai import VoyageAIEmbeddings

    class RetryingVoyageEmbeddings(VoyageAIEmbeddings):
        """Waits and retries when Voyage rate-limits.

        Without a payment method on file, Voyage allows only 3 requests/minute.
        """

        def _retry(self, fn, *args):
            for attempt in range(6):
                try:
                    return fn(*args)
                except voyageai.error.RateLimitError:
                    if attempt == 5:
                        raise
                    print("Voyage rate limit hit, waiting 25 s...")
                    time.sleep(25)

        def embed_documents(self, texts):
            return self._retry(super().embed_documents, texts)

        def embed_query(self, text):
            return self._retry(super().embed_query, text)

    return RetryingVoyageEmbeddings(model=EMBED_MODEL)


# ---------------------------------------------------------------- indexing
def load_docs(docs_dir=DOCS_DIR):
    """Read every Markdown file in docs/ into a LangChain Document."""
    docs = []
    for path in sorted(Path(docs_dir).glob("*.md")):
        docs.append(
            Document(page_content=path.read_text(encoding="utf-8"),
                     metadata={"source": path.name})
        )
    return docs


def split_docs(docs, chunk_size=1200, chunk_overlap=150):
    """Split by Markdown heading first, then by size for long sections.

    Each chunk keeps its source file name and heading path in metadata,
    which is what the answer cites.
    """
    header_splitter = MarkdownHeaderTextSplitter(HEADERS, strip_headers=False)
    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in docs:
        sections = header_splitter.split_text(doc.page_content)
        for section in size_splitter.split_documents(sections):
            section.metadata["source"] = doc.metadata["source"]
            section.metadata["section"] = " > ".join(
                section.metadata[h] for _, h in HEADERS if h in section.metadata
            )
            chunks.append(section)
    return chunks


def build_vectorstore(chunks, embeddings=None, persist_dir=CHROMA_DIR):
    """Embed chunks into a fresh Chroma collection (old one is replaced)."""
    from langchain_chroma import Chroma

    embeddings = embeddings or get_embeddings()
    store = Chroma(collection_name=COLLECTION, embedding_function=embeddings,
                   persist_directory=str(persist_dir))
    store.reset_collection()  # re-running ingest never duplicates chunks
    ids = [f"{c.metadata['source']}::{i}" for i, c in enumerate(chunks)]
    store.add_documents(chunks, ids=ids)
    return store


def load_vectorstore(embeddings=None, persist_dir=CHROMA_DIR):
    from langchain_chroma import Chroma

    if not Path(persist_dir).exists():
        raise FileNotFoundError("No index found. Run `python ingest.py` first.")
    return Chroma(collection_name=COLLECTION,
                  embedding_function=embeddings or get_embeddings(),
                  persist_directory=str(persist_dir))


# ---------------------------------------------------------------- prompts
RAG_TEMPLATE = """You are UtilityRAG, an assistant for GIS conversion analysts at GridLine Data Services.

Answer the question using ONLY the context below. Rules:
- Cite the source file in square brackets after each fact, e.g. [04_qa_thresholds.md].
- Cooperative-specific pages override the general standards when they conflict.
- If the context does not contain the answer, reply with exactly: {abstain}
- Do not use outside knowledge to fill gaps. Keep the answer short.

Context:
{context}

Question: {question}
"""

BASELINE_TEMPLATE = """You are an assistant for GIS conversion analysts at GridLine Data Services, a company that converts electric cooperative GIS data into its own target model.

Answer the question. Keep the answer short. If you do not know the answer, reply with exactly: {abstain}

Question: {question}
"""

# Open baseline: the bare question, no company context and no permission to abstain.
# This is how an analyst would use a general chatbot.
OPEN_BASELINE_TEMPLATE = "{question}"

rag_prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE).partial(abstain=ABSTAIN_PHRASE)
baseline_prompt = ChatPromptTemplate.from_template(BASELINE_TEMPLATE).partial(abstain=ABSTAIN_PHRASE)
open_baseline_prompt = ChatPromptTemplate.from_template(OPEN_BASELINE_TEMPLATE)


def format_docs(docs):
    """Label each chunk with its file and section so the LLM can cite it."""
    return "\n\n---\n\n".join(
        f"[source: {d.metadata['source']} | section: {d.metadata.get('section', '')}]\n"
        f"{d.page_content}"
        for d in docs
    )


# ---------------------------------------------------------------- chains
def build_rag_chain(retriever, llm):
    """Returns {"context": [Document], "question": str, "answer": str}.

    Same pattern as the rag-from-scratch "rag_chain_with_source": retrieve
    once, keep the documents, and pass them to the prompt.
    """
    answer = (
        RunnablePassthrough.assign(context=lambda x: format_docs(x["context"]))
        | rag_prompt
        | llm
        | StrOutputParser()
    )
    return RunnableParallel(
        context=retriever, question=RunnablePassthrough()
    ).assign(answer=answer)


def build_baseline_chain(llm):
    """Same LLM, no retrieval."""
    return {"question": RunnablePassthrough()} | baseline_prompt | llm | StrOutputParser()


def build_open_baseline_chain(llm):
    """Same LLM, no retrieval, no context, no abstain instruction."""
    return {"question": RunnablePassthrough()} | open_baseline_prompt | llm | StrOutputParser()


# ---------------------------------------------------------------- scoring
def _normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def fact_found(answer, alternatives):
    """True if any accepted spelling of a key fact appears in the answer.

    Number-like facts must match as a whole token, so "22" does not match "2026".
    """
    ans = _normalize(answer)
    for alt in alternatives:
        alt = _normalize(alt)
        pattern = r"(?<![\w.\-])" + re.escape(alt) + r"(?![\w])"
        if re.search(pattern, ans):
            return True
    return False


# Other ways a model says it doesn't know (mostly from the open baseline).
ABSTAIN_MARKERS = [
    ABSTAIN_PHRASE, "i don't know", "i do not know", "i don't have", "i do not have",
    "not familiar with", "not aware of", "no information", "don't have access",
    "do not have access", "can't confirm", "cannot confirm", "unable to confirm",
    "not a standard", "isn't a standard", "not publicly", "don't recognize",
    "do not recognize",
]


def abstained(answer):
    ans = _normalize(answer).replace("’", "'")
    return any(m in ans for m in ABSTAIN_MARKERS)


def score_answer(item, answer, retrieved_sources=None):
    """Automatic scores for one question. Hallucination is a flag for manual review."""
    covered = item["covered"]
    did_abstain = abstained(answer)
    facts = item.get("key_facts", [])
    hits = [fact_found(answer, alts) for alts in facts]

    if covered:
        accuracy = sum(hits) / len(hits) if hits else None
        # Answered but missed a key fact: likely stated a wrong value.
        halluc_flag = (not did_abstain) and accuracy is not None and accuracy < 1
    else:
        accuracy = None
        # Anything other than abstaining on an uncovered question is invented.
        halluc_flag = not did_abstain

    row = {
        "id": item["id"],
        "type": item["type"],
        "accuracy": accuracy,
        "facts_hit": f"{sum(hits)}/{len(hits)}" if hits else "",
        "abstained": did_abstain,
        "abstain_correct": did_abstain == (not covered),
        "hallucination_flag": halluc_flag,
    }
    if retrieved_sources is not None:
        row["retrieved"] = ", ".join(retrieved_sources)
        row["retrieval_hit"] = (
            item["source"] in retrieved_sources if item.get("source") else None
        )
    return row
