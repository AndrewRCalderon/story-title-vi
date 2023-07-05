sinclude .env
export

PYENV=pipenv run


##@ Basic Usage Shorcuts
.PHONY: all
all: clean-epa-complaints-14-23 clean-epa-complaints-96-13 analysis/output_data/mapped_epa_complaints_2014_2023.csv analysis/output_data/joined_epa_complaints_2014_2023.csv analysis/output_data/appended_epa_complaints_1996_2023.csv

.PHONY: tests
tests:
	${PYENV} pytest

.PHONY: clean
clean: clean-output_data	

##@ Basic Usage Commands 
clean-output_data: 
	rm -rf analysis/output_data/*

##@ Pipeline for 1996-2013 & 2014-2023 data
clean-epa-complaints-14-23: analysis/source_data/epa_data/epa_ecrco_complaints_2014_2023_06_13.csv
	${PYENV} python analysis/processors/clean_epa_complaints_2014_2023.py --file_path=$< --output_path='analysis/output_data/epa_complaints_2014_2023.csv' --recent_status_date='2023-06-13'

clean-epa-complaints-96-13: analysis/source_data/cpi_data/epa-complaints-1996-2013.csv
	${PYENV} python analysis/processors/clean_epa_complaints_1996_2013.py --file_path=$< --output_path='analysis/output_data/epa_cpi_complaints_1996_2013.csv'

analysis/output_data/mapped_epa_complaints_2014_2023.csv: analysis/output_data/epa_complaints_2014_2023.csv
	${PYENV} python analysis/processors/map_complaint_data.py --file_path=$< --output_path=$@

analysis/output_data/joined_epa_complaints_2014_2023.csv: analysis/output_data/mapped_epa_complaints_2014_2023.csv analysis/source_data/manual_data/manual_process_complaint_data_2014_2023.csv
	${PYENV} python analysis/processors/join_manual_and_recent_complaint_data.py $^ --output_path=$@

analysis/output_data/appended_epa_complaints_1996_2023.csv: analysis/output_data/joined_epa_complaints_2014_2023.csv analysis/output_data/epa_cpi_complaints_1996_2013.csv 
	${PYENV} python analysis/processors/append_cpi_and_joined_data.py $^ --output_path=$@

