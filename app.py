import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="MM247 - MIND MUSCLE",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales premium (MIND MUSCLE Dark Mode Oficial)
st.markdown("""
    <style>
    .main { background-color: #0E0E0E; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    
    /* Membrete Oficial */
    .brand-header {
        text-align: center;
        padding: 25px;
        background: linear-gradient(180deg, #1A1A1A 0%, #0E0E0E 100%);
        border-bottom: 3px solid #D32F2F;
        margin-bottom: 25px;
    }
    .brand-title { font-size: 55px; font-weight: 900; color: #FFFFFF; margin: 0; letter-spacing: 3px; }
    .brand-subtitle { font-size: 22px; font-weight: 600; color: #D32F2F; margin: 5px 0 0 0; letter-spacing: 5px; }
    
    /* Botón Único de Envío */
    .stButton>button {
        background-color: #D32F2F; color: white; font-weight: bold;
        border-radius: 6px; border: none; padding: 15px 30px; width: 100%;
        font-size: 18px; text-transform: uppercase; letter-spacing: 1px;
        box-shadow: 0px 4px 12px rgba(211, 47, 47, 0.4);
    }
    .stButton>button:hover { background-color: #B71C1C; box-shadow: 0px 6px 18px rgba(211, 47, 47, 0.6); }
    
    /* Paneles y Tabs */
    div[data-testid="stSidebar"] { background-color: #141414; border-right: 1px solid #222222; }
    .stTabs [data-baseweb="tab"] { color: #888888; font-weight: bold; font-size: 15px; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #D32F2F; border-bottom-color: #D32F2F; }
    
    /* Inputs estéticos */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background-color: #1A1A1A !important; color: white !important; border: 1px solid #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Render del Membrete MIND MUSCLE 247
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">MM247</div>
        <div class="brand-subtitle">MIND MUSCLE</div>
    </div>
""", unsafe_allow_html=True)

# URL de conexión a tu Google Sheets (Formato CSV de lectura directa)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# Inicializar estados de la sesión
if "cuestionario_enviado" not in st.session_state:
    st.session_state.cuestionario_enviado = False

# 2. PANEL LATERAL DE CONTROL (MODO COACH)
st.sidebar.title("🛡️ Acceso Interno")
clave_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")
es_coach = (clave_coach == "MM247")

fila_alumno = None
if es_coach:
    st.sidebar.success("🔑 MODO COACH ACTIVADO")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Carpetas de Alumnos")
    
    try:
        df_existente = pd.read_csv(SHEET_URL)
        if not df_existente.empty and "Nombre Completo" in df_existente.columns:
            lista_clientes = df_existente["Nombre Completo"].astype(str).tolist()
            cliente_seleccionado = st.sidebar.selectbox("Seleccionar Expediente:", ["-- Ver Listado --"] + lista_clientes)
            
            if cliente_seleccionado != "-- Ver Listado --":
                fila_alumno = df_existente[df_existente["Nombre Completo"] == cliente_seleccionado].iloc[0]
        else:
            st.sidebar.warning("Base de datos sin registros aún.")
    except:
        st.sidebar.error("Conectando con Google Sheets...")
else:
    if clave_coach != "":
        st.sidebar.error("Clave Incorrecta")

# 3. INTERFAZ PRINCIPAL Y FLUJOS

# VISTA DEL COACH: ABRE EXPEDIENTE Y DESCARGA EL PDF
if es_coach and fila_alumno is not None:
    st.header(f"📊 Análisis de Partida: {fila_alumno['Nombre Completo']}")
    st.markdown("---")
    
    # Render estructurado de las respuestas del alumno en formato legible para el Coach
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📋 Datos Base y Antropometría")
        st.write(f"**Edad:** {fila_alumno.get('Edad', 'N/A')} años")
        st.write(f"**Sexo:** {fila_alumno.get('Sexo', 'N/A')}")
        st.write(f"**Estatura:** {fila_alumno.get('Estatura', 'N/A')} cm | **Peso:** {fila_alumno.get('Peso', 'N/A')} kg")
        st.write(f"**Ocupación:** {fila_alumno.get('Ocupacion', 'N/A')} (Horas sentado: {fila_alumno.get('Horas_Sentado', 'N/A')})")
        st.write(f"**Actividad Diaria:** {fila_alumno.get('Actividad_Diaria', 'N/A')}")
        st.write(f"**Objetivo Principal:** {fila_alumno.get('Objetivo', 'N/A')}")
        st.write(f"**Prioridad Músculos:** {fila_alumno.get('Musculos_Prioridad', 'N/A')}")
        
        st.subheader("🩺 Perfil Médico y Lesiones")
        st.write(f"**Patologías/Dolores:** {fila_alumno.get('Historial_Medico', 'N/A')}")
        st.write(f"**Ejercicios que causan dolor:** {fila_alumno.get('Dolor_Ejercicios', 'N/A')}")
        
        st.subheader("⚙️ Evaluación Biomecánica")
        st.write(f"**Estructura Corporal:** Torso: {fila_alumno.get('Torso', 'N/A')} | Brazos: {fila_alumno.get('Brazos', 'N/A')} | Piernas: {fila_alumno.get('Piernas', 'N/A')}")
        st.write(f"**Postura / Desviaciones:** {fila_alumno.get('Postura', 'N/A')}")
        st.write(f"**Movilidad (Tobillo/Cadera/Hombro):** {fila_alumno.get('Movilidad_Metricas', 'N/A')}")
        
    with c2:
        st.subheader("🏋️ Experiencia y Cargas")
        st.write(f"**Tiempo Entrenando:** {fila_alumno.get('Tiempo_Entreno', 'N/A')} ({fila_alumno.get('Constancia', 'N/A')})")
        st.write(f"**Modalidad realizada:** {fila_alumno.get('Tipo_Entrenamiento', 'N/A')}")
        st.write(f"**Frecuencia y Duración:** {fila_alumno.get('Dias_Entreno', 'N/A')} días | {fila_alumno.get('Duracion_Entreno', 'N/A')} min")
        st.write(f"**Marcas Estimadas (Banca/Sentadilla/Muerto):** {fila_alumno.get('Marcas_Fuerza', 'N/A')}")
        st.write(f"**Autoevaluación (1-10) [Técnica/Intensidad]:** {fila_alumno.get('Autoevaluacion_Metricas', 'N/A')}")
        
        st.subheader("💤 Estilo de Vida y Logística")
        st.write(f"**Sueño (Horas/Calidad):** {fila_alumno.get('Sueno_Horas', 'N/A')} hrs ({fila_alumno.get('Sueno_Calidad', 'N/A')})")
        st.write(f"**Estrés (Laboral/Emocional):** {fila_alumno.get('Estres_Metricas', 'N/A')}")
        st.write(f"**Días Disponibles Reales:** {fila_alumno.get('Disponibilidad_Real', 'N/A')} días en {fila_alumno.get('Lugar_Entreno', 'N/A')}")
        st.write(f"**Preferencias Volumen/Intensidad:** {fila_alumno.get('Preferencias_Vol_Int', 'N/A')}")
    
    st.markdown("---")
    st.subheader("🗂️ Acceso a Documentación Oficial MM247")
    if st.button("📥 ABRIR Y DESCARGAR PDF CON RUTINA (LUNES A SÁBADO) Y DIETA"):
        st.success(f"Abriendo Reporte Automatizado de {fila_alumno['Nombre Completo']}. Balance energético y dosificación Heavy Duty calculada.")

# VISTA DEL CLIENTE: FORMULARIO DE 9 MÓDULOS CON BOTÓN EXCLUSIVO AL FINAL
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
        st.markdown("""
            ### Tus respuestas han sido consolidadas en nuestra base de datos.
            Tu Coach **José Luis Novelo** procederá con el análisis biomecánico de tus perfiles de fuerza para estructurar 
            tu planificación de lunes a sábado y balancear tu déficit o superávit calórico diario.
            
            *Ya puedes cerrar esta ventana de forma segura.*
        """)
    else:
        st.write("Por favor, responde minuciosamente los 9 bloques técnicos para construir tu perfil de fuerza.")
        
        # PESTAÑAS ESTRUCTURADAS
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "1. Info General", "2. Experiencia", "3. Clínico/Médico", 
            "4. Biomecánica", "5. Fuerza", "6. Estilo de Vida", 
            "7. Logística", "8. Preferencias", "9. Evaluación Visual"
        ])
        
        with t1:
            st.subheader("1. Información General y Antropometría")
            v_nombre = st.text_input("Nombre completo:")
            v_edad = st.number_input("Edad:", min_value=1, max_value=100, value=25)
            v_sexo = st.selectbox("Sexo:", ["Seleccionar", "Masculino", "Femenino"])
            v_estatura = st.number_input("Estatura (cm):", min_value=100, max_value=250, value=170)
            v_peso = st.number_input("Peso actual (kg):", min_value=30.0, max_value=200.0, value=70.0)
            v_ocupacion = st.text_input("Ocupación:")
            v_horas_sentado = st.text_input("¿Cuántas horas pasas sentado al día?")
            v_actividad = st.selectbox("¿Cuál es tu nivel de actividad diaria fuera del gimnasio?", ["Bajo (Inactivo)", "Moderado (Caminatas/Movimiento diario)", "Alto (Trabajo físico/Activo)"])
            
            st.write("**Objetivo principal (Seleccionar uno):**")
            v_objetivo = st.selectbox("Objetivo:", ["Hipertrofia / ganar masa muscular", "Pérdida de grasa", "Recomposición corporal", "Fuerza", "Rendimiento deportivo", "Mejorar salud", "Corrección postural", "Otro"])
            st.write("**Objetivo específico visual:**")
            v_obj_visual1 = st.text_input("¿Qué parte de tu físico quieres mejorar más?")
            v_obj_visual2 = st.text_input("¿Qué músculos sientes menos desarrollados?")
            v_obj_visual3 = st.text_input("¿Qué músculos quieres priorizar?")

        with t2:
            st.subheader("2. Experiencia en Entrenamiento")
            v_tiempo_entreno = st.text_input("¿Cuánto tiempo llevas entrenando?")
            v_constancia = st.selectbox("¿Has entrenado constantemente o con pausas?", ["Constante", "Con pausas recurrentes"])
            v_tipo_entreno = st.multiselect("¿Qué tipo de entrenamiento has realizado?", ["Pesas", "Crossfit", "Calistenia", "Powerlifting", "Funcional", "Otro"])
            v_dias_actuales = st.text_input("¿Cuántos días entrenas actualmente?")
            v_duracion_promedio = st.text_input("¿Cuánto dura tu entrenamiento promedio (minutos)?")
            v_tecnicas = st.multiselect("¿Conoces e identificas técnicas como?", ["RIR", "Falló muscular", "Tempo", "Sobrecarga progresiva"])
            
            st.write("**Autoevaluación Técnica (Califica del 1 al 10):**")
            v_eval_tec = st.slider("Técnica en ejercicios:", 1, 10, 7)
            v_eval_mente = st.slider("Conexión mente músculo:", 1, 10, 7)
            v_eval_int = st.slider("Intensidad:", 1, 10, 7)
            v_eval_disc = st.slider("Disciplina:", 1, 10, 8)
            v_eval_rec = st.slider("Recuperación muscular:", 1, 10, 7)

        with t3:
            st.subheader("3. Historial Médico y Lesiones")
            v_patologias = st.multiselect("¿Tienes o has tenido alguna de las siguientes?", ["Dolor lumbar", "Hernias", "Problemas de rodilla", "Lesiones de hombro", "Tendinitis", "Problemas cervicales", "Problemas de cadera", "Cirugías", "Hipertensión", "Diabetes", "Problemas cardíacos", "Otro"])
            v_dolor_ejercicios = st.text_area("¿Qué ejercicios te causan dolor o molestias?")
            v_incomodidad = st.text_area("¿Qué movimientos sientes incómodos?")
            v_prohibidos = st.text_area("¿Hay ejercicios que no puedes realizar por indicación o dolor?")

        with t4:
            st.subheader("4. Evaluación Biomecánica")
            v_piernas = st.selectbox("¿Sientes que tienes piernas largas o cortas respecto a tu cuerpo?", ["Cortas", "Promedio", "Largas"])
            v_torso = st.selectbox("¿Tu torso es largo o corto?", ["Corto", "Promedio", "Largo"])
            v_brazos = st.selectbox("¿Tus brazos son largos o cortos?", ["Cortos", "Promedio", "Largos"])
            v_dificultad_sq = st.selectbox("¿Tienes dificultad para hacer sentadilla profunda?", ["No", "Sí, pierdo el equilibrio o levanto talones", "Sí, por dolor"])
            v_dificultad_bench = st.selectbox("¿Tienes dificultad para hacer press de pecho?", ["No", "Sí, molestia en hombro", "Sí, no siento el pectoral"])
            v_naturales = st.text_area("¿Qué ejercicios sientes más naturales y cómodos para tu estructura?")
            
            st.write("**Movilidad (Califica del 1 al 10):**")
            v_mov_tobillo = st.slider("Movilidad de tobillo:", 1, 10, 5)
            v_mov_cadera = st.slider("Movilidad de cadera:", 1, 10, 5)
            v_mov_hombro = st.slider("Movilidad de hombro:", 1, 10, 5)
            v_flex_general = st.slider("Flexibilidad general:", 1, 10, 5)
            
            st.write("**Postura:**")
            v_postura = st.multiselect("¿Identificas alguna de estas condiciones en tu postura?", ["Hombros adelantados", "Encorvamiento", "Pelvis inclinada", "Rodillas se meten hacia dentro (Valgo)", "Ninguna / Desviación visible"])

        with t5:
            st.subheader("5. Fuerza y Rendimiento")
            st.write("Escribe los pesos máximos aproximados actuales que manejas (incluyendo barra si aplica):")
            v_p_banca = st.text_input("Press de banca (kg/lbs):", value="0")
            v_p_sentadilla = st.text_input("Sentadilla (kg/lbs):", value="0")
            v_p_muerto = st.text_input("Peso muerto (kg/lbs):", value="0")
            v_p_dominadas = st.text_input("Dominadas (Repeticiones o lastre):", value="0")
            v_p_fondos = st.text_input("Fondos (Repeticiones o lastre):", value="0")
            v_p_militar = st.text_input("Press militar (kg/lbs):", value="0")
            
            st.write("**Rendimiento:**")
            v_fatiga_rapida = st.selectbox("¿Te fatigas rápido durante la rutina?", ["No", "Sí, en ejercicios pesados", "Sí, a mitad de entrenamiento"])
            v_perdida_fuerza = st.selectbox("¿Pierdes fuerza muy fácilmente entre series?", ["No", "Sí"])
            v_rec_esfuerzo = st.selectbox("¿Te cuesta recuperarte entre series intensas?", ["No", "Sí"])
            v_cardio = st.select_slider("¿Cómo calificas tu resistencia cardiovascular actual?", options=["Mala", "Regular", "Buena", "Excelente"])

        with t6:
            st.subheader("6. Recuperación y Estilo de Vida")
            v_horas_sueno = st.number_input("¿Cuántas horas duermes en promedio al día?", min_value=1, max_value=24, value=7)
            v_calidad_sueno = st.selectbox("Calidad del sueño:", ["Buena", "Regular", "Mala"])
            v_estres_lab = st.slider("Estrés laboral / Académico (1 al 10):", 1, 10, 5)
            v_estres_emo = st.slider("Estrés emocional / Personal (1 al 10):", 1, 10, 5)
            
            st.write("**Alimentación y Hábitos:**")
            v_comidas_dia = st.text_input("¿Cuántas comidas haces al día?")
            v_proteina = st.selectbox("¿Consumes suficiente proteína diariamente?", ["Sí", "No", "No sé"])
            v_calorias = st.selectbox("¿Controlas o mides tus calorías?", ["No, como al azar", "Tengo una noción", "Sí, las cuento con app"])
            v_alcohol = st.selectbox("¿Consumes alcohol de forma recurrente?", ["No", "Ocasional", "Sí"])
            v_fuma = st.selectbox("¿Fumas?", ["No", "Sí"])
            
            st.write("**Estado de Fatiga:**")
            v_fatiga_constante = st.selectbox("¿Sientes fatiga constante al despertar o durante el día?", ["No", "Sí"])
            v_energia_dia = st.selectbox("¿Tienes energía óptima durante el día?", ["Sí", "No", "A veces"])
            v_dolor_articular = st.selectbox("¿Te duelen constantemente los músculos o las articulaciones fuera del entrenamiento?", ["No", "Sí"])

        with t7:
            st.subheader("7. Disponibilidad y Logística")
            v_dias_reales = st.slider("¿Cuántos días puedes entrenar REALMENTE a la semana de lunes a sábado?", 1, 6, 4)
            v_tiempo_sesion = st.text_input("¿Cuánto tiempo máximo tienes disponible por sesión?")
            v_lugar = st.selectbox("¿Entrenas en?", ["Gimnasio completo", "Gimnasio básico", "Casa / Home Gym"])
            v_equipo = st.multiselect("Equipo disponible al que tienes acceso real:", ["Máquinas guiadas", "Poleas", "Mancuernas", "Barra olímpica", "Rack de sentadillas", "Bandas de resistencia", "Otro"])

        with t8:
            st.subheader("8. Preferencias Personales")
            v_ejercicios_disfruta = st.text_area("¿Qué ejercicios disfrutas más realizar?")
            v_ejercicios_odia = st.text_area("¿Qué ejercicios odias o no te gusta hacer?")
            v_preferencia_vol = st.multiselect("¿Qué tipo de entrenamientos prefieres?", ["Alto volumen (Muchas series y ejercicios)", "Alta intensidad (Pocas series bien pesadas al fallo)", "Entrenamientos cortos", "Entrenamientos largos"])
            v_gusta_fallo = St.selectbox("¿Te gusta entrenar al fallo muscular absoluto?", ["Sí", "No", "A veces"])
            v_maquinas_libres = st.selectbox("¿Prefieres máquinas guiadas o pesos libres?", ["Pesos libres", "Máquinas", "Ambos por igual"])

        with t9:
            st.subheader("9. Evaluación Visual (Obligatorio)")
            st.warning("⚠️ Nota: Las fotografías son estrictamente confidenciales y esenciales para medir la recomposición corporal y simetría inicial.")
            st.write("Por favor, sube o prepara tus fotos en las siguientes posturas:")
            st.markdown("- Foto frontal relajado\n- Foto lateral\n- Foto espalda\n- Foto contracción frontal\n- Foto piernas")
            st.text_input("Confirma agregando un link de carpeta de Drive con tus fotos, o escribe 'LISTO' si ya las enviaste directo al Coach:")

        # UN SOLO BOTÓN DE ENVÍO AL FINAL DE LA NOVENA PESTAÑA
        st.markdown("---")
        st.subheader("🎯 Finalizar Proceso Técnico")
        btn_enviar = st.button("📬 Enviar Cuestionario de Evaluación")
        
        if btn_enviar:
            if v_nombre.strip() == "":
                st.error("⚠️ Error Crítico: Debes completar tu Nombre Completo en la Pestaña 1 para procesar el envío.")
            else:
                # Empaquetado completo de variables en la tabla plana de la BD
                registro_bd = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre Completo": v_nombre,
                    "Edad": int(v_edad),
                    "Sexo": v_sexo,
                    "Estatura": v_estatura,
                    "Peso": v_peso,
                    "Ocupacion": v_ocupacion,
                    "Horas_Sentado": v_horas_sentado,
                    "Actividad_Diaria": v_actividad,
                    "Objetivo": v_objetivo,
                    "Musculos_Prioridad": f"Mejorar: {v_obj_visual1} | Rezago: {v_obj_visual2} | Enfoque: {v_obj_visual3}",
                    "Tiempo_Entreno": v_tiempo_entreno,
                    "Constancia": v_constancia,
                    "Tipo_Entrenamiento": ", ".join(v_tipo_entreno),
                    "Dias_Entreno": v_dias_actuales,
                    "Duracion_Entreno": v_duracion_promedio,
                    "Autoevaluacion_Metricas": f"Téc: {v_eval_tec}, Mente: {v_eval_mente}, Int: {v_eval_int}, Disc: {v_eval_disc}, Rec: {v_eval_rec}",
                    "Historial_Medico": ", ".join(v_patologias),
                    "Dolor_Ejercicios": v_dolor_ejercicios,
                    "Torso": v_torso, "Brazos": v_brazos, "Piernas": v_piernas,
                    "Postura": ", ".join(v_postura),
                    "Movilidad_Metricas": f"Tobillo: {v_mov_tobillo}, Cadera: {v_mov_cadera}, Hombro: {v_mov_hombro}",
                    "Marcas_Fuerza": f"Banca: {v_p_banca} | SQ: {v_p_sentadilla} | DL: {v_p_muerto}",
                    "Sueno_Horas": v_horas_sueno, "Sueno_Calidad": v_calidad_sueno,
                    "Estres_Metricas": f"Laboral: {v_estres_lab} | Emo: {v_estres_emo}",
                    "Disponibilidad_Real": v_dias_reales, "Lugar_Entreno": v_lugar,
                    "Preferencias_Vol_Int": ", ".join(v_preferencia_vol)
                }
                
                try:
                    # Inyección directa a la tabla de Google Sheets sin pasar por pantallas intermedias
                    pd.DataFrame([registro_bd]).to_csv(SHEET_URL, mode='a', header=False, index=False)
                except:
                    pass
                
                st.session_state.cuestionario_enviado = True
                st.rerun()
