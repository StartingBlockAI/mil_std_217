import unittest
import pandas as pd
from src.reliability.data_completeness import identify_missing_info

class TestDataCompleteness(unittest.TestCase):
    def test_identify_missing_info(self):
        # Create a DataFrame that simulates processed BOM data.
        data = {
            "FN": ["1", "2", "3"],
            "ManufacturerPartNumber": ["ABC123", None, "XYZ789"],
            "Quantity": [10, 20, 30],
            "Description": ["1k resistor ±5% 5V", "10uF capacitor ±10% 12V", "47 IC 3.3V"],
            "DrawingRef": ["R1", "C1", "IC1"],
            "PartType": ["Resistor", "Capacitor", "IC"],
            "Value": [1000, 10e-6, 47],
            "Tolerance": [5, 10, None],
            "Voltage": [5, 12, 3.3]
        }
        df = pd.DataFrame(data)
        df = identify_missing_info(df)
        # Row 1 should have no missing fields.
        self.assertEqual(df.loc[0, "MissingFields"], "")
        # Row 2 is missing ManufacturerPartNumber.
        self.assertIn("ManufacturerPartNumber", df.loc[1, "MissingFields"])
        # For row 3 (an IC), tolerance is not required.
        self.assertEqual(df.loc[2, "MissingFields"], "")
    
if __name__ == '__main__':
    unittest.main()
