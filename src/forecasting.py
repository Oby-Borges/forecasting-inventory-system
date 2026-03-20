"""Forecasting methods used in Version 1 of the project."""

import pandas as pd


WEIGHTED_AVERAGE_WEIGHTS = [0.5, 0.3, 0.2]
SES_ALPHA = 0.3


def add_forecasts(data: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the data with forecast columns added."""
    forecast_data = data.copy()
    forecast_data["Naive Forecast"] = naive_forecast(forecast_data["Demand"])
    forecast_data["3-Period Moving Average"] = moving_average_forecast(
        forecast_data["Demand"], window=3
    )
    forecast_data["Weighted Moving Average"] = weighted_moving_average_forecast(
        forecast_data["Demand"], WEIGHTED_AVERAGE_WEIGHTS
    )
    forecast_data["Simple Exponential Smoothing"] = simple_exponential_smoothing(
        forecast_data["Demand"], alpha=SES_ALPHA
    )
    return forecast_data



def naive_forecast(demand: pd.Series) -> pd.Series:
    """Forecast each period using the previous period's demand."""
    return demand.shift(1)



def moving_average_forecast(demand: pd.Series, window: int) -> pd.Series:
    """Forecast using a simple moving average of previous periods."""
    return demand.shift(1).rolling(window=window).mean()



def weighted_moving_average_forecast(
    demand: pd.Series, weights: list[float]
) -> pd.Series:
    """Forecast using weighted averages of the most recent periods.

    The first weight is applied to the most recent previous period.
    """
    forecast = pd.Series(index=demand.index, dtype=float)
    periods_needed = len(weights)

    for index in range(periods_needed, len(demand)):
        recent_values = demand.iloc[index - periods_needed:index].tolist()
        recent_values.reverse()
        weighted_total = sum(value * weight for value, weight in zip(recent_values, weights))
        forecast.iloc[index] = weighted_total

    return forecast



def simple_exponential_smoothing(demand: pd.Series, alpha: float) -> pd.Series:
    """Forecast using simple exponential smoothing.

    The first forecast is not available because there is no previous demand.
    For the second period, the forecast starts with the first actual demand value.
    """
    forecast = pd.Series(index=demand.index, dtype=float)

    if demand.empty:
        return forecast

    for index in range(1, len(demand)):
        if index == 1:
            forecast.iloc[index] = demand.iloc[index - 1]
        else:
            forecast.iloc[index] = (
                alpha * demand.iloc[index - 1]
                + (1 - alpha) * forecast.iloc[index - 1]
            )

    return forecast
