# 💱 USD/TRY Exchange Rate Forecasting Project

This project compares **LSTM (Deep Learning)** and **XGBoost (Machine Learning)** models to forecast the **US Dollar / Turkish Lira (USD/TRY)** exchange rate. Our goal is to predict future exchange rates using historical data and evaluate the performance of both models.

---

## 🎯 Objective
Using the past 30 days of exchange rate data, predict the next day’s closing rate and analyze which model performs better.

---

## 📊 Data Source
- **Symbol**: `USDTRY=X`
- **Source**: Yahoo Finance (`yfinance`)
- **Time Period**: January 1, 2018 – June 1, 2024
- **Frequency**: Daily
- **Column Used**: `Close` (Closing Rate)

---

## 🧠 Models Used
| Model      | Description |
|-----------|-------------|
| **LSTM**  | A deep learning model capable of capturing long-term dependencies in time series. It understands sequential patterns, making it strong for forecasting tasks. |
| **XGBoost** | A gradient-boosted decision tree algorithm. Powerful for structured data but limited when applied directly to raw time series without feature engineering. |

---

## 🔧 Technical Details
- **Sequence Length (seq_length)**: 30 days
- **Train/Test Split**: 80% / 20%
- **Data Normalization**: `MinMaxScaler` (scaled to 0–1 range)
- **Evaluation Metrics**: MAE (Mean Absolute Error), RMSE (Root Mean Squared Error)
- **Libraries Used**: `yfinance`, `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `tensorflow`, `xgboost`

---

## 📈 Time Series Visualization

The graph below shows the USD/TRY exchange rate fluctuations between 2018 and 2024. The currency experienced significant volatility, especially after 2020.

![USD/TRY Time Series](2018_2024_yillari_arasinda_usdtry_doviz_kuru_degisimi.png)

> 📌 **Graph Description**:  
> The exchange rate was around 3.8 in 2018 and surged up to nearly 28 by 2023. This high volatility presents a major challenge for forecasting models.

---

## 📊 Model Comparison Results

The graph below compares the predictions of the LSTM and XGBoost models against actual values on the test set.

![Model Comparison](usdtry_doviz_kuru_tahmini_karsilastirmasi_LSTMvsXGBoost.png)

> 📌 **Graph Description**:  
> - **Black line**: Actual exchange rate  
> - **Red dashed line**: LSTM prediction  
> - **Blue dotted line**: XGBoost prediction  
> 
> LSTM better follows the overall trend, while XGBoost struggles to adapt to sudden market movements.

---

## 📊 Error Analysis (Performance Metrics)

| Model      | MAE (Mean Absolute Error) | RMSE (Root Mean Squared Error) |
|-----------|----------------------------|-------------------------------|
| **LSTM**  | 0.87                       | 1.03                          |
| **XGBoost** | 8.11                     | 9.28                          |

### 🔍 Interpretation:
- **LSTM** achieves **significantly better performance** in both MAE and RMSE.
- The high error in XGBoost stems from its inability to inherently understand temporal dependencies when trained on raw sequential data.
- LSTM, designed for sequences, captures long-term trends more effectively.

---

## 🏆 Conclusion: Which Model is Better?

✅ **LSTM** is the **superior model** for this forecasting task.

> 🔎 **Why?**  
> Time series forecasting requires understanding of ordered, sequential dependencies. LSTM can store and utilize these patterns internally, while XGBoost treats each input window as an independent vector without explicit time awareness. Therefore, on raw time series data, LSTM typically outperforms XGBoost.

---

## 🚫 Disclaimer: Not Financial Advice

> ⚠️ This project is **purely educational**.  
> Financial markets are influenced by political events, inflation, interest rates, and global developments. This model only analyzes historical prices. **Never rely solely on such models for real-world investment decisions.**

---



