# Forecasting and Inventory Decision Support System

## Project Overview
This beginner-friendly Python project demonstrates a simple demand forecasting workflow for an inventory decision support system. It reads historical demand from a CSV file, applies several forecasting methods, evaluates their accuracy, prints a comparison table in the terminal, calculates basic inventory planning values, and saves detailed results for later review.

Version 2 still focuses on clarity and ease of understanding. The project is designed to be small, readable, well-commented, and easy to extend.

## Folder Structure
```text
forecasting-inventory-system/
├── data/
│   └── demand_data.csv
├── outputs/
│   ├── forecast_plot.png
│   ├── forecast_results.csv
│   ├── inventory_summary.csv
│   └── model_comparison.csv
├── src/
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── forecasting.py
│   ├── inventory.py
│   ├── main.py
│   └── visualization.py
├── README.md
└── requirements.txt
```

## Setup Instructions
1. Make sure Python 3.10+ is installed.
2. Open a terminal in the project root folder.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Run the Program
Run the program from the project root:

```bash
python src/main.py
```

The program will:
- load `data/demand_data.csv`
- validate the input columns
- generate forecasts for each method
- calculate evaluation metrics
- print a forecast summary table in the terminal
- calculate inventory values from the historical demand
- print a clean inventory summary in the terminal
- save detailed outputs into the `outputs/` folder
- generate a forecast comparison plot and save it as `outputs/forecast_plot.png`

## Forecasting Methods
### 1. Naive Forecast
Uses the previous period's actual demand as the forecast for the next period.

### 2. 3-Period Moving Average
Uses the average of the previous 3 demand values.

### 3. Weighted Moving Average
Uses the previous 3 demand values with weights `[0.5, 0.3, 0.2]`, where the most recent demand gets the highest weight.

### 4. Simple Exponential Smoothing
Uses a smoothing factor of `alpha = 0.3` to update forecasts over time. Recent demand is included more heavily than older data, but older information still matters.

## Inventory Logic
Version 2 adds a simple, beginner-friendly inventory summary based on the historical `Demand` column.

After forecasting results and model comparison are created, the program also calculates:
- average demand
- demand standard deviation
- lead time demand
- safety stock
- reorder point

The inventory summary is:
- printed in the terminal
- saved to `outputs/inventory_summary.csv`

## Inventory Assumptions Used in Version 2
- Lead time = `2` periods
- Service level = `95%`
- Z-score = `1.65`

## Inventory Formulas Used
- **Average demand** = mean of `Demand`
- **Demand standard deviation** = standard deviation of `Demand`
- **Lead time demand** = average demand × lead time
- **Safety stock** = z-score × demand standard deviation × √lead time
- **Reorder point** = lead time demand + safety stock

## Forecast Visualization
After the forecast results are generated, the program also creates a comparison line chart that shows the actual demand and all forecast methods on one figure. The chart is saved to `outputs/forecast_plot.png`, and it is also displayed when you run the script locally.

## Evaluation Metrics
### MAD (Mean Absolute Deviation)
Shows the average absolute forecast error.

### MSE (Mean Squared Error)
Shows the average of squared forecast errors. Larger errors are penalized more heavily.

### RMSE (Root Mean Squared Error)
The square root of MSE. This keeps the error value in the same unit as demand.

### MAPE (Mean Absolute Percentage Error)
Shows the average percentage error between actual and forecast values.

## Assumptions Used in This Project
- The input file is always named `demand_data.csv`.
- The file is stored in the `data/` folder.
- The CSV contains exactly the required columns: `Period` and `Demand`.
- Demand values are numeric and do not contain missing values.
- Forecast accuracy is calculated only for periods where a forecast exists.
- This version handles a single time series only.
- The inventory summary uses one common set of assumptions for lead time and service level.

## What Each File Does
- `src/main.py`: Runs the full forecasting and inventory workflow and saves outputs.
- `src/data_loader.py`: Loads the CSV file and validates the input data.
- `src/forecasting.py`: Contains the forecasting methods and adds forecast columns.
- `src/evaluation.py`: Calculates MAD, MSE, RMSE, and MAPE for each method.
- `src/inventory.py`: Calculates average demand, demand variability, safety stock, and reorder point.
- `src/visualization.py`: Builds the forecast comparison chart and saves it as a PNG image.
- `data/demand_data.csv`: Example dataset so the project can run immediately.
- `outputs/`: Stores generated result files after the program runs.
- `requirements.txt`: Lists the Python packages required by the project.
