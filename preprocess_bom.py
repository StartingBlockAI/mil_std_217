import pandas as pd
from mil_hdbk_217_sections import mil_hdbk_217_dict

def preprocess_bom(file_path):
    """Loads and preprocesses the BOM file for MIL-HDBK-217 analysis."""
    try:
        # Load the BOM, skipping the first row
        df = pd.read_excel(file_path, skiprows=1)
        
        # Extract necessary columns
        bom_data = df.iloc[:, :6]  # Columns A-F
        analysis_columns = df.iloc[:, 6:12]  # Columns G-L
        
        # Clean column names
        bom_data.columns = ["Next Higher Assembly", "FN", "QTY", "Part Number", "Description", "Reference Designators"]
        analysis_columns.columns = ["MFG", "Part Type", "Subtype", "LM PiQ", "Value (cap/power)", "Notes"]
        
        # Extract Part Type as text before the first comma in the Description column
        analysis_columns["Part Type"] = bom_data["Description"].apply(lambda x: str(x).split(',')[0] if isinstance(x, str) else "")
        analysis_columns["Subtype"] = bom_data["Description"].apply(lambda x: str(x).split(',')[1] if isinstance(x, str) else "")
        
        # Process specific components like capacitors
        def extract_capacitor_info(description):
            parts = str(description).split(', ')
            subtype = parts[1] if len(parts) > 1 else ""
            value = next((p for p in parts if 'uF' in p), "")
            remaining_info = ', '.join([p for p in parts if p not in [subtype, value]]) if len(parts) > 2 else ""
            return subtype, value, remaining_info
        
        # Map components to MIL-HDBK-217 sections
        def map_to_mil_hdbk_section(part_type):
            for section, data in mil_hdbk_217_dict.items():
                if isinstance(data, dict) and part_type in data.values():
                    return section
            return "Unknown"
        
        analysis_columns["MIL-HDBK-217 Section"] = analysis_columns["Part Type"].apply(map_to_mil_hdbk_section)
        
        # Fill missing values with blank instead of placeholders
        analysis_columns.fillna("", inplace=True)
        
        # Merge back for a complete dataset
        processed_bom = pd.concat([bom_data, analysis_columns], axis=1)
        
        return processed_bom
    
    except Exception as e:
        print(f"Error processing BOM: {e}")
        return None