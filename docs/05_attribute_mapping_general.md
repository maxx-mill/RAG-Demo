# General Attribute Mapping Rules

These rules apply during the Mapping phase for every cooperative. Cooperative pages list exceptions.

## Identifier Mapping

- Copy the source identifier into `CNV_SRC_ID` unchanged, including leading zeros.
- Generate `GL_ID` with the `Assign GL_ID` tool. Never hand-type a `GL_ID`.

## Voltage Mapping

Source voltage is often stored as text such as `7.2/12.47` or `12470`. Map it to `OPR_VOLT_KV` as the line-to-line value in kV:

| Source value | OPR_VOLT_KV |
|---|---|
| `7.2/12.47`, `12470`, `12.47` | 12.47 |
| `14.4/24.9`, `24940`, `24.9` | 24.9 |
| `7.62/13.2`, `13200` | 13.2 |

When the source voltage is blank, null, or cannot be parsed, set `OPR_VOLT_KV` to the sentinel value **-77** and write `VOLT_UNRESOLVED` in `CNV_NOTE`. Do not guess the voltage from neighboring segments.

## Phase Mapping

Map source phase text (for example `A`, `AB`, `ABC`, `RED`, `1`) to `PHS_CD` using the lookup table `LKP_PHASE` for that cooperative. If the source phase is missing, use 90.

## Status Mapping

Map source status values to `OPR_STAT_CD`. Unmapped source status values stop the Mapping gate.

## Null Handling

Text fields with no source value are left null, except `CNV_NOTE`, which receives `NO_SRC` when the whole source record had no attributes.
