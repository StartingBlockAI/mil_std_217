import unittest
import pandas as pd
from io import BytesIO
from src.reliability.bom_processor import parse_description, convert_value, process_bom

class TestBomProcessor(unittest.TestCase):

    def test_parse_description_resistor(self):
        desc = "1k resistor ±5% 5V"
        result = parse_description(desc)
        self.assertEqual(result['PartType'], "Resistor")
        # 1k should be converted to 1000
        self.assertAlmostEqual(result['Value'], 1000, places=2)
        self.assertAlmostEqual(result['Voltage'], 5, places=2)
        # Tolerance extraction is handled in parse_description, so check if tolerance was captured.
        self.assertAlmostEqual(result['Tolerance'], 5, places=2)

    def test_convert_value(self):
        self.assertAlmostEqual(convert_value("1k"), 1000, places=2)
        self.assertAlmostEqual(convert_value("10uF"), 10e-6, places=8)
        self.assertAlmostEqual(convert_value("100pF"), 100e-12, places=12)
    
    def test_process_bom(self):
        # Create a sample DataFrame that simulates a BOM file.
        data = {
            "FN": ["1", "2"],
            "Manufacturer Part Number": ["ABC123", "XYZ789"],
            "Quantity": [10, 20],
            "Description": ["1k resistor ±5% 5V", "10uF capacitor ±10% 12V"],
            "Reference\nDesignators": ["R1", "C1"]
        }
        df = pd.DataFrame(data)
        # Write a dummy first row as an indicator and then the data with headers.
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            pd.DataFrame([["Indicator row"]]).to_excel(writer, header=False, index=False)
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        
        processed_df = process_bom(excel_buffer)
        self.assertIn("PartType", processed_df.columns)
        self.assertIn("Value", processed_df.columns)
        self.assertIn("Tolerance", processed_df.columns)
        self.assertEqual(processed_df.shape[0], 2)

if __name__ == '__main__':
    unittest.main()
