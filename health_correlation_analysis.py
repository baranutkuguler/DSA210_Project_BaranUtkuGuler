import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import numpy as np

def analyze_blood_trends():
    """Kan değerlerinin zaman içindeki değişimini analiz et"""
    try:
        # Kan tahlillerini tarih sırasına göre düzenle
        blood_df = pd.DataFrame({
            'date': [
                '2021-08-02', '2022-07-30', '2022-08-04', '2024-09-11', 
                '2024-11-01'
            ],
            'iron': [236.0, 172.0, 223.0, 183.0, 70.0],
            'ferritin': [64.0, 110.0, 100.0, 136.0, 154.0],
            'b12': [237.0, None, None, 399.0, 417.0],
            'kreatin': [107.0, 1.12, 2705.0, None, 88.0]
        })
        blood_df['date'] = pd.to_datetime(blood_df['date'])
        
        # Grafik çiz
        plt.figure(figsize=(15, 10))
        
        # Demir ve Ferritin
        plt.subplot(2, 1, 1)
        plt.plot(blood_df['date'], blood_df['iron'], 'b-o', label='Demir')
        plt.plot(blood_df['date'], blood_df['ferritin'], 'r-o', label='Ferritin')
        plt.title('Demir ve Ferritin Değişimi')
        plt.xlabel('Tarih')
        plt.ylabel('Değer')
        plt.grid(True)
        plt.legend()
        
        # B12 ve Kreatin
        plt.subplot(2, 1, 2)
        plt.plot(blood_df['date'], blood_df['b12'], 'g-o', label='B12')
        plt.plot(blood_df['date'], blood_df['kreatin'], 'y-o', label='Kreatin')
        plt.title('B12 ve Kreatin Değişimi')
        plt.xlabel('Tarih')
        plt.ylabel('Değer')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
        # İstatistiksel analiz
        print("\nİstatistiksel Analiz:")
        print("-" * 40)
        
        for param in ['iron', 'ferritin', 'b12', 'kreatin']:
            values = blood_df[param].dropna()
            print(f"\n{param.upper()} Analizi:")
            print(f"Ortalama: {values.mean():.1f}")
            print(f"Minimum: {values.min():.1f}")
            print(f"Maximum: {values.max():.1f}")
            
            # Trend analizi
            if len(values) >= 2:
                trend = values.iloc[-1] - values.iloc[0]
                print(f"Genel trend: {'Artış' if trend > 0 else 'Azalış'} " +
                      f"({abs(trend):.1f} birim)")
                
                # Özel durumlar
                if param == 'iron' and values.iloc[-1] < 100:
                    print("! Dikkat: Son demir değeri düşük")
                elif param == 'b12' and values.iloc[-1] < 200:
                    print("! Dikkat: Son B12 değeri düşük")
                elif param == 'kreatin' and values.max() > 1000:
                    print("! Dikkat: Yüksek CK değeri tespit edildi")
        
    except Exception as e:
        print(f"Analiz hatası: {str(e)}")

def main():
    print("Sağlık verileri trend analizi başlıyor...")
    analyze_blood_trends()

if __name__ == "__main__":
    main()