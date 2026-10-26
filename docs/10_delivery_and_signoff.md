# Delivery and Sign-off

## Delivery Package

The delivery package is produced by the `Build Delivery` tool and contains:

- A file geodatabase named `<coopcode>_<yyyymmdd>_GETM_v<n>.gdb`, for example `3380_20260415_GETM_v2.gdb`. The version number starts at 1 and increments for every redelivery to the same cooperative.
- A manifest file `manifest.json` with feature counts per class.
- The latest QA report from `gl-cnv report`.

## Sign-off

Delivery requires sign-off from **two** people: the conversion analyst and a QA reviewer who did not work on the conversion. Record both names in the `gate-delivery` ticket.

## Retention

Staging databases are kept for 120 days after sign-off and then deleted. Delivery packages are kept for seven years.
