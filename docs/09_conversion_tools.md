# Conversion Tools

## GLConvert Toolbox

`GLConvert.atbx` is the ArcGIS Pro toolbox for the conversion team. Install it from the conversion tools repository; do not copy it from another analyst's machine.

| Tool | Purpose |
|---|---|
| `Load Staging` | Loads source data into `CNV_<coopcode>_STG.gdb` and writes the row count report |
| `Apply Mapping` | Runs the mapping rules for a cooperative using its mapping profile |
| `Assign GL_ID` | Generates `GL_ID` values for all feature classes |
| `Strip Z/M` | Removes Z and M values |
| `Build Delivery` | Creates the delivery geodatabase and manifest |

## gl-cnv Command Line

The `gl-cnv` command line tool runs QA outside ArcGIS Pro.

- `gl-cnv validate --coop 5512 --profile rev7` runs the QA suite for a cooperative using the Revision 7 thresholds plus that cooperative's exceptions.
- `gl-cnv validate --coop 5512 --profile rev7 --check snap` runs only the connectivity snapping check.
- `gl-cnv report --coop 5512` writes the QA report to `QA_<coopcode>_<yyyymmdd>.html`.

The `--profile rev6` option still exists for re-running historic conversions. Do not use it for new work.

## Mapping Profiles

Each cooperative has a mapping profile `map_<coopcode>.yaml` that lists its lookup tables and exceptions. Changes to a mapping profile require review by a second analyst.
