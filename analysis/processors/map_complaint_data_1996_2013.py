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

        self.data["final_adjudication_&_reason"] = (
            self.data["final_adjudication_&_reason"].str.strip().str.replace("  ", " ")
        )

        self.data["simplified_status_primary"] = self.data[
            "final_adjudication_&_reason"
        ].apply(lambda x: [k for k, v in mapping.items() if re.fullmatch(v, str(x))][0])

        data = self.data

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
