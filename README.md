# MIL-HDBK-217 Reliability Analysis Tool

## Project Overview
This project provides a **Streamlit-based GUI tool** for **MIL-HDBK-217 reliability analysis**. Users can upload a **Bill of Materials (BOM) Excel file**, which is then processed to extract relevant information, map components to their respective **MIL-HDBK-217 sections**, and generate a reliability analysis report.

## Project Structure
```
MIL-HDBK-217-Tool/
│── preprocess_bom.py         # Processes the BOM and maps components to MIL-HDBK-217 sections
│── mil_hdbk_217_sections.py  # Dictionary mapping MIL-HDBK-217 sections and subsections
│── streamlit_app.py          # Streamlit web app for file upload and processing
│── README.md                 # Project documentation
```

## Installation
To run this project, install the necessary dependencies:
```bash
pip install streamlit pandas openpyxl
```

## Usage
### Running the Streamlit Application
```bash
streamlit run streamlit_app.py
```

### Features
- **File Upload:** Users can upload a BOM Excel file.
- **Automatic Processing:** Extracts **Part Type, Subtype, and Capacitance**.
- **MIL-HDBK-217 Mapping:** Identifies the correct **MIL-HDBK-217 section** for each component.
- **Download Processed Data:** Users can download the updated BOM file.

## Example BOM Processing Workflow
1. **Upload BOM file** in `.xls` or `.xlsx` format.
2. **Processing occurs automatically**, extracting capacitor subtypes, values, and mapping to MIL-HDBK-217.
3. **Processed BOM is displayed and available for download.**

## Future Enhancements
- **Automated reliability calculations** based on MIL-HDBK-217 formulas.
- **Expanded part type classification** beyond capacitors.
- **Database integration** for storing processed data.

## License
MIT License

