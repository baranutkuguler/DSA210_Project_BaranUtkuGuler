import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def analyze_24h_periods(df):
    """24 saatlik periyotları analiz et"""
    
    # Veriyi 24 saatlik periyotlara böl
    df['period'] = df['timestamp'].dt.strftime('%Y-%m-%d')
    
    # Her periyot için alt grafikler oluştur
    periods = df['period'].unique()
    fig, axes = plt.subplots(len(periods), 1, figsize=(15, 5*len(periods)))
    
    if len(periods) == 1:
        axes = [axes]
    
    for idx, period in enumerate(periods):
        period_data = df[df['period'] == period]
        
        # Saatlik veriler
        hourly_stats = period_data.groupby(period_data['timestamp'].dt.hour).agg({
            'value': ['mean', 'std', 'count']
        })['value']
        
        # Grafik çizimi
        ax = axes[idx]
        
        # Ortalama çizgisi
        ax.plot(hourly_stats.index, hourly_stats['mean'], 
                color='blue', linewidth=2, label='Ortalama')
        
        # Standart sapma aralığı
        ax.fill_between(hourly_stats.index,
                       hourly_stats['mean'] - hourly_stats['std'],
                       hourly_stats['mean'] + hourly_stats['std'],
                       alpha=0.2, color='blue', label='±1 Standart Sapma')
        
        # Ölçüm sayıları
        for hour, stats in hourly_stats.iterrows():
            if not np.isnan(stats['count']):
                ax.text(hour, stats['mean'], f'n={int(stats["count"])}', 
                       ha='center', va='bottom')
        
        # Grafik düzenlemeleri
        ax.set_title(f'24 Saatlik Periyot: {period}')
        ax.set_xlabel('Saat')
        ax.set_ylabel('Kalp Atış Hızı (BPM)')
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend()
        
        # İstatistiksel özet
        print(f"\nPeriyot: {period}")
        print("-" * 40)
        print(f"Ortalama: {hourly_stats['mean'].mean():.1f} BPM")
        print(f"Minimum: {hourly_stats['mean'].min():.1f} BPM")
        print(f"Maksimum: {hourly_stats['mean'].max():.1f} BPM")
        print(f"Toplam ölçüm: {int(hourly_stats['count'].sum())}")
    
    plt.tight_layout()
    plt.show()

def main():
    # Veriyi oku
    df = pd.read_csv('processed_health_data_sample.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 24 saatlik periyot analizi
    analyze_24h_periods(df)

if __name__ == "__main__":
    main() 