sinclude .env
export

PIPENV=pipenv run


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
	${PIPENV} pytest

##@ Run processors

# clean-epa-complaints-14-21: analysis/source_data/epa-complaints-2014-2021.csv
# 	${PIPENV} python analysis/processors/clean_epa_complaints_2014_2021.py --file_path=$<

# clean-epa-complaints-14-22: analysis/source_data/epa-complaints-2014-2022-7-8.csv
# 	${PIPENV} python analysis/processors/clean_epa_complaints_2014_2022.py

clean-epa-complaints-14-23: analysis/source_data/epa_data/epa_ecrco_complaints_2014_2023_2_9.csv
	${PIPENV} python analysis/processors/clean_epa_complaints_2014_2023.py --file_path=$< --output_path='analysis/output_data/epa_complaints_2014_2023.csv'

analysis/output_data/mapped_epa_complaints_2014_2023: analysis/output_data/epa-complaints-2014-2023.csv
	${PYENV} python analysis/processors/map_complaint_data.py


