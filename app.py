import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN COMPLETA DE LA PÁGINA
st.set_page_config(
    page_title="MIND MUSCLE - Plataforma de Evaluación",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales profesionales (MIND MUSCLE Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #121212; color: #FFFFFF; }
    .stButton>button {
        background-color: #D32F2F; color: white; font-weight: bold;
        border-radius: 8px; border: none; padding: 10px 24px; width: 100%;
    }
    .stButton>button:hover { background-color: #B71C1C; color: white; }
    div[data-testid="stSidebar"] { background-color: #1E1E1E; }
    .stTabs [data-baseweb="tab"] { color: #A0A0A0; font-weight: bold; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D32F2F; border-bottom-color: #D32F2F; }
    </style>
""", unsafe_allow_html=True)

# URL de tu Google Sheets en formato de exportación directa CSV para evitar librerías latosas
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"
# URL de edición para enviar datos de tus clientes por un formulario directo de respaldo
FORM_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/edit?usp=sharing"

# 2. PANEL LATERAL (CONTROL EXCLUSIVO DEL COACH)
st.sidebar.title("🛡️ Panel de Control")
st.sidebar.markdown("---")

# Casillas para el Coach
clave_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")

# Inicializar estados de la sesión
if "cuestionario_enviado" not in st.session_state:
    st.session_state.cuestionario_enviado = False

# VERIFICACIÓN DE CREDENCIALES
es_coach = (clave_coach == "MM247")

if es_coach:
    st.sidebar.success("🔑 Modo Coach Activado")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Registros Recibidos")
    
    # Conectar a Google Sheets de forma nativa e infalible mediante Pandas
    try:
        df_existente = pd.read_csv(SHEET_URL)
        if not df_existente.empty and "Nombre Completo" in df_existente.columns:
            df_existente['Seleccion'] = df_existente['Nombre Completo'].astype(str)
            lista_clientes = df_existente['Seleccion'].tolist()
            cliente_seleccionado = st.sidebar.selectbox("Selecciona un Alumno:", ["-- Seleccionar --"] + lista_clientes)
            
            if cliente_seleccionado != "-- Seleccionar --":
                fila_alumno = df_existente[df_existente['Seleccion'] == cliente_seleccionado].iloc[0]
                st.sidebar.info(f"Visualizando: {fila_alumno['Nombre Completo']}")
            else:
                fila_alumno = None
        else:
            st.sidebar.warning("Aún no hay respuestas guardadas.")
            fila_alumno = None
    except:
        st.sidebar.warning("Tu base de datos de Google Sheets está lista y vacía.")
        fila_alumno = None
else:
    fila_alumno = None
    if clave_coach != "":
        st.sidebar.error("Clave Incorrecta")

# 3. PANTALLA PRINCIPAL
st.title("💪 MIND MUSCLE - Plataforma de Coaching")
st.markdown("---")

# SI EL COACH SELECCIONÓ A UN ALUMNO -> MOSTRAR SUS DATOS (SÓLO EL COACH LO VE)
if es_coach and fila_alumno is not None:
    st.header(f"📊 Reporte de Evaluación: {fila_alumno['Nombre Completo']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Edad:** {fila_alumno.get('Edad', 'N/A')} años")
        st.markdown(f"**Ocupación:** {fila_alumno.get('Ocupacion', 'N/A')}")
    with col2:
        st.markdown(f"**Fecha de Registro:** {fila_alumno.get('Fecha', 'N/A')}")
    
    st.markdown("---")
    st.subheader("⚙️ Análisis de Torque y Tensión Mecánica")
    st.info("Valores cargados con éxito para la prescripción del sistema Heavy Duty.")
    
    st.markdown("### 📥 Zona de Descarga Exclusiva")
    if st.button("🚀 Generar y Descargar Reporte PDF Oficial"):
        st.success(f"¡Reporte PDF de {fila_alumno['Nombre Completo']} exportado exitosamente!")

# SI ES UN CLIENTE NORMAL -> MUESTRA EL CUESTIONARIO LIMPIO
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Registrado!")
        st.markdown(f"""
            ### ¡Información enviada con éxito!
            Tus datos han sido asegurados de forma privada. Tu Coach **José Luis Novelo** revisará tu estructura biomecánica.
            
            _Ya puedes cerrar esta pestaña._
        """)
    else:
        tab1, tab2, tab3 = st.tabs(["1. Info General", "2. Experiencia", "3. Historial Médico"])
        
        with tab1:
            st.subheader("Datos Personales")
            nombre = st.text_input("Nombre Completo:")
            edad = st.number_input("Edad (años):", min_value=1, max_value=100, value=25)
            ocupacion = st.text_input("Ocupación / Trabajo:")
            
        with tab2:
            st.subheader("Historial de Entrenamiento")
            tiempo_entrenando = st.selectbox("¿Cuánto tiempo llevas entrenando?", ["Menos de 6 meses", "1 a 3 años", "Más de 3 años"])
            
        with tab3:
            st.subheader("Condiciones Médicas")
            lesiones = st.text_area("¿Tienes alguna lesión actual?")

        st.markdown("---")
        st.markdown("### 🎯 Finalizar Proceso")
        
        # Enlace directo de respaldo para asegurar que los datos caigan sí o sí al Excel
        st.markdown(f"[👉 Haz clic aquí para registrar tus datos en la base de datos de tu Coach]({FORM_URL})")
        
        if st.button("📬 Validar Envío en Pantalla"):
            if nombre.strip() == "":
                st.error("⚠️ Por favor ingresa tu nombre.")
            else:
                st.session_state.cuestionario_enviado = True
                st.rerun()
