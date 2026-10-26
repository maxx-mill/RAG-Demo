"""Extra analysis for the report (run after ingest.py).

1. Retrieval depth: where the correct source file first appears in the top 10,
   and the similarity of the best chunk (does it separate covered from uncovered?).
2. Stability: each system answers every question N times. Claude no longer accepts
   temperature=0, so answers can vary between runs.

Usage:  python analysis.py [N]      (default N = 3)
Writes results/analysis_retrieval.csv and results/analysis_repeats.csv.
"""

import json
import sys

import pandas as pd

from rag_core import (
    EVAL_FILE, RESULTS_DIR, TOP_K, build_baseline_chain, build_open_baseline_chain,
    format_docs, get_embeddings, get_llm, load_keys, load_vectorstore, rag_prompt,
    score_answer,
)
from langchain_core.output_parsers import StrOutputParser


def main(n_repeats=3):
    load_keys()
    questions = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    embd = get_embeddings()
    store = load_vectorstore(embd)
    llm = get_llm()

    # ---- 1. retrieval depth (one embedding call per question, reused below)
    retrieval_rows, top4 = [], {}
    for item in questions:
        vec = embd.embed_query(item["question"])
        hits = store.similarity_search_by_vector_with_relevance_scores(vec, k=10)
        top4[item["id"]] = [d for d, _ in hits[:TOP_K]]
        sources = [d.metadata["source"] for d, _ in hits]
        rank = sources.index(item["source"]) + 1 if item["source"] in sources else None
        retrieval_rows.append({
            "id": item["id"], "type": item["type"], "expected": item["source"],
            "first_correct_rank": rank,
            "top1_source": sources[0], "top1_section": hits[0][0].metadata.get("section"),
            "top1_distance": round(hits[0][1], 3),
        })
    retrieval = pd.DataFrame(retrieval_rows)

    # ---- 2. stability: N answers per system per question
    rag_answer = rag_prompt | llm | StrOutputParser()
    guarded, open_ = build_baseline_chain(llm), build_open_baseline_chain(llm)
    rows = []
    for rep in range(1, n_repeats + 1):
        for item in questions:
            q = item["question"]
            print(f"run {rep} {item['id']}")
            docs = top4[item["id"]]
            answers = {
                "rag": rag_answer.invoke({"context": format_docs(docs), "question": q}),
                "baseline": guarded.invoke(q),
                "baseline_open": open_.invoke(q),
            }
            for system, ans in answers.items():
                rows.append({**score_answer(item, ans), "system": system, "run": rep,
                             "answer": ans})
    repeats = pd.DataFrame(rows)

    RESULTS_DIR.mkdir(exist_ok=True)
    retrieval.to_csv(RESULTS_DIR / "analysis_retrieval.csv", index=False)
    repeats.to_csv(RESULTS_DIR / "analysis_repeats.csv", index=False)

    print("\nRetrieval depth:\n", retrieval.to_string(index=False))
    covered = repeats[repeats["accuracy"].notna()]
    print("\nAccuracy per run:\n",
          covered.groupby(["system", "run"])["accuracy"].mean().unstack().round(3))
    print("\nAbstentions per run:\n",
          repeats.groupby(["system", "run"])["abstained"].sum().unstack())


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
