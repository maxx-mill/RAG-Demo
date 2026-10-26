"""Run the 10-question test: baseline (LLM alone) vs. RAG.

Usage:  python evaluate.py

Writes results/answers.csv (every answer, for manual review) and
results/summary.csv (the results table). Fill in the `manual_hallucination`
column of answers.csv by hand after reading each answer.
"""

import json

import pandas as pd

from rag_core import (
    EVAL_FILE, RESULTS_DIR, TOP_K, build_baseline_chain, build_open_baseline_chain, build_rag_chain,
    get_llm, load_keys, load_vectorstore, score_answer,
)


def run_eval(rag_chain, baseline_chain, questions, open_baseline_chain=None):
    rows = []
    for item in questions:
        q = item["question"]
        print(f"[{item['id']}] {q}")

        base_answer = baseline_chain.invoke(q)
        rows.append({**score_answer(item, base_answer), "system": "baseline",
                     "question": q, "answer": base_answer})

        if open_baseline_chain is not None:
            open_answer = open_baseline_chain.invoke(q)
            rows.append({**score_answer(item, open_answer), "system": "baseline_open",
                         "question": q, "answer": open_answer})

        out = rag_chain.invoke(q)
        sources = list(dict.fromkeys(d.metadata["source"] for d in out["context"]))
        rows.append({**score_answer(item, out["answer"], sources), "system": "rag",
                     "question": q, "answer": out["answer"]})
    return pd.DataFrame(rows)


def summarize(df):
    """One row per system: the metrics from the proposal."""
    def agg(g):
        covered = g[g["accuracy"].notna()]
        uncovered = g[g["type"] == "uncovered"]
        return pd.Series({
            "accuracy (key facts)": covered["accuracy"].mean(),
            "hallucination flags": int(g["hallucination_flag"].sum()),
            "abstained on uncovered": f"{int(uncovered['abstained'].sum())}/{len(uncovered)}",
            "false abstentions": int((g["abstained"] & g["accuracy"].notna()).sum()),
            "retrieval hit rate": g["retrieval_hit"].dropna().astype(float).mean()
                                  if "retrieval_hit" in g else None,
        })
    return df.groupby("system").apply(agg, include_groups=False)


def main():
    keys = load_keys()
    if not (keys["ANTHROPIC_API_KEY"] and keys["VOYAGE_API_KEY"]):
        raise SystemExit("ANTHROPIC_API_KEY and VOYAGE_API_KEY are required.")

    questions = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    llm = get_llm()
    retriever = load_vectorstore().as_retriever(search_kwargs={"k": TOP_K})

    df = run_eval(build_rag_chain(retriever, llm), build_baseline_chain(llm), questions,
                  build_open_baseline_chain(llm))
    df["manual_hallucination"] = ""  # fill in by hand

    RESULTS_DIR.mkdir(exist_ok=True)
    df.to_csv(RESULTS_DIR / "answers.csv", index=False)
    summary = summarize(df)
    summary.to_csv(RESULTS_DIR / "summary.csv")

    print("\nPer question:")
    print(df.pivot(index="id", columns="system",
                   values=["accuracy", "abstained", "hallucination_flag"]).to_string())
    print("\nSummary:")
    print(summary.to_string())


if __name__ == "__main__":
    main()
