import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ YARDIMCI FONKSİYONLAR ------------------
def calculate_emission(data, factors):
    emissions = {
        'beef': data.get('beef', 0) * factors.get('beef', 0),
        'chicken': data.get('chicken', 0) * factors.get('chicken', 0),
        'electricity': data.get('electricity', 0) * factors.get('electricity', 0),
        'car': data.get('car_distance', 0) * factors.get('car', {}).get(data.get('car', ''), 0)
    }
    total = sum(emissions.values())
    return total, emissions


def generate_advice(emissions):
    advice = []
    if emissions.get('beef', 0) > 8:
        advice.append("🥩 Dana eti tüketiminiz yüksek. Hayvansal protein yerine bitkisel kaynaklara yönelin.")
    if emissions.get('chicken', 0) > 6:
        advice.append("🍗 Tavuk tüketiminiz fazla. Haftalık tüketimi sınırlamayı deneyin.")
    if emissions.get('car', 0) > 5:
        advice.append("🚗 Araba kullanımınızdan kaynaklı emisyon yüksek. Toplu taşıma veya yürüyüşü değerlendirin.")
    if emissions.get('electricity', 0) > 25:
        advice.append("💡 Elektrik tüketiminiz yüksek. Tasarruflu ampuller ve enerji verimli cihazlar kullanın.")
    if not advice:
        advice.append("🌱 Harika! Karbon ayak izinizi düşük seviyede tutuyorsunuz.")
    return advice


def log_to_csv(data, emission, filename='veri_kayit.csv'):
    import os
    row = data.copy()
    row['total_emission'] = emission
    df_row = pd.DataFrame([row])
    os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
    if os.path.exists(filename):
        df_hist = pd.read_csv(filename)
        df_hist = pd.concat([df_hist, df_row], ignore_index=True)
    else:
        df_hist = df_row
    df_hist.to_csv(filename, index=False)

# ------------------ SAYFA AYARLARI ------------------
st.set_page_config(page_title='Karbon Ayak İzi', layout='wide', page_icon='🌍')

# Stil
st.markdown("""
<style>
body{background:#0f0f0f;color:#fff;}
.card-container{display:flex;justify-content:space-between;margin:20px 0;}
.card{flex:1;background:#1b1b1b;padding:16px;border-radius:12px;margin:0 8px;
    box-shadow:0 0 8px rgba(57,255,20,0.3);text-align:center;border:1px solid rgba(57,255,20,0.2)}
.card h4{color:#bbb;margin-bottom:4px;font-size:16px}
.card p{color:#39ff14;font-size:20px;font-weight:bold;margin:0}
</style>
""",unsafe_allow_html=True)

st.title('🌱 Karbon Ayak İzi Hesaplama')
st.markdown('##### Günlük alışkanlıklarını gir, emisyonunu öğren!')

# ------------------ SIDEBAR FORM ------------------
st.sidebar.header('🔍 Girdi Bilgileri')
with st.sidebar.form('form'):
    beef = st.number_input('Dana eti (kg)',0.0,step=0.1)
    chicken = st.number_input('Tavuk eti (kg)',0.0,step=0.1)
    electricity = st.number_input('Elektrik (kWh)',0.0,step=1.0)
    car = st.selectbox('Araç tipi',['Yok','Benzin','Dizel','Elektrik'])
    car_distance = st.number_input('Araç km',0.0,step=1.0)
    city = st.selectbox('Şehir',['İstanbul','Ankara','İzmir','Diğer'])
    submit=st.form_submit_button('💨 Hesapla')

# Faktörler
factors={'beef':27.0,'chicken':6.9,'electricity':0.4,'car':{'Yok':0.0,'Benzin':0.021,'Dizel':0.025,'Elektrik':0.012}}

# Önceki
if 'res' not in st.session_state:
    try:
        df=pd.read_csv('veri_kayit.csv')
        if not df.empty:
            last = df.iloc[-1].to_dict()
            prev_input = {
                'beef': last.get('beef', 0),
                'chicken': last.get('chicken', 0),
                'electricity': last.get('electricity', 0),
                'car': last.get('car', 'Yok'),
                'car_distance': last.get('car_distance', 0),
                'city': last.get('city', '')
            }
            prev_total, prev_details = calculate_emission(prev_input, factors)
            st.session_state['res'] = {'inp': prev_input, 'total': prev_total, 'details': prev_details}
    except FileNotFoundError:
        pass

# Hesap
if submit:
    inp={'beef':beef,'chicken':chicken,'electricity':electricity,'car':car,'car_distance':car_distance,'city':city}
    total,det=calculate_emission(inp,factors)
    log_to_csv(inp,total)
    st.session_state['res']={'inp':inp,'total':total,'details':det}

# Görsel
if 'res' in st.session_state:
    data=st.session_state['res']
    inp=data['inp'];total=data['total'];det=data['details'] or {}
    df_all=pd.read_csv('veri_kayit.csv')
    a=df_all['beef'].mean();b=df_all['chicken'].mean();c=df_all['electricity'].mean();d=df_all['car_distance'].mean()
    # Ortalama kart
    st.markdown(f"""
<div class="card-container">
    <div class="card"><h4>🥩 Ort. Dana Eti</h4><p>{a:.2f}</p></div>
    <div class="card"><h4>🍗 Ort. Tavuk Eti</h4><p>{b:.2f}</p></div>
    <div class="card"><h4>⚡ Ort. Elektrik</h4><p>{c:.2f}</p></div>
    <div class="card"><h4>🚗 Ort. Araç km</h4><p>{d:.2f}</p></div>
</div>""",unsafe_allow_html=True)
    # Sonuç kart
    pred=inp['electricity']*0.35+inp['beef']*25;fark=abs(total-pred)
    st.markdown(f"""
<div class="card-container">
    <div class="card"><h4>🌍 Toplam Emisyon</h4><p>{total:.2f}kg CO₂</p></div>
    <div class="card"><h4>🤖 Tahmin</h4><p>{pred:.2f}kg</p></div>
    <div class="card"><h4>⚖️ Fark</h4><p>{fark:.2f}kg</p></div>
</div>""",unsafe_allow_html=True)
    # Grafikler
    pc,lc=st.columns(2)
    cats=['Dana Eti','Tavuk Eti','Elektrik','Araç'];vals=[a,b,c,d]
    with pc: st.subheader('Aylık Dağılım');st.plotly_chart(px.pie(names=cats,values=vals,hole=0.4),use_container_width=True)
    with lc: st.subheader('Kayıt Zamanı');df_all.index=pd.to_datetime(df_all.index.astype(str));st.plotly_chart(px.line(df_all,x=df_all.index,y=['beef','chicken','electricity','car_distance'],markers=True),use_container_width=True)
    # Öneri
    st.subheader('💡 Öneriler')
    for msg in generate_advice(det): st.info(msg)
