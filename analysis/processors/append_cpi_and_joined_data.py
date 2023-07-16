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
    def rename_columns(data: pd.DataFrame):
        new_columns = {
            "clean_date_received": "date_received",
            "detailed_status": "original_detailed_status",
            "primary_status_map": "mapped_primary_status_original_detailed",
            "simplified_status": "manual_simplified_status",
        }

        data = data.rename(new_columns, axis=1)

        return data


def main(file_path1: str, file_path2: str, output_path: str):
    """Merge mapped_data and manual_data"""

    logging.warning(f"Reading data from {file_path1} and {file_path2}")

    mapped_data = pd.read_csv(file_path1)
    manual_data = pd.read_csv(file_path2)

    appended_data = EpaCpiDataAppender(mapped_data, manual_data).append_data()

    cleaned_data = EpaCpiDataAppender.clean_data(appended_data)

    renamed_data = EpaCpiDataAppender.rename_columns(cleaned_data)

    renamed_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
