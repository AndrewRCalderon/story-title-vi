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
            left_on="epa_file_#",
            right_on="epa_complaint_#",
            indicator=True,
        )

        merged_data = self.filter_columns(merged_data)

        return merged_data

    @staticmethod
    def filter_columns(data: pd.DataFrame):
        """Filter columns"""

        filter_columns = [
            "fy_rec'd",
            "summary_status",
            "epa_file_#",
            "named_entity_x",
            "clean_date_received_x",
            "detailed_status",
            "primary_status",
            "primary_status_map",
            "clean_current_status",
            "secondary_status",
            "clean_current_status_reason",
            "recent_status_date",
            "referred_agency",
            "disc_basis_1",
            "disc_basis_2",
            "time_difference",
            "investigated_not_investigated",
            "manual_final_adjudication_reason",
            "_merge",
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
