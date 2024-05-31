from typing import List
import pandas as pd
from utils import log_debug

class DataValidator:
    def validate_columns(self, data: pd.DataFrame, required_columns: List[str]) -> bool:
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            log_debug(f"Missing required columns: {', '.join(missing_columns)}")
            return False
        return True

    def validate_data_types(self, data: pd.DataFrame) -> bool:
        for column in ['Price', 'Inventory Count']:
            if column in data.columns:
                try:
                    data[column] = pd.to_numeric(data[column], errors='raise')
                except ValueError as e:
                    log_debug(f"Data type error in column '{column}': {e}")
                    return False
        return True