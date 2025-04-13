import streamlit as st
import pandas as pd
from preprocess_bom import preprocess_bom

# Title of the application
st.title("MIL-HDBK-217 Reliability Analysis Tool")

# User input for Baseplate Temperature
baseplate_temp = st.number_input("Enter Baseplate Temperature (°C)", min_value=-50.0, max_value=200.0, value=25.0, step=0.1)

# File uploader
uploaded_file = st.file_uploader("Upload Bill of Materials (Excel file)", type=["xls", "xlsx"])

if uploaded_file is not None:
    try:
        # Save uploaded file temporarily
        file_path = "temp_bom.xlsx"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Preprocess BOM file
        processed_bom = preprocess_bom(file_path)
        
        # Display the processed BOM data
        st.write("### Processed BOM Data:")
        st.dataframe(processed_bom)
        
        # Provide download option
        processed_bom.to_excel("processed_bom.xlsx", index=False)
        with open("processed_bom.xlsx", "rb") as file:
            st.download_button(label="Download Processed BOM", data=file, file_name="processed_bom.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        
    except Exception as e:
        st.error(f"Error processing BOM: {e}")

# Footer
st.write("Developed for MIL-HDBK-217 reliability analysis.")
