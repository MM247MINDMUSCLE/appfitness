import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

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

# URL de tu Google Sheets (Conectado directamente)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/edit?usp=sharing"

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
    
    # Conectar a Google Sheets para leer respuestas anteriores
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_existente = conn.read(spreadsheet=SHEET_URL, ttl="5s")
        
        if not df_existente.empty and "Nombre Completo" in df_existente.columns:
            # Crear lista de clientes con la fecha
            df_existente['Seleccion'] = df_existente['Nombre Completo'] + " (" + df_existente['Fecha'].astype(str) + ")"
            lista_clientes = df_existente['Seleccion'].tolist()
            
            cliente_seleccionado = st.sidebar.selectbox("Selecciona un Alumno:", ["-- Seleccionar --"] + lista_clientes)
            
            if cliente_seleccionado != "-- Seleccionar --":
                # Filtrar la fila del alumno elegido
                fila_alumno = df_existente[df_existente['Seleccion'] == cliente_seleccionado].iloc[0]
                st.sidebar.info(f"Visualizando datos de: {fila_alumno['Nombre Completo']}")
        else:
            st.sidebar.warning("Aún no hay respuestas en la base de datos.")
            fila_alumno = None
    except:
        st.sidebar.error("Conectando con la base de datos...")
        fila_alumno = None
else:
    fila_alumno = None
    if clave_coach != "":
        st.sidebar.error("Clave Incorrecta")

# 3. PANTALLA PRINCIPAL
st.title("💪 MIND MUSCLE - Plataforma de Coaching")
st.write("Por favor, rellena detalladamente cada una de las pestañas del cuestionario.")
st.markdown("---")

# SI EL COACH SELECCIONÓ A UN ALUMNO -> MOSTRAR SUS DATOS CON BOTÓN DE PDF (SÓLO EL COACH LO VE)
if es_coach and fila_alumno is not None:
    st.header(f"📊 Reporte de Evaluación: {fila_alumno['Nombre Completo']}")
    
    # Mostrar resumen de datos al Coach
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Edad:** {fila_alumno.get('Edad', 'N/A')} años")
        st.markdown(f"**Ocupación:** {fila_alumno.get('Ocupacion', 'N/A')}")
    with col2:
        st.markdown(f"**Fecha de Registro:** {fila_alumno.get('Fecha', 'N/A')}")
    
    st.markdown("---")
    
    # AQUÍ SE COLOCA TU LÓGICA BIOMECÁNICA INTERNA DE HEAVY DUTY
    st.subheader("⚙️ Análisis de Torque y Tensión Mecánica")
    st.info("Sistema listo para procesar intensidades basándose en las métricas guardadas.")
    
    # BOTÓN EXCLUSIVO PARA DESCARGAR EL PDF (El cliente jamás lo verá en su casa)
    st.markdown("### 📥 Zona de Descarga")
    btn_pdf = st.button("🚀 Generar y Descargar Reporte PDF Oficial")
    if btn_pdf:
        st.success(f"¡Reporte PDF de {fila_alumno['Nombre Completo']} generado exitosamente! (Simulado)")

# SI ES UN CLIENTE NORMAL (O NO SE HA SELECCIONADO ALUMNO) -> MUESTRA EL CUESTIONARIO LIMPIO
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado Exitosamente!")
        st.markdown("""
            ### ¡Muchas gracias por completar tu información!
            Tu Coach **José Luis Novelo** ha recibido tus datos de manera segura. 
            Él se encargará de analizar tu nivel biomecánico y diseñar tu estrategia bajo los principios de **MIND MUSCLE (Heavy Duty)**. 
            
            *Ya puedes cerrar esta ventana de forma segura.*
        """)
        if st.button("Llenar otro cuestionario"):
            st.session_state.cuestionario_enviado = False
            st.rerun()
            
    else:
        # PESTAÑAS DEL CUESTIONARIO PARA EL CLIENTE
        tab1, tab2, tab3 = st.tabs(["1. Info General", "2. Experiencia", "3. Historial Médico"])
        
        with tab1:
            st.subheader("Datos Personales")
            nombre = st.text_input("Nombre Completo:")
            edad = st.number_input("Edad (años):", min_value=1, max_value=100, value=25)
            ocupacion = st.text_input("Ocupación / Trabajo:")
            
        with tab2:
            st.subheader("Historial de Entrenamiento")
            tiempo_entrenando = st.selectbox("¿Cuánto tiempo llevas entrenando en gimnasio?", ["Menos de 6 meses", "6 meses a 1 año", "1 a 3 años", "Más de 3 años"])
            
        with tab3:
            st.subheader("Condiciones Médicas")
            lesiones = st.text_area("¿Tienes alguna lesión o dolor articular actual? Detalla por favor:")

        st.markdown("---")
        
        # BOTÓN ÚNICO DE ENVÍO PARA EL CLIENTE
        st.markdown("### 🎯 Finalizar Proceso")
        btn_enviar = st.button("📬 Enviar Cuestionario de Evaluación")
        
        if btn_enviar:
            if nombre.strip() == "":
                st.error("⚠️ Por favor, introduce tu Nombre Completo antes de enviar.")
            else:
                # Preparar la nueva fila con la fecha de hoy
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.now().strftime("%Y-%m-%col1_%H:%M"),
                    "Nombre Completo": nombre,
                    "Edad": int(edad),
                    "Ocupacion": ocupacion
                }])
                
                try:
                    # Enviar los datos directo al Google Sheets en la nube
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_actual = conn.read(spreadsheet=SHEET_URL, ttl="0s")
                    df_final = pd.concat([df_actual, nueva_fila], ignore_index=True)
                    conn.update(spreadsheet=SHEET_URL, data=df_final)
                    
                    # Cambiar estado para bloquear la pantalla del cliente
                    st.session_state.cuestionario_enviado = True
                    st.rerun()
                except Exception as e:
                    st.error("Hubo un problema de conexión al enviar. Por favor intenta de nuevo.")
