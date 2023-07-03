# TitleVI

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Testing](#testing)
7. [Authors](#authors)
8. [Source Data](#source-data)
9. [Output Data](#output-data)
10. [Data Dictionary](#data-dictionary)
11. [Analysis](#analysis)
12. [Review](#review)
13. [Editor's Notes](#editors-notes)
14. [Acknowledgments](#acknowledgments)

## Introduction

This repository captures the ETL for the Title VI project. The project is a collaboratin between teh Center for Public Integrity and Andrew Rodriguez Calderon (computational journalist) and Grey Moran (investigative reporter).

The repo extracts, transforms and loads data from the following sources:

- The Environmental Protection Agency (EPA)
- The Center for Public Integrity (CPI)

The repo also contains the following:

- a Pipfile that captures the dependencies for the project
- a Makefile that orchestrates the ETL process
- the source data received from the EPA and from CPI
- code that loads and cleans the data
- some helper functions
- scaffolding for testing (not implemented)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

1. Clone the repo
2. Install the dependencies using pipenv
3. Run the Makefile using `make all` command
4. Visit the Observable Notebook to see the analysis

## Prerequisites

- Python 3.9
- Pipenv
- Make

## Usage

The most useful commands are in the Makefile. The following commands are available:

- `make all` - runs the entire ETL process without tests
- `make clean` - removes all the files created by the ETL process
- `make tests` - runs the tests

For the compository commands see the Makefile.

## Project Structure

The file structure is as follows:

```
├── analysis
│   ├── README.md
│   ├── helper_functions
│   │   └── helpers.py
│   ├── output_data
│   │   ├── __init__.py
│   │   ├── clean.py
│   │   ├── load.py
│   │   └── transform.py
│   ├── processors
│   │   ├── __init__.py
│   │   ├── append_cpi_and_joined_data.py
│   │   ├── clean_epa_complaints_1996_2013.py
│   │   ├── join_manual_and_recent_complaint_data.py
│   │   └── map_complaint_data.py
│   ├── source_data
│   │   ├── cpi_data
│   │   │   └── epa-complaints-1996-2013.csv
│   │   ├── epa_data
│   │   │   └── epa_ecrco_complaints_2014_2023_2_9.csv
│   │   └── manual_data
│   │       └── manual_process_complaint_data_2014_2022.csv
│   └── tests
│       ├── __init__.py
│       └── processors
│           ├── __init__.py
│           └── test_complaints.py
├── Makefile
├── Pipfile
├── Pipfile.lock
```

## Testing

To run the tests, run the following command:

```
make tests
```

## Source Data

We have Title VI complaint logs from the Evironmental Protection Agency (EPA) from multiple sources:

1. Complaints from Sept. 1996 to Dec. 2013 stored in `analysis/source_data/cpi_data/epa-complaints-1996-2013.csv` that CPI received via FOIA for their initial investigation.

2. Complaints from Jan. 2014 to June. 13, 2023 that we pulled from the [EPA website](https://www.epa.gov/external-civil-rights/external-civil-rights-docket-2014-present) and copied and pasted into a [spreadsheet](https://docs.google.com/spreadsheets/d/1Q2VbeaBSrd24LUqCO6YDi0joNUE3DRs5tweOHhUa5Yk/edit?pli=1#gid=733128710) that we downloaded as a CSV and loaded into the rig.

3. Complaints from Jan. 2014 to 2023 that Jamie manually verified as a testing dataset stored in `analysis/source_data/manual_data/manual_process_complaint_data_2014_2023.csv`

## Output Data

TBD

## Data Dictonary

There are categories that the EPA uses to categorize the data. The way that the EPA write them into the data isn't always consistent.

The following is a list of those categories removing some of the inconsistencies:

- **Rejected** - The unique identifier for the complaint.

  - **Lack of jurisdiction** - The date the complaint was closed.
  - **Lack of timely discriminatory act** - The date the complaint was closed.
  - **Converted to compliance review** - The date the complaint was closed.
  - **Allegations insuffieciently grounded in fact** - The date the complaint was closed.

- **Rejected without prejudice** - The date the complaint was filed.
  - **Not ripe for review**
- **Rejected and Closed** - The date the complaint was closed.
  - **ADR Settlment**
- **Rejected and Admin Closure** - The date the complaint was closed.
- **Pending** - The type of complaint.
  - **Under jusrisditional review** - The date the complaint was closed.
  - **Under investigation** - The date the complaint was closed.
  - **Information resolution negotiation** - The date the complaint was closed.
- **Admin Closure** - The date the complaint was filed.
  - **Complaint withdrawn** - The date the complaint was closed
- **Rejected and Referred** - The date the complaint was closed.
  - **Lack of jurisdiction** - The date the complaint was closed.
- **Not Accepted for Investigation** - The date the complaint was closed.
- **Resolved** - The date the complaint was closed.
  - **Through informal resolution Agreement** - The date the complaint was closed.
- **Technical Assistance to Recipient**

In `analysis/processors/map_complaint_data.py` we map these categories into simpler categories that allow for analysis.

## Analysis

The analysis is done in [Observable](https://observablehq.com/d/bca22d56bd66a046). The following CSVs are imported to Observable to generate the analysis:

- `analysis/output_data/appended_epa_complaints_1996_2023.csv`

## Review

For reviewers, the most important files to review are scripts in processors. Those files handles the ETL logic, which starts with cleaning the data, then mapping the data, then joining the data, and finally appending the data.

I didn't have time to make the tests robust, so I would not assume that those are shoring up our pipeline. I did however sprinkle in some assert statements to make sure that the data is being transformed as expected, but it's possible that I missed something.

So for the review, the two crucial pieces of the codebase to verify are the logic of the processors and the interpretation of the mapping of the data itself.

## Editor's Notes

As we have deepended our reporting, Jamie, Yvette, Grey and I have considered various themes and angles to pursue. We have also started to note holes in the data and caveats to bear in mind. I am including those notes here for reference.

- The EPA is regularly updating the data. So we must frequently check for updates and re-run the ETL process. We should also consider how to handle the data updates in the Observable notebook.

- The EPA consolidates some of its cases, meaning that a single row can actually stand is for multiple complaints. Jamie decided to handle this manually by flagging singular and multifaceted complaints after a review of the original case files. When the cases were not split, she then flagged the final case status based on the "highest level of action from the EPA." She notes that "we should be mindful of later status updates, because in some cases this might change which complaint to count as the unique one."

- There are cases in the EPA data that are not properly environmental justice complaints. Jamie notes that we should make this distinction to ensure that we are counting only environmental justice complaints.

- Andrew & Grey had initially processed some data manually but Jamie also did the same thing and added new fields. So at this point, I think that it makes more sense to replace our manual data with hers. This change will show up in the Git history but won't be evident to someone closing the repo after the fact.

- CPI published its original [methodology](https://publicintegrity.org/environment/how-we-acquired-and-analyzed-data-for-environmental-justice-denied/) where they describe the categorization of the data. The EPA published some [data](https://web.archive.org/web/20140710070743/http://www2.epa.gov/ocr/complaints-filed-epa-under-title-vi-civil-rights-act-1964) about environmental justice complaints, but CPI noticed discrepancies and requested all of the underlying documents. CPI notes in their methodology that "when calculating how long cases took to wind through the review process, the Center omitted those that were pending, so as not to skew the results."

## Action Items

- [x] Bring in new data from Jamie's manual processing and replace it with Greta & Andrew's manual processing.

- [ ] Jamie wants us to compare cases in the data from the 2015 investigation to the 2023 data to see which ones were open, and what changes.

- [ ] Re-run analysis that compares what the data looks like when we treat each row as a case vs when we consolidate related cases using the "highest level of action from the EPA" as the final case status.

- [ ] Put together a list of findings to run by the EPA

- [x] Any admin closures, copy the final status from manual data

- [ ] Split manual data based on ":" before doing comparison to get primary and secondary status

- [x] Change statuses from CPI data based on new [data dictionary](https://docs.google.com/spreadsheets/d/1Z3_kPsV0PrScznsHPxhT0aDQKFmfZq2CuEPyZIolpoI/edit#gid=450381695)

## Authors

- Andrew Rodriguez Calderon, Computational Journalist
- Grey Moran
  ...
