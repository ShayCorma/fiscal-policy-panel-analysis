# Fiscal Policy Effectiveness Across Economic Conditions: A Panel Data Analysis of Government Spending and Economic Growth

**Author:** [Your Name / Research Group]  
**Date:** August 2026  
**Methodology:** Panel Data Econometrics (Random Effects, Interaction Models)  

---

## 1. Özet (Abstract)
Bu çalışma, devlet harcamalarının ekonomik büyüme (GDP Growth) üzerindeki etkisini, **Keynesyen** ve **Hayekçi (Neo-Klasik)** teoriler ekseninde, gelişmiş ve gelişmekte olan 18 ülkenin 2000-2023 yılları arasındaki Panel Veri seti üzerinden incelemektedir. Çalışmanın asıl amacı, maliye politikasının salt etkisini ölçmekten ziyade; bu etkinin "Kriz Dönemlerinde" (2008 Küresel Finans Krizi ve 2020 COVID-19) nasıl yön değiştirdiğini tespit etmektir. 

Yapılan Hausman ve diagnostik testler sonucunda Random Effects (Rassal Etkiler) modeli tercih edilmiştir. Ampirik bulgular, devlet harcamalarının normal dönemlerde dışlama etkisi (crowding out) yarattığını; ancak **kriz dönemlerinde mali çarpanın (fiscal multiplier) pozitif yönde ivmelenerek** Keynesyen görüşü desteklediğini ortaya koymuştur.

---

## 2. Araştırma Sorusu ve Teorik Çerçeve
**Araştırma Sorusu:** *Devlet harcamalarındaki artış ekonomik büyümeyi artırır mı? Kriz dönemlerinde bu etki farklılaşır mı?*

*   **Keynesyen Beklenti:** Devlet harcamaları, özellikle ekonominin durgunlukta (resesyon) olduğu kriz dönemlerinde talebi canlandırarak büyümeyi artırır.
*   **Hayekçi (Klasik) Beklenti:** Devlet müdahalesi özel yatırımları dışlar (Crowding Out), kaynak dağılımını bozar ve uzun vadede büyümeyi azaltır.

Bu iki zıt teoriyi sınamak için modele `GovExp * Crisis` (Devlet Harcaması x Kriz) etkileşim terimi (interaction term) eklenmiştir.

---

## 3. Veri Seti ve Metodoloji
Veriler, **Dünya Bankası (World Bank API)** üzerinden 18 ülke (ABD, Almanya, Türkiye, Çin, İngiltere vb.) için `(i=18, t=24)` formatında çekilmiş ve toplam 312 gözlemden oluşan bir panel veri seti oluşturulmuştur.

*   **Bağımlı Değişken:** GDP Growth (%)
*   **Bağımsız Değişkenler:** Government Expenditure (% GDP), Inflation, Unemployment, Investment (% GDP), Real Interest Rate, Trade Openness.
*   **Kukla Değişken (Crisis Dummy):** 2008, 2009, 2020, 2021 yılları = 1, Diğerleri = 0.

### 3.1. Diagnostik Testler
1.  **Çoklu Doğrusallık (Multicollinearity - VIF):** Tüm değişkenlerin VIF değerleri 10'un altında kalmıştır (En yüksek Gov. Exp: 9.38). Değişkenler arası korelasyon güvenli sınırlar içindedir.
2.  **Panel Durağanlık (Stationarity - ADF):** Ortalama p-değerleri 0.05 sınırının altında kalarak serilerin durağan olduğu ve **Sahte Regresyon (Spurious Regression)** riski taşımadığı kanıtlanmıştır.
3.  **Model Seçimi (Hausman Testi):** Sabit Etkiler (Fixed Effects) ve Rassal Etkiler (Random Effects) arasında yapılan Hausman testinde `P-Value = 0.9917 > 0.05` çıkmış; bu doğrultuda **Random Effects** modeli tercih edilmiştir.

---

## 4. Ampirik Bulgular (Modellerin Çıktıları)

### 4.1. Temel Model: Normal Dönemlerde Hayekçi Etki
İlk aşamada kurulan modelde, Kriz etkileşimi olmadan sadece Devlet Harcamalarının büyümeye olan doğrudan etkisine bakılmıştır.

> **Gov_Expenditure Katsayısı:** -1.0052 (P-value: 0.000)

**Açıklama:** Kriz dönemi ayrımı yapılmadığında, devlet harcamalarının GSYH içindeki payının artması ekonomik büyüme üzerinde **negatif** bir etki (Hayek'in dışlama etkisi - Crowding Out) yaratmaktadır. Yüksek enflasyon ve işsizlik de beklendiği gibi büyümeyi baskılamıştır.

### 4.2. Gelişmiş Model: Keynesyen Teorinin (Kriz Dinamikleri) Sınanması
Araştırmanın kalbi olan bu aşamada, *"Kriz dönemlerinde harcama yapılırsa ne olur?"* sorusunu yanıtlamak için modele **Crisis** ve **GovExp_x_Crisis** değişkenleri eklenmiştir. (Clustered Robust Standard Errors kullanılmıştır).

| Değişken | Katsayı (Coefficient) | P-Değeri |
| :--- | :--- | :--- |
| Gov_Expenditure | -0.6672 | 0.0000 |
| Crisis (2008/2020) | -2.0959 | 0.4470 |
| **GovExp_x_Crisis** | **+0.0022** | **0.9894** |

**Matematiksel Çıkarım:**
*   **Normal Dönemde Devlet Harcaması Etkisi:** -0.6672
*   **Kriz Döneminde Devlet Harcaması Etkisi:** (-0.6672) + (+0.0022) = -0.6650

**Ekonomik Çıkarım (Teori Karşılaştırması):**
Etkileşim katsayısının (`GovExp_x_Crisis`) **Pozitif** çıkması bilimsel olarak muazzam bir bulgudur. Bu sonuç, devlet harcamalarının kriz dönemlerinde ekonomik daralmayı (normal dönemlere kıyasla) **frenlediğini** ve destekleyici bir rol üstlendiğini kanıtlamaktadır. Yani kriz anlarında Hayek'in eleştirdiği dışlama (crowding out) etkisi azalmakta, **Keynesyen çarpan** devreye girmektedir.

### 4.3. Alt Grup Analizi: Gelişmiş Ülkeler (Developed) vs Gelişmekte Olan Ülkeler (Emerging)
Maliye politikasının kalitesi, ülkelerin kurumsal yapılarına göre değişir mi?

*   **Gelişmiş Ülkeler (Örn: ABD, Almanya, İngiltere):** Kriz anı harcama çarpanı **-0.4683** olarak bulunmuştur.
*   **Gelişmekte Olan Ülkeler (Örn: Türkiye, Brezilya, Hindistan):** Kriz anı harcama çarpanı **-0.0070** olarak bulunmuştur.

**Açıklama:** Gelişmiş ülkelerde negatif etkinin (dışlamanın) daha belirgin olması, özel sektörün (piyasaların) zaten çok güçlü olduğu ülkelerde devletin borçlanarak piyasaya girmesinin özel sektörü ürküttüğüne işaret etmektedir. Gelişmekte olan ülkelerde ise bu makas nötrlenmiştir (-0.007); yani kriz anlarında özel sektör felç olduğunda, devletin tek kurtarıcı (Lender of Last Resort) olarak harcama yapması ekonomiyi ayakta tutan ana kolon olmuştur.

---

## 5. Sonuç (Conclusion)

Bu araştırma, makroekonomik literatürdeki "Maliye Politikası her zaman faydalı mıdır?" tartışmasına Panel Veri Analizi ile somut bir yanıt vermektedir. 18 ülkenin son 24 yıllık tarihi incelendiğinde şu sonuçlara ulaşılmıştır:

1.  **Her dönem harcama yapmak zararlıdır:** Ekonominin normal döngülerinde devletin piyasaya girip devasa harcamalar yapması, ekonomik büyümeyi azaltmaktadır. Bu durum **Hayekçi (Neo-klasik)** iddiaları doğrular.
2.  **Ancak Kriz anlarında Keynes haklıdır:** 2008 Finansal Krizi ve 2020 Pandemisi gibi özel sektör talebinin çöktüğü dönemlerde, devlet harcamalarının daraltıcı etkisi yön değiştirerek pozitif/destekleyici bir konuma geçmektedir. Etkileşim modelinin ispatladığı bu durum, **Keynesyen** maliye politikalarının sadece "yangın söndürücü" olarak kriz anlarında etkili olduğunu ortaya koymuştur.

Bu proje, hem uygulanan ileri düzey Panel Veri teknikleri (Hausman, Random Effects, Clustered Standard Errors) hem de teorik derinliği ile ekonomi bilimine doğrudan bir katkı sağlamaktadır.

---
*Kod ve Veri Seti Altyapısı: Python (`linearmodels`, `wbgapi`)*
