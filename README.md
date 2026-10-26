# UtilityRAG

GeoAI 582 final project. A small LangChain RAG system that answers GIS conversion questions from internal documentation, cites the source file, or says "not in the docs." A 10-question test compares it with the same LLM without retrieval.

All documents, cooperatives, codes, and values are fictional.

## Files

| Path | What it is |
|---|---|
| `UtilityRAG.ipynb` | Walkthrough notebook, structured like LangChain's rag-from-scratch (indexing, retrieval, generation), plus baseline, evaluation, and an optional multi-query section |
| `rag_core.py` | Shared pipeline: loading, heading-based chunking, Chroma index, prompts, chains, scoring |
| `ingest.py` | Load, chunk, embed, and store `docs/` in Chroma (`chroma_db/`) |
| `ask.py` | Ask a question (`--baseline` for the LLM alone) |
| `evaluate.py` | Run the 10-question test (RAG, guarded baseline, open baseline) and write `results/answers.csv` and `results/summary.csv` |
| `analysis.py` | Retrieval depth (rank of the correct file, best-match distance) and 3 repeat runs for stability |
| `docs/` | 12 synthetic conversion docs for a fictional team and three fictional cooperatives |
| `eval/questions.json` | Questions, answer key (key facts), and expected source file |

## Stack

- LLM: Claude Haiku 5.5 (`langchain-anthropic`)
- Embeddings: Voyage AI `voyage-3.5-lite`
- Vector store: Chroma (persisted locally)
- Chunking: `MarkdownHeaderTextSplitter`, then `RecursiveCharacterTextSplitter` for long sections
- Retrieval: top 4 chunks

## Run

```bash
conda activate RAG_Project
pip install langchain langchain-community langchain-anthropic langchain-voyageai langchain-chroma langchain-text-splitters langsmith tiktoken numpy pandas python-dotenv

cp .env.example .env      # add your keys

python ingest.py
python ask.py "What snapping tolerance should I use for Prairie Wind?"
python ask.py --baseline "What snapping tolerance should I use for Prairie Wind?"
python evaluate.py
```

After `evaluate.py`, read each answer in `results/answers.csv` and fill in the `manual_hallucination` column.

## Test design

| Type | Questions | What it tests |
|---|---|---|
| Local convention | Q01, Q02, Q05, Q06 | Values a general LLM can't know |
| Cooperative exception | Q03, Q04, Q07 | Retrieving the exception instead of the default |
| Not covered | Q08, Q09 | Saying "not in the docs" instead of inventing an answer |
| Public control | Q10 | Public GIS knowledge both systems should get right |

Metrics: accuracy (share of key facts answered), hallucination (flagged automatically, confirmed by hand), abstention, and retrieval hit (correct source file in the top 4).
