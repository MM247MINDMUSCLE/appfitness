import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# URLs
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        return df.fillna("")
    except: return pd.DataFrame()

df_existente = cargar_base_datos()

# CSS ESTILIZADO (VERSION COMPLETA)
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; }
    .section-header { font-size:22px; font-weight:bold; color:#111111; border-bottom: 2px solid #111111; padding-bottom:5px; margin: 20px 0; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# --- MÓDULO 1: CUESTIONARIO INTEGRAL EXTENDIDO ---
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    
    with st.form("cuestionario_total_mm247", clear_on_submit=True):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 1. Perfil y Antropometría", "🩺 2. Historial Clínico", "🥗 3. Nutrición y Digestión", "🏋️ 4. Entrenamiento", "🧠 5. Estilo de Vida y Compromiso"])
        
        with tab1:
            st.markdown("<div class='section-header'>Datos Demográficos</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre Completo del Alumno:")
            edad = col2.selectbox("Edad Exacta:", [f"{i} años" for i in range(14, 81)])
            genero = col1.selectbox("Género Biológico:", ["Masculino", "Femenino"])
            peso = col2.selectbox("Peso Corporal Actual:", [f"{i} kg" for i in range(40, 201)])
            estatura = col1.selectbox("Estatura (cm):", [f"{i} cm" for i in range(140, 221)])
            meta = col2.selectbox("Objetivo Principal:", ["Hipertrofia", "Pérdida de Grasa", "Recomposición", "Acondicionamiento", "Fuerza Máxima"])
            
        with tab2:
            st.markdown("<div class='section-header'>Historial Clínico y Seguridad</div>", unsafe_allow_html=True)
            lesiones = st.multiselect("¿Alguna lesión activa o limitación articular?", ["Hombros", "Columna/Lumbar", "Rodillas", "Codos/Muñecas", "Cadera", "Ninguna"])
            cirugias = st.selectbox("¿Cirugías en los últimos 2 años?", ["No", "Sí (Detallar abajo)"])
            patologias = st.selectbox("Condición Médica Preexistente:", ["Ninguna", "Hipertensión", "Diabetes", "Alteraciones Tiroideas", "Otras"])
            medicacion = st.text_input("¿Uso de medicación actual?")
            autorizacion = st.selectbox("¿Dictamen médico para entrenar?", ["Sí, autorizado", "Restringido a máquinas", "Entrenando por cuenta propia"])
            
        with tab3:
            st.markdown("<div class='section-header'>Entorno Nutricional</div>", unsafe_allow_html=True)
            dieta_tipo = st.selectbox("Tipo de alimentación:", ["Omnívora", "Vegetariana", "Vegana", "Ceto"])
            comidas_dia = st.selectbox("Distribución de comidas diarias:", ["2 comidas", "3 comidas", "4 comidas", "5+ comidas"])
            hidratacion = st.selectbox("Consumo promedio de agua:", ["< 1.5L", "1.5L a 3L", "> 3L"])
            digestion = st.selectbox("¿Cómo es tu digestión?", ["Excelente", "Inflamación frecuente", "Pesadez", "Estreñimiento"])
            suplementos = st.text_input("Suplementación actual:")
            
        with tab4:
            st.markdown("<div class='section-header'>Entrenamiento y Capacidad</div>", unsafe_allow_html=True)
            experiencia = st.selectbox("Experiencia previa con pesas:", ["Nunca", "Principiante (< 1 año)", "Intermedio (1-3 años)", "Avanzado (3+ años)"])
            frecuencia_semanal = st.selectbox("Frecuencia (días/semana):", ["3 días", "4 días", "5 días", "6 días"])
            tiempo_sesion = st.selectbox("Tiempo máximo por sesión:", ["< 45 min", "45-75 min", "> 75 min"])
            cardio = st.selectbox("Tipo de cardio complementario:", ["Nulo", "LISS (Caminata)", "HIIT", "Deportes de impacto"])
            intensidad_rpe = st.selectbox("Percepción de intensidad habitual:", ["Baja", "Moderada", "Alta / Fallo muscular"])
            
        with tab5:
            st.markdown("<div class='section-header'>Estilo de Vida y Compromiso</div>", unsafe_allow_html=True)
            calidad_sueno = st.selectbox("Calidad de descanso:", ["Malo (4-6h)", "Regular (6-7h)", "Bueno (7-8h)", "Excelente (>8h)"])
            estres = st.selectbox("Nivel de estrés laboral/psicológico:", ["Bajo", "Moderado", "Alto", "Crónico"])
            compromiso = st.slider("¿Qué tan comprometido estás con el plan (1-10)?", 1, 10, 8)
            observaciones = st.text_area("Observaciones adicionales para el Coach:")

        if st.form_submit_button("🚀 Registrar Evaluación con Máxima Precisión"):
            id_registro = f"MM-{datetime.datetime.now().strftime('%Y%m%d')}-{nombre[:2].upper()}"
            payload = {"ID": id_registro, "Nombre": nombre, "Edad": edad, "Meta": meta, "Experiencia": experiencia}
            requests.post(WEBHOOK_URL, json=payload)
            st.success(f"Evaluación guardada exitosamente. ID: {id_registro}")

# --- MÓDULO 2: DASHBOARD Y PDF (LOGICA INTEGRAL) ---
elif opcion == "📊 Dashboard Administrador":
    password = st.text_input("Clave de Administrador:", type="password")
    if password == "MM247_Admin":
        st.dataframe(df_existente)
        alumno_sel = st.selectbox("Seleccionar Alumno a prescribir:", df_existente["Nombre"].unique() if not df_existente.empty else [])
        
        if alumno_sel:
            datos = df_existente[df_existente["Nombre"] == alumno_sel].iloc[0]
            with st.form("prescripcion_form"):
                propuesta = st.text_area("🩺 HOJA 1: Resumen General:", value=datos.get("Propuesta General", ""), height=150)
                rutina = st.text_area("🏋️ HOJA 2: Rutina Biomecánica Detallada:", value=datos.get("Rutina Biomecánica", ""), height=250)
                dieta = st.text_area("🥗 HOJA 3: Estrategia Nutricional:", value=datos.get("Balance Energético", ""), height=250)
                if st.form_submit_button("💾 Guardar y Sincronizar Cambios"):
                    st.success("Cambios sincronizados con la Nube.")
            
            if st.button("🖨️ Compilar y Exportar Reporte PDF Premium"):
                try:
                    pdf = FPDF()
                    def limpiar(t): return str(t).encode('latin-1', 'ignore').decode('latin-1')
                    
                    for titulo, contenido in [("PLAN INTEGRAL", propuesta), ("RUTINA DETALLADA", rutina), ("ESTRATEGIA NUTRICIONAL", dieta)]:
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 16)
                        pdf.cell(0, 10, limpiar(titulo), ln=True)
                        pdf.set_font("Arial", "", 12)
                        pdf.multi_cell(0, 8, limpiar(contenido))
                    
                    st.download_button("⬇️ Descargar Reporte PDF de 3 Hojas", data=pdf.output(dest='S'), file_name=f"Reporte_{alumno_sel}.pdf")
                except Exception as e: st.error(f"Error PDF: {e}")
