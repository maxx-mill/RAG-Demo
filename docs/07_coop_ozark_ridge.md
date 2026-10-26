# Ozark Ridge Electric Membership Corporation (OREMC) - Conversion Notes

GridLine coop code: **3380**. Staging database: `CNV_3380_STG.gdb`.

## Source System

OREMC delivers a file geodatabase from an older engineering analysis system. Source coordinate system is NAD83 Missouri State Plane Central (US feet).

## Attribute Exceptions

### Phase Colors

OREMC stores phase as conductor color: `RED` = A, `BLU` = B, `YEL` = C. Multi-phase lines combine colors with a hyphen, e.g. `RED-YEL` = AC. Load the OREMC version of `LKP_PHASE`, which maps these to GETM `PHS_CD` values.

### Retired Poles

OREMC requires that retired poles be **kept in the deliverable for 18 months** after their retirement date instead of being dropped. Map them to `OPR_STAT_CD` = `RTD` and populate `CNV_NOTE` with `RTD_DATE=<yyyy-mm-dd>`. Poles retired more than 18 months before the conversion date are dropped as usual.

### Underground Primary

OREMC underground primary has no conductor size in the source. Set `COND_SZ` to `UNK-UG`.

## QA Exceptions

The dangle length check is raised to 5.0 ft for OREMC overhead primary only.
