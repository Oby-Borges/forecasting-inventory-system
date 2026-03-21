"""Main program for the Forecasting and Inventory Decision Support System."""

from pathlib import Path

import pandas as pd

from data_loader import load_demand_data
from evaluation import calculate_all_metrics
from forecasting import add_forecasts
from inventory import calculate_inventory_summary, format_inventory_summary
from visualization import create_forecast_plot


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "demand_data.csv"
OUTPUTS_DIR = BASE_DIR / "outputs"
FORECAST_RESULTS_FILE = OUTPUTS_DIR / "forecast_results.csv"
MODEL_COMPARISON_FILE = OUTPUTS_DIR / "model_comparison.csv"
INVENTORY_SUMMARY_FILE = OUTPUTS_DIR / "inventory_summary.csv"
PLOT_FILE = OUTPUTS_DIR / "forecast_plot.png"



def ensure_output_folder_exists() -> None:
    """Create the outputs folder if it does not already exist."""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)



def format_summary_table(metrics: pd.DataFrame) -> str:
    """Return a clean string version of the model comparison table."""
    display_table = metrics.copy()

    for column in ["MAD", "MSE", "RMSE", "MAPE"]:
        display_table[column] = display_table[column].map(lambda value: f"{value:.2f}")

    return display_table.to_string(index=False)



def save_results(
    forecast_data: pd.DataFrame,
    metrics: pd.DataFrame,
    inventory_summary: pd.DataFrame,
) -> None:
    """Save forecast details, model comparison, and inventory summary files."""
    forecast_data.to_csv(FORECAST_RESULTS_FILE, index=False, float_format="%.4f")
    metrics.to_csv(MODEL_COMPARISON_FILE, index=False, float_format="%.6f")
    inventory_summary.to_csv(INVENTORY_SUMMARY_FILE, index=False, float_format="%.4f")



def main() -> None:
    """Run the Version 2 forecasting and inventory workflow."""
    try:
        ensure_output_folder_exists()
        demand_data = load_demand_data(DATA_FILE)
        forecast_data = add_forecasts(demand_data)
        metrics = calculate_all_metrics(forecast_data)
        inventory_summary = calculate_inventory_summary(demand_data)
        save_results(forecast_data, metrics, inventory_summary)
        create_forecast_plot(forecast_data, PLOT_FILE)

        print("\nForecasting and Inventory Decision Support System - Version 2")
        print("=" * 63)
        print(f"Loaded data from: {DATA_FILE}")
        print(f"Number of periods: {len(demand_data)}")
        print("\nModel Comparison Summary")
        print("-" * 63)
        print(format_summary_table(metrics))
        print("\nInventory Summary")
        print("-" * 63)
        print(format_inventory_summary(inventory_summary))
        print("\nFiles saved successfully:")
        print(f"- {FORECAST_RESULTS_FILE}")
        print(f"- {MODEL_COMPARISON_FILE}")
        print(f"- {INVENTORY_SUMMARY_FILE}")
        print(f"- {PLOT_FILE}")
    except FileNotFoundError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Data validation error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
