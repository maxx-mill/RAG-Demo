"""Ask UtilityRAG a question.

Usage:
    python ask.py "What snapping tolerance does Prairie Wind use?"
    python ask.py --baseline "..."     # same LLM, no retrieval
    python ask.py                      # interactive prompt
"""

import argparse

from rag_core import (
    TOP_K, build_baseline_chain, build_rag_chain, get_llm, load_keys, load_vectorstore,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="*")
    parser.add_argument("--baseline", action="store_true", help="skip retrieval")
    parser.add_argument("-k", type=int, default=TOP_K, help="chunks to retrieve")
    args = parser.parse_args()

    keys = load_keys()
    if not keys["ANTHROPIC_API_KEY"]:
        raise SystemExit("ANTHROPIC_API_KEY is missing. Add it to .env.")

    llm = get_llm()
    if args.baseline:
        chain = build_baseline_chain(llm)
    else:
        retriever = load_vectorstore().as_retriever(search_kwargs={"k": args.k})
        chain = build_rag_chain(retriever, llm)

    def run(q):
        out = chain.invoke(q)
        if args.baseline:
            print(f"\n{out}\n")
            return
        print(f"\n{out['answer']}\n")
        print("Retrieved:")
        for d in out["context"]:
            print(f"  - {d.metadata['source']}  ({d.metadata.get('section', '')})")
        print()

    if args.question:
        run(" ".join(args.question))
    else:
        while (q := input("Question (blank to quit): ").strip()):
            run(q)


if __name__ == "__main__":
    main()
