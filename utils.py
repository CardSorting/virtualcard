import pandas as pd
from typing import Union, List

DEBUG = True  # Debug flag to control logging

def log_debug(message: Union[str, pd.DataFrame, pd.Series]):
    if DEBUG:
        print(message)  # Use print for debugging in utility functions

def prepare_data(data: pd.DataFrame) -> pd.DataFrame:
    # Ensure columns are of string type for filtering
    for col in ['Card Name', 'Set']:
        if col in data.columns:
            data[col] = data[col].astype(str)

    # Drop rows with missing 'Card Name'
    data = data.dropna(subset=['Card Name'])

    # Handle Spells and Traps to not require archetype, level, or attribute
    data.loc[data['Type'].isin(['Spells', 'Traps']), ['Archetype', 'Level', 'Attribute']] = 'Not specified'

    return data

def validate_columns(data: pd.DataFrame, required_columns: List[str]) -> bool:
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        log_debug(f"Missing required columns: {', '.join(missing_columns)}")
        return False
    return True

def validate_data_types(data: pd.DataFrame) -> bool:
    for column in ['Price', 'Inventory Count']:
        if column in data.columns:
            try:
                data[column] = pd.to_numeric(data[column], errors='raise')
            except ValueError as e:
                log_debug(f"Data type error in column '{column}': {e}")
                return False
    return True