import streamlit as st

st.set_page_config(page_title="İletişim", layout="centered")

st.markdown("""
<style>
body {
    background-color: #0d0d0d;
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}
.contact-box {
    border: 1px solid #00ff88;
    border-radius: 20px;
    padding: 35px;
    max-width: 480px;
    margin: 50px auto;
    text-align: center;
    background: linear-gradient(145deg, #1c1c1c, #111111);
    box-shadow: 0 0 25px rgba(0, 255, 136, 0.4);
    transition: 0.4s ease;
}
.contact-box:hover {
    box-shadow: 0 0 35px rgba(0, 255, 136, 0.8);
    transform: scale(1.01);
}
.linkedin-logo {
    width: 70px;
    margin-bottom: 15px;
    transition: 0.3s;
}
.linkedin-logo:hover {
    transform: scale(1.1) rotate(3deg);
}
.contact-info {
    font-size: 15px;
    color: #eeeeee;
    line-height: 2.1;
}
a {
    color: #00ff88;
    text-decoration: none;
    font-weight: 500;
    transition: 0.3s;
}
a:hover {
    text-decoration: underline;
    color: #00ffaa;
}
h2.title {
    color: #00ff88;
    font-size: 24px;
    margin-bottom: 18px;
}
</style>

<div class="contact-box">
    <h2 class="title">📬 Bana Ulaşın</h2>
    <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" class="linkedin-logo" />
    <div class="contact-info">
        <strong>LinkedIn:</strong><br>
        <a href="https://www.linkedin.com/in/ali-can-%C3%A7oban-71485a199/" target="_blank">
            Ali Can ÇOBAN
        </a><br><br>
        <strong>E-posta:</strong><br>
        <a href="mailto:accoban837@gmail.com">accoban837@gmail.com</a>
    </div>
</div>
""", unsafe_allow_html=True)
