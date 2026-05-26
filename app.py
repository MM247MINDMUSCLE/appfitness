import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

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
    .brand-title-main { font-size: 52px; font-weight: 900; color: #FFFFFF; letter-spacing: 5px; font-family: 'Arial Black', sans-serif; }
    .stButton>button { background-color: #E0E0E0; color: #000000; font-weight: bold; border-radius: 4px; border: none; padding: 18px 36px; width: 100%; font-size: 20px; text-transform: uppercase; }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div, .stNumberInput>div>div>input { background-color: #161616 !important; color: white !important; border: 1px solid #333333 !important; }
    </style>
""", unsafe_allow_html=True)

# 2. CABECERA
c_logo1, c_logo2, c_logo3 = st.columns([1, 3, 1])
with c_logo2:
    st.markdown('<div style="text-align:center;"><h1 class="brand-title-main">MINDMUSCLE247</h1></div>', unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# 3. LÓGICA DE CONTROL
if "cuestionario_enviado" not in st.session_state: st.session_state.cuestionario_enviado = False

st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
modo = st.sidebar.radio("Seleccionar Vista:", ["📝 Cuestionario Alumno", "📊 Dashboard Administrador"])
clave_coach = st.sidebar.text_input("Clave de Acceso:", type="password")

# --- VISTA ADMINISTRADOR ---
if modo == "📊 Dashboard Administrador":
    if clave_coach == "MM247":
        st.header("⚡ Panel de Control")
        try:
            df = pd.read_csv(SHEET_URL)
            st.metric("Total Alumnos", len(df))
            alumno_sel = st.selectbox("Seleccionar Alumno:", df["Nombre Completo"].unique())
            datos = df[df["Nombre Completo"] == alumno_sel].iloc[0]
            st.write(datos)
        except:
            st.error("Error al cargar la base de datos.")
    else:
        st.warning("Acceso restringido.")

# --- VISTA ALUMNO ---
else:
    if st.session_state.cuestionario_enviado:
        st.success("✅ ¡Cuestionario Enviado!")
    else:
        # DEFINICIÓN ÚNICA DE TABS (Corregido para evitar errores)
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", 
            "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Fotos"
        ])

        with t1:
            st.subheader("📋 Datos Personales")
            v_nombre = st.text_input("Nombre Completo:")
            v_edad = st.number_input("Edad:", value=25)
            # ... (Aquí irían el resto de tus campos originales) ...
        
        with t9:
            st.subheader("📸 Evaluación Visual")
            if st.button("🚀 ENVIAR EVALUACIÓN"):
                st.session_state.cuestionario_enviado = True
                st.rerun()
