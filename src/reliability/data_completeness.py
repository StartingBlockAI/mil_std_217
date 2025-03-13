"""
Module: data_completeness
Description: Provides functionality to check the processed BOM DataFrame for missing required
             information needed to perform MIL‑STD‑217 calculations.
"""

import pandas as pd

def identify_missing_info(df):
    """
    Checks the DataFrame for missing required fields needed for MIL‑STD‑217 calculations.

    For example, the following fields are typically required:
      - ManufacturerPartNumber: The manufacturer's part number.
      - PartType: Derived from the description.
      - Value: Numeric value (e.g., resistance, capacitance).
      - Tolerance: Tolerance percentage (for resistors and capacitors).
      - Voltage: Voltage rating.

    Args:
        df (pandas.DataFrame): The processed BOM DataFrame with computed columns.

    Returns:
        pandas.DataFrame: A copy of the DataFrame with an added "MissingFields" column
                          that lists any fields that are missing for that row.
    """
    required_fields = ["ManufacturerPartNumber", "PartType", "Value", "Tolerance", "Voltage"]

    def missing_fields(row):
        missing = []
        for field in required_fields:
            # For tolerance, we require it only for resistors and capacitors.
            if field == "Tolerance" and row["PartType"] not in ["Resistor", "Capacitor"]:
                continue
            if pd.isna(row[field]):
                missing.append(field)
        return ", ".join(missing) if missing else ""

    df = df.copy()
    df["MissingFields"] = df.apply(missing_fields, axis=1)
    return df

if __name__ == "__main__":
    # For testing purposes, import the BOM processor and check data completeness.
    from bom_processor import process_bom
    try:
        processed_bom = process_bom("BOM Only.xlsx")
        completeness_report = identify_missing_info(processed_bom)
        print(completeness_report[["FN", "ManufacturerPartNumber", "PartType", "Value", "Tolerance", "Voltage", "MissingFields"]])
    except Exception as e:
        print(f"Error in data completeness check: {e}")
