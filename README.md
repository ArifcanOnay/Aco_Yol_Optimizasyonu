# ACO Tabanlı Yol Optimizasyonu Projesi (Yapay Zeka Dersi Ödevi)

## 1. Proje Hakkında

Bu proje, Karınca Kolonisi Optimizasyonu (ACO) algoritmasını kullanarak belirli noktalar arasındaki en kısa rotayı bulmayı amaçlar.

**Problem:** Ankara'da bulunan 10 farklı göletten su numunesi toplanması için gerekli olan en kısa rotayı hesapladık.

### Kullanılan Ana Teknolojiler

* **Algoritma:** Karınca Kolonisi Optimizasyonu (ACO).
* **Mesafe Verisi:** Google Maps Distance Matrix API'den alınan **gerçek sürüş mesafeleri** kullanılmıştır.
* **Arayüz:** Streamlit ile basit bir web uygulaması oluşturulmuştur.

## 2. Proje Yapısı ve Dosyalar

Hocamızın istediği dosyalama yapısına uygun olarak düzenlenmiştir.

* `main.py`: Streamlit uygulamasının başladığı ana dosya.
* `config.py`: ACO'nun karınca sayısı, iterasyon ve feromon ($\alpha$, $\beta$) gibi parametrelerinin ayarlandığı yer.
* `core/`: Algoritmanın çekirdek kodları burada bulunur. (`ant_algorithm.py`, `matrix_utils.py` vb.)
* `data/`: Şehir koordinatları gibi başlangıç verilerinin bulunduğu klasör.
* `visual/`: Sonuçların harita ve grafiklerle gösterildiği dosyalar.
* `.streamlit/`: API anahtarının gizlendiği klasör.

## 3. Çalıştırma Notları

1.  Gerekli kütüphaneleri `pip install` ile yükleyin (Streamlit, Googlemaps vb.).
2.  Google Maps API anahtarınızı `.streamlit/secrets.toml` dosyasına kaydedin. (Bu dosya güvenlik nedeniyle repoya yüklenmemiştir.)
3.  Uygulamayı başlatmak için: `streamlit run main.py`

## 4. Algoritma Hakkında

ACO, karıncaların yiyecek ararken bıraktığı feromon izlerini taklit eder. Daha kısa yollar daha çok feromonla güçlendirilir. Algoritma bu feromon yoğunluğunu kullanarak en optimum rotayı bulur.
