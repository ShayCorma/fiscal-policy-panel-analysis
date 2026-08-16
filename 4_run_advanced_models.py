import pandas as pd
import numpy as np
import statsmodels.api as sm
from linearmodels.panel import RandomEffects
import warnings
warnings.filterwarnings('ignore')

# 1. Veri Hazırlığı
df = pd.read_csv('panel_macro_data.csv')

# --- KRİZ DEĞİŞKENLERİ (DUMMY) VE ETKİLEŞİM TERİMİ (INTERACTION) ---
# 2008-2009 Küresel Finans Krizi ve 2020-2021 COVID-19 Pandemisi
kriz_yillari = [2008, 2009, 2020, 2021]
df['Crisis'] = df['Year'].apply(lambda x: 1 if x in kriz_yillari else 0)

# Keynesyen Teori Testi: Devlet Harcamaları krizde daha mı etkili?
df['GovExp_x_Crisis'] = df['Gov_Expenditure'] * df['Crisis']

df = df.set_index(['Country', 'Year'])

# Ülke Grupları (Gelişmiş vs Gelişmekte Olan)
developed = ['USA', 'DEU', 'GBR', 'FRA', 'CAN', 'JPN', 'ITA', 'ESP', 'KOR']
# emerging are the rest in the index

def run_model(data, name):
    Y = data['GDP_Growth']
    # Bağımsız değişkenler + Kriz değişkenleri
    X = data[['Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 
              'Real_Interest_Rate', 'Trade_Openness', 'Crisis', 'GovExp_x_Crisis']]
    X = sm.add_constant(X)
    
    # Hausman testi RE gösterdiği için Random Effects kullanıyoruz
    model = RandomEffects(Y, X)
    res = model.fit(cov_type='robust')
    return res

# 2. Tam Örneklem (Full Sample) Modeli
res_full = run_model(df, "Tüm Ülkeler")

# 3. Gelişmiş Ülkeler (Developed) Alt Grup Analizi
df_developed = df[df.index.get_level_values('Country').isin(developed)]
res_dev = run_model(df_developed, "Gelişmiş Ülkeler")

# 4. Gelişmekte Olan Ülkeler (Emerging) Alt Grup Analizi
df_emerging = df[~df.index.get_level_values('Country').isin(developed)]
res_emg = run_model(df_emerging, "Gelişmekte Olan Ülkeler")

# 5. Akademik Raporlama
with open('6_advanced_models_results.txt', 'w') as f:
    f.write("=== FAZ 4: KRİZ DİNAMİKLERİ VE ALT GRUP ANALİZİ SONUÇLARI ===\n\n")
    
    f.write("A. TÜM ÖRNEKLEMDE KEYNESYEN TEORİNİN TESTİ (Crisis & Interaction)\n")
    f.write("="*70 + "\n")
    f.write(res_full.summary.as_text())
    
    # Çıkarımlar
    coef_gov = res_full.params['Gov_Expenditure']
    coef_interaction = res_full.params['GovExp_x_Crisis']
    
    f.write("\n\n-- EKONOMİK ÇIKARIM (FULL SAMPLE) --\n")
    f.write(f"Normal Dönemlerde Devlet Harcaması Etkisi: {coef_gov:.4f}\n")
    f.write(f"Kriz Dönemlerinde Devlet Harcaması Etkisi (Gov + Interaction): {(coef_gov + coef_interaction):.4f}\n")
    if coef_interaction > 0:
        f.write("SONUÇ: Etkileşim katsayısı POZİTİF çıktı. Bu, devlet harcamalarının KRİZ DÖNEMLERİNDE ekonomik büyümeyi, normal dönemlere kıyasla daha güçlü bir şekilde desteklediğini (veya daralmayı azalttığını) gösterir. Bu sonuç DOĞRUDAN KEYNESYEN GÖRÜŞÜ DESTEKLER.\n\n")
    else:
        f.write("SONUÇ: Etkileşim katsayısı negatif. Keynesyen genişlemenin krizlerde beklenen etkiyi yaratmadığı, Hayekçi görüşün (Crowding out) baskın olduğu görülmektedir.\n\n")

    f.write("\nB. GELİŞMİŞ ÜLKELER (DEVELOPED) ANALİZİ\n")
    f.write("="*70 + "\n")
    f.write(res_dev.summary.as_text())
    
    f.write("\n\nC. GELİŞMEKTE OLAN ÜLKELER (EMERGING) ANALİZİ\n")
    f.write("="*70 + "\n")
    f.write(res_emg.summary.as_text())
    
    f.write("\n\n-- ALT GRUP KARŞILAŞTIRMASI (DEVELOPED vs EMERGING) --\n")
    dev_gov_effect = res_dev.params['Gov_Expenditure'] + res_dev.params['GovExp_x_Crisis']
    emg_gov_effect = res_emg.params['Gov_Expenditure'] + res_emg.params['GovExp_x_Crisis']
    
    f.write(f"Gelişmiş Ülkelerde Kriz Anı Harcama Çarpanı: {dev_gov_effect:.4f}\n")
    f.write(f"Gelişmekte Olan Ülkelerde Kriz Anı Harcama Çarpanı: {emg_gov_effect:.4f}\n")
    f.write("Eğer Gelişmiş Ülkelerde etki daha pozitifse, bu durum kurumların güçlü olduğu, borçlanma maliyetlerinin (risk priminin) düşük olduğu ülkelerde devletin maliye politikasının çok daha etkin kullanılabildiği tezini doğrular.\n")

print("Faz 4 (Dinamik/Kriz ve Alt Grup Analizleri) başarıyla tamamlandı. Rapor '6_advanced_models_results.txt' dosyasına yazıldı.")
