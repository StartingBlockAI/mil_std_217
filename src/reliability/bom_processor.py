"""
Module: bom_processor
Description: Reads and processes a Bill of Materials (BOM) Excel file.
             The BOM template is expected to have an indicator row as the first row and
             the actual column names on the second row. This module cleans and normalizes
             column names, reads only the essential input columns, and computes additional
             columns (such as PartType, Value, Voltage, etc.) for further reliability analysis.
"""

import re
import math
import pandas as pd
import logging

# Set up logging for debugging.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Expected column mapping: each expected key is associated with a list of possible variants.
EXPECTED_COLUMNS = {
    "FN": ["fn", "find number", "find_number", "find no", "find no.", "find#"],
    "ManufacturerPartNumber": [
        "manufacturer part number",
        "mfg part number",
        "part number",
        "pn",
        "mfr part",
        "manufacturer"
    ],
    "Quantity": ["quantity", "qty", "qnty"],
    "Description": ["description", "desc", "part description", "partdescription"],
    "DrawingRef": ["drawingref", "drawing reference", "drawing_ref", "dr", "drawing", "draw ref", "reference designators"]
}

def clean_string(s):
    """
    Normalizes a string by lowercasing and removing whitespace and punctuation.
    
    Args:
        s (str): The string to clean.
        
    Returns:
        str: The cleaned string.
    """
    return re.sub(r'[\W_]+', '', s.lower().strip())

def standardize_columns(columns):
    """
    Builds a mapping from the original column names to standardized expected names.
    
    For each column in the input, this function compares the cleaned version of the name
    against the expected variants. If a match is found, it maps the original name to the
    standardized expected key.
    
    Args:
        columns (iterable): List or iterable of column names from the BOM file.
        
    Returns:
        dict: Mapping from the original column name to the standardized expected name.
    """
    mapping = {}
    for col in columns:
        cleaned = clean_string(col)
        found = False
        for expected, variants in EXPECTED_COLUMNS.items():
            for variant in variants:
                if cleaned == clean_string(variant):
                    mapping[col] = expected  # Replace original with standardized name.
                    found = True
                    break
            if found:
                break
    logger.info(f"Column mapping: {mapping}")
    return mapping

def round_sig(x, sig=4):
    """
    Rounds a number to the specified number of significant digits.
    
    Args:
        x (float): The number to round.
        sig (int): The number of significant digits.
        
    Returns:
        float: The rounded number.
    """
    if x == 0:
        return 0.0
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

def convert_value(value_str):
    """
    Converts a value string (e.g., "1k", "10uF", "100pF", "47") to a numeric value
    using appropriate multipliers, then rounds it to 4 significant digits.
    
    Args:
        value_str (str): The value string extracted from the description.
        
    Returns:
        float or None: The numeric value converted to base units and rounded, or None if conversion fails.
    """
    pattern = re.compile(r"(\d+\.?\d*)\s*([A-Za-zµ]*)")
    match = pattern.fullmatch(value_str.strip())
    if not match:
        return None
    number = float(match.group(1))
    unit = match.group(2)
    
    # Define multipliers.
    if unit == "":
        multiplier = 1
    elif unit in ['k', 'K']:
        multiplier = 1e3
    elif unit == 'M':  # Mega (resistors, etc.)
        multiplier = 1e6
    elif unit == 'm':  # milli
        multiplier = 1e-3
    elif unit in ['uF', 'UF', 'µF']:
        multiplier = 1e-6
    elif unit.lower() == 'pf':
        multiplier = 1e-12
    else:
        multiplier = 1  # fallback
    value = number * multiplier
    return round_sig(value, 4)

def parse_description(desc):
    """
    Parses the description string to extract part details and converts the value and voltage to numbers.
    
    This parser looks for key patterns:
      - Part type: Determines if the part is a resistor, capacitor, IC, inductor, connector, or Other.
      - Value: Extracts the first numeric value with an optional unit (e.g., "1k", "10uF", "100pF")
               and converts it to a number rounded to 4 significant digits.
      - Voltage: Extracts a voltage value (e.g., "5V") and converts it to a number, rounded to 4 significant digits.
    
    Args:
        desc (str): The part description from the BOM.
    
    Returns:
        dict: A dictionary with keys 'PartType', 'Value', and 'Voltage'.
    """
    if not isinstance(desc, str):
        return {"PartType": None, "Value": None, "Voltage": None}
    
    desc_lower = desc.lower()
    if "resistor" in desc_lower:
        part_type = "Resistor"
    elif "capacitor" in desc_lower:
        part_type = "Capacitor"
    elif "integrated circuit" in desc_lower or re.search(r'\bic\b', desc_lower):
        part_type = "IC"
    elif "inductor" in desc_lower or "coil" in desc_lower:
        part_type = "Inductor"
    elif "connector" in desc_lower:
        part_type = "Connector"
    else:
        part_type = "Other"
    
    # Extract value string and convert it.
    value_match = re.search(r"(\d+\.?\d*\s*(?:[kK]|[M]|[m]|(?:[uU]F)|(?:[pP]F))?)", desc)
    if value_match:
        value_str = value_match.group(0).strip()
        numeric_value = convert_value(value_str)
    else:
        numeric_value = None
    
    # Extract voltage.
    voltage_match = re.search(r"(\d+\.?\d*\s*(?:V|volts))", desc, re.IGNORECASE)
    if voltage_match:
        voltage_str = voltage_match.group(0).strip()
        try:
            voltage_numeric = float(re.sub(r'[^\d\.]', '', voltage_str))
            voltage_numeric = round_sig(voltage_numeric, 4)
        except Exception:
            voltage_numeric = None
    else:
        voltage_numeric = None
    
    return {"PartType": part_type, "Value": numeric_value, "Voltage": voltage_numeric}

def process_bom(file, sheet_name=0):
    """
    Reads and processes a BOM Excel file.
    
    Expected:
      - The first row is an indicator row.
      - The actual column names are in row 2.
      - Essential input columns: "FN", "ManufacturerPartNumber", "Quantity", "Description", "DrawingRef".
    
    This function:
      1. Reads only the essential input columns.
      2. Renames them to standardized names.
      3. Computes additional columns:
         - "PartType": Derived from Description.
         - "Value": Numeric value extracted from Description.
         - "Voltage": Numeric voltage extracted from Description.
         - "Tolerance": Placeholder (None).
         - "AdditionalInfo": Placeholder (empty string).
         - "CalculatedQuantity": Copies the original Quantity.
    
    Args:
        file: The file-like object or file path for the BOM Excel file.
        sheet_name: The sheet to read from (default is the first sheet).
    
    Returns:
        pandas.DataFrame: A DataFrame with the essential input columns and the computed columns.
    """
    # Read Excel file, skipping the first row.
    df = pd.read_excel(file, sheet_name=sheet_name, skiprows=1, header=0)
    logger.info(f"Original columns: {df.columns.tolist()}")
    
    # Build mapping and rename columns.
    col_mapping = standardize_columns(df.columns)
    for required in EXPECTED_COLUMNS:
        if required not in col_mapping.values():
            available = df.columns.tolist()
            raise ValueError(f"Missing required column for '{required}'. Expected variants: {EXPECTED_COLUMNS[required]}. Available columns: {available}")
    df = df.rename(columns=col_mapping)
    logger.info(f"Columns after renaming: {df.columns.tolist()}")
    
    # Subset DataFrame to essential input columns.
    required_input_columns = ["FN", "ManufacturerPartNumber", "Quantity", "Description", "DrawingRef"]
    df = df[required_input_columns]
    
    # Process Description column to compute additional values.
    try:
        parsed_info = df["Description"].apply(parse_description)
    except KeyError as e:
        raise KeyError(f"Error accessing 'Description' column. Available columns: {df.columns.tolist()}") from e
    parsed_df = pd.DataFrame(parsed_info.tolist())
    
    # Append computed columns.
    df["PartType"] = parsed_df["PartType"]
    df["Value"] = parsed_df["Value"]
    df["Voltage"] = parsed_df["Voltage"]
    df["Tolerance"] = None
    df["AdditionalInfo"] = ""
    df["CalculatedQuantity"] = df["Quantity"]
    
    # Drop rows missing critical input data.
    df = df.dropna(subset=["FN", "ManufacturerPartNumber", "Quantity", "Description"])
    
    # Log rows with potential parsing issues.
    for idx, row in parsed_df.iterrows():
        if row["PartType"] is None or row["Value"] is None:
            logger.info(f"Row {idx} might have an unrecognized description: {df.loc[idx, 'Description']}")
    
    return df

if __name__ == "__main__":
    # For testing, replace 'BOM Only.xlsx' with the actual BOM file path.
    bom_file_path = "BOM Only.xlsx"
    try:
        processed_bom = process_bom(bom_file_path)
        print(processed_bom.head())
    except Exception as e:
        print(f"Error processing BOM: {e}")
