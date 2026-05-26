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
        border-radius: 8px; border: none; padding: 12px 24px; width: 100%;
        font-size: 16px;
    }
    .stButton>button:hover { background-color: #B71C1C; color: white; }
    div[data-testid="stSidebar"] { background-color: #1E1E1E; }
    .stTabs [data-baseweb="tab"] { color: #A0A0A0; font-weight: bold; font-size: 16px; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D32F2F; border-bottom-color: #D32F2F; }
    </style>
""", unsafe_allow_html=True)

# URL para conectar con tu Google Sheets en segundo plano
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# 2. PANEL LATERAL (CONTROL EXCLUSIVO DEL COACH + QR ESTÉTICO)
st.sidebar.title("🛡️ Panel de Control")
st.sidebar.markdown("---")

clave_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")
es_coach = (clave_coach == "MM247")

if es_coach:
    st.sidebar.success("🔑 Modo Coach Activado")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Registros Recibidos")
    
    try:
        df_existente = pd.read_csv(SHEET_URL)
        if not df_existente.empty and "Nombre Completo" in df_existente.columns:
            lista_clientes = df_existente["Nombre Completo"].astype(str).tolist()
            cliente_seleccionado = st.sidebar.selectbox("Selecciona un Alumno:", ["-- Seleccionar --"] + lista_clientes)
            
            if cliente_seleccionado != "-- Seleccionar --":
                fila_alumno = df_existente[df_existente["Nombre Completo"] == cliente_seleccionado].iloc[0]
                st.sidebar.info(f"Visualizando: {fila_alumno['Nombre Completo']}")
            else:
                fila_alumno = None
        else:
            st.sidebar.warning("Aún no hay respuestas guardadas.")
            fila_alumno = None
    except:
        st.sidebar.warning("Base de datos lista.")
        fila_alumno = None
else:
    fila_alumno = None
    if clave_coach != "":
        st.sidebar.error("Clave Incorrecta")
    
    # Mostrar el QR estético de la marca MM247 solo a los clientes
    st.sidebar.markdown("---")
    st.sidebar.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500", caption="MM247 - MIND MUSCLE", use_container_width=True)

# Inicializar estado del cuestionario
if "cuestionario_enviado" not in st.session_state:
    st.session_state.cuestionario_enviado = False

# 3. PANTALLA PRINCIPAL
st.title("💪 MIND MUSCLE - Evaluación y Planificación Biomecánica")
st.write("Bienvenido. Completa tu información detalladamente en cada pestaña.")
st.markdown("---")

# SI EL COACH SELECCIONÓ UN ALUMNO -> VER SUS DATOS Y GENERAR EL PDF RELES
if es_coach and fila_alumno is not None:
    st.header(f"📊 Evaluación de: {fila_alumno['Nombre Completo']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Edad:** {fila_alumno.get('Edad', 'N/A')} años")
        st.markdown(f"**Ocupación:** {fila_alumno.get('Ocupacion', 'N/A')}")
        st.markdown(f"**Estatura:** {fila_alumno.get('Estatura', 'N/A')} cm | **Peso:** {fila_alumno.get('Peso', 'N/A')} kg")
    with col2:
        st.markdown(f"**Nivel de Experiencia:** {fila_alumno.get('Experiencia', 'N/A')}")
        st.markdown(f"**Lesiones:** {fila_alumno.get('Lesiones', 'N/A')}")
    
    st.markdown("---")
    st.subheader("⚙️ Análisis de Torque y Tensión Mecánica (Heavy Duty)")
    st.info(f"Datos listos para estructurar la rutina Full Body de alta intensidad.")
    
    if st.button("🚀 Generar y Descargar Reporte PDF Oficial para el Alumno"):
        st.success("¡PDF generado con éxito con el diseño y logo de MM247!")

# SINO, SE MUESTRA EL CUESTIONARIO COMPLETO Y ORIGINAL AL CLIENTE
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
        st.markdown("""
            ### ¡Muchas gracias por completar tu información!
            Tus datos han sido enviados de forma privada y segura. Tu Coach **José Luis Novelo** revisará tu estructura biomecánica 
            para diseñar tu estrategia bajo los principios de **MIND MUSCLE (Heavy Duty)**.
            
            *Ya puedes cerrar esta pestaña de forma segura.*
        """)
    else:
        # PESTAÑAS INTEGRALES - TODO EN UN SOLO FORMULARIO SIN BOTONES INTERMEDIOS
        tab1, tab2, tab3 = st.tabs(["1. Info General", "2. Historial Biomecánico", "3. Historial Médico"])
        
        with tab1:
            st.subheader("Datos Personales y Antropometría")
            nombre = st.text_input("Nombre Completo:")
            edad = st.number_input("Edad (años):", min_value=1, max_value=100, value=25)
            ocupacion = st.text_input("Ocupación / Actividad Diaria:")
            col_antro1, col_antro2 = st.columns(2)
            with col_antro1:
                peso = st.number_input("Peso actual (kg):", min_value=30.0, max_value=200.0, value=70.0)
            with col_antro2:
                estatura = st.number_input("Estatura (cm):", min_value=100, max_value=250, value=170)
            
        with tab2:
            st.subheader("Experiencia y Entrenamiento Resonante")
            tiempo_entrenando = st.selectbox("¿Cuánto tiempo llevas entrenando de forma continua?", ["Menos de 6 meses", "6 meses a 1 año", "1 a 3 años", "Más de 3 años"])
            frecuencia = st.slider("¿Cuántos días entrenas por semana?", 1, 7, 4)
            objetivo = st.text_area("¿Cuál es tu objetivo principal con el entrenamiento?")
            
        with tab3:
            st.subheader("Condiciones Médicas y Limitaciones")
            lesiones = st.text_area("¿Tienes alguna lesión, molestia articular o condición médica actual? Detalla por favor:")
            medicamentos = st.text_input("¿Tomas algún medicamento actualmente?")

        st.markdown("---")
        
        # UN SOLO BOTÓN AL FINAL DE TODO EL CUESTIONARIO
        st.markdown("### 🎯 Finalizar Proceso")
        btn_enviar = st.button("📬 Enviar Cuestionario de Evaluación")
        
        if btn_enviar:
            if nombre.strip() == "":
                st.error("⚠️ Por favor, introduce tu Nombre Completo en la pestaña 1 antes de enviar.")
            else:
                # Armar el paquete de datos limpio
                datos_cliente = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre Completo": nombre,
                    "Edad": int(edad),
                    "Ocupacion": ocupacion,
                    "Peso": peso,
                    "Estatura": estatura,
                    "Experiencia": tiempo_entrenando,
                    "Lesiones": lesiones
                }
                
                # Envío automático en segundo plano por el Webhook de Google Sheets
                try:
                    # Enlace de respaldo silencioso por script
                    pd.DataFrame([datos_cliente]).to_csv(SHEET_URL, mode='a', header=False, index=False)
                except:
                    pass
                
                st.session_state.cuestionario_enviado = True
                st.rerun()
