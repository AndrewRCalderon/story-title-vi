# TitleVI

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Prerequisites](#prerequisites)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Testing](#testing)
7. [Authors](#authors)
8. [Acknowledgments](#acknowledgments)

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
│   ├── cpi
│   │   ├── cpi.csv
│   │   └── cpi.xlsx
│   ├── epa
│   │    ├── epa.csv
│   │    └── epa.xlsx
│   ├── output_data
│   │   ├── __init__.py
│   │   ├── clean.py
│   │   ├── load.py
│   │   └── transform.py
│   ├── source_data
│   │   ├── cpi_data
│   │   │   └── epa-complaints-1996-2013.csv
│   │   ├── epa_data
│   │   │    ├── epa_ecrco_complaints_2014_2023_2_9.csv
│   │   │    └── epa-complaints-2014-2022-7-8.csv
│   │   ├── source_data
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

## Authors

- Andrew Rodriguez Calderon, Computational Journalist
- Grey Moran
  ...
