#!/usr/bin/env python

import pandas as pd
import fire
import logging
import re


class EpaCpiDataAppender:
    """Append mapped_data and manual_data and match CPI 1996 - 2013 categoris
    to new categories from 2014 to present"""

    def __init__(self, joined_data, cpi_data):
        self.joined_data = joined_data
        self.cpi_data = cpi_data

    def flag_dfs(self):
        """Flag df"""

        self.joined_data["origin"] = "epa"
        self.cpi_data["origin"] = "cpi"

    def append_data(self):
        """Merge joined_data and cpi_data"""

        # add a column to each dataframe that indicates the origin of the data
        self.flag_dfs()
        # map the new primary status to the cpi statuses
        self.cpi_data = self.map_new_primary_status_to_cpi_statuses(self.cpi_data)

        appended_data = pd.concat(
            [self.joined_data, self.cpi_data],
            ignore_index=True,
        )

        return appended_data

    @staticmethod
    def clean_data(data):
        """Clean data"""

        data = data.dropna(subset=["epa_file_#"])

        assert len(data) == 539, f"Data is {len(data)} not the correct length"

        return data

    @staticmethod
    def map_new_primary_status_to_cpi_statuses(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        mapping = {
            "rejected": r"^Denied - Claims, Untimely|^Denied - Financial, Claims, Untimely|^Denied - Financial, Untimely|^Denied - Untimely, Claims|^Denied - Financial|^Denied|^Denied - Financial, Untimely|^Denied - Untimely, Litigation|^Denied - Financial, Claims|^Denied - Financial, Untimely, Claims|^Dismissed - Moot|^Dismissed Without Prejudice|^Dismissed without prejudice; Denied - Untimely|^Dismissed without prejudice; Denied - Financial|^Dismissed without prejudice|^Denied - Untimely Claims|^Denied- Claims|^Denied - Untimely Litigation|^Dismissed|^Denied - Untimely|^Denied - Moot|^Denied - Financial|^Denied|^Denied - Claim|^Denied - Claims|^Denied - Claims Untimely|^Denied - Financial  Untimely|^Denied - Financial Claims",
            "rejected and referred": r"^Denied - Untimely, Referred|^Denied - Financial, Claims, Referred|^Denied - Referred|^Denied - Financial, Referred|^Denied - Financial; Referred|^Closed - Referred|^Denied - Claim \(referred\)|^Denied - Claims Referred|^Denied - Claims, Referred|^Denied - Financial Referred",
            "closed: complaint withdrawn": r"^Closed - Withdrawn",
            "pending": r"Pending",
            "resolved: agreement": r"^Closed - Agreement|^Closed - Informally Resolved|^Closed - Settlement",
            "": r".*",
        }

        data["final_adjudication_&_reason"] = (
            data["final_adjudication_&_reason"].str.strip().str.replace("  ", " ")
        )

        data["primary_status_map"] = data["final_adjudication_&_reason"].apply(
            lambda x: [k for k, v in mapping.items() if re.fullmatch(v, str(x))][0]
        )

        return data


def main(file_path1: str, file_path2: str, output_path: str):
    """Merge mapped_data and manual_data"""

    logging.warning(f"Reading data from {file_path1} and {file_path2}")

    mapped_data = pd.read_csv(file_path1)
    manual_data = pd.read_csv(file_path2)

    appended_data = EpaCpiDataAppender(mapped_data, manual_data).append_data()

    cleaned_data = EpaCpiDataAppender.clean_data(appended_data)

    cleaned_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
