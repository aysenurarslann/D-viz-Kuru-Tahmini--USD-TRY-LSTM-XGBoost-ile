# USD/TRY Döviz Kuru Tahmini Projesi

Bu proje, **Amerikan Doları / Türk Lirası (USD/TRY)** döviz kuru tahmini yapmak için **LSTM (derin öğrenme)** ve **XGBoost (Makine öğrenmesi)** modellerini karşılaştırır.
--
## Amaç
Geçmiş 30 günlük döviz kuru verilerini kullanarak, bir sonraki günün kapanış kurunu tahmin etmek ve hangi modelin daha iyi perfrmans gösterdiğini analiz etmek.
--
## Veri Kaynağı
-**Sembol**: 'USDTRY=X'
-**Kaynak**: Yahoo Finance ('yfinance')
-**Zaman Aralığı**: 2018-01-01 ile 2024-06-01
-**Frekans**: Günlük
-**Sütun**: 'Close' (Kapanış kuru)

--
## Teknik Detaylar
-**Zaman penceresi**: 30 gün
-**Eğitim/Test oranı** : %80 / %20
-**Normalizasyon**: MinMaxScaller (0-1)
-**Metrikler**: MAE, RMSE

--
## Sonuçlar
- LSTM, zaman serisi verilerinde genellikle daha iyi performans gösterir
- XGBoost, hızlı ve az veride iyi çalışabilir.
- Gerçek piyasa, siyasi/ekonomik şoklarla etkilendiği için, model tahminleri sınırlıdır.

--

## Uyarı
Bu proje **eğitim amaçlıdır**. Gerçek döviz alım satım için kullanılmamalıdır. Finansal kararlar için profesyonel danışın.
