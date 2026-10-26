# Coordinate Systems and Projection Standards

## Staging Coordinate System

Source data is loaded into staging in its original coordinate system. It is not reprojected during staging.

## Target Coordinate System

All GETM deliverables use the GridLine custom projection **GL Albers Conversion**, registered internally as WKID **990417**. It is an Albers Equal Area Conic projection on NAD83(2011) with linear units in US survey feet. The projection definition file is `GL_Albers_Cnv.prj` in the conversion tools repository.

Do not deliver in Web Mercator (EPSG:3857) or in a state plane system, even if the cooperative asks. Cooperatives receive a state plane export separately through the reporting team.

## Field GPS Data

Field-collected GPS points arrive in WGS 84 geographic coordinates (EPSG:4326). They must be projected to WKID 990417 using the transformation `WGS_1984_(ITRF08)_To_NAD_1983_2011`. Never project GPS points without specifying this transformation.

## Vertical Data

GETM does not store elevation. Drop Z values during the Mapping phase using the `Strip Z/M` tool in `GLConvert.atbx`.
