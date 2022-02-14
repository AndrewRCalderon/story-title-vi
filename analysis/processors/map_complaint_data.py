import pandas as pd
import numpy as np

class transformMapComplaintdata: 

    def __init__(self, filepath):
        self.filepath = filepath
        self.mapped_data = self.map_current_status()
    
    def map_current_status(self):
        data = pd.read_csv(self.filepath)


        # describe regex matches
        regex_rejected_match = r'(^rejected$|not accepted.*|^rejected/closed|^rejected and closed|^rejected 5)'
        regex_rejected_referred_match = r'(^rejected.*referred)'
        regex_rejected_without_prejudice_match = r'(^rejected without prejudice)'

        regex_admin_closure_match = r'(^admin|^accepted and admin.*)'

        regex_pending_match = r'(^pending)'

        regex_resolved_match = r'(^resolved.*)'

        

        # store extracted strings
        data['rejected'] = data['clean_current_status'].str.extract(regex_rejected_match)
        data['rejected_referred'] = data['clean_current_status'].str.extract(regex_rejected_referred_match)

        data['admin_closure'] = data['clean_current_status'].str.extract(regex_admin_closure_match)

        data['pending'] = data['clean_current_status'].str.extract(regex_pending_match)

        data['resolved'] = data['clean_current_status'].str.extract(regex_resolved_match)

        data['rejected_without_prejudice'] = data['clean_current_status'].str.extract(regex_rejected_without_prejudice_match)

        

        # set conditions for value mapping
        rejected_conditions = [(data['rejected'].str.contains('.*') == True)]
        rejected_referred_conditions = [(data['rejected_referred'].str.contains('.*') == True)]
        rejected_without_prejudice_conditions = [(data['rejected_without_prejudice'].str.contains('.*') == True)]

        admin_closure_conditions = [(data['admin_closure'].str.contains('.*') == True)]

        pending_conditions = [(data['pending'].str.contains('.*') == True)]

        resolved_conditions = [(data['resolved'].str.contains('.*') == True)]

        

        # set choices based on conditions above
        rejected_choices = ["rejected"]
        rejected_referred_choices = ["rejected & referred"]
        rejected_without_prejudice_choices = ["rejected without prejudice"]

        admin_closure_choices = ["administrative closure"]

        pending_choices = ["pending"]

        resolved_choices = ["resolved"]

        # apply conditions and choices to create new mapped columns
        data['rejected_map'] = np.select(rejected_conditions, rejected_choices, default='')
        data['rejected_referred_map'] = np.select(rejected_referred_conditions, rejected_referred_choices, default='')
        data['rejected_without_prejudice_map'] = np.select(rejected_without_prejudice_conditions, rejected_without_prejudice_choices, default='')

        data['admin_closure_map'] = np.select(admin_closure_conditions, admin_closure_choices, default='')

        data['pending_map'] = np.select(pending_conditions, pending_choices, default='')

        data['resolved_map'] = np.select(resolved_conditions, resolved_choices, default='')

        # generate single column with all mapped variables
        data['mapped_current_case_status'] = data['rejected_map'] +\
            data['rejected_referred_map'] +\
                data['rejected_without_prejudice_map'] +\
                    data['admin_closure_map'] +\
                        data['pending_map'] +\
                            data['resolved_map'] 
                            
        

        
        return data

        

def main():

    filepath = 'analysis/output_data/data_complaint_logs_titlevi.csv'

    mapper = transformMapComplaintdata(filepath)
    mapper.map_current_status()

    mapper.mapped_data.to_csv('analysis/output_data/mapped_data_complaint_logs_titlevi.csv', index = False)

if __name__ == "__main__":
    main()