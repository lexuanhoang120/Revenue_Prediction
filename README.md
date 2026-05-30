# Revenue Prediction — ICOOL Restaurant Chain

> This project was developed during my time at **[VTCODE Company](https://vtcode.vn/)**.

Daily revenue forecasting for the ICOOL restaurant chain using Facebook Prophet. Predicts revenue for each store individually, 10 months ahead, with custom seasonality and holiday effects tuned per location.

---

## What it does

Given 5 years of daily revenue data (2017–2022) across 17 restaurant locations, the model forecasts daily revenue for the next ~10 months. Each store gets its own Prophet model with tuned parameters, cap/floor constraints based on store size, and custom features for Vietnamese holidays and weekend patterns.

Output is daily revenue in millions VND, per store, saved as CSV files ready for financial planning.

---

## Results

Annual revenue predictions for 2022 (March–December), in billions VND:

| Store | Annual Revenue (tỷ VND) | Store | Annual Revenue (tỷ VND) |
|---|---|---|---|
| CH 7 | 40.05 | CH 14 | 36.45 |
| CH 1 | 38.20 | CH 6 | 22.31 |
| CH 18 | 30.89 | CH 4 | 20.28 |
| CH 10 | 29.87 | CH 22 | 20.56 |
| CH 12 | 28.59 | CH 5 | 16.18 |
| CH 17 | 15.49 | CH 9 | 13.62 |
| CH 13 | 12.14 | CH 23 | 10.34 |
| CH 11 | 8.54 | CH 16 | 8.04 |
| CH 19 | 8.19 | | |

**Total projected revenue across all 17 stores: ~360 tỷ VND** for the 10-month forecast period.

---

## Approach

### Model: Facebook Prophet

Each store gets its own Prophet model with logistic growth — revenue can't grow infinitely, so each store has a ceiling (`cap`) and floor (`floor`) based on its historical maximum and minimum daily revenue.

**Parameters:**

| Parameter | Value | Purpose |
|---|---|---|
| Weekly seasonality | 6 | Captures day-of-week patterns (weekends spike, Mondays dip) |
| Monthly seasonality | 3 | Captures within-month cycles |
| Yearly seasonality | 6 | Annual trends and seasonality |
| Seasonality prior | 0.8 | How flexible the seasonal pattern is |
| Holiday prior | 9 | Weight of holiday effects |
| Changepoint prior | 0.8 | Sensitivity to trend changes |
| Growth | Logistic | Bounded growth with cap/floor |

**Custom features:**

- **NFL Sunday / NFL Monday** — Vietnamese weekend pattern (Saturday = NFL Sunday, Monday = NFL Monday). These days have dramatically different revenue patterns, so custom binary regressors were added.
- **Lunar calendar** — Vietnamese holidays (Tết, etc.) follow the lunar calendar, incorporated as additional regressors.
- **Store-level caps** — Each store has different capacity (`xmax`/`xmin`), manually set based on historical data: larger stores at 300–400M VND/day, smaller ones at 50–80M VND/day.

### Data pipeline

```
Raw daily revenue CSVs (2017–2022)
    ↓
Clean: date, store_id, revenue columns only
    ↓
Revenue normalized to millions VND (÷1,000,000)
    ↓
Per-store Prophet model training
    ↓
Model serialized to JSON (model_{version}_{store_id}.json)
    ↓
Inference: predict 306 days per store → output CSV
```

### Training & evaluation

Two training periods:
1. **Group 1** (7 stores): trained on data up to Feb 9, 2022, validated against Feb 9–17
2. **Group 2** (10 stores): trained on data up to Feb 17, 2022

Models were evaluated with RMSE against a held-out validation period before final prediction.

---

## Project structure

```
.
├── data/                           # Revenue data (daily, per store)
│   ├── DT_20210101_20211231.csv    # 2021 full year (1,840 rows)
│   ├── DT_20220103_20220405.csv    # 2022 Q1 (681 rows)
│   └── sales_train.csv             # Additional training data
├── revenue/
│   ├── data/                       # Historical revenue CSVs (2017–2022)
│   ├── source/
│   │   ├── 3.train.ipynb           # Main training notebook
│   │   ├── 3.deploy.ipynb          # Deployment/batch prediction
│   │   ├── 4.statistic.ipynb       # Annual revenue aggregation
│   │   ├── inference.ipynb         # Single-store inference demo
│   │   ├── models/                 # Serialized Prophet models (JSON, 17 stores)
│   │   └── params.py               # Model parameters
│   ├── output/                     # Predictions per store (306 days each)
│   └── docs/
│       └── DEPLOY_REVENUE_PREDICTION.pptx
└── README.md
```

---

## How to run

```bash
cd revenue/source
pip install fbprophet pandas plotly lunar-calendar

# Train a store
jupyter notebook 3.train.ipynb

# Batch predict all stores
jupyter notebook 3.deploy.ipynb

# View annual revenue totals
jupyter notebook 4.statistic.ipynb
```

Models are saved as JSON and can be reloaded without retraining:

```python
from fbprophet.serialize import model_from_json
with open('models/model_1.0_6.json') as f:
    model = model_from_json(json.load(f))
```

---

## Notes

- Revenue values are in **millions VND** — divide raw values by 1,000,000 before training.
- The `sales_train.csv` file is from a separate Kaggle competition dataset (Predict Future Sales) and was used for exploration.
- Store cap/floor values (`xmax`/`xmin`) are manually tuned per store based on historical ranges — they're not learned automatically.
