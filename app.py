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
    
    .brand-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        padding: 30px 10px;
        background: #0B0B0B;
        margin-bottom: 20px;
    }
    .brand-title-main {
        font-size: 52px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 5px;
        margin: 0;
        line-height: 1;
    }
    .stTabs [data-baseweb="tab"] { color: #757575; font-weight: bold; font-size: 15px; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #E0E0E0; border-bottom-color: #E0E0E0; }
    .stButton>button {
        background-color: #E0E0E0; color: #000000; font-weight: bold;
        border-radius: 4px; border: none; padding: 18px 36px; width: 100%;
        font-size: 20px; text-transform: uppercase; letter-spacing: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. CABECERA: Logo y Nombre alineados
c_logo1, c_logo2, c_logo3 = st.columns([1, 3, 1])
with c_logo2:
    col_img, col_txt = st.columns([1, 3])
    with col_img:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=110)
    with col_txt:
        st.markdown('<div style="padding-top: 25px;"><h1 class="brand-title-main">MINDMUSCLE</h1></div>', unsafe_allow_html=True)

# Lógica principal (sin cambios en la base de datos)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"
if "cuestionario_enviado" not in st.session_state: st.session_state.cuestionario_enviado = False

# [Aquí iría el resto de tu lógica de formularios de los Tabs 1 al 8 igual que antes]
# ... (Mantén el código de tus Tabs 1 al 8 exactamente como los tenías) ...

# 3. PESTAÑA 9 LIMPIA (Solo fotos, sin QR)
with t9:
    st.subheader("📸 Evaluación Visual Inicial")
    st.info("Sube tus fotos de frente, perfil y espalda desde tu galería.")
    
    uploaded_photos = st.file_uploader(
        "📬 Selecciona tus fotos:", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    if uploaded_photos:
        st.success(f"💪 ¡Se han cargado {len(uploaded_photos)} imágenes!")
    
    st.markdown("---")
    st.subheader("🎯 Finalizar Registro")
    btn_enviar = st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA")
    
    if btn_enviar:
        # [Tu lógica de guardado]
        st.session_state.cuestionario_enviado = True
        st.rerun()
