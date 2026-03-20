"""Evaluation metrics for comparing forecasting methods."""

import numpy as np
import pandas as pd


FORECAST_COLUMNS = [
    "Naive Forecast",
    "3-Period Moving Average",
    "Weighted Moving Average",
    "Simple Exponential Smoothing",
]



def calculate_all_metrics(forecast_data: pd.DataFrame) -> pd.DataFrame:
    """Calculate error metrics for each forecasting method."""
    metrics_rows = []

    for column in FORECAST_COLUMNS:
        valid_rows = forecast_data[["Demand", column]].dropna()
        actual = valid_rows["Demand"]
        forecast = valid_rows[column]

        metrics_rows.append(
            {
                "Method": column,
                "MAD": mean_absolute_deviation(actual, forecast),
                "MSE": mean_squared_error(actual, forecast),
                "RMSE": root_mean_squared_error(actual, forecast),
                "MAPE": mean_absolute_percentage_error(actual, forecast),
            }
        )

    metrics = pd.DataFrame(metrics_rows)
    return metrics.sort_values(by="RMSE").reset_index(drop=True)



def mean_absolute_deviation(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate mean absolute deviation (MAD)."""
    return (actual - forecast).abs().mean()



def mean_squared_error(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate mean squared error (MSE)."""
    return ((actual - forecast) ** 2).mean()



def root_mean_squared_error(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate root mean squared error (RMSE)."""
    mse = mean_squared_error(actual, forecast)
    return float(np.sqrt(mse))



def mean_absolute_percentage_error(actual: pd.Series, forecast: pd.Series) -> float:
    """Calculate mean absolute percentage error (MAPE)."""
    percentage_errors = ((actual - forecast).abs() / actual) * 100
    return percentage_errors.mean()
