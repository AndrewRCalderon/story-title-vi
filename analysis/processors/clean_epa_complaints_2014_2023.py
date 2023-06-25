#!/usr/bin/env python

import pandas as pd
import helper_functions.helpers as helpers
import fire
import pdb
import logging


class TitleVIDataClean:
    """Class that handles cleaning EPA Complaints data from 2014 to 2023-02-09"""

    def __init__(self, file_path: str, recent_status_date: str):
        self.RECENT_STATUS_DATE = recent_status_date
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        data = pd.read_csv(self.file_path)
        # data = data.drop("Unnamed: 7", axis="columns")

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

    def check_expected_columns(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        expected_columns = [
            "fy_rec'd",
            "summary_status",
            "epa_file_#",
            "named_entity",
            "date_received",
            "alleged_discrimination_basis",
            "detailed_status",
            "primary_status",
            "referred_agency",
            "secondary_status",
            "recent_status_date",
            "clean_alleged_discrimination_basis",
            "disc_basis_1",
            "disc_basis_2",
            "clean_date_received",
            "time_difference",
        ]

        current_column_names = list(self.data.columns.values)

        assert (
            expected_columns == current_column_names
        ), f"Expected columns: {expected_columns} but got {current_column_names}"

        return self.data.columns

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
        repeat_headers = self.data[self.data["fy_rec'd"].str.contains("Rec'd")]

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

    def remove_spaces(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data = self.data.apply(
            lambda s: s.str.replace("  ", " ") if s.dtype == object else s,
            axis="index",
        )

        self.data["epa_file_#"] = self.data["epa_file_#"].str.replace(" ", "")

        return self

    def change_date_format(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data["clean_date_received"] = pd.to_datetime(
            self.data["date_received"], errors="coerce"
        )

        if self.data["clean_date_received"].isnull().sum() > 0:
            logging.warning(
                f"Number of null values in clean_date_received: {self.data['clean_date_received'].isnull().sum()}"
            )
        else:
            logging.warning("No null values in clean_date_received")

        self.data["recent_status_date"] = pd.to_datetime(
            self.data["recent_status_date"], errors="coerce"
        )

    def extract_primary_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        primary_status_captures = self.capture_patterns_to_dict(
            self.data,
            "detailed_status",
            "primary_status",
            r"^(.*?)\d{1,2}/\d{1,2}/\d{4}[;: ]|(.*):|(^resolved|^technical)",
            3,
        )

        # assign primary_status column to data with captures
        self.data = self.data.assign(**primary_status_captures)

        # extract referral agency from primary_status
        # before cleaning the column
        self.extract_referrals()

        # clean primary status column
        self.data = self.clean_primary_status(self.data)

        return self

    def extract_secondary_status(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # Write regex that capture everything after : except dates

        secondary_status_captures = self.capture_patterns_to_dict(
            self.data,
            "detailed_status",
            "secondary_status",
            r":(.*)(?!\d{1,2}\/\d{1,2}\/\d{4})",
            1,
        )

        # assign secondary_status column to data with captures
        self.data = self.data.assign(**secondary_status_captures)

        # clean secondary status column
        self.data = self.clean_secondary_status(self.data)

        return self

    def extract_dates(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # the regex uses a positive lookbehind to make sure that the date is preceded by a space
        date_captures = self.capture_patterns_to_dict(
            self.data,
            "detailed_status",
            "recent_status_date",
            r"(\b\d{1,2}\/\d{1,2}\/\d{4}\b)(?=[^\/]*$)",
            1,
        )

        # assign secondary_status column to data with captures
        self.data = self.data.assign(**date_captures)

        # fill null values in recent_status_date column
        self.data.recent_status_date = self.fill_recent_status_date()

        return self

    def fill_recent_status_date(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data["recent_status_date"] = self.data["recent_status_date"].fillna(
            self.RECENT_STATUS_DATE
        )

        return self.data["recent_status_date"]

    def extract_referrals(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        referred_agency_captures = self.capture_patterns_to_dict(
            self.data,
            "primary_status",
            "referred_agency",
            " (hud) | to (.*)| \((.*)\)",
            3,
        )

        # assign secondary_status column to data with captures
        self.data = self.data.assign(**referred_agency_captures)

        return self

    def extract_discrimination_basis(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        discrimination_basis_captures = self.capture_patterns_to_dict(
            self.data,
            "alleged_discrimination_basis",
            "clean_alleged_discrimination_basis",
            r".*: (.*)",
            1,
        )

        # assign clean_alleged_discrimination_basis column to data with captures
        self.data = self.data.assign(**discrimination_basis_captures)

        # clean clean_alleged_discrimination_basis column
        self.data = self.clean_discrimination_basis(self.data)

        return self

    def calculate_time_difference(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        self.data["time_difference"] = (
            self.data["recent_status_date"] - self.data["clean_date_received"]
        ).dt.days

        return self

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

        # remove all unwanted single and double spaces
        self.remove_spaces()

        # extract primary status from detailed_status
        self.extract_primary_status()

        # extract secondary status from detailed_status
        self.extract_secondary_status()

        # extract most recent status date from detailed_status
        self.extract_dates()

        # extract discrimination basis from alleged__discrimination__basis
        self.extract_discrimination_basis()

        # change date format to datetime for date_received and recent_status_date
        self.change_date_format()

        # calculate time difference
        self.calculate_time_difference()

        # get column to assert that all expected columns are present
        self.check_expected_columns()

        # filter columns to include only the columns for the final analysis
        data = self.filter_columns(self.data)

        return data

    @staticmethod
    def capture_patterns_to_dict(
        data,
        regex_column_name: str,
        new_column_name: str,
        pattern: str,
        number_of_capture_groups: int,
    ):
        """
        This method processes a column using pattern-matching and produces
        a dict based on the capture groups from the pattern.

        Args:
            data (pd.DataFrame): _description_
            regex_column_name (str): _description_
            new_column_name (str): _description_
            pattern (str): _description_
            number_of_capture_groups (int): _description_

        Returns:
            dict: _description_
        """

        capture_groups_dict = {}
        capture_groups = data[regex_column_name].str.extract(pattern, expand=False)

        if number_of_capture_groups == 1:
            capture_groups_dict = {new_column_name: capture_groups}

        if number_of_capture_groups == 2:
            capture_groups_dict = {
                new_column_name: capture_groups[0].fillna(capture_groups[1])
            }

        if number_of_capture_groups == 3:
            capture_groups_dict = {
                new_column_name: capture_groups[0]
                .fillna(capture_groups[1])
                .fillna(capture_groups[2])
            }

        return capture_groups_dict

    @staticmethod
    def clean_primary_status(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        data["primary_status"] = (
            data["primary_status"]
            .str.replace("1", "", regex=False)
            .str.replace(r" to \w+", "", regex=True)
            .str.replace(r" with.*", "", regex=True)
            .str.replace(r" \(.*\)", "", regex=True)
            .str.replace(r"\d{1,2}/\d{1,2}/\d{4}.*", "", regex=True)
            .str.replace(r" -.*", "", regex=True)
            .str.replace(r" office.*", "", regex=True)
            .str.replace(r" w/o prejudice.*", "", regex=True)
            .str.replace(r" \d.*", "", regex=True)
            .str.strip()
        )

        return data

    @staticmethod
    def clean_secondary_status(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        data["secondary_status"] = (
            data["secondary_status"]
            .str.replace(r"\d+.*;", "", regex=True)
            .str.replace(r"\d+.*\d", "", regex=True)
            .str.strip()
        )

        return data

    @staticmethod
    def clean_discrimination_basis(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_

        Returns:
            _type_: _description_
        """
        data[["disc_basis_1", "disc_basis_2"]] = data[
            "clean_alleged_discrimination_basis"
        ].str.split(r",|;", expand=True)

        return data

    @staticmethod
    def filter_columns(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_
        """

        filter_columns = [
            "fy_rec'd",
            "summary_status",
            "epa_file_#",
            "named_entity",
            "clean_date_received",
            "detailed_status",
            "primary_status",
            "secondary_status",
            "recent_status_date",
            "referred_agency",
            "disc_basis_1",
            "disc_basis_2",
            "time_difference",
        ]

        return data[filter_columns]


def main(file_path: str, output_path: str, recent_status_date: str):
    """
    Calls TitleVIDataClean class to clean data. Outputs cleaned data to csv.

    Args:
        file_path (str): file_path to EPA complaint data from 2023

    Returns:
        None
    """
    # Instantiate an instance of TitleVIDataClean
    analyzer = TitleVIDataClean(file_path, recent_status_date)

    # Load the data
    data = analyzer.load_data()

    # Assert that the number of rows is 275
    assert len(data) == 275, f"Unexpected number of rows in dataframe: ${len(data)}"

    # Runs all the cleaning functions for the entire class
    data_clean = analyzer.clean_data()

    # Save the cleaned data to a csv
    data_clean.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
