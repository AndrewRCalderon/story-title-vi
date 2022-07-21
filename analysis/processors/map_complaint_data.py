import pandas as pd
import numpy as np
import re

class transformMapComplaintdata: 

    def __init__(self, filepath):
        self.filepath = filepath
        self.mapped_data = self.map_current_status()
    
    def map_current_status(self):
        data = pd.read_csv(self.filepath)

        data['clean_current_status'].fillna('', inplace=True)

        mapping = {
            'rejected': r'^rejected$|not accepted.*|^rejected/closed|^rejected and closed|^rejected 5',
            'rejected & referred': r'^rejected.*referred',
            'rejected without prejudice': r'^rejected without prejudice',
            'administrative closure': r'^admin|^accepted and admin.*',
            'pending': r'^pending',
            'resolved': r'^resolved.*',
            'blank': r'.*'

        }

        data['mapped_current_case_status'] = data['clean_current_status'].apply(lambda x: [k for k, v in mapping.items() if re.match(v, str(x))][0])
                            
        return data
        

def main():

    filepath = 'analysis/output_data/epa_complaints_2014_2021.csv'

    analyzer = transformMapComplaintdata(filepath)
    analyzer.map_current_status()

    analyzer.mapped_data.to_csv('analysis/output_data/mapped_data_complaint_logs_titlevi.csv', index = False)

if __name__ == "__main__":
    main()