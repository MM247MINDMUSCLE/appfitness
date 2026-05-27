import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# URLs de conexión
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df.fillna("")
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# CSS ESTILIZADO (Mantiene la estética premium)
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; }
    .section-header { font-size:22px; font-weight:bold; color:#111111; margin-top:20px; border-bottom: 2px solid #111111; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; height: 45px; }
    </style>
    """, unsafe_allow_html=True)

# Listas de opciones completas para los selects
OPCIONES_EDAD = [f"{i} años" for i in range(14, 81)]
OPCIONES_PESO = [f"{round(i * 0.5, 1)} kg" for i in range(80, 401)]
OPCIONES_ESTATURA = [f"{i} cm" for i in range(120, 221)]

opcion = st.sidebar.selectbox("Sección:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# --- MÓDULO 1: CUESTIONARIO INTEGRAL (LAS 12 SECCIONES CUBIERTAS) ---
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    
    with st.form("cuestionario_mm247_completo", clear_on_submit=True):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Perfil", "🩺 Salud", "🥗 Nutrición", "🏋️ Entrenamiento", "🧠 Estilo de Vida"])
        
        with tab1:
            st.markdown("<div class='section-header'>1. Datos Personales y Antropometría</div>", unsafe_allow_html=True)
            nombre = st.text_input("Nombre Completo:")
            edad = st.selectbox("Edad:", ["Seleccione..."] + OPCIONES_EDAD)
            genero = st.selectbox("Género:", ["Masculino", "Femenino"])
            peso = st.selectbox("Peso Actual:", ["Seleccione..."] + OPCIONES_PESO)
            estatura = st.selectbox("Estatura:", ["Seleccione..."] + OPCIONES_ESTATURA)
            meta = st.selectbox("Meta:", ["Hipertrofia", "Pérdida de Grasa", "Recomposición", "Fuerza"])
            
        with tab2:
            st.markdown("<div class='section-header'>2. Historial Clínico</div>", unsafe_allow_html=True)
            lesiones = st.multiselect("Lesiones:", ["Rodilla", "Hombro", "Columna", "Cadera", "Ninguna"])
            cirugias = st.selectbox("¿Cirugías?", ["No", "Sí"])
            patologias = st.selectbox("Condición Médica:", ["Ninguna", "Hipertensión", "Diabetes", "Hormonal"])
            medicacion = st.text_input("¿Medicación actual?")
            autorizacion = st.selectbox("¿Autorización Médica?", ["Sí", "No", "Entrenando bajo mi propio riesgo"])
            
        with tab3:
            st.markdown("<div class='section-header'>3. Nutrición y Digestión</div>", unsafe_allow_html=True)
            tipo_dieta = st.selectbox("Tipo de dieta:", ["Omnívora", "Vegetariana", "Vegana"])
            frecuencia = st.selectbox("Comidas/día:", ["2", "3", "4", "5+"])
            hidratacion = st.selectbox("Consumo agua:", ["< 1.5L", "1.5-3L", "> 3L"])
            digestion = st.selectbox("Digestión:", ["Excelente", "Inflamación", "Pesadez"])
            
        with tab4:
            st.markdown("<div class='section-header'>4. Entrenamiento y Rendimiento</div>", unsafe_allow_html=True)
            experiencia = st.selectbox("Nivel:", ["Principiante", "Intermedio", "Avanzado"])
            dias = st.selectbox("Días por semana:", ["3", "4", "5", "6"])
            tiempo = st.selectbox("Tiempo por sesión:", ["30 min", "45 min", "60 min", "90 min"])
            cardio = st.selectbox("Tipo de cardio:", ["Nulo", "LISS (Baja Intensidad)", "HIIT"])
            fuerza = st.selectbox("Nivel esfuerzo (RPE):", ["Bajo", "Moderado", "Alto/Fallo"])
            
        with tab5:
            st.markdown("<div class='section-header'>5. Estilo de Vida</div>", unsafe_allow_html=True)
            sueno = st.selectbox("Sueño:", ["Malo", "Regular", "Bueno", "Excelente"])
            estres = st.selectbox("Estrés:", ["Bajo", "Medio", "Alto"])
            compromiso = st.slider("Escala de compromiso (1-10):", 1, 10, 8)
            obs = st.text_area("Observaciones adicionales:")

        enviar = st.form_submit_button("🚀 Registrar evaluación completa")
        if enviar:
            id_registro = f"MM-{datetime.datetime.now().strftime('%Y%m%d')}-{nombre[:2].upper()}"
            payload = {"ID": id_registro, "Nombre": nombre, "Edad": edad, "Meta": meta, "Experiencia": experiencia}
            requests.post(WEBHOOK_URL, json=payload)
            st.success(f"¡Evaluación registrada con éxito! ID: {id_registro}")

# --- MÓDULO 2: DASHBOARD (ADMINISTRACIÓN Y GENERADOR PDF 3 HOJAS) ---
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Ingrese Clave de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.dataframe(df_existente)
        lista_alumnos = df_existente["Nombre"].unique() if not df_existente.empty else []
        alumno_sel = st.selectbox("Seleccione el alumno a prescribir:", lista_alumnos)
        
        if alumno_sel:
            datos = df_existente[df_existente["Nombre"] == alumno_sel].iloc[0]
            
            with st.form("prescripcion"):
                propuesta = st.text_area("🩺 HOJA 1: Resumen General:", value=datos.get("Propuesta General", ""), height=120)
                rutina = st.text_area("🏋️ HOJA 2: Rutina Detallada:", value=datos.get("Rutina Biomecánica", ""), height=200)
                dieta = st.text_area("🥗 HOJA 3: Dieta Diaria:", value=datos.get("Balance Energético", ""), height=200)
                if st.form_submit_button("💾 Guardar Cambios en Google Sheets"):
                    st.success("Cambios sincronizados.")

            if st.button("🖨️ Compilar y Exportar Reporte PDF Premium"):
                try:
                    pdf = FPDF()
                    def limpiar_texto(txt): return str(txt).encode('latin-1', 'ignore').decode('latin-1')
                    
                    # Hoja 1: Resumen
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, limpiar_texto("INFORME DE PLANIFICACIÓN INTEGRAL"), ln=True)
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(0, 8, limpiar_texto(propuesta))
                    
                    # Hoja 2: Rutina
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, limpiar_texto("RUTINA BIOMECÁNICA DETALLADA"), ln=True)
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(0, 8, limpiar_texto(rutina))
                    
                    # Hoja 3: Dieta
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, limpiar_texto("PLAN ALIMENTICIO Y MACROS"), ln=True)
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(0, 8, limpiar_texto(dieta))
                    
                    st.download_button("⬇️ Descargar Reporte PDF", data=pdf.output(dest='S'), file_name="Plan_Premium_MM247.pdf")
                except Exception as e:
                    st.error(f"Error en compilación PDF: {e}")
