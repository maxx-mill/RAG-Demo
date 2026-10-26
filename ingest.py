"""Load, chunk, embed, and store the conversion docs in Chroma.

Usage:  python ingest.py

At work, load_docs() would become a Confluence loader
(langchain_community.document_loaders.ConfluenceLoader); everything after it stays the same.
"""

from rag_core import CHROMA_DIR, build_vectorstore, load_docs, load_keys, split_docs


def main():
    keys = load_keys()
    if not keys["VOYAGE_API_KEY"]:
        raise SystemExit("VOYAGE_API_KEY is missing. Add it to .env.")

    docs = load_docs()
    chunks = split_docs(docs)
    print(f"Loaded {len(docs)} docs -> {len(chunks)} chunks")

    store = build_vectorstore(chunks)
    print(f"Stored {store._collection.count()} chunks in {CHROMA_DIR}")


if __name__ == "__main__":
    main()
