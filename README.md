# Fiscal Policy Effectiveness Across Economic Conditions: A Panel Data Analysis of Government Spending and Economic Growth

**Author:** [Your Name / Research Group]  
**Date:** August 2026  
**Methodology:** Panel Data Econometrics (Random Effects, Interaction Models)  

---

## 1. Özet (Abstract)
Bu çalışma, devlet harcamalarının ekonomik büyüme (GDP Growth) üzerindeki etkisini gelişmiş ve gelişmekte olan 18 ülkenin 2000-2023 yılları arasındaki Panel Veri seti üzerinden incelemektedir. Çalışmanın odak noktası, maliye politikasının ekonomik büyüme üzerindeki genel etkisini ve bu etkinin 2008 Küresel Finans Krizi ile 2020 COVID-19 Pandemisi gibi kriz dönemlerinde farklılaşıp farklılaşmadığını ampirik olarak test etmektir. 

Uygulanan diagnostik testler ve Hausman testi sonucunda Random Effects (Rassal Etkiler) modeli tercih edilmiştir. Ampirik bulgular, incelenen örneklemde devlet harcamalarındaki artışın ekonomik büyüme üzerinde istatistiksel olarak anlamlı ve negatif yönde bir etkiye sahip olduğunu göstermektedir. Öte yandan, kriz dönemlerinde bu etkinin farklılaştığını (Keynesyen çarpanın devreye girdiğini) öngören hipotez, kriz etkileşim teriminin istatistiksel olarak anlamsız (p > 0.05) çıkması nedeniyle mevcut veri seti kapsamında desteklenememiştir.

---

## 2. Araştırma Sorusu ve Teorik Çerçeve
**Araştırma Sorusu:** *Devlet harcamalarındaki artış ekonomik büyümeyi artırır mı? Kriz dönemlerinde bu ilişki farklılaşır mı?*

Bu sorular, literatürde iki temel makroekonomik yaklaşım ekseninde tartışılmaktadır:
*   **Keynesyen Yaklaşım:** Devlet harcamaları, özellikle ekonominin durgunlukta (resesyon) olduğu dönemlerde toplam talebi canlandırarak büyümeyi destekler.
*   **Klasik / Yeni Klasik Yaklaşım (Dışlama Etkisi):** Devletin piyasaya müdahalesi ve borçlanması faiz oranlarını artırarak özel sektör yatırımlarını dışlar (Crowding Out). Bu durum uzun vadede büyümeyi baskılayabilir.

Bu yaklaşımları sınamak amacıyla modele `GovExp * Crisis` etkileşim terimi dahil edilmiştir.

---

## 3. Veri Seti ve Metodoloji
Veriler, Dünya Bankası veri tabanından 18 ülke için `(i=18, t=24)` formatında çekilmiş ve 312 gözlemden oluşan bir panel veri seti kullanılmıştır.

*   **Bağımlı Değişken:** GDP Growth (%)
*   **Bağımsız Değişkenler:** Government Expenditure (% GDP), Inflation, Unemployment, Investment (% GDP), Real Interest Rate, Trade Openness.
*   **Kriz Kuklası (Crisis Dummy):** 2008, 2009, 2020, 2021 yılları = 1, Diğerleri = 0.

### 3.1. Diagnostik Testler
1.  **Çoklu Doğrusallık (VIF):** Tüm bağımsız değişkenlerin VIF değerleri sınır değer olan 10'un altında (maksimum 9.38) kalmıştır.
2.  **Panel Durağanlık (Stationarity - ADF):** Ortalama p-değerleri 0.05'in altında hesaplanarak serilerin durağan olduğu saptanmıştır.
3.  **Model Seçimi:** Sabit Etkiler ve Rassal Etkiler tahmincileri arasındaki Hausman testinde `P-Value = 0.9917 > 0.05` bulunmuş ve analizlere Random Effects ile devam edilmiştir. Analizlerde dirençli (robust) standart hatalar kullanılmıştır.

---

## 4. Ampirik Bulgular

### 4.1. Kriz Etkileşim Modeli (Tam Örneklem)
Kriz dönemlerindeki ayrışmayı test eden genişletilmiş modelin temel katsayıları şu şekildedir:

| Değişken | Katsayı (Coefficient) | P-Değeri (P-Value) | Anlamlılık |
| :--- | :--- | :--- | :--- |
| Gov_Expenditure | -0.6672 | 0.0000 | İstatistiksel olarak %1 düzeyinde anlamlı |
| Crisis (2008/2020) | -2.0959 | 0.4470 | Anlamsız |
| **GovExp_x_Crisis** | **+0.0022** | **0.9894** | **İstatistiksel olarak anlamsız** |

**Ampirik Çıkarımlar:**
1.  **Devlet Harcamalarının Genel Etkisi:** `Gov_Expenditure` değişkeninin katsayısı negatif (-0.6672) ve istatistiksel olarak son derece anlamlıdır (p = 0.0000). Elde edilen bu bulgu, incelenen örneklemde devlet harcamalarının büyüme üzerindeki etkisinin negatif yönlü olduğunu göstermektedir. Bu sonuç, devlet harcamalarının özel sektörü dışladığını öne süren Hayekçi (Klasik) yaklaşımla uyumlu olarak yorumlanabilir.
2.  **Kriz Dönemleri Dinamiği (Etkileşim Terimi):** Etkileşim katsayısı (+0.0022) matematiksel olarak pozitif görünse de, **p-değeri (0.9894) oldukça yüksektir.** Bu durum, etkileşim katsayısının istatistiksel olarak sıfırdan farklı olduğuna dair ampirik bir kanıt bulunmadığı anlamına gelir. Dolayısıyla, mevcut model ve veri seti altında, devlet harcamalarının kriz dönemlerinde normal dönemlere kıyasla daha farklı (veya daha faydalı) bir etki yarattığına dair anlamlı bir kanıt bulunamamıştır.

### 4.2. Alt Grup İncelemesi: Gelişmiş vs. Gelişmekte Olan Ülkeler
Veri seti, Gelişmiş (Developed) ve Gelişmekte Olan (Emerging) ülkeler olarak ikiye ayrıldığında:
*   Gelişmiş ülkelerde devlet harcamalarının negatif etkisi (`-0.3296`, `p=0.000`) istatistiksel olarak varlığını korumuştur.
*   Gelişmekte olan ülkelerde ise devlet harcamaları katsayısı (`-0.0277`, `p=0.8087`) istatistiksel olarak anlamsızlaşmıştır.
*   Her iki grupta da kriz etkileşim terimleri (GovExp_x_Crisis) istatistiksel olarak anlamsız (`p > 0.10`) bulunmuştur.

---

## 5. Sonuç (Conclusion)

Bu çalışma, 18 ülkeyi kapsayan 2000-2023 dönemine ait panel veri seti üzerinden, maliye politikası ile ekonomik büyüme arasındaki ilişkiye dair ampirik bulgular sunmaktadır.

Uygulanan ekonometrik modeller neticesinde, analiz edilen dönem ve ülke örneklemi özelinde devlet harcamalarındaki artışın ekonomik büyüme ile istatistiksel olarak anlamlı ve negatif bir ilişki içinde olduğu saptanmıştır. Bu bulgu, mali genişlemenin dışlama etkisi (crowding out) yaratabileceğini savunan klasik ekol beklentileriyle tutarlıdır.

Öte yandan çalışmanın temel motivasyonlarından biri olan "kriz dönemlerinde devlet müdahalesinin ekonomik daralmayı engelleyici bir rol oynadığı (Keynesyen çarpan)" hipotezi test edilmiştir. Kriz yıllarını temsil eden kukla değişken ile harcamaların etkileşim terimi incelendiğinde, bu iki dönem arasında istatistiksel olarak anlamlı bir farklılaşma tespit edilememiştir. Bir başka deyişle, devlet harcamalarının büyüme üzerindeki negatif yönlü ilişkisinin kriz dönemlerinde yapısal bir kırılmaya uğradığını destekleyecek yeterli ampirik kanıt bulunamamıştır.

Gelecek çalışmalarda harcamaların kompozisyonu (cari harcamalar vs. yatırım harcamaları) veya farklı enstrümanlarla (Araç Değişken / GMM) yapılacak modeller, bu dinamiklerin daha net ayrıştırılmasına olanak tanıyabilir.
