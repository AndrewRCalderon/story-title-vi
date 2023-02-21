#!/usr/bin/env python

import pandas as pd
import helper_functions.helpers as helpers
import fire
import pdb
import logging


class TitleVIDataClean:
    """Class that handles cleaning EPA Complaints data from 2014 to 2023-02-09"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        data = pd.read_csv(self.file_path)

        return data

    def get_data(self, return_copy=True):
        """_summary_

        Args:
            return_copy (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if return_copy:
            return self.data.copy()

    def standardize_columns(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        old_columns = self.data.columns
        self.data.columns = helpers.clean_columns(self.data)

        logging.warning(
            f"The columns names have changed. Old columns: {old_columns} and new columns: {self.data.columns}"
        )

    def filter_headers(self):
        """_summary_"""
        data_length = len(self.data)
        repeat_headers = self.data[self.data["fy__rec'd"].str.contains("Rec'd")]

        logging.warning(f"Number of repeated headers in data: {len(repeat_headers)}")

        # remove rows with repeated headers cotaining "FY Rec'd"
        # by index
        self.data = self.data.drop(repeat_headers.index)

        assert data_length - len(repeat_headers) == len(
            self.data
        ), f"Expected {data_length - len(repeat_headers)} rows, got {len(self.data)}"

        return self

    def remove_newline_characters(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data = self.data.apply(
            lambda s: s.str.lower()
            .str.strip()
            .str.replace("\r", " ")
            .str.replace("\n", " ")
            if s.dtype == object
            else s,
            axis="index",
        )

        return self

    def change_date_format(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data["clean_date_received"] = pd.to_datetime(
            self.data["date__received"], errors="coerce"
        )

        if self.data["clean_date_received"].isnull().sum() > 0:
            logging.warning(
                f"Number of null values in clean_date_received: {self.data['clean_date_received'].isnull().sum()}"
            )
        else:
            logging.warning("No null values in clean_date_received")

    def clean_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # standardize column names using helpers function
        self.standardize_columns()

        # removes all repetive column names from OCR
        self.filter_headers()

        # remove newline characters from all values
        self.remove_newline_characters()

        # change date format to datetime
        self.change_date_format()

        data = self.data

        return data


def main(file_path: str, output_path: str):
    """
    Calls TitleVIDataClean class to clean data. Outputs cleaned data to csv.

    Args:
        file_path (str): file_path to EPA complaint data from 2023
    """
    analyzer = TitleVIDataClean(file_path)
    data = analyzer.load_data()

    print(data.columns)

    assert len(data) == 251, f"Unexpected number of rows in dataframe: ${len(data)}"

    data_clean = analyzer.clean_data()

    # data_clean.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
