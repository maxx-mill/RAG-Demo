# GridLine Electric Target Model (GETM) Schema

GETM is the target schema for every electric conversion. It is loosely based on public utility data models but uses GridLine's own feature class and field names. Do not substitute field names from the Esri Utility Network or any other public model.

## Feature Classes

| Feature class | Geometry | Description |
|---|---|---|
| `ELC_PriOHLine` | Polyline | Overhead primary conductor |
| `ELC_PriUGLine` | Polyline | Underground primary conductor |
| `ELC_SecLine` | Polyline | Secondary and service conductor |
| `ELC_Xfmr` | Point | Distribution transformer bank |
| `ELC_SvcPt` | Point | Service point (one per meter location) |
| `ELC_Pole` | Point | Support structure |
| `ELC_ProtDev` | Point | Fuses, reclosers, sectionalizers |

## Common Fields

Every GETM feature class carries these fields.

| Field | Type | Description |
|---|---|---|
| `GL_ID` | Text(20) | GridLine identifier, format `<coopcode>-<class abbreviation>-<sequence>`, e.g. `4127-XF-000123` |
| `CNV_SRC_ID` | Text(64) | The identifier from the source system, copied unchanged |
| `OPR_STAT_CD` | Text(3) | Operating status code (see `02_domain_codes.md`) |
| `CNV_BATCH` | Short | Conversion batch number, starting at 1 |
| `CNV_NOTE` | Text(255) | Free-text conversion note |

## Conductor Fields

Primary and secondary line classes also carry:

| Field | Type | Description |
|---|---|---|
| `PHS_CD` | Short | Phase code (see `02_domain_codes.md`) |
| `OPR_VOLT_KV` | Double | Operating line-to-line voltage in kV |
| `COND_SZ` | Text(16) | Conductor size, e.g. `1/0 ACSR` |
| `NEUT_PRES` | Short | 1 if a neutral is present, 0 if not |

## Transformer Fields

| Field | Type | Description |
|---|---|---|
| `XFMR_TYP_CD` | Text(4) | Transformer type code (see `02_domain_codes.md`) |
| `KVA_TOT` | Double | Total bank kVA |
| `PHS_CD` | Short | Phase code |
