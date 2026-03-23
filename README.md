# Forecasting and Inventory Decision Support System

## Project Overview
This beginner-friendly Python project demonstrates a simple demand forecasting workflow for an inventory decision support system. It reads historical demand from a CSV file, applies several forecasting methods, evaluates their accuracy, selects the best-performing method using MAPE, converts the best forecast into inventory planning values, and saves detailed results for later review.

Version 3 keeps the project small, readable, well-commented, and easy to extend while introducing forecast-to-inventory integration and EOQ.

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
- identify the best forecast model using the lowest MAPE
- use the most recent available forecast from that best model as expected demand per period
- calculate inventory values from the forecast and historical demand variation
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

## Forecast-to-Inventory Integration
Version 3 connects forecasting results directly to inventory planning.

Instead of using the historical average demand, the project now:
1. compares all forecast methods
2. selects the method with the **lowest MAPE**
3. takes the **most recent available forecast value** from that best model
4. uses that value as the **expected demand per period** in the inventory calculations

This makes the inventory summary more forward-looking because it uses the best available forecast rather than only relying on past average demand.

## Inventory Logic in Version 3
After forecasting results and model comparison are created, the program also calculates:
- best model
- expected demand per period
- demand standard deviation
- lead time demand
- safety stock
- reorder point
- annual demand
- EOQ

The inventory summary is:
- printed in the terminal
- saved to `outputs/inventory_summary.csv`

## Reorder Point Meaning
The **reorder point** is the inventory level where a new order should be placed.

It combines:
- the demand expected during lead time
- extra safety stock to protect against uncertainty

If on-hand inventory drops to the reorder point, that is the signal to reorder.

## EOQ Meaning
The **economic order quantity (EOQ)** is the order size that balances:
- ordering too often, which increases ordering costs
- ordering too much at once, which increases holding costs

EOQ gives a simple estimate of the most cost-efficient order quantity under the assumptions used in this project.

## Assumptions Used in Version 3
### Reorder Point Assumptions
- Lead time = `2` periods
- Service level = `95%`
- Z-score = `1.65`

### EOQ Assumptions
- Periods per year = `12`
- Annual demand = expected demand per period × periods per year
- Ordering cost per order = `50`
- Holding cost per unit per year = `8`

## Formulas Used in Version 3
### Best Model Selection
- **Best model** = forecasting method with the lowest MAPE

### Demand and Reorder Point Formulas
- **Expected demand per period** = most recent available forecast from the best model
- **Demand standard deviation** = standard deviation of historical `Demand`
- **Lead time demand** = expected demand per period × lead time
- **Safety stock** = z × demand standard deviation × √lead time
- **Reorder point** = lead time demand + safety stock

### EOQ Formula
- **Annual demand** = expected demand per period × periods per year
- **EOQ** = √((2DS) / H)
  - `D` = annual demand
  - `S` = ordering cost per order
  - `H` = holding cost per unit per year

## Example Terminal Output
```text
Forecasting and Inventory Decision Support System - Version 3
===============================================================
Loaded data from: /workspace/forecasting-inventory-system/data/demand_data.csv
Number of periods: 15
Best model selected using MAPE: Naive Forecast

Model Comparison Summary
---------------------------------------------------------------
                     Method   MAD   MSE RMSE MAPE
              Naive Forecast 2.71  8.43 2.90 1.98
     Weighted Moving Average 4.19 18.50 4.30 2.99
     3-Period Moving Average 4.89 24.74 4.97 3.49
Simple Exponential Smoothing 6.71 48.82 6.99 4.81

Inventory Summary
---------------------------------------------------------------
Best forecast model (lowest MAPE): Naive Forecast
    Best Model Expected Demand per Period Demand Standard Deviation Lead Time Service Level Z-Score Lead Time Demand Safety Stock Reorder Point Periods per Year Annual Demand Ordering Cost per Order Holding Cost per Unit per Year    EOQ
Naive Forecast                     151.00                     10.82         2          0.95    1.65           302.00        25.25        327.25               12       1812.00                   50.00                           8.00 150.50
```

## Structure of `outputs/inventory_summary.csv`
The generated file contains one row with these columns:

```text
Best Model,
Expected Demand per Period,
Demand Standard Deviation,
Lead Time,
Service Level,
Z-Score,
Lead Time Demand,
Safety Stock,
Reorder Point,
Periods per Year,
Annual Demand,
Ordering Cost per Order,
Holding Cost per Unit per Year,
EOQ
```

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
- The inventory summary uses one common set of assumptions for lead time, service level, and EOQ inputs.

## What Each File Does
- `src/main.py`: Runs the full forecasting and inventory workflow, selects the best model, prints summaries, and saves outputs.
- `src/data_loader.py`: Loads the CSV file and validates the input data.
- `src/forecasting.py`: Contains the forecasting methods and adds forecast columns.
- `src/evaluation.py`: Calculates MAD, MSE, RMSE, and MAPE for each method.
- `src/inventory.py`: Selects the best forecast model and calculates forecast-based inventory values and EOQ.
- `src/visualization.py`: Builds the forecast comparison chart and saves it as a PNG image.
- `data/demand_data.csv`: Example dataset so the project can run immediately.
- `outputs/`: Stores generated result files after the program runs.
- `requirements.txt`: Lists the Python packages required by the project.
