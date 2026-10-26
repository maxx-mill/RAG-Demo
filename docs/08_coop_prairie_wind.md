# Prairie Wind Rural Electric (PWRE) - Conversion Notes

GridLine coop code: **5512**. Staging database: `CNV_5512_STG.gdb`.

## Source System

Most PWRE data was digitized from scanned paper maps in the early 2000s and later edited in a desktop GIS. Source coordinate system is NAD83 Nebraska State Plane (US feet).

## Dual Voltage System

PWRE operates both 12.47 kV and 24.9 kV distribution. The source field `VOLT_CLASS` holds `L` for 12.47 kV and `H` for 24.9 kV. Map these to `OPR_VOLT_KV` before running the general voltage rules. A null `VOLT_CLASS` still receives the -77 sentinel.

## QA Exceptions

### Snapping Tolerance

Because the PWRE network was digitized from paper, endpoints are rarely coincident. PWRE uses a **snapping tolerance of 0.25 ft** instead of the Revision 7 default. This exception was approved by the QA lead and applies to all PWRE feature classes.

### Orphan Service Points

The orphan service point threshold for PWRE is 1.5% for batch 1 only. Later batches use the default.
