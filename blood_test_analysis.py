import pdfplumber
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import re

def parse_test_line(line):
    """Parse a single test result line"""
    # Farklı format paternleri
    patterns = [
        r'(\d{1,2}/\d{1,2}/\d{4}).*?(Hemoglobin|Demir|Ferritin|Vitamin B12|ALT|AST|Kreatin|HDL|LDL|CK).*?(\d+\.?\d*)\s+(\w+/?\w*)',
        r'[-]\s+(Hemoglobin|Demir|Ferritin|Vitamin B12|ALT|AST|Kreatin|HDL|LDL|CK)\s+(\d+\.?\d*)\s+(\w+/?\w*)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            groups = match.groups()
            if len(groups) == 4:  # Tam tarihli format
                date, test_name, result, unit = groups
            else:  # Tarihsiz format
                test_name, result, unit = groups
                date = None
                
            return {
                'date': date,
                'test_name': test_name.strip(),
                'result': float(result),
                'unit': unit.strip()
            }
    return None

def extract_blood_data(folder_path='enabızveri'):
    """Extract blood test data from multiple PDF files"""
    all_blood_tests = []
    
    try:
        pdf_files = sorted([f for f in os.listdir(folder_path) 
                          if f.startswith('Enabiz-Tahlilleri-') and f.endswith('.pdf')])
        
        print(f"Bulunan dosyalar: {len(pdf_files)}")
        
        current_date = None
        for pdf_file in pdf_files:
            full_path = os.path.join(folder_path, pdf_file)
            print(f"\nDosya işleniyor: {pdf_file}")
            
            try:
                with pdfplumber.open(full_path) as pdf:
                    for page in pdf.pages:
                        text = page.extract_text()
                        lines = text.split('\n')
                        
                        for line in lines:
                            # Tarih satırını kontrol et
                            date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', line)
                            if date_match:
                                current_date = date_match.group(1)
                            
                            result = parse_test_line(line)
                            if result:
                                if result['date'] is None and current_date:
                                    result['date'] = current_date
                                all_blood_tests.append(result)
                
            except Exception as e:
                print(f"PDF okuma hatası ({pdf_file}): {str(e)}")
                continue
        
        # DataFrame oluştur
        df = pd.DataFrame(all_blood_tests)
        if not df.empty:
            # Tarihleri datetime'a çevir
            df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
            # Tarihe göre sırala
            df = df.sort_values('date')
        
        return df
        
    except Exception as e:
        print(f"Klasör okuma hatası: {str(e)}")
        return pd.DataFrame()

def analyze_blood_tests(df):
    """Analyze blood test parameters"""
    if df.empty:
        print("Analiz edilecek veri bulunamadı!")
        return
    
    # Her test için trend analizi
    for test_name in df['test_name'].unique():
        test_data = df[df['test_name'] == test_name]
        
        plt.figure(figsize=(12, 6))
        plt.plot(test_data['date'], test_data['result'], 'o-', label='Ölçüm')
        plt.title(f'{test_name} Değişimi')
        plt.xlabel('Tarih')
        plt.ylabel(f'Değer ({test_data["unit"].iloc[0]})')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
        
        # İstatistiksel özet
        print(f"\n{test_name} İstatistikleri:")
        print("-" * 40)
        print(f"Ölçüm sayısı: {len(test_data)}")
        print(f"Ortalama: {test_data['result'].mean():.2f}")
        print(f"Minimum: {test_data['result'].min():.2f}")
        print(f"Maximum: {test_data['result'].max():.2f}")

def main():
    print("Kan tahlili analizi başlıyor...")
    print(f"Çalışma dizini: {os.getcwd()}")
    
    blood_df = extract_blood_data()
    
    if blood_df.empty:
        print("Veri çıkarılamadı!")
        return
    
    print("\nBulunan test parametreleri:")
    print(blood_df['test_name'].unique())
    
    analyze_blood_tests(blood_df)

if __name__ == "__main__":
    main()