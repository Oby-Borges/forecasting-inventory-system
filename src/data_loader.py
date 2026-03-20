"""Utilities for loading and validating demand data."""

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = ["Period", "Demand"]


def load_demand_data(file_path: Path) -> pd.DataFrame:
    """Load demand data from a CSV file and validate its structure.

    Args:
        file_path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the demand data.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        ValueError: If required columns are missing, the file is empty,
            or demand values cannot be converted to numbers.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    try:
        data = pd.read_csv(file_path)
    except pd.errors.EmptyDataError as error:
        raise ValueError("The input CSV file is empty.") from error
    except Exception as error:
        raise ValueError(f"Unable to read the CSV file: {error}") from error

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing_columns)
        )

    data = data.copy()

    try:
        data["Demand"] = pd.to_numeric(data["Demand"])
    except Exception as error:
        raise ValueError("All Demand values must be numeric.") from error

    if data["Demand"].isna().any():
        raise ValueError("Demand column contains missing values.")

    return data
