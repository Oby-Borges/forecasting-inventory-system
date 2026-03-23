"""Forecast-based inventory calculations for Version 3 of the project.

This module keeps the inventory logic beginner-friendly and readable.
Instead of using the historical average demand as the expected demand,
Version 3 uses the forecast from the best-performing model.

The best model is selected from the model comparison table by choosing
the method with the lowest MAPE value.
"""

from math import sqrt

import pandas as pd

# Version 3 assumptions for reorder point calculations.
LEAD_TIME_PERIODS = 2
SERVICE_LEVEL = 0.95
Z_SCORE = 1.65

# Version 3 assumptions for EOQ calculations.
PERIODS_PER_YEAR = 12
ORDERING_COST_PER_ORDER = 50
HOLDING_COST_PER_UNIT_PER_YEAR = 8



def select_best_model(metrics: pd.DataFrame) -> str:
    """Return the forecast method with the lowest MAPE.

    Args:
        metrics: Model comparison table that must contain Method and MAPE columns.

    Returns:
        The name of the best-performing forecast method.
    """
    if metrics.empty:
        raise ValueError("Model comparison results are empty.")

    best_model_row = metrics.sort_values(by="MAPE").iloc[0]
    return str(best_model_row["Method"])



def get_expected_demand_per_period(forecast_data: pd.DataFrame, best_model: str) -> float:
    """Return the most recent available forecast from the best model.

    Args:
        forecast_data: Forecast results table containing forecast columns.
        best_model: Column name of the best forecast model.

    Returns:
        The latest non-missing forecast value from the best model.
    """
    if best_model not in forecast_data.columns:
        raise ValueError(f"Best model column '{best_model}' was not found in forecast data.")

    available_forecasts = forecast_data[best_model].dropna()

    if available_forecasts.empty:
        raise ValueError(f"No forecast values are available for '{best_model}'.")

    return float(available_forecasts.iloc[-1])



def calculate_demand_standard_deviation(demand: pd.Series) -> float:
    """Return the sample standard deviation of the historical demand values."""
    return float(demand.std())



def calculate_lead_time_demand(
    expected_demand_per_period: float,
    lead_time: int = LEAD_TIME_PERIODS,
) -> float:
    """Return expected demand during the lead time."""
    return expected_demand_per_period * lead_time



def calculate_safety_stock(
    demand_standard_deviation: float,
    z_score: float = Z_SCORE,
    lead_time: int = LEAD_TIME_PERIODS,
) -> float:
    """Return the safety stock using the Version 3 formula."""
    return z_score * demand_standard_deviation * sqrt(lead_time)



def calculate_reorder_point(lead_time_demand: float, safety_stock: float) -> float:
    """Return the reorder point."""
    return lead_time_demand + safety_stock



def calculate_annual_demand(
    expected_demand_per_period: float,
    periods_per_year: int = PERIODS_PER_YEAR,
) -> float:
    """Convert expected demand per period into annual demand."""
    return expected_demand_per_period * periods_per_year



def calculate_eoq(
    annual_demand: float,
    ordering_cost: float = ORDERING_COST_PER_ORDER,
    holding_cost: float = HOLDING_COST_PER_UNIT_PER_YEAR,
) -> float:
    """Return the economic order quantity (EOQ)."""
    return sqrt((2 * annual_demand * ordering_cost) / holding_cost)



def calculate_inventory_summary(
    demand_data: pd.DataFrame,
    forecast_data: pd.DataFrame,
    best_model: str,
) -> pd.DataFrame:
    """Build a one-row inventory summary using the best forecast model.

    Args:
        demand_data: Input data containing the historical Demand column.
        forecast_data: Forecast table containing all forecast method columns.
        best_model: Name of the forecast column selected in main.py.

    Returns:
        A one-row pandas DataFrame that can be printed or saved as CSV.
    """
    expected_demand_per_period = get_expected_demand_per_period(forecast_data, best_model)
    demand_standard_deviation = calculate_demand_standard_deviation(demand_data["Demand"])
    lead_time_demand = calculate_lead_time_demand(expected_demand_per_period)
    safety_stock = calculate_safety_stock(demand_standard_deviation)
    reorder_point = calculate_reorder_point(lead_time_demand, safety_stock)
    annual_demand = calculate_annual_demand(expected_demand_per_period)
    eoq = calculate_eoq(annual_demand)

    summary = pd.DataFrame(
        [
            {
                "Best Model": best_model,
                "Expected Demand per Period": expected_demand_per_period,
                "Demand Standard Deviation": demand_standard_deviation,
                "Lead Time": LEAD_TIME_PERIODS,
                "Service Level": SERVICE_LEVEL,
                "Z-Score": Z_SCORE,
                "Lead Time Demand": lead_time_demand,
                "Safety Stock": safety_stock,
                "Reorder Point": reorder_point,
                "Periods per Year": PERIODS_PER_YEAR,
                "Annual Demand": annual_demand,
                "Ordering Cost per Order": ORDERING_COST_PER_ORDER,
                "Holding Cost per Unit per Year": HOLDING_COST_PER_UNIT_PER_YEAR,
                "EOQ": eoq,
            }
        ]
    )

    return summary



def format_inventory_summary(inventory_summary: pd.DataFrame) -> str:
    """Return a clean string version of the inventory summary table."""
    display_summary = inventory_summary.copy()

    for column in display_summary.columns:
        if column == "Best Model":
            continue
        if column in ["Lead Time", "Periods per Year"]:
            display_summary[column] = display_summary[column].map(lambda value: f"{int(value)}")
        else:
            display_summary[column] = display_summary[column].map(lambda value: f"{value:.2f}")

    return display_summary.to_string(index=False)
