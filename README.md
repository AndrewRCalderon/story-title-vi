# Center for Public Integrity

Reporters: Greta Moran & Andrew Rodriguez Calderón

## The data

We have Title VI complaint logs from the Evironmental Protection Agency (EPA) from multiple sources:

1. Complaints from Sept. 1996 to Dec. 2013 stored in `analysis/output_data/epa-complaints-1996-2013.csv` that CPI received via FOIA for their initial investigation.

2. Complaints from Jan. 2014 to Nov. 2021 that Greta received from directly from the EPA stored in `analysis/output_data/epa-complaints-2014-2021.csv

3. Complaints from Jan. 2014 to Jul. 8, 2022 that Andrew pulled from EPA ECRCO's website stored in `analysis/output_data/epa-complaints-2014-2022-7-8.csv`

## The code

# To-do

1. Check that all of the last update dates properly parse in the rows that have multiple updates in the `current_status` column
2. Check that all of the `alleged_discrimination_basis` values made their way into the clean columns
3. concat the 2014-2022 date with the 1996-2013 data
