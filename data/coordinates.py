import pandas as pd

# 1 Başlangıç/Bitiş Noktası (Depo) + 10 Gölet (Toplam 11 Durak)
ANKARA_LOCATIONS = {
    "Start/End Point (Depo)": "Çevre ve Şehircilik Bakanlığı, Söğütözü/Ankara",
    "Mogan Gölü": "Mogan Gölü, Gölbaşı/Ankara",
    "Eymir Gölü": "Eymir Gölü, Ankara",
    "Gölbaşı Kent Gölü": "Gölbaşı Kent Gölü, Ankara",
    "Kızılcahamam Soğuksu Milli Parkı": "Kızılcahamam Soğuksu Milli Parkı, Ankara",
    "Çubuk 2 Barajı": "Çubuk 2 Barajı, Ankara",
    "Karagöl (Çubuk)": "Karagöl, Çubuk/Ankara",
    "Bayındır Barajı": "Bayındır Barajı, Mamak/Ankara",
    "Çamlıdere Barajı": "Çamlıdere Barajı, Ankara",
    "Kesikköprü Barajı": "Kesikköprü Barajı, Kırşehir-Ankara yolu",
    "Beytepe Göleti": "Beytepe Göleti, Çankaya/Ankara"
}

LOCATION_NAMES = list(ANKARA_LOCATIONS.keys())

def get_location_df():
    return pd.DataFrame(
        list(ANKARA_LOCATIONS.items()),
        columns=['Name', 'Address']
    )
