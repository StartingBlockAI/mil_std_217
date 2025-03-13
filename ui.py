"""
Module: ui
Description: Provides a Streamlit-based user interface to load a BOM Excel file,
             process MIL‑STD‑217 data, and output an Excel report.
"""

import streamlit as st
import pandas as pd
from agent import get_milstd217_info_for_parts
from excel_output import create_output_excel

def main():
    st.title("Reliability Prediction Tool")
    st.write("Upload your Bill of Materials (Excel format) to begin.")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "xlsm"])
    if uploaded_file is not None:
        try:
            # Read the BOM into a DataFrame
            bom_df = pd.read_excel(uploaded_file)
            st.write("BOM Loaded Successfully:")
            st.dataframe(bom_df)

            # Process the BOM to extract part numbers and other details.
            # Assume your BOM has a column called "PartNumber"
            if "PartNumber" not in bom_df.columns:
                st.error("BOM must include a 'PartNumber' column.")
                return

            part_numbers = bom_df["PartNumber"].tolist()
            st.write("Searching for MIL‑STD‑217 data for the provided parts...")
            
            # Get MIL‑STD‑217 relevant info for each part
            milstd_data = get_milstd217_info_for_parts(part_numbers)
            
            # Merge MIL‑STD‑217 data with BOM (this example assumes both are DataFrames)
            # In practice, you may need to adjust merging based on your data schema.
            output_df = pd.merge(bom_df, milstd_data, on="PartNumber", how="left")
            st.write("Processed Data:")
            st.dataframe(output_df)
            
            # Generate output Excel file
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
