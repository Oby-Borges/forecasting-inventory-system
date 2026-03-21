"""Simple inventory calculations for Version 2 of the project.

This module keeps the inventory logic small and beginner-friendly.
It uses the historical Demand column to calculate average demand,
variability, safety stock, and the reorder point.
"""

from math import sqrt

import pandas as pd

# Version 2 assumptions.
LEAD_TIME_PERIODS = 2
SERVICE_LEVEL = 0.95
Z_SCORE = 1.65



def calculate_average_demand(demand: pd.Series) -> float:
    """Return the mean of the demand values."""
    return float(demand.mean())



def calculate_demand_standard_deviation(demand: pd.Series) -> float:
    """Return the sample standard deviation of the demand values."""
    return float(demand.std())



def calculate_lead_time_demand(average_demand: float, lead_time: int = LEAD_TIME_PERIODS) -> float:
    """Return expected demand during lead time."""
    return average_demand * lead_time



def calculate_safety_stock(
    demand_standard_deviation: float,
    z_score: float = Z_SCORE,
    lead_time: int = LEAD_TIME_PERIODS,
) -> float:
    """Return the safety stock using the Version 2 formula."""
    return z_score * demand_standard_deviation * sqrt(lead_time)



def calculate_reorder_point(lead_time_demand: float, safety_stock: float) -> float:
    """Return the reorder point."""
    return lead_time_demand + safety_stock



def calculate_inventory_summary(demand_data: pd.DataFrame) -> pd.DataFrame:
    """Build a one-row summary table with the main inventory values.

    Args:
        demand_data: Input data that must contain a numeric Demand column.

    Returns:
        A one-row pandas DataFrame that can be printed or saved as CSV.
    """
    average_demand = calculate_average_demand(demand_data["Demand"])
    demand_standard_deviation = calculate_demand_standard_deviation(demand_data["Demand"])
    lead_time_demand = calculate_lead_time_demand(average_demand)
    safety_stock = calculate_safety_stock(demand_standard_deviation)
    reorder_point = calculate_reorder_point(lead_time_demand, safety_stock)

    summary = pd.DataFrame(
        [
            {
                "Average Demand": average_demand,
                "Demand Standard Deviation": demand_standard_deviation,
                "Lead Time": LEAD_TIME_PERIODS,
                "Service Level": SERVICE_LEVEL,
                "Z-Score": Z_SCORE,
                "Lead Time Demand": lead_time_demand,
                "Safety Stock": safety_stock,
                "Reorder Point": reorder_point,
            }
        ]
    )

    return summary



def format_inventory_summary(inventory_summary: pd.DataFrame) -> str:
    """Return a clean string version of the inventory summary table."""
    display_summary = inventory_summary.copy()

    # Keep lead time as a whole number and show other values with two decimals.
    for column in display_summary.columns:
        if column == "Lead Time":
            display_summary[column] = display_summary[column].map(lambda value: f"{int(value)}")
        else:
            display_summary[column] = display_summary[column].map(lambda value: f"{value:.2f}")

    return display_summary.to_string(index=False)
