#!/usr/bin/env python

import pandas as pd
import fire
import logging


class JoinComplaintData:
    """ """

    def __init__(self, mapped_data, manual_data):
        self.mapped_data = mapped_data
        self.manual_data = manual_data
        self.merged_data = self.merge_data()

    def merge_data(self):
        """Merge mapped_data and manual_data"""

        merged_data = pd.merge(
            self.mapped_data,
            self.manual_data,
            how="outer",
            on="epa_file_#",
            indicator=True,
        )

        merged_data = self.change_column_names(merged_data)
        merged_data = self.filter_columns(merged_data)

        return merged_data

    @staticmethod
    def change_column_names(data: pd.DataFrame):
        """_summary_

        Returns:
            _type_: _description_
        """
        rename_columns_dict = {
            "clean_date_received_x": "clean_date_received",
            "named_entity_x": "named_entity",
        }

        return data.rename(columns=rename_columns_dict)

    @staticmethod
    def filter_columns(data: pd.DataFrame):
        """Filter columns"""

        filter_columns = [
            "fy_rec'd",
            "summary_status",
            "epa_file_#",
            "_merge",
            "named_entity",
            "clean_date_received",
            "recent_status_date",
            "time_difference",
            "detailed_status",
            "primary_status",
            "primary_status_map",
            "simplified_status",
            "reason_for_rejection_if_applicable",
            "presidential_administration",
            "environmental_justice_issue_cited",
            "city",
            "state",
            "zip_code",
            "community_impacted",
            "referred_agency",
            "is_unique",
            "filed_by_a_lawyer",
            "group_filing",
            "filed_on_behalf_of",
            "epa_initiated_compliance_review",
            "complaint_about_environmental_justice_matter",
            "Notes_on_ej_categorization",
            "more_than_one_complaint",
            "total_related_complaints",
            "related_complaint_numbers",
            "complaint_link",
            "notes",
            "additional_notes",
            "disc_basis_1",
            "disc_basis_2",
            "related_documents",
        ]

        data = data[filter_columns]

        return data


def main(file_path1: str, file_path2: str, output_path: str):
    """Merge mapped_data and manual_data"""

    logging.warning(f"Reading data from {file_path1} and {file_path2}...")

    mapped_data = pd.read_csv(file_path1)
    manual_data = pd.read_csv(file_path2)

    merged_data = JoinComplaintData(mapped_data, manual_data).merged_data

    merged_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
