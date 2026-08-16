import pandas as pd
import wbgapi as wb
import time

print("Faz 1: Panel Veri Toplama Süreci Başlıyor...")

# 1. Ülke Listesi (Gelişmiş ve Gelişmekte Olan Seçilmiş G20 Ülkeleri)
countries = [
    'USA', 'DEU', 'GBR', 'FRA', 'CAN', 'JPN', 'ITA', 'ESP', 'KOR', # Gelişmiş
    'TUR', 'BRA', 'MEX', 'IND', 'POL', 'ZAF', 'IDN', 'ARG', 'CHN'  # Gelişmekte Olan
]

# 2. İndikatör Listesi (Dünya Bankası Kodları)
indicators = {
    'NY.GDP.MKTP.KD.ZG': 'GDP_Growth',               # Bağımlı Değişken (Ekonomik Büyüme %)
    'NE.CON.GOVT.ZS': 'Gov_Expenditure',             # Bağımsız Değişken (Devlet Harcamaları / GSYH %)
    'FP.CPI.TOTL.ZG': 'Inflation',                   # Enflasyon (%)
    'SL.UEM.TOTL.ZS': 'Unemployment',                # İşsizlik (%)
    'BX.KLT.DINV.WD.GD.ZS': 'Investment_FDI',        # Yatırım (FDI / GSYH %)
    'FR.INR.RINR': 'Real_Interest_Rate',             # Reel Faiz Oranı (%)
    'NE.TRD.GNFS.ZS': 'Trade_Openness'               # Ticaret Açıklığı (İthalat+İhracat / GSYH %)
}

years = range(2000, 2024) # 2000 - 2023 arası

print(f"-> {len(countries)} ülke için {len(indicators)} makroekonomik değişken Dünya Bankası'ndan çekiliyor...")
print("-> Bu işlem birkaç dakika sürebilir, lütfen bekleyin...")

# 3. Veriyi API'den Çekmek
try:
    # wbgapi.data.DataFrame returns a multi-index panel format automatically!
    df_raw = wb.data.DataFrame(
        series=list(indicators.keys()), 
        economy=countries, 
        time=years, 
        labels=False
    )
except Exception as e:
    print(f"HATA: Dünya Bankası API'sine bağlanılamadı. Detay: {e}")
    exit(1)

print("-> Veriler başarıyla çekildi. Panel yapılandırması (Country-Year) yapılıyor...")

# 4. Veri Manipülasyonu: Panel Yapıya Çevirme (Melt / Unstack / Stack)
# The dataframe format returned by wbgapi is generally (economy, series) as rows, and (YR2000, YR2001...) as columns
# We need to unstack series to columns, and melt years to rows.
df_raw = df_raw.reset_index()

# Yılların sütun adlarını (YR2000 -> 2000) düzeltelim
rename_dict = {f'YR{y}': str(y) for y in years}
df_raw.rename(columns=rename_dict, inplace=True)

# Melt işlemi ile yılları satırlara alıyoruz
df_melted = pd.melt(df_raw, id_vars=['economy', 'series'], value_vars=[str(y) for y in years], 
                    var_name='Year', value_name='Value')

# Pivot işlemi ile serileri sütunlara alıyoruz
df_panel = df_melted.pivot_table(index=['economy', 'Year'], columns='series', values='Value').reset_index()

# Sütun isimlerini okunabilir hale getirelim
df_panel.rename(columns=indicators, inplace=True)
df_panel.rename(columns={'economy': 'Country'}, inplace=True)

# Sütunların sırasını düzenleyelim
cols = ['Country', 'Year', 'GDP_Growth', 'Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']
df_panel = df_panel[cols]

# Yılı integer yapalım
df_panel['Year'] = df_panel['Year'].astype(int)

# 5. Eksik Veri Temizliği (Missing Values Handling)
print(f"-> Ham veri seti boyutu: {df_panel.shape}")
print("-> Eksik veriler interpolasyon ile dolduruluyor ve kullanılamayanlar temizleniyor...")

# Ülke bazında gruplayarak doğrusal interpolasyon yapıyoruz (Boşlukları en yakın verilerle doldurmak için)
df_panel = df_panel.groupby('Country', group_keys=False).apply(lambda group: group.interpolate(method='linear', limit_direction='both'))

# İnterpolasyon sonrası hala boş kalan (hiç ölçülmemiş) satırları sil
df_panel.dropna(inplace=True)

print(f"-> Temizlenmiş nihai veri seti boyutu: {df_panel.shape}")

# 6. CSV Olarak Kaydet
df_panel.to_csv('panel_macro_data.csv', index=False)
print("-> 'panel_macro_data.csv' dosyası başarıyla kaydedildi!")
print("Faz 1 Tamamlandı.")
