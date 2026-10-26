# Troubleshooting Common QA Errors

QA errors from `gl-cnv validate` use the prefix `GLC-`.

## GLC-102: Unmapped status value

A source status value has no entry in the cooperative's status lookup. Add the value to the mapping profile and rerun `Apply Mapping`.

## GLC-214: Downstream phase not a subset of upstream phase

A conductor carries a phase that its upstream conductor does not have, for example a C-phase tap (`PHS_CD` 13) fed from an AB line (`PHS_CD` 21). This is usually a source data error, not a mapping error.

**Resolution:** trace upstream to the first segment where the phase changes. If the source attributes are wrong, correct `PHS_CD` on the downstream segment and record `PHS_FIX=GLC214` in `CNV_NOTE`. If you cannot tell which segment is wrong, set the downstream segment to `PHS_CD` 90 and send the location to the cooperative. Do not change the upstream segment without confirmation from the cooperative.

## GLC-305: Orphan service point threshold exceeded

More service points than allowed are not connected to a transformer. Check the snapping tolerance in the profile first; most GLC-305 errors come from running the wrong profile.

## GLC-410: Transformer with zero kVA

A transformer has `KVA_TOT` = 0. Look up the kVA in the cooperative's asset list. If it is not available, the transformer goes to the hold table `CNV_HOLD_XFMR`.
