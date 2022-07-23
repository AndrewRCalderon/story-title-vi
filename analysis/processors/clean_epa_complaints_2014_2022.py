#!/usr/bin/env python   

import pandas as pd
import analysis.helper_functions.helpers as helpers
import fire
import pdb

class TitleVIDataModel: 
    FILE_PATH = "analysis/source_data/epa-complaints-2014-2022-7-8.csv"

    def __init__(self):
        self.filepath = self.FILE_PATH
        self.data = self.load_data()
    
    def load_data(self):
        data = pd.read_csv(self.FILE_PATH)

        return data
        
    def clean_data(self):
        # standardize column names using helpers function
        self.data.columns = helpers.clean_columns(self.data)

        # some column names are repeated throughout the dataset 
        # after textract
        self.data.drop_duplicates(inplace=True)
        self.data.drop(self.data[self.data['epa_complaint_#'] == "EPA Complaint #"].index, inplace = True)

        # remove newline characters from all values, lowercase and strip extra whitespace
        self.data = self.data.apply(lambda s: s.str.lower().str.strip().str.replace('\r', '').str.replace('\n', '') if s.dtype == object else s, axis = 0)


        # change date format
        self.data['clean_date_received'] = pd.to_datetime(self.data['date_received'], errors='coerce')

        return self
    
    def transform_data(self):
        data_copy = self.data
        # extract multiple capture groups from same string, 
        # combine in a single list series and put into a dataframe
        # and fill in blanks in the new dataframe with original values
        # finally, concat that new df horizontally to existing data
        clean_status_capture_groups = data_copy['current_status'].str.extract('(.*) \d{1,2}\/\d{1,2}\/\d{4}:|(.*)', expand=False)

        capture_group_dict  = {
            
            'clean_current_status': clean_status_capture_groups[0].fillna(clean_status_capture_groups[1])
            
            }

        # the fillna method is a safety here. just in case the above regexes missed anything, 
        # the result will be Nan. Those Nans will be filled with the original string, making
        # it easier to identify a failure.
        clean_status_capture_groups_df = pd.DataFrame(capture_group_dict)['clean_current_status'].fillna(data_copy['current_status']) 
        data_copy = pd.concat([data_copy, clean_status_capture_groups_df], axis=1)


        # also handle multiple captures of matching patterns for date in current_status
        clean_status_date_capture_groups = data_copy['current_status'].str.extract('.* (\d{1,2}/\d{1,2}/\d{4}).*|[:a-z](\d{1,2}/\d{1,2}/\d{4})', expand=False)

        status_date_capture_group_dict  = {
            
            'clean_current_status_date': clean_status_date_capture_groups[0].fillna(clean_status_date_capture_groups[1])
            
            }

        clean_status_date_capture_groups = pd.DataFrame(status_date_capture_group_dict)['clean_current_status_date']
        data_copy = pd.concat([data_copy, clean_status_date_capture_groups], axis=1)

        data_copy['clean_current_status_date'] = pd.to_datetime(data_copy['clean_current_status_date'], errors='coerce') # ERROR: all worked except for extraction on complaint # 06R-15-R6 -> has two dates in description  

        # single captures
        data_copy['clean_current_status_reason'] = data_copy['current_status'].str.extract('.*: (.*)', expand=True)
        data_copy['clean_alleged_discrimination_basis'] = data_copy['alleged_discrimination_basis'].str.extract('.*: (.*)', expand=True) 

        # split data
        split_columns = data_copy['clean_alleged_discrimination_basis'].str.split(pat=",|;", expand=True)
        data_copy = pd.concat([data_copy, split_columns], axis=1)

        # calculate time difference

        data_copy['time_elapsed_since_update'] = (data_copy['clean_current_status_date'] - data_copy['clean_date_received']).dt.days

        self.data = data_copy

        return self
    
    def filter_columns(self): 
        filter_columns = [
            'epa_complaint_#',
            'named_entity',
            'clean_date_received',
            'current_status',
            'clean_current_status',
            'clean_current_status_date',
            'clean_current_status_reason',
            'clean_alleged_discrimination_basis',
            0,
            1,
            'time_elapsed_since_update',
            ]
        
        self.data = self.data[filter_columns]

        return self
    
    def get_data(self, return_copy=True):
        if return_copy:
            return self.data.copy()
        
        return self.data




def main():
    analyzer = TitleVIDataModel()

    loaded_data = analyzer.get_data()
    assert len(loaded_data) == 212

    analysis_data_export = analyzer.clean_data().transform_data().filter_columns().get_data()
    assert len(analysis_data_export) == 204
    
    analysis_data_export.to_csv('analysis/output_data/data_complaint_logs_titlevi_2014_2022.csv', index=False)


if __name__ == "__main__":
    fire.Fire(main)
