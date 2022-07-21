import pandas as pd
import helpers

class TitleVIDataModel: 

    def __init__(self, filepath):
        self.filepath = filepath
        self.cleaned_data = self.clean_data()
        self.transformed_data = self.transform_data()
        self.filtered_data = self.filter_columns()
    
    def clean_data(self):
        data = pd.read_csv(self.filepath)

        # standardize column names using helper function
        data.columns = helpers.clean_columns(data)

        # some column names are repeated throughout the dataset 
        # after textract
        data.drop_duplicates(inplace=True)
        data.drop(data[data['epa_complaint_#'] == "EPA Complaint #"].index, inplace = True)

        # remove newline characters from all values, lowercase and strip extra whitespace
        data = data.apply(lambda s: s.str.lower().str.strip().str.replace('\r', ' ').str.replace('\n', ' ') if s.dtype == object else s, axis = 0)

        # change date format
        data['clean_date_received'] = pd.to_datetime(data['date_received'], errors='coerce')

        return data
    
    def transform_data(self):
        data = self.cleaned_data

        # extract multiple capture groups from same string, 
        # combine in a single list series and put into a dataframe
        # and fill in blanks in the new dataframe with original values
        # finally, concat that new df horizontally to existing data
        clean_status_capture_groups = data['current_status'].str.extract('(.*) \d{1,2}/\d{1,2}/\d{4}:|(.*):', expand=False)
        clean_status_capture_groups_df = pd.DataFrame({'clean_current_status': clean_status_capture_groups[0].fillna(clean_status_capture_groups[1])})['clean_current_status'].fillna(data['current_status']) 
        data = pd.concat([data, clean_status_capture_groups_df], axis=1)

        # single captures
        data['clean_current_status_date'] = data['current_status'].str.extract('.* (\d{1,2}/\d{1,2}/\d{4}).*', expand=True)
        data['clean_current_status_reason'] = data['current_status'].str.extract('.*: (.*)', expand=True)
        data['clean_alleged_discrimination_basis'] = data['alleged_discrimination_basis'].str.extract('.*: (.*)', expand=True) 
        data['clean_current_status_date'] = pd.to_datetime(data['clean_current_status_date']) # ERROR: all worked except for extraction on complaint # 06R-15-R6 -> has two dates in description

        # split data
        split_columns = data['clean_alleged_discrimination_basis'].str.split(pat=",|;", expand=True)
        data = pd.concat([data, split_columns], axis=1)

        # calculate time difference

        data['time_elapsed_since_update'] = (data['clean_current_status_date'] - data['clean_date_received']).dt.days

        return data
    
    def filter_columns(self): 
        data = self.transformed_data

        filter_columns = [
            'epa_complaint_#',
            'named_entity',
            'clean_date_received',
            'clean_current_status',
            'clean_current_status_date',
            'clean_current_status_cause',
            'clean_alleged_discrimination_basis',
            0,
            1,
            'time_elapsed_since_update'
            ]
        
        data = data[filter_columns]

        return data


def main():
    filepath = 'analysis/source_data/epa-complaints-2014-2022-7-8.csv'

    analyzer = TitleVIDataModel(filepath)
    analyzer.clean_data()
    analyzer.transform_data()
    # analyzer.filter_columns()

    analyzer.transformed_data.to_csv('analysis/output_data/data_complaint_logs_titlevi_2014_2022.csv', index=False)


if __name__ == "__main__":
    main()
