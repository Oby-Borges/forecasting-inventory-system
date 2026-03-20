# Forecasting and Inventory Decision Support System

## Project Overview
This beginner-friendly Python project demonstrates a simple demand forecasting workflow for an inventory decision support system. It reads historical demand from a CSV file, applies several forecasting methods, evaluates their accuracy, prints a comparison table in the terminal, and saves detailed results for later review.

Version 1 focuses on clarity and ease of understanding. The project is designed to be small, readable, and easy to extend.

## Folder Structure
```text
forecasting-inventory-system/
├── data/
│   └── demand_data.csv
├── outputs/
│   ├── forecast_results.csv
│   └── model_comparison.csv
├── src/
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── forecasting.py
│   └── main.py
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
- print a summary table in the terminal
- save detailed outputs into the `outputs/` folder

## Forecasting Methods
### 1. Naive Forecast
Uses the previous period's actual demand as the forecast for the next period.

### 2. 3-Period Moving Average
Uses the average of the previous 3 demand values.

### 3. Weighted Moving Average
Uses the previous 3 demand values with weights `[0.5, 0.3, 0.2]`, where the most recent demand gets the highest weight.

### 4. Simple Exponential Smoothing
Uses a smoothing factor of `alpha = 0.3` to update forecasts over time. Recent demand is included more heavily than older data, but older information still matters.

## Evaluation Metrics
### MAD (Mean Absolute Deviation)
Shows the average absolute forecast error.

### MSE (Mean Squared Error)
Shows the average of squared forecast errors. Larger errors are penalized more heavily.

### RMSE (Root Mean Squared Error)
The square root of MSE. This keeps the error value in the same unit as demand.

### MAPE (Mean Absolute Percentage Error)
Shows the average percentage error between actual and forecast values.

## Assumptions Used in Version 1
- The input file is always named `demand_data.csv`.
- The file is stored in the `data/` folder.
- The CSV contains exactly the required columns: `Period` and `Demand`.
- Demand values are numeric and do not contain missing values.
- Forecast accuracy is calculated only for periods where a forecast exists.
- This version handles a single time series only.
- This version focuses on forecasting support and does not yet include inventory optimization logic.

## What Each File Does
- `src/main.py`: Runs the full forecasting workflow and saves outputs.
- `src/data_loader.py`: Loads the CSV file and validates the input data.
- `src/forecasting.py`: Contains the forecasting methods and adds forecast columns.
- `src/evaluation.py`: Calculates MAD, MSE, RMSE, and MAPE for each method.
- `data/demand_data.csv`: Example dataset so the project can run immediately.
- `outputs/`: Stores generated result files after the program runs.
- `requirements.txt`: Lists the Python packages required by the project.
