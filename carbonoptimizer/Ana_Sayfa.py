import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ✅ Önce df_all'u her durumda tanımlıyoruz
df_all = None  # Eğer CSV okunmazsa bile bu tanımlı kalır
# Ortalama değerler her durumda tanımlanır (blok dışına çıkmalı!)
avg_beef = 0.0
avg_chicken = 0.0
avg_elec = 0.0
avg_car = 0.0

# ------------------ YARDIMCI FONKSİYONLAR ------------------
def calculate_emission(data, factors):
    beef_emission = data.get("beef", 0) * factors.get("beef", 0)
    chicken_emission = data.get("chicken", 0) * factors.get("chicken", 0)
    electricity_emission = data.get("electricity", 0) * factors.get("electricity", 0)
    car_emission = factors.get("car", {}).get(data.get("car", ""), 0) * data.get("car_distance", 0)

    total = beef_emission + chicken_emission + electricity_emission + car_emission
    details = {
        "Dana Eti": beef_emission,
        "Tavuk Eti": chicken_emission,
        "Elektrik": electricity_emission,
        "Araç": car_emission
    }
    return total, details


def log_to_csv(data, emission, filename="veri_kayit.csv"):
    import os
    row = data.copy()
    row["total_emission"] = emission
    df_row = pd.DataFrame([row])
    os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
    if os.path.exists(filename):
        df_hist = pd.read_csv(filename)
        df_hist = pd.concat([df_hist, df_row], ignore_index=True)
    else:
        df_hist = df_row
    df_hist.to_csv(filename, index=False)

# ------------------ SAYFA AYARLARI ------------------
st.set_page_config(page_title="Karbon Ayak İzi", layout="wide", page_icon="🌍")

# Genel stil
st.markdown("""
<style>
body {background-color: #0f0f0f; color: white;}
.card-container {display: flex; justify-content: space-between; margin-top: 20px;}
.card {flex: 1; background-color: #1b1b1b; padding: 16px; border-radius: 12px; margin: 0 8px;
       box-shadow: 0 0 8px rgba(57,255,20,0.3); text-align: center; border: 1px solid rgba(57,255,20,0.2);}
.card h4 {color: #bbbbbb; margin-bottom: 4px; font-size: 16px;}
.card p {color: #39ff14; font-size: 20px; font-weight: bold; margin: 0;}
</style>
""", unsafe_allow_html=True)


# Başlık
st.markdown("""
<style>
.custom-title {
    font-size: 22px;
    font-weight: 600;
    color: #00ff88;
    text-align: center;
    margin-bottom: 4px;
    font-family: 'Segoe UI', sans-serif;
}

.custom-subtitle {
    font-size: 14px;
    color: #ccc;
    text-align: center;
    margin-bottom: 16px;
    font-family: 'Segoe UI', sans-serif;
}
</style>

<div class="custom-title">🌱 Karbon Ayak İzi Paneli</div>
<div class="custom-subtitle">Günlük tüketim alışkanlıklarını gir, emisyon değerini öğren!</div>
""", unsafe_allow_html=True)

 

# ------------------ SIDEBAR GİRİŞ FORMU ------------------
st.sidebar.header("🔍 Girdi Bilgileri")
with st.sidebar.form(key='emission_form'):
    city = st.selectbox("Şehir", ["Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara",
    "Antalya", "Ardahan", "Artvin", "Aydın", "Balıkesir", "Bartın", "Batman",
    "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale",
    "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan",
    "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkâri", "Hatay",
    "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman",
    "Kars", "Kastamonu", "Kayseri", "Kilis", "Kırıkkale", "Kırklareli", "Kırşehir",
    "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla",
    "Muş", "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun",
    "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ", "Tokat", "Trabzon",
    "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"])
    beef = st.number_input("Dana eti tüketimi (kg)", min_value=0, step=1)
    chicken = st.number_input("Tavuk eti tüketimi (kg)", min_value=0, step=1)
    electricity = st.number_input("Elektrik tüketimi (kWh)", min_value=0, step=1)
    car = st.selectbox("Araç tipi", ["Yok", "Benzin", "Dizel", "Elektrik"])
    car_distance = st.number_input("Araç mesafesi (km)", min_value=0, step=1)
    
    submit = st.form_submit_button("💨 Hesapla")

# Emisyon faktörleri
emission_factors = {
    "beef": 27.0,
    "chicken": 6.9,
    "electricity": 0.4,
    "car": {"Yok": 0.0, "Benzin": 0.021, "Dizel": 0.025, "Elektrik": 0.012}
}

# ------------------ ÖNCEKİ VERİYİ YÜKLE ------------------
if "results" not in st.session_state:
    try:
        df_hist = pd.read_csv("veri_kayit.csv")
        if not df_hist.empty:
            last = df_hist.iloc[-1].to_dict()
            st.session_state["results"] = {
                "input": {
                    "beef": last.get("beef", 0),
                    "chicken": last.get("chicken", 0),
                    "electricity": last.get("electricity", 0),
                    "car": last.get("car", "Yok"),
                    "car_distance": last.get("car_distance", 0),
                    "city": last.get("city", "")
                },
                "total_emission": last.get("total_emission", 0),
                "details": None
            }
    except FileNotFoundError:
        pass

# ------------------ HESAPLAMA ------------------
if submit:
    input_data = {"beef": beef, "chicken": chicken, "electricity": electricity,"car": car, "car_distance": car_distance, "city": city}
    total_emission, details = calculate_emission(input_data, emission_factors)
    log_to_csv(input_data, total_emission)
    

    input_data = {"beef": beef,"chicken": chicken,"electricity": electricity,"car": car,"car_distance": car_distance,"city": city}
    total_emission, emission_details = calculate_emission(input_data, emission_factors)
    st.session_state["results"] = {"input": input_data,"total_emission": total_emission,"details": details}
    
st.markdown("""
<div style="height: 3px; border-radius: 3px; background: linear-gradient(to right, #00ffcc, #00ffaa, #00ffcc); margin: 30px 0;"></div>
""", unsafe_allow_html=True)

# ------------------ KARTLAR ------------------

vg_beef = avg_chicken = avg_elec = avg_car = 0.0

# Sonuçlar varsa işlemleri başlat
if "results" in st.session_state:
    res = st.session_state["results"]
    inp = res["input"]
    total_emission = res["total_emission"]
    details = res.get("details", {})

    # Dosya varsa ortalamaları oku
    if os.path.exists("veri_kayit.csv"):
        try:
            df_all = pd.read_csv("veri_kayit.csv")
            if not df_all.empty:
                avg_beef = df_all["beef"].mean()
                avg_chicken = df_all["chicken"].mean()
                avg_elec = df_all["electricity"].mean()
                avg_car = df_all["car_distance"].mean()
        except Exception as e:
            st.info("ℹ️ Okunacak veri henüz girilmedi.")

    # Stil tanımı
    st.markdown("""
    <style>
    .card-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 10px;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .card {
        flex: 1;
        min-width: 120px;
        background: #111;
        border: 1px solid #00ff88;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 6px #00ff88;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    .card h4 {
        font-size: 14px;
        margin-bottom: 6px;
        color: #00ff88;
    }
    .card p {
        font-size: 16px;
        font-weight: bold;
        color: white;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Ortalama değer kartları
    st.markdown(f"""
    <div class="card-container">
        <div class="card"><h4>🥩 Ort. Dana Eti (kg)</h4><p>{avg_beef:.2f}</p></div>
        <div class="card"><h4>🍗 Ort. Tavuk Eti (kg)</h4><p>{avg_chicken:.2f}</p></div>
        <div class="card"><h4>⚡ Ort. Elektrik (kWh)</h4><p>{avg_elec:.2f}</p></div>
        <div class="card"><h4>🚗 Ort. Araç (km)</h4><p>{avg_car:.2f}</p></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; margin: 30px 0;">
    <span style="font-size: 20px; color: #4ED7F1;">━ ✦ ━</span>
</div>
""", unsafe_allow_html=True)

    # Sonuç kartları
# Model tahmini hesapla
if "results" in st.session_state:
    inp = st.session_state["results"]["input"]
    
    # float'a çevirerek hata önleme
    try:
        total_emission = float(st.session_state["results"]["total_emission"])
        electricity = float(inp.get("electricity", 0))
        beef = float(inp.get("beef", 0))

        prediction = electricity * 0.35 + beef * 25
        fark = abs(total_emission - prediction)

        st.markdown(f"""
        <div class="card-container">
            <div class="card"><h4>🌍 Toplam Emisyon</h4><p>{total_emission:.2f} kg CO₂</p></div>
            <div class="card"><h4>🤖 Model Tahmini</h4><p>{prediction:.2f} kg CO₂</p></div>
            <div class="card"><h4>⚖️ Fark</h4><p>{fark:.2f} kg CO₂</p></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
<div style="height: 1px; background-color: #129990; margin: 25px 0;"></div>
""", unsafe_allow_html=True)


    except Exception as e:
        st.error(f"🔴 Hata oluştu: {e}")

else:
    st.info("ℹ️ Henüz emisyon hesaplaması yapılmadı. Lütfen formu doldurun.")



    # Grafikler: ortalama dağılım ve zaman serisi (en altta)
try:
    if 'df_all' in locals() and df_all is not None and not df_all.empty:
        pie_col, line_col = st.columns(2)
        categories = ["Dana Eti", "Tavuk Eti", "Elektrik", "Araç"]
        values = [avg_beef, avg_chicken, avg_elec, avg_car]

        with pie_col:
            st.subheader("Aylık Ortalama Dağılım")
            fig_pie = px.pie(
                names=categories,
                values=values,
                hole=0.4
            )
            fig_pie.update_layout(
                height=300,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with line_col:
            st.subheader("Toplam Emisyonlar")
            df_ts = df_all.copy()

            fig_line = px.line(
                df_ts,
                x=df_ts.index,
                y="total_emission",
                markers=True,
                labels={"index": "Kayıt #", "total_emission": "Toplam Emisyon (kg CO₂)"},
            )
            fig_line.update_layout(
                height=300,
                margin=dict(t=10, b=10, l=10, r=10)
            )
            st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Henüz gösterilecek grafik verisi yok.", icon="ℹ️")

except Exception as e:
    st.error(f"Hata oluştu: {e}")



    st.markdown("""
<div style="height: 2px; background: linear-gradient(to right, #00ff88, #00ffaa); border: none; margin: 20px 0;"></div>
""", unsafe_allow_html=True)


def generate_advice(emissions):
    advice = []
    if emissions.get('Dana Eti', 0) > 5:
        advice.append(f"🥩 Dana eti tüketiminiz yüksek ({emissions['Dana Eti']:.1f} kg CO₂). Bitkisel protein kaynaklarını daha fazla tercih edin.")   
    if emissions.get('Tavuk Eti', 0) > 4:
        advice.append(f"🍗 Tavuk tüketiminiz fazla ({emissions['Tavuk Eti']:.1f} kg CO₂). Haftalık miktarı azaltmayı düşünebilirsiniz.")
    if emissions.get('Araç', 0) > 3:
        advice.append(f"🚗 Araç kullanımınızdan kaynaklı emisyon ({emissions['Araç']:.1f} kg CO₂) yüksek. Toplu taşıma veya bisiklet gibi alternatifleri değerlendirin.")
    if emissions.get('Elektrik', 0) > 20:
        advice.append(f"💡 Elektrik tüketiminiz ({emissions['Elektrik']:.1f} kg CO₂) fazla. Enerji tasarruflu cihazlar ve ampuller kullanın.")
    if not advice:
        advice.append("🌱 Harika! Karbon ayak izinizi düşük seviyede tutuyorsunuz. Böyle devam edin!")
    return advice


def senaryo_simulasyon(input_data, base_total, emission_factors):
    st.subheader("🔍 Senaryo Simülasyonu")

    senaryolar = {
        "🥩 Dana eti tüketimini %50 azaltırsanız": ("beef", 0.5),
        "🍗 Tavuk eti tüketimini %30 azaltırsanız": ("chicken", 0.7),
        "🚗 Araç mesafenizi %40 azaltırsanız": ("car_distance", 0.6),
        "💡 Elektrik kullanımınızı %25 azaltırsanız": ("electricity", 0.75),
    }

    for aciklama, (key, carpim_orani) in senaryolar.items():
        yeni_girdi = input_data.copy()
        yeni_girdi[key] = input_data.get(key, 0) * carpim_orani
        yeni_toplam, _ = calculate_emission(yeni_girdi, emission_factors)
        fark = base_total - yeni_toplam
        st.info(f"{aciklama}, toplam karbon emisyonunuz yaklaşık **{fark:.2f} kg CO₂** azalır.")

# ------------------ SUBMIT İŞLEMİ ------------------

        st.markdown("<hr style='border: 2px solid #1DB954;'>", unsafe_allow_html=True)
  
    
    # CSV’ye kaydet
    log_to_csv(input_data, total_emission)
    
    # Önerileri üret ve session_state’e kaydet
    advice_list = generate_advice(emission_details)
    
    st.session_state["results"] = {
        "input": input_data,
        "total_emission": total_emission,
        "details": emission_details
    }
    st.session_state["advice"] = advice_list

# ------------------ ÖNERİLERİ GÖSTER ------------------
if submit:
    input_data = {
        "beef": beef,
        "chicken": chicken,
        "electricity": electricity,
        "car": car,
        "car_distance": car_distance,
        "city": city
    }

    # Emisyonları hesapla
    total_emission, emission_details = calculate_emission(input_data, emission_factors)

    # Önerileri üret
    advice_list = generate_advice(emission_details)

    # Önerileri session_state'e kaydet
    st.session_state["advice"] = advice_list

# Öneriler varsa göster
if "advice" in st.session_state:
    st.subheader("📌 Kişiselleştirilmiş Önerileriniz:")
    for item in st.session_state["advice"]:
        st.success(item)

            


# ------------------ SENARYO SİMÜLASYONU (YENİ DÜZENLENMİŞ) ------------------
def senaryo_simulasyon(input_data, total_emission, emission_factors):
    st.subheader("🔍 Simülasyonlar (Senaryo Tabanlı Öngörüler)")

    col1, col2, col3, col4 = st.columns(4)

    # input_data'daki sayısal değerleri float'a çevir (güvenlik için)
    beef = float(input_data.get("beef", 0) or 0)
    chicken = float(input_data.get("chicken", 0) or 0)
    electricity = float(input_data.get("electricity", 0) or 0)
    car = input_data.get("car", "Yok")

    total_emission = float(total_emission or 0)

    # Dana eti %50 azaltma senaryosu
    with col1:
        yeni_girdi = input_data.copy()
        yeni_girdi["beef"] = beef * 0.5
        yeni_toplam, _ = calculate_emission(yeni_girdi, emission_factors)
        fark = total_emission - yeni_toplam
        st.info(f"""🥩 **Dana eti tüketimini %50 azaltsaydınız**
                    
Yeni tahmini emisyon: **{yeni_toplam:.2f} kg CO₂**  
Tasarruf edilen miktar: **{fark:.2f} kg CO₂**
""", icon="🌿")

    # Tavuk eti %30 azaltma senaryosu
    with col2:
        yeni_girdi = input_data.copy()
        yeni_girdi["chicken"] = chicken * 0.7
        yeni_toplam, _ = calculate_emission(yeni_girdi, emission_factors)
        fark = total_emission - yeni_toplam
        st.info(f"""🍗 **Tavuk eti tüketimini %30 azaltsaydınız**
                    
Yeni tahmini emisyon: **{yeni_toplam:.2f} kg CO₂**  
Tasarruf edilen miktar: **{fark:.2f} kg CO₂**
""", icon="🐔")

    # Elektrik %30 azaltma senaryosu
    with col3:
        yeni_girdi = input_data.copy()
        yeni_girdi["electricity"] = electricity * 0.7
        yeni_toplam, _ = calculate_emission(yeni_girdi, emission_factors)
        fark = total_emission - yeni_toplam
        st.info(f"""💡 **Elektrik tüketiminiz %30 az olsaydı**
                    
Yeni tahmini emisyon: **{yeni_toplam:.2f} kg CO₂**  
Tasarruf edilen miktar: **{fark:.2f} kg CO₂**
""", icon="⚡")

    # Araba yerine toplu taşıma
    with col4:
        yeni_girdi = input_data.copy()
        yeni_girdi["car"] = "Yok"
        yeni_toplam, _ = calculate_emission(yeni_girdi, emission_factors)
        fark = total_emission - yeni_toplam
        st.info(f"""🚇 **Araç yerine toplu taşıma kullansaydınız**
                    
Yeni tahmini emisyon: **{yeni_toplam:.2f} kg CO₂**  
Tasarruf edilen miktar: **{fark:.2f} kg CO₂**
""", icon="🚉")


# ------------------ SENARYO SİMÜLASYONU ÇAĞRISI ------------------
if "results" in st.session_state:
    res = st.session_state["results"]
    input_data = res.get("input", {})
    total_emission = res.get("total_emission", 0)
    senaryo_simulasyon(input_data, total_emission, emission_factors)

st.markdown("<hr style='border: 2px solid #1DB954;'>", unsafe_allow_html=True)

import pandas as pd
import os
from datetime import datetime
import csv
import streamlit as st

#st.subheader("📊 Kullanıcı Girdi Geçmişi (Veri Seti)")

#log_file = "veri_kayit.csv"

# Eğer dosya varsa oku ve işle
#if os.path.exists(log_file):
 #   df_log = pd.read_csv(log_file)

    # Tarih sütununu datetime olarak ayarla
  #  df_log["timestamp"] = pd.to_datetime(df_log["timestamp"])

    # Tarihe göre ters sırala (son veri en üstte)
   # df_log.sort_values(by="timestamp", ascending=False, inplace=True)

    # Sütun adlarını daha okunabilir hale getir
    #df_log.rename(columns={
     #   "beef": "Dana Eti (kg)",
      #  "chicken": "Tavuk Eti (kg)",
       # "electricity": "Elektrik (kWh)",
       #  "car": "Araç Türü",
       #  "car_distance": "Araç Mesafesi (km)",
       #  "city": "Şehir",
       #  "total_emission": "Toplam Emisyon (kg CO2e)",
      #   "timestamp": "Tarih",
    # }, inplace=True)

    # st.dataframe(df_log, use_container_width=True)
# else:
    # st.info("Henüz veri kaydı yapılmamış.")

#import pandas as pd
#import os
#from datetime import datetime

# def log_to_csv(input_data, total_emission):
   #  log_file = "veri_kayit_yeni_duzenli.csv"

    # Yeni veri oluştur
   #  input_data["total_emission"] = total_emission
   #  input_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   #  new_row = pd.DataFrame([input_data])

    # if os.path.exists(log_file):
      #   df = pd.read_csv(log_file)
      #   df = pd.concat([df, new_row], ignore_index=True)
    # else:
       #  df = new_row

    # Artık index sütunu eklemiyoruz
    # df.to_csv(log_file, index=False)


