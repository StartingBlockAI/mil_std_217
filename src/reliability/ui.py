import streamlit as st
import pandas as pd
from bom_processor import process_bom
from data_completeness import identify_missing_info
from excel_output import create_output_excel

def main():
    st.title("Reliability Prediction Tool")
    st.write("Upload your BOM Excel file to begin processing.")

    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "xlsm"])
    if uploaded_file is not None:
        try:
            bom_df = process_bom(uploaded_file)
            st.write("Processed BOM:")
            st.dataframe(bom_df)
            
            # Check for missing required fields.
            completeness_report = identify_missing_info(bom_df)
            st.write("Data Completeness Report:")
            st.dataframe(completeness_report[["FN", "ManufacturerPartNumber", "PartType", "Value", "Tolerance", "Voltage", "MissingFields"]])
            
            # Generate output Excel file.
            output_file = create_output_excel(bom_df)
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
