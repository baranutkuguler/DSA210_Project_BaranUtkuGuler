# 1. Gerekli kütüphaneleri yükle
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# 2. XML dosyasını yükle
file_path = 'dışa aktarılan.xml'  # XML dosyanın tam adı burada
tree = ET.parse(file_path)
root = tree.getroot()

# 3. Kalp atış hızı (heart rate) verilerini seç
heart_rate_data = []

for record in root.findall('Record'):
    if record.attrib.get('type') == 'HKQuantityTypeIdentifierHeartRate':  # Sadece kalp atışı verisi
        heart_rate_data.append({
            'timestamp': record.attrib.get('startDate'),  # Tarih
            'heart_rate': record.attrib.get('value')      # Kalp atışı değeri
        })

# 4. Veriyi pandas DataFrame'e dönüştür
df = pd.DataFrame(heart_rate_data)

# 5. Veriyi temizle ve dönüştür
df['heart_rate'] = pd.to_numeric(df['heart_rate'], errors='coerce')  # Sayısal forma çevir
df['timestamp'] = pd.to_datetime(df['timestamp'])  # Tarih formatına çevir
df = df.dropna()  # Eksik değerleri kaldır
df = df[(df['heart_rate'] > 40) & (df['heart_rate'] < 180)]  # Mantıklı değerleri filtrele

# 6. Veriyi kontrol et
print("İlk 5 satır:\n", df.head())
print("\nVeri Özeti:\n", df.describe())

# 7. Basit bir zaman serisi grafiği oluştur
plt.plot(df['timestamp'], df['heart_rate'])
plt.title("Heart Rate Over Time")
plt.xlabel("Time")
plt.ylabel("Heart Rate (BPM)")
plt.xticks(rotation=45)
plt.show()
# Zaman serisi grafiği
plt.figure(figsize=(10, 5))  # Grafiği daha büyük yap
plt.plot(df['timestamp'], df['heart_rate'], label='Heart Rate')
plt.title("Heart Rate Over Time")
plt.xlabel("Time")
plt.ylabel("Heart Rate (BPM)")
plt.legend()
plt.grid()
plt.xticks(rotation=45)  # X eksenindeki tarihleri yatay çevir
plt.tight_layout()
plt.show()
# Günlük ortalama kalp atış hızı
df['date'] = df['timestamp'].dt.date  # Sadece tarih kısmını al
daily_avg = df.groupby('date')['heart_rate'].mean()

# Günlük ortalama grafiği
plt.figure(figsize=(10, 5))
daily_avg.plot(kind='bar', color='skyblue')
plt.title("Daily Average Heart Rate")
plt.xlabel("Date")
plt.ylabel("Average Heart Rate (BPM)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Saatlik analiz ekleyelim
df['hour'] = df['timestamp'].dt.hour
hourly_avg = df.groupby('hour')['heart_rate'].agg(['mean', 'std'])

# Saatlik ortalama grafiği
plt.figure(figsize=(12, 6))
plt.errorbar(hourly_avg.index, hourly_avg['mean'], yerr=hourly_avg['std'], 
             capsize=5, capthick=1, ecolor='gray', color='blue')
plt.title("Average Heart Rate by Hour of Day")
plt.xlabel("Hour")
plt.ylabel("Heart Rate (BPM)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Hafta içi vs hafta sonu analizi
df['weekday'] = df['timestamp'].dt.day_name()
weekday_avg = df.groupby('weekday')['heart_rate'].mean()
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_avg = weekday_avg.reindex(weekday_order)

plt.figure(figsize=(10, 6))
weekday_avg.plot(kind='bar', color=['blue']*5 + ['green']*2)
plt.title("Average Heart Rate by Day of Week")
plt.xlabel("Day")
plt.ylabel("Average Heart Rate (BPM)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# EKG verilerini yükle ve analiz et
def load_ecg_data(file_path):
    df = pd.read_csv(file_path, skiprows=12)  # Header'ı atla
    df = df.iloc[:, 0]  # Sadece veri sütununu al
    return df

# EKG dosyalarını analiz et
ecg_files = ['electrocardiograms/ecg_2021-11-25.csv', 
             'electrocardiograms/ecg_2021-11-26.csv',
             'electrocardiograms/ecg_2021-11-27.csv']

plt.figure(figsize=(15, 10))
for file in ecg_files:
    ecg_data = load_ecg_data(file)
    date = file.split('_')[1].split('.')[0]
    plt.plot(ecg_data[:1000], label=date)  # İlk 1000 veri noktası

plt.title("EKG Dalga Formları Karşılaştırması")
plt.xlabel("Örnek Sayısı")
plt.ylabel("Voltaj (µV)")
plt.legend()
plt.grid(True)
plt.show()

# Aktivite analizi için kalp atış hızı istatistikleri
def analyze_heart_rate_stats(df):
    stats = {
        'mean': df['heart_rate'].mean(),
        'std': df['heart_rate'].std(),
        'max': df['heart_rate'].max(),
        'min': df['heart_rate'].min()
    }
    return stats

# Günlük aktivite analizi
daily_stats = df.groupby(df['timestamp'].dt.date).apply(analyze_heart_rate_stats)
print("\nGünlük Kalp Atış Hızı İstatistikleri:")
print(daily_stats)