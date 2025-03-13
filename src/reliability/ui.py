"""
Module: ui
Description: Provides a Streamlit-based user interface for uploading a BOM Excel file,
             processing MIL‑STD‑217 data, and generating an Excel report.
"""

import streamlit as st
import pandas as pd
from bom_processor import process_bom
from agent import get_milstd217_info_for_parts
from excel_output import create_output_excel

def main():
    st.title("Reliability Prediction Tool")
    st.write("Upload your Bill of Materials (Excel format) to begin processing.")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "xlsm"])
    if uploaded_file is not None:
        try:
            bom_df = process_bom(uploaded_file)
            st.write("BOM Loaded Successfully:")
            st.dataframe(bom_df)

            # Ensure required columns exist for further processing.
            if "FN" not in bom_df.columns or "Quantity" not in bom_df.columns:
                st.error("BOM must include 'FN' (find number) and 'Quantity' columns.")
                return

            # Get the list of part numbers (using the 'FN' column)
            part_numbers = bom_df["FN"].tolist()
            st.write("Searching for MIL‑STD‑217 data for the provided parts...")
            
            milstd_data = get_milstd217_info_for_parts(part_numbers)
            # Merge the BOM with the MIL‑STD‑217 data on the find number
            output_df = pd.merge(bom_df, milstd_data, left_on="FN", right_on="PartNumber", how="left")
            st.write("Processed Data:")
            st.dataframe(output_df)
            
            output_file = create_output_excel(output_df)
            st.success("Output Excel file generated successfully!")
            st.download_button(
                label="Download Output Excel",
                data=output_file,
                file_name="milstd217_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Error processing file: {e}")

if __name__ == "__main__":
    main()
