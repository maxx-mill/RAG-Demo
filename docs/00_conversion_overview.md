# GridLine Conversion Program Overview

GridLine Data Services converts legacy electric distribution GIS data from member cooperatives into the GridLine Electric Target Model (GETM). This page describes the conversion phases and where to find the detailed standards. All cooperatives, codes, and values in this documentation set are fictional.

## Conversion Phases

Every conversion moves through five phases. A phase cannot start until the previous phase gate is signed off.

1. **Intake** - receive source data, record the source system and coordinate system on the intake form, and assign the cooperative a four-digit GridLine coop code.
2. **Staging** - load source data unchanged into a staging geodatabase named `CNV_<coopcode>_STG.gdb` (for example `CNV_4127_STG.gdb`).
3. **Mapping** - apply attribute mapping rules (see `05_attribute_mapping_general.md` and the cooperative-specific page).
4. **QA** - run the GridLine QA suite (see `04_qa_thresholds.md`). The QA suite must pass before delivery.
5. **Delivery and Sign-off** - package and deliver the converted data (see `10_delivery_and_signoff.md`).

## Phase Gates

Each phase gate requires a gate ticket in the CNV project with the label `gate-<phase>`. The Staging gate requires a row count reconciliation between source and staging that matches exactly. The Mapping gate requires that no field in the target model is left with an unmapped status.

## Cooperatives Currently in Conversion

| Cooperative | Short name | GridLine coop code | Page |
|---|---|---|---|
| Bluestem Valley Electric Cooperative | BVEC | 4127 | `06_coop_bluestem_valley.md` |
| Ozark Ridge Electric Membership Corporation | OREMC | 3380 | `07_coop_ozark_ridge.md` |
| Prairie Wind Rural Electric | PWRE | 5512 | `08_coop_prairie_wind.md` |

Cooperative-specific pages always override the general standards when they conflict.
