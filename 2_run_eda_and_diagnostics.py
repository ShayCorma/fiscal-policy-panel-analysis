import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller
import warnings

warnings.filterwarnings('ignore')

# Veri setini yükle
df = pd.read_csv('panel_macro_data.csv')

# 1. Tanımlayıcı İstatistikler (Descriptive Statistics)
# Verilerin ortalama, standart sapma, min/max değerlerinin raporlanması
desc_stats = df.describe().round(3)
with open('1_descriptive_statistics.txt', 'w') as f:
    f.write("Panel Veri Tanımlayıcı İstatistikleri\n")
    f.write("="*50 + "\n")
    f.write(desc_stats.to_string())

# 2. Korelasyon Analizi (Correlation Matrix & Heatmap)
# Bağımsız değişkenler arasındaki ilk ilişkilerin görselleştirilmesi
plt.figure(figsize=(10, 8))
cols_for_corr = ['GDP_Growth', 'Gov_Expenditure', 'Inflation', 'Unemployment', 
                 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']
corr = df[cols_for_corr].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".2f", linewidths=0.5)
plt.title("Makroekonomik Değişkenler Korelasyon Matrisi")
plt.tight_layout()
plt.savefig('2_correlation_heatmap.png', dpi=300)
plt.close()

# 3. Çoklu Doğrusallık (Multicollinearity) - VIF Testi
# VIF kuralı: < 5 iyi, > 5 dikkat, > 10 problemli.
X_vars = df[['Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']]
X_vars = X_vars.dropna()

vif_data = pd.DataFrame()
vif_data["Degisken"] = X_vars.columns
vif_data["VIF_Skoru"] = [variance_inflation_factor(X_vars.values, i) for i in range(len(X_vars.columns))]

with open('3_vif_multicollinearity_test.txt', 'w') as f:
    f.write("VIF (Çoklu Doğrusallık) Test Sonuçları\n")
    f.write("="*50 + "\n")
    f.write(vif_data.to_string(index=False))
    f.write("\n\nNot: VIF skorlarının 5'in altında olması değişkenler arası korelasyon sorunu olmadığını gösterir.\n")

# 4. Panel Birim Kök (Stationarity) Testleri
# Sahte regresyonu önlemek için değişkenlerin durağanlığının kontrolü
results = []
for country in df['Country'].unique():
    country_data = df[df['Country'] == country]
    if len(country_data) > 10:  
        # Her ülke için bağımsız ADF testi (Levin-Lin-Chu mantığı simülasyonu)
        adf_gdp = adfuller(country_data['GDP_Growth'])[1]  
        adf_gov = adfuller(country_data['Gov_Expenditure'])[1]
        results.append({'Country': country, 'GDP_Growth_p_val': adf_gdp, 'GovExp_p_val': adf_gov})

adf_df = pd.DataFrame(results)
avg_p_gdp = adf_df['GDP_Growth_p_val'].mean()
avg_p_gov = adf_df['GovExp_p_val'].mean()

with open('4_panel_unit_root_tests.txt', 'w') as f:
    f.write("Panel Birim Kök (Stationarity) Test Özeti\n")
    f.write("="*50 + "\n")
    f.write(f"GDP_Growth Ortalama P-Value: {avg_p_gdp:.4f}\n")
    f.write(f"Gov_Expenditure Ortalama P-Value: {avg_p_gov:.4f}\n")
    f.write("\nSonuç: P-değerleri 0.05 civarında veya altındaysa seriler genel hatlarıyla durağandır.\n")

print("Faz 2 (EDA ve Diagnostik testler) başarıyla tamamlandı.")
