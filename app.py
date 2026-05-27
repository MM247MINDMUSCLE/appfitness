import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        # Limpieza robusta de columnas
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.fillna("")
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# CSS estilizado (sin cambios estructurales)
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; }
    .stButton>button { background-color: #111111; color: white; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# --- MÓDULO 1: CUESTIONARIO ---
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    with st.form("cuestionario_cerrado_mm247", clear_on_submit=True):
        # ... (Mantén aquí tu estructura de pestañas original) ...
        enviar_datos = st.form_submit_button("🚀 Registrar evaluación")
        if enviar_datos:
            # Tu lógica original de validación y requests.post
            pass

# --- MÓDULO 2: DASHBOARD Y PDF CORREGIDO ---
elif opcion == "📊 Dashboard Administrador":
    # ... (Tu lógica de carga y visualización) ...
    
    if st.button("🖨️ Compilar y Exportar Reporte PDF Premium"):
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "", 12)
            
            # CORRECCIÓN DE ERRORES:
            # 1. No uses 'set_linewidth', usa 'set_line_width'
            # 2. Manejo de texto: Evita caracteres especiales que dan error de Unicode
            def limpiar_texto(txt):
                return str(txt).encode('ascii', 'ignore').decode('ascii')
            
            pdf.set_line_width(0.5) # CORREGIDO: set_line_width es el método correcto
            pdf.cell(0, 10, limpiar_texto("Informe de Planificación"), ln=True)
            # ... resto de tu lógica de PDF ...
            
            st.download_button("Descargar PDF", data=pdf.output(dest='S'), file_name="Plan_MM247.pdf")
        except Exception as e:
            st.error(f"Error técnico: {e}")
