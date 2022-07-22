import unittest
from analysis.processors.clean_epa_complaints_2014_2022  import TitleVIDataModel


class TestEPAComplaintsClean2014to2022(unittest.TestCase):

    def setUp(self):
        self.file_path = 'analysis/source_data/epa-complaints-2014-2021.csv'
        self.analyzer = TitleVIDataModel(self.file_path)
        
        self.columns_list_after_transform = [
            'epa_complaint_#',
            'named_entity',
            'date_received',
            'alleged_discrimination_basis',
            'current_status',
            'clean_date_received',
            'clean_current_status',
            'clean_current_status_date',
            'clean_current_status_reason',
            'clean_alleged_discrimination_basis',
            0,
            1,
            'time_elapsed_since_update']
        
        self.filter_columns = [
            'epa_complaint_#',
            'named_entity',
            'clean_date_received',
            'clean_current_status',
            'clean_current_status_date',
            'clean_current_status_reason',
            'clean_alleged_discrimination_basis',
            0,
            1,
            'time_elapsed_since_update',
            ]
    
    def test_epa_complaint_data_2014_2022_clean_and_tranforms(self):
        data = self.analyzer.clean_data().transform_data().get_data()

        self.assertCountEqual(data.columns, self.columns_list_after_transform)
    
    def test_epa_complaint_data_2014_2022_filter_columns(self):
        data = self.analyzer.clean_data().transform_data().filter_columns().get_data()

        self.assertCountEqual(data.columns, self.filter_columns)

if __name__ == '__main__':
    unittest.main()