import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. CONFIGURACIÓN E INICIALIZACIÓN
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide", initial_sidebar_state="expanded")

# Estilos CSS con Animaciones
st.markdown("""
    <style>
    .main { background-color: #0B0B0B; }
    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }
    .stApp { animation: fadeIn 0.8s ease-in; }
    .brand-title-main { font-size: 52px; font-weight: 900; color: #FFFFFF; letter-spacing: 5px; }
    .metric-card { background: #161616; padding: 20px; border-radius: 15px; border-left: 5px solid #E0E0E0; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. CABECERA
c_logo1, c_logo2, c_logo3 = st.columns([1, 3, 1])
with c_logo2:
    st.markdown('<div style="text-align:center;"><h1 class="brand-title-main">MINDMUSCLE247</h1></div>', unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# 3. LÓGICA DE CONTROL (ROLES)
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
rol = st.sidebar.radio("Selecciona tu Vista:", ["📝 Cuestionario Alumno", "📊 Dashboard Administrador"])

# --- VISTA COACH (DASHBOARD) ---
if rol == "📊 Dashboard Administrador":
    clave = st.sidebar.text_input("Clave de Acceso:", type="password")
    if clave == "MM247":
        st.header("⚡ Panel de Control Profesional")
        try:
            df = pd.read_csv(SHEET_URL)
            st.metric("Total Alumnos Evaluados", len(df))
            
            alumno_sel = st.selectbox("Seleccionar Alumno para Reporte:", df["Nombre Completo"].unique())
            datos_alumno = df[df["Nombre Completo"] == alumno_sel].iloc[0]
            
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.subheader(f"Detalle: {alumno_sel}")
            st.write(datos_alumno)
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("📥 EXPORTAR REPORTE PDF OFICIAL"):
                st.info("Generando reporte... (Próximo paso de desarrollo)")
        except:
            st.error("Base de datos inaccesible.")
    else:
        st.warning("Acceso restringido.")

# --- VISTA ALUMNO (FORMULARIO ORIGINAL) ---
else:
    if "cuestionario_enviado" not in st.session_state: st.session_state.cuestionario_enviado = False
    
    if st.session_state.cuestionario_enviado:
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
    else:
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "⚡ Info", "🏋️ Exp", "🩺 Médico", "📐 Bio", "💥 Fuerza", "🥗 Nut", "📅 Log", "🎯 Pref", "📸 Fotos"
        ])
        
        # AQUÍ TUS PESTAÑAS 1-9 COMPLETAS (SE MANTIENEN IGUAL)
        with t1:
            st.subheader("📋 Datos Personales")
            v_nombre = st.text_input("Nombre Completo:")
            v_edad = st.number_input("Edad:", value=25)
            # ... (Mantén aquí toda tu lógica original de inputs) ...
            
        with t9:
            st.subheader("🎯 Finalizar Evaluación")
            if st.button("🚀 ENVIAR EVALUACIÓN"):
                # Aquí va tu lógica original de dict y pd.DataFrame.to_csv
                st.session_state.cuestionario_enviado = True
                st.rerun()
