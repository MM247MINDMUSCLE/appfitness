import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="MINDMUSCLE247",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales premium
st.markdown("""
    <style>
    .main { background-color: #0B0B0B; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0) !important; }
    .stApp img { border: none !important; box-shadow: none !important; }
    .brand-container { display: flex; align-items: center; justify-content: center; gap: 20px; padding: 30px 10px; background: #0B0B0B; margin-bottom: 20px; }
    .brand-title-main { font-size: 52px; font-weight: 900; color: #FFFFFF; letter-spacing: 5px; font-family: 'Arial Black', sans-serif; margin: 0; line-height: 1; }
    .stButton>button { background-color: #E0E0E0; color: #000000; font-weight: bold; border-radius: 4px; border: none; padding: 18px 36px; width: 100%; font-size: 20px; text-transform: uppercase; letter-spacing: 2px; }
    </style>
""", unsafe_allow_html=True)

# 2. BARRA LATERAL (QR MOVIDO AQUÍ)
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
st.sidebar.markdown("**📲 Acceso Rápido:**")
link_app = "https://appfitness-mindmuscle247.streamlit.app"
qr_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={link_app}&choe=UTF-8"
st.sidebar.image(qr_url)
st.sidebar.markdown("---")

# LÓGICA DE CLAVE COACH
clave_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")
es_coach = (clave_coach == "MM247")

# 3. CABECERA
c_logo1, c_logo2, c_logo3 = st.columns([1, 3, 1])
with c_logo2:
    col_img, col_txt = st.columns([1, 3])
    with col_img:
        if os.path.exists("logo.png"): st.image("logo.png", width=110)
    with col_txt:
        st.markdown('<div style="padding-top: 25px;"><h1 class="brand-title-main">MINDMUSCLE</h1></div>', unsafe_allow_html=True)

# Lógica de conexión
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"
if "cuestionario_enviado" not in st.session_state: st.session_state.cuestionario_enviado = False

# 4. CONTENIDO (VISTA ALUMNO)
st.write("🔥 Bienvenido al radar de evaluación técnica de **MINDMUSCLE247**.")

# DEFINICIÓN DE PESTAÑAS
t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
    "⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", 
    "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Foto"
])

# Rellena cada pestaña con tus campos originales
with t1:
    st.subheader("📋 Datos Personales")
    v_nombre = st.text_input("✍ *Escribe tu Nombre Completo:*")
    # ... (Aquí puedes pegar todos tus campos originales de T1 a T8) ...

with t9:
    st.subheader("📸 Evaluación Visual Inicial")
    st.info("Sube tus fotos de frente, perfil y espalda desde tu galería.")
    uploaded_photos = st.file_uploader("📬 Selecciona tus fotos:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    st.markdown("---")
    if st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA"):
        st.success("¡Datos enviados con éxito!")
