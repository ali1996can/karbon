import streamlit as st

st.set_page_config(page_title="Karbon Ayak İzi Bilgilendirme", layout="wide")

st.markdown("<h2 style='color:#00FFAA;'>🌍 Karbon Ayak İzi Bilgilendirme</h2>", unsafe_allow_html=True)

# Giriş paragrafı
st.markdown("""
Karbon ayak izi, **bir kişinin veya kuruluşun doğrudan ve dolaylı olarak atmosfere saldığı toplam sera gazı miktarıdır**.  
Bu emisyonlar genellikle **kilogram veya ton cinsinden CO₂ eşdeğeri** ile ifade edilir.
""")

# Bölüm: Neden Önemlidir?
with st.expander("📌 Karbon Ayak İzi Neden Önemlidir?"):
    st.write("""
    Karbon ayak izimizi anlamak, küresel ısınma ve iklim değişikliğiyle mücadelede ilk adımdır. 
    Günlük yaşamımızdaki pek çok faaliyet – ulaşım, beslenme, enerji kullanımı – karbon salımına neden olur.
    
    **Önemli Noktalar:**
    - Daha az et tüketimi = Daha az metan gazı salınımı
    - Enerji tasarrufu = Daha az kömür/termik kaynaklı emisyon
    - Toplu taşıma = Kişi başına daha düşük emisyon
    """)

# Görsel destekli bilgi kutusu
st.info("💡 Ortalama bir kişinin yıllık karbon ayak izi yaklaşık **4-6 ton CO₂** civarındadır. Ancak bu, yaşam tarzına göre büyük farklılıklar gösterebilir.", icon="📏")

# Hesaplama hakkında
with st.expander("🧮 Karbon Ayak İzi Nasıl Hesaplanır?"):
    st.write("""
    Karbon ayak izi, genellikle aşağıdaki başlıklar altında hesaplanır:
    - 🚗 Ulaşım (otomobil, uçak, toplu taşıma)
    - 🍽️ Beslenme (et, süt, sebze, işlenmiş gıdalar)
    - ⚡ Enerji (elektrik tüketimi, doğalgaz)
    - 🛍️ Tüketim alışkanlıkları (alışveriş, tekstil, elektronik)

    Hesaplama sırasında her aktiviteye karşılık gelen **emisyon faktörleri** (kg CO₂ birim başına) kullanılır.
    """)

# Bölüm: Azaltma yolları
st.markdown("<hr style='border:1px solid #444;'>", unsafe_allow_html=True)
st.markdown("### 🌱 Karbon Ayak İzini Azaltmanın Yolları")

col1, col2 = st.columns(2)

with col1:
    st.success("🚴‍♂️ Kısa mesafelerde bisiklet veya yürüyüş tercih edin.", icon="🚶‍♂️")
    st.success("💡 Enerji verimli cihazlar kullanın (A++ sınıfı).", icon="🔌")
    st.success("🌿 Bitki ağırlıklı beslenmeyi artırın, kırmızı et tüketimini azaltın.", icon="🥗")

with col2:
    st.success("🛍️ Az tüketin, yeniden kullanın ve geri dönüştürün.", icon="♻️")
    st.success("🌞 Güneş enerjisi gibi yenilenebilir kaynaklara yönelin.", icon="🔋")
    st.success("✈️ Uçak yerine tren ya da otobüs tercih edin.", icon="🚆")

# Bölüm çizgisi
st.markdown("<hr style='border:1px dashed #888;'>", unsafe_allow_html=True)


# 🌿 Bilgilendirici Kart
st.markdown("""
<div style="background-color: #1e1e1e; padding: 20px; border-radius: 12px; box-shadow: 0 0 15px #00ff88; margin-bottom: 30px;">
    <h3 style="color: #00ff88;">🌿 Sürdürülebilir Yaşam İçin Adım Atın</h3>
    <p style="color: #dddddd; font-size: 16px;">
        Küçük değişiklikler büyük farklar yaratır. Günlük alışkanlıklarımızı değiştirerek hem çevremizi koruyabilir hem de geleceğe daha yaşanabilir bir dünya bırakabiliriz.
    </p>
    <ul style="color: #cccccc; font-size: 15px;">
        <li>⚡ Gereksiz enerji tüketiminden kaçının</li>
        <li>🍎 Yerel ve mevsimsel ürünler tercih edin</li>
        <li>🔄 Geri dönüşüm konusunda aktif olun</li>
    </ul>
</div>
""", unsafe_allow_html=True)




