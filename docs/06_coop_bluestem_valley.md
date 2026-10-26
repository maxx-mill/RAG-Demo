# Bluestem Valley Electric Cooperative (BVEC) - Conversion Notes

GridLine coop code: **4127**. Staging database: `CNV_4127_STG.gdb`.

## Source System

BVEC delivers data from a legacy CAD-based mapping system exported to shapefiles. The source coordinate system is NAD83 Kansas State Plane South (US feet).

## Attribute Exceptions

### Service Points with Status RET

BVEC uses the source status `RET` for meters that were disconnected but whose service drop is still in the field. These are not retired in the GETM sense. Map source status `RET` to `OPR_STAT_CD` = `OOS`, and copy the original status into `CNV_NOTE` as `SRC_STAT=RET`.

Service points with source status `RET` that have no meter number must also be copied into the hold table `CNV_HOLD_SVC` for the cooperative to review before delivery.

### Transformer Types

BVEC labels pad-mounted transformers `PAD` regardless of phase. Determine single vs three phase from the `PHS_CD` of the transformer and map to `PD1` or `PD3`.

## QA Exceptions

None. BVEC uses the default Revision 7 thresholds.
