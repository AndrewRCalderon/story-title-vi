# Center for Public Integrity

Reporters: Greta Moran & Andrew Rodriguez Calderón

## The data

We have Title VI complaint logs from the Evironmental Protection Agency (EPA) from multiple sources:

1. Complaints from Sept. 1996 to Dec. 2013 stored in `analysis/output_data/epa-complaints-1996-2013.csv` that CPI received via FOIA for their initial investigation. (n rows 266)

2. Complaints from Jan. 2014 to Nov. 2021 that Greta received from directly from the EPA stored in `analysis/output_data/epa-complaints-2014-2021.csv (n rows 196)

3. Complaints from Jan. 2014 to Jul. 8, 2022 that Andrew pulled from EPA ECRCO's website stored in `analysis/output_data/epa-complaints-2014-2022-7-8.csv` (n rows 111)

## The pipeline

The Makefile orchestrates the entire notebook. `make all` runs every rule to the files used for analysis; otherwise you can run each rule individually.

## Analysis

These are the CSVs are imported to Observable to generate the analysis:

- `output_data/data_complaint_logs_titlevi_2014_2022.csv`

## What we don't know

1. We don't know how the 1996-2013 categorizes `Overview Ruling` which is synonymous with `clean_current_status_reason` in our more recent data. If we can't figure this out, then we won't be able to merge the 1996 data with the post-2013 data to create a long timeline.

2.

## What we want to know

1. How does the rejection rate from the initial investigation compare to the current data?

# To-do

1. Check that all of the last update dates properly parse in the rows that have multiple updates in the `current_status` column
2. Check that all of the `alleged_discrimination_basis` values made their way into the clean columns
3. Concat the 2014-2022 date with the 1996-2013 data
