#!/usr/bin/env python

import pandas as pd
import numpy as np
import re
import fire


class ComplaintDataMap:
    """_summary_"""

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

    def map_primary_status(self):
        """_summary_"""

        mapping = {
            "rejected": r"^rejected$|not accepted.*|^rejected/closed|^rejected and closed|^rejected 5|^rejected/admin.*|^rejected without prejudice",
            "rejected & referred": r"^rejected.*referred.*|^referred.*",
            "administrative closure": r"^admin|^accepted and admin.*",
            "pending": r"^pending.*",
            "resolved": r"^resolved.*",
            "": r".*",
        }

        self.data["primary_status_map"] = self.data["primary_status"].apply(
            lambda x: [k for k, v in mapping.items() if re.match(v, str(x))][0]
        )

        data = self.reorder_columns()

        return data

    def reorder_columns(self):
        """ """
        reorder_columns = [
            "fy__rec'd",
            "summary__status",
            "epa__file__#",
            "named_entity",
            "clean_date_received",
            "detailed_status",
            "primary_status",
            "primary_status_map",
            "secondary_status",
            "recent_status_date",
            "referred_agency",
            "disc_basis_1",
            "disc_basis_2",
            "time_difference",
        ]

        data = self.data[reorder_columns]

        return data


def main(file_path: str, output_path: str):
    """_summary_

    Args:
        file_path (str): _description_
        output_path (str): _description_
    """
    analyzer = ComplaintDataMap(file_path)
    mapped_data = analyzer.map_primary_status()

    mapped_data.to_csv(output_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
