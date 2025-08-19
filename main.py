# -----------------------------
# 1. GEREKLİ KÜTÜPHANELERİ YÜKLE
# -----------------------------
!pip install yfinance xgboost scikit-learn matplotlib pandas numpy tensorflow

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from xgboost import XGBRegressor
import warnings
warnings.filterwarnings("ignore")

# ----------------------------------
# 2. VERİYİ İNDİR: USD/TRY DÖVİZ KURU
# ----------------------------------
# Yahoo Finance'te döviz çiftleri "USDTTRY=X" formatında yazılır
ticker = "USDTRY=X"
data = yf.download(ticker, start="2018-01-01", end="2024-06-01")

# Sadece kapanış fiyatını al
df = data[['Close']].copy()
df.reset_index(inplace=True)
df.columns = ['Date', 'Exchange_Rate']  # Daha anlaşılır sütun adı

print("İlk 5 veri:")
print(df.head())

# ----------------------------------
# 3. VERİYİ GÖRSELLEŞTİR
# ----------------------------------
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Exchange_Rate'], color='purple', linewidth=1.5)
plt.title('USD/TRY Döviz Kuru (2018 - 2024)', fontsize=16)
plt.xlabel('Tarih', fontsize=12)
plt.ylabel('1 USD = ? TRY', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ----------------------------------
# 4. VERİ ÖN İŞLEME: NORMALİZASYON
# ----------------------------------
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(df['Exchange_Rate'].values.reshape(-1, 1))

# ----------------------------------
# 5. ZAMAN PENCERESİ OLUŞTUR
# ----------------------------------
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i - seq_length:i, 0])
        y.append(data[i, 0])
    return np.array(X), np.array(y)

SEQ_LENGTH = 30  # Son 30 gün verisiyle 31. günü tahmin et
X, y = create_sequences(scaled_data, SEQ_LENGTH)

# Eğitim (%80) ve test (%20) böl
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# LSTM için veriyi 3D'ye çevir: (örnek sayısı, zaman adımı, özellik)
X_train_lstm = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test_lstm = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# XGBoost için (2D)
X_train_xgb = X_train
X_test_xgb = X_test

# ----------------------------------
# 6. LSTM MODELİ
# ----------------------------------
print("\n➡️ LSTM Modeli Eğitiliyor...")

model_lstm = Sequential([
    LSTM(50, return_sequences=True, input_shape=(SEQ_LENGTH, 1)),
    LSTM(50, return_sequences=False),
    Dense(25),
    Dense(1)
])

model_lstm.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
model_lstm.fit(X_train_lstm, y_train, epochs=20, batch_size=32, verbose=1)

# Tahmin
y_pred_lstm_scaled = model_lstm.predict(X_test_lstm)
y_pred_lstm = scaler.inverse_transform(y_pred_lstm_scaled)
y_test_actual = scaler.inverse_transform(y_test.reshape(-1, 1))

# ----------------------------------
# 7. XGBOOST MODELİ
# ----------------------------------
print("\n➡️ XGBoost Modeli Eğitiliyor...")

model_xgb = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
model_xgb.fit(X_train_xgb, y_train)

y_pred_xgb_scaled = model_xgb.predict(X_test_xgb)
y_pred_xgb = scaler.inverse_transform(y_pred_xgb_scaled.reshape(-1, 1))

# ----------------------------------
# 8. SONUÇLARI GÖSTER
# ----------------------------------
test_dates = df['Date'].values[split + SEQ_LENGTH:]

plt.figure(figsize=(16, 8))
plt.plot(test_dates, y_test_actual, label='Gerçek Kur', color='black', linewidth=2)
plt.plot(test_dates, y_pred_lstm, label='LSTM Tahmini', color='red', alpha=0.8, linestyle='--')
plt.plot(test_dates, y_pred_xgb, label='XGBoost Tahmini', color='blue', alpha=0.7, linestyle='-.')
plt.title('USD/TRY Döviz Kuru Tahmini Karşılaştırması (LSTM vs XGBoost)', fontsize=14)
plt.xlabel('Tarih')
plt.ylabel('Döviz Kuru (TRY)')
plt.legend()
plt.xticks(rotation=60)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ----------------------------------
# 9. HATA ANALİZİ
# ----------------------------------
def evaluate(y_true, y_pred, name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f"{name} - MAE: {mae:.4f}, RMSE: {rmse:.4f}")
    return mae, rmse

print("\n📊 MODEL PERFORMANSI")
lstm_mae, lstm_rmse = evaluate(y_test_actual, y_pred_lstm, "LSTM")
xgb_mae, xgb_rmse = evaluate(y_test_actual, y_pred_xgb, "XGBoost")

print("\n🏆 KAZANAN MODEL:")
if lstm_rmse < xgb_rmse:
    print("✅ LSTM, XGBoost'a göre daha az hata yaptı (RMSE açısından).")
else:
    print("✅ XGBoost, LSTM'e göre daha az hata yaptı (RMSE açısından).")
