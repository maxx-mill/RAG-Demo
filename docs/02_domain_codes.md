# GETM Domain Codes

These coded value domains apply to every cooperative unless the cooperative page says otherwise.

## Phase Codes (PHS_CD)

GETM does not use the common bitmask phase convention (A=4, B=2, C=1). Phase codes are two-digit integers where the first digit is the number of phases.

| Phase | PHS_CD |
|---|---|
| A | 11 |
| B | 12 |
| C | 13 |
| AB | 21 |
| AC | 22 |
| BC | 23 |
| ABC | 31 |
| Unknown | 90 |

A conductor with an unknown phase must be coded 90, never left null.

## Operating Status Codes (OPR_STAT_CD)

| Status | OPR_STAT_CD |
|---|---|
| In service | `INS` |
| Proposed / designed, not built | `PRP` |
| Out of service, still in the field | `OOS` |
| Retired (removed from the field) | `RTD` |
| Abandoned in place (underground only) | `ABP` |

## Transformer Type Codes (XFMR_TYP_CD)

| Type | XFMR_TYP_CD |
|---|---|
| Overhead pole-mounted | `OHPM` |
| Pad-mounted single phase | `PD1` |
| Pad-mounted three phase | `PD3` |
| Submersible / vault | `VLT` |
| Step-down / step bank | `STEP` |
