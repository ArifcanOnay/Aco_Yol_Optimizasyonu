import streamlit as st
import pandas as pd
import os

# Projenin diğer modüllerini içeri aktarma
from data.coordinates import get_location_df, LOCATION_NAMES
from core.matrix_utils import get_distance_matrix, get_coordinates
from core.ant_algorithm import ACOptimizer
from visual.plotting import plot_route_convergence, plot_optimized_route
from config import ACO_PARAMS as PARAMETRELER # ACO parametrelerini daha doğal bir isimle alıyoruz

# --- Sayfa Yapılandırması ve Başlık ---
st.set_page_config(page_title="Gerçek Yol Optimizasyonu (ACO)", layout="wide")
st.title("💧 Çevre Bakanlığı: Gölet Numunesi Toplama Rotası Optimizasyonu")
st.markdown("---")

# 1. API Anahtarını Çekme
try:
    API_ANAHTARI = st.secrets["google"]["api_key"]
except KeyError:
    st.error("🚨 Hata: Google Maps API anahtarı `secrets.toml` dosyasında bulunamıyor.")
    st.stop()

konumlar_df = get_location_df()

@st.cache_data
def veri_hazirla_ve_matris_olustur(_konumlar_df, _anahtar):
    """Konum verilerini, koordinatları ve gerçek sürüş mesafesi matrisini hesaplar."""
    with st.spinner("Google Maps API bağlantısı kuruluyor ve matrisler hesaplanıyor..."):
        # Adreslerden koordinatları al
        koordinatli_df = get_coordinates(_konumlar_df, _anahtar)
        # Koordinatlardan gerçek sürüş mesafesi matrisini (KM) al
        mesafe_matrisi = get_distance_matrix(koordinatli_df, _anahtar)
    return koordinatli_df, mesafe_matrisi

st.subheader("1. Proje Konumları ve Veri Yükleme")
st.dataframe(konumlar_df, hide_index=True)

if st.button("Gerçek Dünya Verilerini Yükle"):
    koordinatlar_df, mesafe_matrisi = veri_hazirla_ve_matris_olustur(konumlar_df, API_ANAHTARI)

    if mesafe_matrisi is not None:
        st.session_state['koordinatlar_df'] = koordinatlar_df
        st.session_state['mesafe_matrisi'] = mesafe_matrisi
        st.success("✅ Gerçek Mesafeler başarıyla yüklendi!")

        st.subheader("Konumların Coğrafi Dağılımı")
        # Basit Streamlit haritasında gösterim
        st.map(koordinatlar_df[['latitude', 'longitude']], zoom=8)
    else:
        st.error("API'den veri alınırken hata oluştu. Anahtar veya API kotasını kontrol edin.")


# --- 2. Optimizasyon Bölümü ---
if 'mesafe_matrisi' in st.session_state:
    st.subheader("2. Karınca Kolonisi Optimizasyonunu Başlat")

    with st.sidebar:
        st.header("ACO Algoritması Ayarları")

        # PARAMETRELER (config.py'den gelen) kullanılıyor
        ayarlar = {
            "num_ants": st.slider("Karınca Sayısı", 1, 50, PARAMETRELER['num_ants']),
            "num_iterations": st.slider("İterasyon Sayısı", 10, 500, PARAMETRELER['num_iterations']),
            "rho": st.slider("Buharlaşma Oranı (ρ)", 0.01, 0.99, PARAMETRELER['rho'], 0.01),
            "alpha": st.slider("Feromonun Etkisi (α)", 0.0, 5.0, PARAMETRELER['alpha'], 0.1),
            "beta": st.slider("Mesafe Çekiciliği (β)", 0.0, 10.0, PARAMETRELER['beta'], 0.1),
            "Q": st.number_input("Feromon Güç Sabiti (Q)", 10, 1000, PARAMETRELER['Q'])
        }

    if st.button("En Kısa Rotayı Hesapla", key="run_aco"):
        mesafe_matrisi = st.session_state['mesafe_matrisi']
        koordinatlar_df = st.session_state['koordinatlar_df']

        optimizer = ACOptimizer(mesafe_matrisi)
        optimizer.P.update(ayarlar) # Güncel ayarları algoritmaya geçir

        with st.spinner(f"{ayarlar['num_iterations']} döngüde optimizasyon yapılıyor..."):
            en_iyi_rota_indeksleri, en_kisa_mesafe, gecmis = optimizer.run()

        optimize_edilmis_isimler = [LOCATION_NAMES[i] for i in en_iyi_rota_indeksleri]

        st.success("✨ Optimizasyon Tamamlandı!")
        st.metric(label="En Kısa Toplam Sürüş Mesafesi", value=f"{en_kisa_mesafe:.2f} KM")

        st.subheader("3. Optimize Edilmiş Ziyaret Sırası")
        rota_gosterimi = [f"**({i})** {isim}" for i, isim in enumerate(optimize_edilmis_isimler)]
        st.markdown(f"**Rota Sırası:** {' -> '.join(rota_gosterimi)}")

        # 4. Görselleştirme
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("4. Yakınsama Analizi")
            yakinsama_yolu = plot_route_convergence(gecmis)
            st.image(yakinsama_yolu, caption='Algoritmanın en iyi mesafeye ulaşma grafiği')

        with col2:
            st.subheader("5. Rota Görselleştirmesi")
            rota_yolu = plot_optimized_route(koordinatlar_df, en_iyi_rota_indeksleri)
            st.image(rota_yolu, caption='Bulunan en kısa rotanın konumsal gösterimi')
