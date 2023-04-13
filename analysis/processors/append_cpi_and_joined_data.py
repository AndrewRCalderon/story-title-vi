#!/usr/bin/env python

import pandas as pd
import fire
import logging
import re


class EpaCpiDataAppender:
    """ """

    def __init__(self, joined_data, cpi_data):
        self.joined_data = joined_data
        self.cpi_data = cpi_data

    def append_data(self):
        """Merge joined_data and cpi_data"""

        self.cpi_data = self.map_new_primary_status_to_cpi_statuses(self.cpi_data)

        appended_data = pd.concat(
            [self.joined_data, self.cpi_data],
            ignore_index=True,
        )

        appended_data = self.filter_columns(appended_data)

        return appended_data

    @staticmethod
    def filter_columns(data: pd.DataFrame):
        """Filter columns"""

        filter_columns = [
            "fy_rec'd",
            "summary_status",
            "epa_file_#",
            "named_entity",
            "clean_date_received",
            "detailed_status",
            "primary_status",
            "primary_status_map",
            "final_adjudication_&_reason",
            "secondary_status",
            "clean_current_status_reason",
            "recent_status_date",
            "referred_agency",
            "disc_basis_1",
            "disc_basis_2",
            "disc_basis_3",
            "disc_basis_4",
            "disc_basis_5",
            "time_difference",
            "investigated_not_investigated",
            "manual_final_adjudication_reason",
            "_merge",
        ]

        data = data[filter_columns]

        return data

    @staticmethod
    def map_new_primary_status_to_cpi_statuses(data: pd.DataFrame):
        """_summary_"""

        mapping = {
            "rejected": r"^Denied - Financial, Untimely|^Denied - Untimely, Claims|^Denied - Financial|^Denied|^Denied - Financial,  Untimely|^Denied - Untimely, Litigation|^Denied - Financial, Claims|^Denied - Financial, Untimely, Claims|^Dismissed - Moot|^Dismissed Without Prejudice|^Dismissed without prejudice; Denied - Untimely|^Dismissed without prejudice; Denied - Financial|^Dismissed without prejudice|^Denied - Untimely Claims|^Denied- Claims|^Denied - Untimely Litigation|^Dismissed|^Denied - Untimely|^Denied - Moot|^Denied - Financial|^Denied|^Denied - Claim|^Denied - Claims|^Denied - Claims Untimely|^Denied - Financial  Untimely|^Denied - Financial Claims",
            "rejected & referred": r"Denied - Financial;Referred|^Denied - Financial, Referred|^Denied - Financial; Referred|^Closed - Referred|^Denied - Claim \(referred\)|^Denied - Claims Referred|^Denied - Claims, Referred|^Denied - Referred |^Denied - Financial Referred|^Denied - Financial Untimely Claims",
            "administrative closure": r"^Closed - Withdrawn",
            "pending": r"Pending",
            "resolved": r"^Closed - Agreement|^Closed - Informally Resolved|^Closed - Settlement",
            "": r".*",
        }

        data["primary_status_map"] = data["final_adjudication_&_reason"].apply(
            lambda x: [k for k, v in mapping.items() if re.fullmatch(v, str(x))][0]
        )

        return data


def main(file_path1: str, file_path2: str, output_path: str):
    """Merge mapped_data and manual_data"""

    logging.warning(f"Reading data from {file_path1} and {file_path2}...")

    mapped_data = pd.read_csv(file_path1)
    manual_data = pd.read_csv(file_path2)

    appended_data = EpaCpiDataAppender(mapped_data, manual_data).append_data()

    appended_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
