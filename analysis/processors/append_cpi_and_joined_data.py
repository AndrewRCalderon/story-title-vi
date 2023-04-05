#!/usr/bin/env python

import pandas as pd
import fire
import logging


class JoinedDataCPIDataAppender:
    """ """

    def __init__(self, joined_data, cpi_data):
        self.joined_data = joined_data
        self.cpi_data = cpi_data
        # self.merged_data = self.merge_data()
    

    def append_data(self):
        """Merge joined_data and cpi_data"""

        concat_data = pd.concat(
            self.joined_data,
            self.cpi_data,
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

class JoinedDataCPIDataMapper:
    """_summary_
    """
    
    def map_new_primary_status_to_cpi_statuses(self):
        """_summary_"""

        mapping = {
            "rejected": r"^Dismissed - Moot|^Dismissed Without Prejudice|^Dismissed without prejudice; Denied - Untimely|^Dismissed without prejudice; Denied - Financial|^Dismissed without prejudice|^Denied - Untimely Claims|^Denied- Claims|^Denied - Untimely Litigation|^Dismissed|^Denied - Untimely|^Denied - Moot|^Denied - Financial|^Denied|^Denied - Claim|^Denied - Claims|^Denied - Claims Untimely|^Denied - Financial  Untimely|^Denied - Financial Claims",
            "rejected & referred": r"^Denied - Financial; Referred|^Closed - Referred|^Denied - Claim \(referred\)|^Denied - Claims Referred|^Denied - Referred |^Denied - Financial Referred|^Denied - Financial Untimely Claims",
            "administrative closure": r"^Closed - Withdrawn|",
            "pending": r"Pending",
            "resolved": r"^Closed - Agreement|^Closed - Informally Resolved|^Closed - Settlement",
            "": r".*"}

        self.data["primary_status_map"] = self.data["primary_status"].apply(
            lambda x: [k for k, v in mapping.items() if re.match(v, str(x))][0]
        )

        data = self.reorder_columns()

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
