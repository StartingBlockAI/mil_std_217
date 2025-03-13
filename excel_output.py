"""
Module: excel_output
Description: Provides functions to create an Excel file output that includes all inputs
             for MIL‑STD‑217 calculations and summary totals.
"""

import io
import pandas as pd

def create_output_excel(df):
    """
    Creates an Excel file from the given DataFrame, formatting it as required.
    
    Args:
        df (pandas.DataFrame): Data containing BOM and MIL‑STD‑217 information.
    
    Returns:
        bytes: A binary stream of the Excel file content.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="MIL-STD-217 Data", index=False)
        
        # Optionally, add totals or summary calculations on a separate sheet
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Summary")
        writer.sheets["Summary"] = worksheet
        
        # Write summary information (this is a simple example)
        worksheet.write("A1", "Total Base Failure Rate")
        total_bfr = df["BaseFailureRate"].sum()
        worksheet.write("B1", total_bfr)
        
        # You can extend this section with more sophisticated calculations and formatting
    output.seek(0)
    return output.read()