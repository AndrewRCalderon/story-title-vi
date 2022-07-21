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
	${PYENV} pytest tests

##@ Run processors

clean-textracted-epa-complaints: analysis/source_data/tabula-complaints-received-in-FY-2022-to-date-11-12-2021-thru-FY2014.csv
	${PYENV} python analysis/processors/clean_textracted_complaint_data.py

clean-epa-complaints-14-21: analysis/source_data/epa-complaints-complaints-2014-2021.csv
	${PYENV} python analysis/processors/clean_epa_complaints_2014-2022.py

analysis/output_data/mapped_data_complaint_logs_titlevi.csv: analysis/output_data/data_complaint_logs_titlevi.csv
	${PYENV} python analysis/processors/map_complaint_data.py


