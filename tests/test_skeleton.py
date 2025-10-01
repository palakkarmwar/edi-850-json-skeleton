import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import pandas as pd
from edi850_to_json import parse_edi_850, cleanup_data, generate_ai_summary

class TestEDI850Repo(unittest.TestCase):

    def setUp(self):
        # Use the sample EDI file
        self.edi_file = "sample_edi/sample_850.txt"
        self.parsed_json = parse_edi_850(self.edi_file)
        self.df_clean = cleanup_data(self.parsed_json)

    def test_parse_json_structure(self):
        # Check basic keys
        self.assertIn("PO_Number", self.parsed_json)
        self.assertIn("Buyer", self.parsed_json)
        self.assertIn("Seller", self.parsed_json)
        self.assertIn("Items", self.parsed_json)
        self.assertIsInstance(self.parsed_json["Items"], list)
        self.assertGreater(len(self.parsed_json["Items"]), 0)

    def test_cleanup_dataframe(self):
        # Check numeric columns
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df_clean["Qty"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df_clean["Price"]))
        self.assertTrue(pd.api.types.is_numeric_dtype(self.df_clean["LineTotal"]))
        # Check non-empty
        self.assertGreater(len(self.df_clean), 0)

    def test_summary_file_created(self):
        # Generate AI summary
        generate_ai_summary(self.parsed_json)
        # Check file exists
        self.assertTrue(os.path.exists("outputs/summary.txt"))
        # Check file is not empty
        with open("outputs/summary.txt", "r") as f:
            content = f.read()
        self.assertGreater(len(content), 10)

if __name__ == "__main__":
    unittest.main()
