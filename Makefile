sinclude .env
export

PYENV=pipenv run


##@ Basic Usage
.PHONY: clean
clean: clean/source_data clean/output_data

.PHONY: processors
processors: analysis/output_data/data_complaint_logs_titlevi.csv analysis/output_data/mapped_data_complaint_logs_titlevi.csv


##@ Clean-up
.PHONY: clean/source_data
clean/source_data: 
	rm -rf analysis/source_data/*

.PHONY: clean/output_data
clean/output_data: 
	rm -rf analysis/output_data/*

.PHONY: tests
tests:
	${PYENV} pytest

##@ Run all
.PHONY: all
all: clean-epa-complaints-14-23 analysis/output_data/mapped_epa_complaints_2014_2023.csv analysis/output_data/joined_epa_complaints_2014_2023.csv

##@ Run processors

# clean-epa-complaints-14-21: analysis/source_data/epa-complaints-2014-2021.csv
# 	${PIPENV} python analysis/processors/clean_epa_complaints_2014_2021.py --file_path=$<

# clean-epa-complaints-14-22: analysis/source_data/epa-complaints-2014-2022-7-8.csv
# 	${PIPENV} python analysis/processors/clean_epa_complaints_2014_2022.py

##@ Pipeline for 2014-2023 data
clean-epa-complaints-14-23: analysis/source_data/epa_data/epa_ecrco_complaints_2014_2023_2_9.csv
	${PYENV} python analysis/processors/clean_epa_complaints_2014_2023.py --file_path=$< --output_path='analysis/output_data/epa_complaints_2014_2023.csv'

analysis/output_data/mapped_epa_complaints_2014_2023.csv: analysis/output_data/epa_complaints_2014_2023.csv
	${PYENV} python analysis/processors/map_complaint_data.py --file_path=$< --output_path=$@

analysis/output_data/joined_epa_complaints_2014_2023.csv: analysis/output_data/mapped_epa_complaints_2014_2023.csv analysis/source_data/manual_data/manual_process_complaint_data_2014_2022.csv
	${PYENV} python analysis/processors/join_manual_and_recent_complaint_data.py $^ --output_path=$@

