import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller
import warnings

warnings.filterwarnings('ignore')

# Veri setini yükle
df = pd.read_csv('panel_macro_data.csv')

# 1. Tanımlayıcı İstatistikler (Descriptive Statistics)
desc_stats = df.describe().round(3)
with open('1_descriptive_statistics.txt', 'w') as f:
    f.write("Panel Veri Tanımlayıcı İstatistikleri\n")
    f.write("="*50 + "\n")
    f.write(desc_stats.to_string())

# 2. Korelasyon Analizi (Correlation Matrix & Heatmap)
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
X_vars = df[['Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']]
X_vars = X_vars.dropna()

# DİKKAT: VIF hesaplanırken Orijin (0,0) geçişi hatasını önlemek için sabit (constant) terim eklenmelidir.
X_vars_const = sm.add_constant(X_vars)

vif_data = pd.DataFrame()
vif_data["Degisken"] = X_vars_const.columns
vif_data["VIF_Skoru"] = [variance_inflation_factor(X_vars_const.values, i) for i in range(len(X_vars_const.columns))]

# Sabit terimin VIF değerini rapordan çıkaralım (anlamsızdır)
vif_data = vif_data[vif_data['Degisken'] != 'const']

with open('3_vif_multicollinearity_test.txt', 'w') as f:
    f.write("VIF (Çoklu Doğrusallık) Test Sonuçları\n")
    f.write("="*50 + "\n")
    f.write(vif_data.to_string(index=False))
    f.write("\n\nNot: VIF skorlarının 5'in altında olması değişkenler arası korelasyon sorunu olmadığını gösterir.\n")
    f.write("Değerlerin 1 civarında olması (örneğin 1.2 - 1.5) değişkenler arasında çoklu doğrusallık riskinin olmadığını teyit eder.\n")

# 4. Panel Birim Kök (Stationarity) Testleri - Fisher-ADF Meta Analizi (Choi, 2001)
# Sadece p-değerlerinin ortalamasını almak ekonometrik olarak geçersizdir.
# Fisher testi: Chi-Square = -2 * Sum(ln(p_i)) formülü ile hesaplanır.
results = []
for country in df['Country'].unique():
    country_data = df[df['Country'] == country]
    if len(country_data) > 10:  
        adf_gdp = adfuller(country_data['GDP_Growth'])[1]  
        adf_gov = adfuller(country_data['Gov_Expenditure'])[1]
        
        # Logaritma alırken 0'a çok yakın p-değerleri -inf üretmesin diye küçük bir sınır ekliyoruz
        adf_gdp = max(adf_gdp, 1e-10)
        adf_gov = max(adf_gov, 1e-10)
        
        results.append({'Country': country, 'GDP_Growth_p_val': adf_gdp, 'GovExp_p_val': adf_gov})

adf_df = pd.DataFrame(results)
p_vals_gdp = adf_df['GDP_Growth_p_val'].values
p_vals_gov = adf_df['GovExp_p_val'].values

N = len(p_vals_gdp)
fisher_chi2_gdp = -2 * np.sum(np.log(p_vals_gdp))
fisher_chi2_gov = -2 * np.sum(np.log(p_vals_gov))

# Chi-Square dağılımı (Serbestlik derecesi df = 2 * N)
fisher_p_gdp = stats.chi2.sf(fisher_chi2_gdp, 2 * N)
fisher_p_gov = stats.chi2.sf(fisher_chi2_gov, 2 * N)

with open('4_panel_unit_root_tests.txt', 'w') as f:
    f.write("Panel Birim Kök Test Özeti (Fisher-ADF Testi)\n")
    f.write("="*50 + "\n")
    f.write(f"GDP_Growth Fisher Chi-Square: {fisher_chi2_gdp:.4f}, P-Value: {fisher_p_gdp:.4f}\n")
    f.write(f"Gov_Expenditure Fisher Chi-Square: {fisher_chi2_gov:.4f}, P-Value: {fisher_p_gov:.4f}\n")
    f.write("\nMetodolojik Not:\n")
    f.write("Fisher-ADF testinin Temel Hipotezi (H0) 'Panelde birim kök vardır (durağan değildir)' şeklindedir.\n")
    f.write("Eğer P-Value < 0.05 ise H0 reddedilir ve serinin durağan olduğu sonucuna varılır.\n")

print("Faz 2 (EDA ve Diagnostik testler) başarıyla tamamlandı.")
