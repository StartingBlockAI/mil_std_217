"""
Module: excel_output
Description: Provides functions to generate an Excel output file that includes
             all MIL‑STD‑217 calculation inputs and summary totals.
"""

import io
import pandas as pd

def create_output_excel(df):
    """
    Creates an Excel file from the given DataFrame, with a detailed sheet and a summary sheet.
    
    Args:
        df (pandas.DataFrame): Data containing BOM and MIL‑STD‑217 information.
    
    Returns:
        bytes: A binary stream of the Excel file content.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="MIL-STD-217 Data", index=False)
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Summary")
        writer.sheets["Summary"] = worksheet

        worksheet.write("A1", "Total Base Failure Rate")
        total_bfr = df["BaseFailureRate"].sum() if "BaseFailureRate" in df.columns else 0
        worksheet.write("B1", total_bfr)
    output.seek(0)
    return output.read()
