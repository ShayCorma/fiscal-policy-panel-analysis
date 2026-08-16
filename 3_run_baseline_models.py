import pandas as pd
import numpy as np
from linearmodels.panel import PooledOLS, PanelOLS, RandomEffects
import statsmodels.api as sm
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('panel_macro_data.csv')
df = df.set_index(['Country', 'Year'])

Y = df['GDP_Growth']
X = df[['Gov_Expenditure', 'Inflation', 'Unemployment', 'Investment_FDI', 'Real_Interest_Rate', 'Trade_Openness']]
X_with_const = sm.add_constant(X)

print("Modeller Eğitiliyor (Pooled OLS, Fixed Effects, Random Effects)...\n")

# 2. Pooled OLS Modeli
pooled_ols = PooledOLS(Y, X_with_const)
res_pooled = pooled_ols.fit(cov_type='robust')

# 3. Hausman testi için unadjusted (standart) hata hesaplamaları gerekir.
fe_model = PanelOLS(Y, X_with_const, entity_effects=True)
re_model = RandomEffects(Y, X_with_const)

# Test modelleri (unadjusted)
fe_test = fe_model.fit(cov_type='unadjusted')
re_test = re_model.fit(cov_type='unadjusted')

# 4. Final Modeller (Dirençli Standart Hatalar)
res_fe = fe_model.fit(cov_type='clustered', cluster_entity=True)
res_re = re_model.fit(cov_type='robust')

# 5. Hausman Testi
def hausman_test(fe_res, re_res):
    b = fe_res.params
    B = re_res.params
    v_b = fe_res.cov
    v_B = re_res.cov
    
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
    cov_diff = v_b - v_B
    
    try:
        chi2 = np.dot(diff.T, np.linalg.inv(cov_diff).dot(diff))
        pval = stats.chi2.sf(chi2, df)
        return chi2, pval
    except Exception as e:
        return None, None

chi2_stat, p_value = hausman_test(fe_test, re_test)

# 6. Raporlama
with open('5_baseline_models_results.txt', 'w') as f:
    f.write("=== PANEL VERİ TEMEL MODELLER SONUÇ RAPORU ===\n\n")
    
    f.write("[1] HAUSMAN TESTİ SONUCU\n")
    if p_value is not None:
        f.write(f"Chi-Square Stat: {chi2_stat:.4f}\n")
        f.write(f"P-Value: {p_value:.4f}\n")
        if p_value < 0.05:
            f.write("Karar: P-Value < 0.05 olduğu için H0 (Random Effects Uygundur) reddedildi.\n")
            f.write("KAZANAN MODEL: FIXED EFFECTS (Sabit Etkiler)\n")
        else:
            f.write("Karar: P-Value > 0.05 olduğu için H0 reddedilemedi.\n")
            f.write("KAZANAN MODEL: RANDOM EFFECTS (Rassal Etkiler)\n")
    else:
        f.write("Hausman matrisi asimptotik olarak singular (tersinir değil).\n")

    f.write("\n\n" + "="*80 + "\n\n")
    f.write("[2] RANDOM EFFECTS (RASSAL ETKİLER) MODELİ\n")
    f.write("Not: Robust Standard Errors kullanılmıştır.\n")
    f.write(res_re.summary.as_text())

print("Faz 3 Başarıyla Tamamlandı. '5_baseline_models_results.txt' dosyası oluşturuldu.")
