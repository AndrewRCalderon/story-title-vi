import unittest
import pandas as pd
from analysis.processors.clean_epa_complaints_2014_2022 import TitleVIDataModel


class TestEPAComplaintsClean2014to2022(unittest.TestCase):
    def setUp(self):
        self.analyzer = TitleVIDataModel()

        self.columns_list_after_transform = [
            "epa_complaint_#",
            "named_entity",
            "date_received",
            "alleged_discrimination_basis",
            "current_status",
            "clean_date_received",
            "clean_current_status",
            "clean_current_status_date",
            "clean_current_status_reason",
            "clean_alleged_discrimination_basis",
            0,
            1,
            "time_elapsed_since_update",
        ]

        self.filter_columns = [
            "epa_complaint_#",
            "named_entity",
            "clean_date_received",
            "clean_current_status",
            "clean_current_status_date",
            "clean_current_status_reason",
            "clean_alleged_discrimination_basis",
            0,
            1,
            "time_elapsed_since_update",
        ]

    # def test_epa_complaint_data_2014_2022_clean_and_tranforms(self):
    #     data = (
    #         self.analyzer.clean_data()
    #         .extract_pattern_matches()
    #         .clean_pattern_matches()
    #         .calculate_time_difference()
    #         .filter_columns()
    #         .get_data()
    #     )

    #     self.assertCountEqual(data.columns, self.columns_list_after_transform)

    # def test_epa_complaint_data_2014_2022_filter_columns(self):
    #     data = (
    #         self.analyzer.clean_data()
    #         .extract_pattern_matches()
    #         .clean_pattern_matches()
    #         .calculate_time_difference()
    #         .filter_columns()
    #         .get_data()
    #     )

    #     self.assertCountEqual(data.columns, self.filter_columns)

    def test_capture_patterns_to_dict_on_artificial_string(self):
        case_one_string = "rejected 1/28/2021: lack of jurisdiction"
        case_two_string = "pending: under jurisdictional review"
        test_data = pd.DataFrame.from_dict(
            {
                "artificial_string_column": [
                    case_one_string,
                    case_two_string,
                ]
            }
        )

        capture_groups_dict = self.analyzer.capture_patterns_to_dict(
            test_data,
            "artificial_string_column",
            "new_artificial_string_column",
            "(.*)\d{1,2}/\d{1,2}/\d{4}[: ]|(.*):",
            2,
        )

        print(capture_groups_dict)


if __name__ == "__main__":
    unittest.main()
