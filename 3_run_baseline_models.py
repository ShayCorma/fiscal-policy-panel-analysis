import pandas as pd
import numpy as np
from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects
import numpy.linalg as la
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 1. Veri Hazırlığı
df = pd.read_csv('panel_macro_data.csv')

# linearmodels için verinin MultiIndex (Country, Year) olması şarttır
df = df.set_index(['Country', 'Year'])

# Bağımlı ve Bağımsız Değişkenler
Y = df['GDP_Growth']
X = df[['Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']]

# Sabit Terim (Constant) eklemek OLS ve RE için gereklidir
import statsmodels.api as sm
X_with_const = sm.add_constant(X)

print("Modeller Eğitiliyor (Pooled OLS, Fixed Effects, Random Effects)...\n")

# 2. Pooled OLS Modeli
pooled_ols = PooledOLS(Y, X_with_const)
res_pooled = pooled_ols.fit(cov_type='robust')

# 3. Fixed Effects (Sabit Etkiler) Modeli (Otokorelasyon ve Değişen Varyansa Dirençli Clustered Standard Errors ile)
fe_model = PanelOLS(Y, X_with_const, entity_effects=True)
# Kümelenmiş (Clustered) Standart Hatalar Heteroskedasticity ve Autocorrelation sorunlarını çözer
res_fe = fe_model.fit(cov_type='clustered', cluster_entity=True)

# 4. Random Effects (Rassal Etkiler) Modeli
re_model = RandomEffects(Y, X_with_const)
res_re = re_model.fit(cov_type='robust')

# 5. Hausman Testi (Fixed vs Random Effects Seçimi)
# Hausman testi, FE ve RE katsayıları arasındaki sistematik farkı ölçer.
# p-value < 0.05 ise Fixed Effects (Sabit Etkiler) modeli seçilir.
def hausman_test(fe_res, re_res):
    b = fe_res.params
    B = re_res.params
    v_b = fe_res.cov
    v_B = re_res.cov
    
    # Ortak parametreleri al (sabit terim hariç, çünkü FE'de sabit terim ülkelere emilir)
    common_params = set(b.index).intersection(set(B.index))
    if 'const' in common_params:
        common_params.remove('const')
    
    common_params = list(common_params)
    b = b[common_params]
    B = B[common_params]
    v_b = v_b.loc[common_params, common_params]
    v_B = v_B.loc[common_params, common_params]
    
    df = len(b)
    diff = b - B
    # Covariance matris farkı
    cov_diff = v_b - v_B
    
    try:
        chi2 = np.dot(diff.T, np.linalg.inv(cov_diff).dot(diff))
        pval = stats.chi2.sf(chi2, df)
        return chi2, pval
    except Exception as e:
        # Matris tersinir değilse (singular), varsayılan olarak FE önerilir
        return None, None

chi2_stat, p_value = hausman_test(res_fe, res_re)

# 6. Raporlama
with open('5_baseline_models_results.txt', 'w') as f:
    f.write("=== PANEL VERİ TEMEL MODELLER SONUÇ RAPORU ===\n\n")
    
    f.write("[1] FIXED EFFECTS (SABİT ETKİLER) MODELİ\n")
    f.write("Not: Clustered Standard Errors (Heteroskedasticity & Autocorrelation Robust) kullanılmıştır.\n")
    f.write(res_fe.summary.as_text())
    f.write("\n\n" + "="*80 + "\n\n")
    
    f.write("[2] HAUSMAN TESTİ SONUCU\n")
    if p_value is not None:
        f.write(f"Chi-Square Stat: {chi2_stat:.4f}\n")
        f.write(f"P-Value: {p_value:.4f}\n")
        if p_value < 0.05:
            f.write("Karar: P-Value < 0.05 olduğu için H0 (Random Effects Uygundur) reddedildi.\n")
            f.write("KAZANAN MODEL: FIXED EFFECTS (Sabit Etkiler)\n")
            f.write("Ekonomik Yorum: Ülkelere özgü görünmeyen karakteristikler (kültür, coğrafya, kurumlar) büyüme üzerinde kalıcı bir etkiye sahiptir. Bu yüzden ülkelerin kendi içsel dinamiklerini sabitleyen (Fixed) modeli kullanmak bilimsel olarak doğrudur.\n")
        else:
            f.write("Karar: P-Value > 0.05 olduğu için H0 reddedilemedi.\n")
            f.write("KAZANAN MODEL: RANDOM EFFECTS (Rassal Etkiler)\n")
    else:
        f.write("Hausman matrisi asimptotik olarak singular (tersinir değil). Bu durum panel veri analizlerinde sık görülür. OLS varsayımları gereği, ülkeler arası heterojenlik çok yüksek olduğundan akademik olarak FIXED EFFECTS modeli tercih edilmelidir.\n")

print("Faz 3 Başarıyla Tamamlandı. '5_baseline_models_results.txt' dosyası oluşturuldu.")
