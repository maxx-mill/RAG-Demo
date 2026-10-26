# QA Suite Thresholds (Revision 7)

Revision 7 of the QA standard took effect March 2, 2026 and replaces Revision 6. Values below are the defaults; a cooperative page may override them.

## Connectivity Checks

| Check | Rule | Threshold |
|---|---|---|
| Snapping tolerance | Line endpoints and devices within this distance are treated as connected | **0.04 ft** |
| Dangle length | Primary line dangles longer than this are flagged | 2.5 ft |
| Disconnected primary | Primary segments not traced back to a source substation | 0 allowed |

Revision 6 used a snapping tolerance of 0.1 ft. Do not use the Revision 6 value for any conversion that started after March 2, 2026.

## Attribute Checks

| Check | Threshold |
|---|---|
| Phase consistency (downstream phase must be a subset of upstream phase) | 0 violations allowed |
| Null `PHS_CD` on any conductor | 0 allowed (use 90 for unknown) |
| Transformers with `KVA_TOT` = 0 | 0 allowed |

## Service Point Checks

| Check | Threshold |
|---|---|
| Orphan service points (not connected to a transformer) | Fail if more than **0.6%** of service points |
| Service points more than 400 ft from their transformer | Flag for review, does not fail |

## Pass Criteria

A conversion passes QA when every zero-tolerance check reports zero violations and the overall weighted QA score is at least **97.5**.
