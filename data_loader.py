import pandas as pd
import streamlit as st
from typing import List
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils import log_debug, prepare_data, validate_columns, validate_data_types

class DataLoader:
    def load_and_validate_data(self, files: List[UploadedFile], required_columns: List[str]) -> pd.DataFrame:
        all_data_list = []
        log_debug("Loading and validating data...")

        # Sheets to skip (add more sheet names as needed)
        sheets_to_skip = ['Summary']

        for file in files:
            try:
                # Read the file content as a DataFrame
                excel_data = pd.ExcelFile(file)
                for sheet_name in excel_data.sheet_names:
                    if sheet_name in sheets_to_skip:
                        log_debug(f"Skipping sheet: {sheet_name}")
                        continue
                    df = pd.read_excel(file, sheet_name=sheet_name)
                    df['Type'] = sheet_name
                    log_debug(f"Loaded {sheet_name} sheet with {df.shape[0]} rows.")
                    all_data_list.append(df)
            except ValueError as e:
                log_debug(f"Error loading file {file.name}: {e}")

        if not all_data_list:
            log_debug("No data loaded.")
            return pd.DataFrame()

        all_data = pd.concat(all_data_list, ignore_index=True)

        log_debug(f"Total rows before validation: {all_data.shape[0]}")
        log_debug(all_data.head())

        all_data = prepare_data(all_data)

        log_debug(f"Total rows after preparing data: {all_data.shape[0]}")
        log_debug(all_data.head())

        if not validate_columns(all_data, required_columns):
            log_debug("Column validation failed.")
            log_debug(f"Columns found: {', '.join(all_data.columns)}")
            return pd.DataFrame()

        log_debug(f"Total rows after column validation: {all_data.shape[0]}")
        log_debug(all_data.head())

        if not validate_data_types(all_data):
            log_debug("Data type validation failed.")
            return pd.DataFrame()

        log_debug(f"Total rows after data type validation: {all_data.shape[0]}")
        log_debug(all_data.head())

        # Check for rows with missing required columns
        missing_required = all_data[all_data[required_columns].isnull().any(axis=1)]
        if not missing_required.empty:
            log_debug("Rows with missing required columns:")
            log_debug(missing_required)
            # Fill missing required columns with placeholders to avoid dropping all rows
            for col in required_columns:
                if col in all_data.columns:
                    all_data[col].fillna('Not specified', inplace=True)

        # Re-check if the required columns exist, then fill NA for them
        for col in required_columns:
            if col not in all_data.columns:
                all_data[col] = 'Not specified'
            all_data[col].fillna('Not specified', inplace=True)

        log_debug(f"Total rows after handling missing values in required columns: {all_data.shape[0]}")
        log_debug(all_data.head())

        return all_data