#!/usr/bin/env python

import pandas as pd
from processors import clean_columns
import fire
import logging


def clean_columns(data):
    data.columns = (
        data.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace("\r", "_", regex=False)
        .str.replace("\n", "_", regex=False)
    )

    return data.columns


class TitleVIDataClean:
    """
    Class that handles cleaning EPA complaints data collected by CPI
    from 1996 to 2013
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        """Load data"""
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
        self.data.columns = clean_columns(self.data)

        logging.warning(
            f"The columns names have changed. Old columns: {old_columns} and new columns: {self.data.columns}"
        )

    def check_expected_columns(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        expected_columns = [
            "epa_file_no.",
            "complainant/attorney",
            "date_of_title_vi_complaint",
            "accused_agency",
            "claim_of_discrimination",
            "concern_employment_discrimination?_y/n",
            "grievance_summary",
            "neighborhood",
            "city",
            "state",
            "county",
            "date_epa_received_complaint",
            "complaint_filed_within_180_day_limit?",
            "complaint_describes_title_vi_prohibited_discrimination?",
            "accused_agency_receives_epa_funding?",
            "ocr_review_ruling",
            "referred_agency",
            "date_ocr_sent_review_response_to_complainant",
            "ocr_investigationdate",
            "final_adjudication_&_reason",
            "cpi_ocr_final_investigation_date",
            "documents",
        ]

        current_column_names = list(self.data.columns.values)

        assert (
            expected_columns == current_column_names
        ), f"Expected columns: {expected_columns} but got {current_column_names}"

        return self.data.columns

    def change_column_names(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        rename_columns_dict = {
            "epa_file_no.": "epa_file_#",
            "accused_agency": "named_entity",
        }

        self.data.rename(columns=rename_columns_dict, inplace=True)

    def create_recent_status_date_column(self):
        """
        Combine date columns to preserve the most recent date for each row.

        The CPI data has multiple date columns, and we need one single column
        for our analysis. There is "date_of_title_vi_complaint",
        "date_ocr_sent_review_response_to_complainant", "ocr_investigationdate"
        and "cpi_ocr_final_investigation_date".

        After looking at the graphic, it seems that the time elapsed to resolve
        a case was calculated using the date the case came in, and the most
        recent date that appears in the data in any of the above mentioned columns

        So, we will combine those columns, except "date_of_title_vi_complaint"
        to create one single column.
        """

        # Replace all N/As with empty strings
        self.data["cpi_ocr_final_investigation_date"] = self.data[
            "cpi_ocr_final_investigation_date"
        ].str.replace("N/A", "")

        # There are some instances where "cpi_ocr_final_investigation_date" is empty
        # and "ocr_investigationdate" is not, so we don't want to overwrite those values.
        # So, we will fill the empty values in "cpi_ocr_final_investigation_date" with
        # the values in "ocr_investigationdate"
        self.data["cpi_ocr_final_investigation_date"].fillna(
            self.data["ocr_investigationdate"], inplace=True
        )

        # We place all values of in "ocr_investigationdate" with "cpi_ocr_final_investigation_date"
        # essentially shifting that column over to the left since it has the most recent dates.
        self.data["ocr_investigationdate"] = self.data[
            "cpi_ocr_final_investigation_date"
        ]

        # We will fill the empty values in "ocr_investigationdate" with
        # the values in "date_ocr_sent_review_response_to_complainant"
        self.data["ocr_investigationdate"].fillna(
            self.data["date_ocr_sent_review_response_to_complainant"], inplace=True
        )

    def extract_discrimination_basis(self):
        """_summary_

        Returns:
            _type_: _description_
        """

        # make all values lowercase
        self.data["claim_of_discrimination"] = self.data[
            "claim_of_discrimination"
        ].str.lower()

        # assign clean_alleged_discrimination_basis column to data with captures
        self.data[
            [
                "disc_basis_1",
                "disc_basis_2",
                "disc_basis_3",
                "disc_basis_4",
                "disc_basis_5",
            ]
        ] = self.data["claim_of_discrimination"].str.split(",", expand=True)

        return self

    def change_date_format(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        # the "" suffix is to make sure that I can later merge it with the joined data
        # without having to rename the column
        self.data["clean_date_received"] = pd.to_datetime(
            self.data["date_of_title_vi_complaint"], errors="coerce"
        )

        if self.data["clean_date_received"].isnull().sum() > 0:
            logging.warning(
                f"Number of null values in clean_date_received: {self.data['clean_date_received'].isnull().sum()}"
            )
        else:
            logging.warning("No null values in clean_date_received")

        self.data["recent_status_date"] = pd.to_datetime(
            self.data["ocr_investigationdate"], errors="coerce"
        )

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

        # get column to assert that all expected columns are present
        self.check_expected_columns()

        # change column names
        self.change_column_names()

        # create recent_status_date column
        self.create_recent_status_date_column()

        # split discrimination basis column
        self.extract_discrimination_basis()

        # change date format to datetime for date_received and recent_status_date
        self.change_date_format()

        # calculate time difference
        self.calculate_time_difference()

        # filter columns to include only the columns for the final analysis
        data = self.filter_columns(self.data)

        return data

    @staticmethod
    def filter_columns(data: pd.DataFrame):
        """_summary_

        Args:
            data (pd.DataFrame): _description_
        """

        filter_columns = [
            "epa_file_#",
            "clean_date_received",
            "recent_status_date",
            "time_difference",
            "named_entity",
            "referred_agency",
            "final_adjudication_&_reason",
            "disc_basis_1",
            "disc_basis_2",
            "disc_basis_3",
            "disc_basis_4",
            "disc_basis_5",
        ]

        return data[filter_columns]


def main(file_path: str, output_path: str):
    """
    Calls TitleVIDataClean class to clean data. Outputs cleaned data to csv.

    Args:
        file_path (str): file_path to EPA complaint data from 2023

    Returns:
        None
    """
    # Instantiate an instance of TitleVIDataClean
    analyzer = TitleVIDataClean(file_path)

    # Load the data
    data = analyzer.load_data()

    # Assert that the number of rows is 265
    assert len(data) == 265, f"Unexpected number of rows in dataframe: {len(data)}"

    # Runs all the cleaning functions for the entire class
    data_clean = analyzer.clean_data()

    # Save the cleaned data to a csv
    data_clean.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
