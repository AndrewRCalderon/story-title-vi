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

##@ Run processors

clean-epa-complaints-14-21: analysis/source_data/epa-complaints-2014-2021.csv
	${PYENV} python analysis/processors/clean_epa_complaints_2014_2021.py

clean-epa-complaints-14-22: analysis/source_data/epa-complaints-2014-2022-7-8.csv
	${PYENV} python analysis/processors/clean_epa_complaints_2014_2022.py > test.txt

# analysis/output_data/mapped_data_complaint_logs_titlevi.csv: analysis/output_data/data_complaint_logs_titlevi.csv
# 	${PYENV} python analysis/processors/map_complaint_data.py


