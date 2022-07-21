import unittest
from analysis.processors.clean_epa_complaints_2014_2022 import TitleVIDataModel

class TestEPAComplaintsClean2014to2022(unittest.TestCase):
    
    def test_epa_complaint_data_2014_2022_load(self):
        filepath = './analysis/source_data/epa-complaints-2014-2022-7-8.csv'
        runner = TitleVIDataModel(filepath)

        data = runner.load_data()

        self.assertEqual(len(data), 213)

if __name__ == '__main__':
    unittest.main()