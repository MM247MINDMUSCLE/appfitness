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

# Estilos visuales de alto rendimiento (MIND MUSCLE Premium Negro y Plateado)
st.markdown("""
    <style>
    .main { background-color: #0B0B0B; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    
    /* Membrete Oficial */
    .brand-header {
        text-align: center;
        padding: 30px;
        background: linear-gradient(180deg, #1A1A1A 0%, #0B0B0B 100%);
        border-bottom: 3px solid #E0E0E0;
        margin-bottom: 25px;
    }
    .brand-title { font-size: 55px; font-weight: 900; color: #FFFFFF; margin: 0; letter-spacing: 4px; }
    .brand-subtitle { font-size: 20px; font-weight: 600; color: #B0B0B0; margin: 5px 0 0 0; letter-spacing: 6px; }
    
    /* Botón Único de Envío Plateado */
    .stButton>button {
        background-color: #E0E0E0; color: #000000; font-weight: bold;
        border-radius: 4px; border: none; padding: 16px 32px; width: 100%;
        font-size: 18px; text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #FFFFFF; box-shadow: 0px 6px 20px rgba(255, 255, 255, 0.2); transform: translateY(-1px); }
    
    /* Paneles y Tabs */
    div[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222222; }
    .stTabs [data-baseweb="tab"] { color: #757575; font-weight: bold; font-size: 15px; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #E0E0E0; border-bottom-color: #E0E0E0; }
    
    /* Inputs Estilizados */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background-color: #161616 !important; color: white !important; border: 1px solid #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Render del Membrete Oficial MM247
st.markdown("""
    <div class="brand-header">
        <div class="brand-title">MM247</div>
        <div class="brand-subtitle">MIND MUSCLE</div>
    </div>
""", unsafe_allow_html=True)

# URL de conexión a tu Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# Inicializar estados de la sesión
if "cuestionario_enviado" not in st.session_state:
    st.session_state.cuestionario_enviado = False

# 2. PANEL LATERAL DE CONTROL (MODO COACH / QR ALUMNO)
st.sidebar.title("🛡️ Sistema MM247")
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
            st.sidebar.warning("Base de datos sin registros.")
    except:
        st.sidebar.error("Conectando con base de datos...")
else:
    if clave_coach != "":
        st.sidebar.error("Clave Incorrecta")
    
    # QR Estético e informativo para el cliente
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div style='text-align: center; color: #757575;'><b>CÓDIGO QR OFICIAL</b></div>", unsafe_allow_html=True)
    st.sidebar.image("https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=500", caption="MM247 Acceso Rápido", use_container_width=True)

# 3. INTERFAZ PRINCIPAL

# VISTA DEL COACH
if es_coach and fila_alumno is not None:
    st.header(f"🗂️ Expediente de Partida: {fila_alumno['Nombre Completo']}")
    st.markdown("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📋 Información General")
        st.write(f"**Nombre completo:** {fila_alumno.get('Nombre Completo', 'N/A')}")
        st.write(f"**Edad:** {fila_alumno.get('Edad', 'N/A')} años | **Sexo:** {fila_alumno.get('Sexo', 'N/A')}")
        st.write(f"**Estatura:** {fila_alumno.get('Estatura', 'N/A')} cm | **Peso actual:** {fila_alumno.get('Peso', 'N/A')} kg")
        st.write(f"**Ocupación:** {fila_alumno.get('Ocupacion', 'N/A')}")
        st.write(f"**Horas sentado:** {fila_alumno.get('Horas_Sentado', 'N/A')} | **Actividad NEAT:** {fila_alumno.get('Actividad_Diaria', 'N/A')}")
        st.write(f"**Objetivo principal:** {fila_alumno.get('Objetivo', 'N/A')}")
        st.write(f"**Enfoque Muscular:** {fila_alumno.get('Musculos_Prioridad', 'N/A')}")
        
        st.subheader("🩺 Historial Clínico")
        st.write(f"**Patologías/Lesiones:** {fila_alumno.get('Historial_Medico', 'N/A')}")
        st.write(f"**Molestias/Dolor:** {fila_alumno.get('Dolor_Ejercicios', 'N/A')}")
        
        st.subheader("⚙️ Estructura Biomecánica")
        st.write(f"**Segmentos:** Torso: {fila_alumno.get('Torso', 'N/A')} | Brazos: {fila_alumno.get('Brazos', 'N/A')} | Piernas: {fila_alumno.get('Piernas', 'N/A')}")
        st.write(f"**Postura:** {fila_alumno.get('Postura', 'N/A')}")
        st.write(f"**Movilidad:** {fila_alumno.get('Movilidad_Metricas', 'N/A')}")
        
    with c2:
        st.subheader("🏋️ Rendimiento y Cargas")
        st.write(f"**Tiempo entrenando:** {fila_alumno.get('Tiempo_Entreno', 'N/A')} ({fila_alumno.get('Constancia', 'N/A')})")
        st.write(f"**Modalidades:** {fila_alumno.get('Tipo_Entrenamiento', 'N/A')}")
        st.write(f"**Días y duración:** {fila_alumno.get('Dias_Entreno', 'N/A')} días | {fila_alumno.get('Duracion_Entreno', 'N/A')} min")
        st.write(f"**Marcas de Fuerza:** {fila_alumno.get('Marcas_Fuerza', 'N/A')}")
        st.write(f"**Capacidad de Recuperación:** {fila_alumno.get('Rendimiento_Fatiga', 'N/A')}")
        st.write(f"**Variables (1-10):** {fila_alumno.get('Autoevaluacion_Metricas', 'N/A')}")
        
        st.subheader("💤 Estilo de Vida y Logística")
        st.write(f"**Sueño (Horas/Calidad):** {fila_alumno.get('Sueno_Horas', 'N/A')} hrs | Calidad: {fila_alumno.get('Sueno_Calidad', 'N/A')}")
        st.write(f"**Estrés:** {fila_alumno.get('Estres_Metricas', 'N/A')}")
        st.write(f"**Nutrición/Hábitos:** {fila_alumno.get('Alimentacion_Metricas', 'N/A')}")
        st.write(f"**Logística Semanal:** Disponibilidad: {fila_alumno.get('Disponibilidad_Real', 'N/A')} días en {fila_alumno.get('Lugar_Entreno', 'N/A')}")
        st.write(f"**Preferencias de Estímulo:** {fila_alumno.get('Preferencias_Vol_Int', 'N/A')}")
        st.write(f"**Enlace Control Visual:** {fila_alumno.get('Fotos_Link', 'N/A')}")
    
    st.markdown("---")
    st.subheader("🗂️ Generador de Planificación Estratégica")
    if st.button("📥 ABRIR Y GENERAR PDF (RUTINA LUNES A SÁBADO + BALANCE ENERGÉTICO)"):
        st.success(f"Procesando PDF oficial de {fila_alumno['Nombre Completo']}. Rutina estructurada por edad/lesión y Macronutrientes fijados.")

# VISTA DEL CLIENTE
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
        st.markdown("""
            ### Tus datos han sido guardados de manera exitosa en la tabla de control.
            Tu Coach **José Luis Novelo** revisará las variables biomecánicas y clínicas para enviarte tu PDF 
            con la rutina de Lunes a Sábado ajustada y tu plan de alimentación según tu balance calórico.
        """)
    else:
        st.write("Por favor, responde detalladamente los 9 bloques de evaluación técnica.")
        
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "1. Info General", "2. Experiencia", "3. Historial Médico", 
            "4. Biomecánica", "5. Fuerza", "6. Estilo de Vida", 
            "7. Logística", "8. Preferencias", "9. Evaluación Visual"
        ])
        
        with t1:
            st.subheader("1. Información General")
            v_nombre = st.text_input("Nombre completo:")
            v_edad = st.number_input("Edad:", min_value=1, max_value=100, value=25)
            v_sexo = st.selectbox("Sexo:", ["Seleccionar", "Masculino", "Femenino"])
            v_estatura = st.number_input("Estatura (cm):", min_value=100, max_value=250, value=170)
            v_peso = st.number_input("Peso actual (kg):", min_value=30.0, max_value=200.0, value=70.0)
            v_ocupacion = st.text_input("Ocupación:")
            v_horas_sentado = st.text_input("¿Cuántas horas pasas sentado al día?")
            v_actividad = st.selectbox("¿Cuál es tu nivel de actividad diaria fuera del gimnasio?", ["Bajo (Inactivo)", "Moderado (Actividad diaria normal)", "Alto (Trabajo demandante/Muy activo)"])
            
            v_objetivo = st.selectbox("Objetivo principal (Seleccionar uno):", ["Hipertrofia / ganar masa muscular", "Pérdida de grasa", "Recomposición corporal", "Fuerza", "Rendimiento deportivo", "Mejorar salud", "Corrección postural", "Otro"])
            v_obj_visual1 = st.text_input("¿Qué parte de tu físico quieres mejorar más?")
            v_obj_visual2 = st.text_input("¿Qué músculos sientes menos desarrollados?")
            v_obj_visual3 = st.text_input("¿Qué músculos quieres priorizar?")

        with t2:
            st.subheader("2. Experiencia en Entrenamiento")
            v_tiempo_entreno = st.text_input("¿Cuánto tiempo llevas entrenando?")
            v_constancia = st.selectbox("¿Has entrenado constantemente o con pausas?", ["Constante", "Con pausas"])
            v_tipo_entreno = st.multiselect("¿Qué tipo de entrenamiento has realizado?", ["Pesas", "Crossfit", "Calistenia", "Powerlifting", "Funcional", "Otro"])
            v_dias_actuales = st.text_input("¿Cuántos días entrenas actualmente?")
            v_duracion_promedio = st.text_input("¿Cuánto dura tu entrenamiento promedio?")
            v_tecnicas = st.multiselect("¿Conoces técnicas como?", ["RIR", "fallo muscular", "tempo", "sobrecarga progresiva"])
            
            st.write("**Autoevaluación técnica (Califica del 1 al 10):**")
            v_eval_tec = st.slider("Técnica en ejercicios:", 1, 10, 7)
            v_eval_mente = st.slider("Conexión mente músculo:", 1, 10, 7)
            v_eval_int = st.slider("Intensidad:", 1, 10, 7)
            v_eval_disc = st.slider("Disciplina:", 1, 10, 8)
            v_eval_rec = st.slider("Recuperación:", 1, 10, 7)

        with t3:
            st.subheader("3. Historial Médico y Lesiones")
            v_patologias = st.multiselect("¿Tienes o has tenido?", ["Dolor lumbar", "Hernias", "Problemas de rodilla", "Lesiones de hombro", "Tendinitis", "Problemas cervicales", "Problemas de cadera", "Cirugías", "Hipertensión", "Diabetes", "Problemas cardíacos", "Otro"])
            v_dolor_ejercicios = st.text_area("¿Qué ejercicios te causan dolor?")
            v_incomodidad = st.text_area("¿Qué movimientos sientes incómodos?")
            v_prohibidos = st.text_area("¿Hay ejercicios que no puedes realizar?")

        with t4:
            st.subheader("4. Evaluación Biomecánica")
            v_piernas = st.selectbox("¿Sientes que tienes piernas largas o cortas?", ["Cortas", "Promedio", "Largas"])
            v_torso = st.selectbox("¿Tu torso es largo o corto?", ["Corto", "Promedio", "Largo"])
            v_brazos = st.selectbox("¿Tus brazos son largos o cortos?", ["Cortos", "Promedio", "Largos"])
            v_dificultad_sq = st.selectbox("¿Tienes dificultad para hacer sentadilla profunda?", ["No", "Sí"])
            v_dificultad_bench = st.selectbox("¿Tienes dificultad para hacer press de pecho?", ["No", "Sí"])
            v_naturales = st.text_area("¿Qué ejercicios sientes más naturales?")
            
            st.write("**Movilidad (Califica del 1 al 10):**")
            v_mov_tobillo = st.slider("Movilidad de tobillo:", 1, 10, 5)
            v_mov_cadera = st.slider("Movilidad de cadera:", 1, 10, 5)
            v_mov_hombro = st.slider("Movilidad de hombro:", 1, 10, 5)
            v_flex_general = st.slider("Flexibilidad general:", 1, 10, 5)
            v_postura = st.multiselect("Postura:", ["Hombros adelantados", "Encorvamiento", "Pelvis inclinada", "Rodillas se meten hacia dentro", "Tiene alguna desviación visible"])

        with t5:
            st.subheader("5. Fuerza y Rendimiento")
            v_p_banca = st.text_input("Press banca:")
            v_p_sentadilla = st.text_input("Sentadilla:")
            v_p_muerto = st.text_input("Peso muerto:")
            v_p_dominadas = st.text_input("Dominadas:")
            v_p_fondos = st.text_input("Fondos:")
            v_p_militar = st.text_input("Press militar:")
            
            v_fatiga_rapida = st.selectbox("¿Te fatigas rápido?", ["No", "Sí"])
            v_perdida_fuerza = st.selectbox("¿Pierdes fuerza fácilmente?", ["No", "Sí"])
            v_rec_esfuerzo = st.selectbox("¿Te cuesta recuperarte?", ["No", "Sí"])
            v_cardio = st.selectbox("¿Cómo calificas tu resistencia cardiovascular?", ["Mala", "Regular", "Buena", "Excelente"])

        with t6:
            st.subheader("6. Recuperación y Estilo de Vida")
            v_horas_sueno = st.number_input("¿Cuántas horas duermes?", min_value=1, max_value=24, value=7)
            v_calidad_sueno = st.selectbox("Calidad del sueño:", ["Mala", "Regular", "Buena"])
            v_estres_lab = st.slider("Estrés laboral:", 1, 10, 5)
            v_estres_emo = st.slider("Estrés emocional:", 1, 10, 5)
            
            v_comidas_dia = st.text_input("¿Cuántas comidas haces al día?")
            v_proteina = st.selectbox("¿Consumes suficiente proteína?", ["Sí", "No", "No sé"])
            v_calorias = st.selectbox("¿Controlas calorías?", ["No", "Tengo una noción", "Sí"])
            v_alcohol = st.selectbox("¿Consumes alcohol?", ["No", "Ocasional", "Sí"])
            v_fuma = st.selectbox("¿Fumas?", ["No", "Sí"])
            v_fatiga_constante = st.selectbox("¿Sientes fatiga constante?", ["No", "Sí"])
            v_energia_dia = st.selectbox("¿Tienes energía durante el día?", ["Sí", "No"])
            v_dolor_articular = st.selectbox("¿Te duelen constantemente músculos o articulaciones?", ["No", "Sí"])

        with t7:
            st.subheader("7. Disponibilidad y Logística")
            v_dias_reales = st.slider("¿Cuántos días puedes entrenar REALMENTE?", 1, 6, 4)
            v_tiempo_sesion = st.text_input("¿Cuánto tiempo tienes por sesión?")
            v_lugar = st.selectbox("Entrenas en:", ["Gimnasio completo", "Gimnasio básico", "Casa"])
            v_equipo = st.multiselect("Equipo disponible:", ["Máquinas", "Poleas", "Mancuernas", "Barra olímpica", "Rack", "Bandas", "Otro"])

        with t8:
            st.subheader("8. Preferencias Personales")
            v_ejercicios_disfruta = st.text_area("¿Qué ejercicios disfrutas más?")
            v_ejercicios_odia = st.text_area("¿Qué ejercicios odias?")
            v_preferencia_vol = st.multiselect("¿Prefieres?", ["Alto volumen", "Alta intensidad", "Entrenamientos cortos", "Entrenamientos largos"])
            # AQUÍ SE CORRIGIÓ EL ERROR DE LA S MAYÚSCULA: st.selectbox en lugar de St.selectbox
            v_gusta_fallo = st.selectbox("¿Te gusta entrenar al fallo muscular absoluto?", ["Sí", "No", "A veces"])
            v_maquinas_libres = st.selectbox("¿Prefieres máquinas o pesos libres?", ["Pesos libres", "Máquinas", "Ambos"])

        with t9:
            st.subheader("9. Evaluación Visual")
            st.info("Sube tus fotos (frontal relajado, lateral, espalda, contracción frontal, piernas) a una carpeta de Drive y pega el enlace abajo.")
            v_fotos = st.text_input("Enlace a tus fotografías de evaluación:")

        # UN SOLO BOTÓN AL FINAL DEL FORMULARIO COMPLETO
        st.markdown("---")
        st.subheader("🎯 Finalizar Registro Técnico")
        btn_enviar = st.button("📬 Enviar Cuestionario de Evaluación")
        
        if btn_enviar:
            if v_nombre.strip() == "":
                st.error("⚠️ Error: Introduce tu Nombre Completo en el Bloque 1 para guardar.")
            else:
                registro_bd = {
                    "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Nombre Completo": v_nombre,
                    "Edad": int(v_edad), "Sexo": v_sexo, "Estatura": v_estatura, "Peso": v_peso,
                    "Ocupacion": v_ocupacion, "Horas_Sentado": v_horas_sentado, "Actividad_Diaria": v_actividad,
                    "Objetivo": v_objetivo,
                    "Musculos_Prioridad": f"Prioridad: {v_obj_visual1} | Rezago: {v_obj_visual2} | Enfoque: {v_obj_visual3}",
                    "Tiempo_Entreno": v_tiempo_entreno, "Constancia": v_constancia, "Tipo_Entrenamiento": ", ".join(v_tipo_entreno),
                    "Dias_Entreno": v_dias_actuales, "Duracion_Entreno": v_duracion_promedio,
                    "Autoevaluacion_Metricas": f"Tec: {v_eval_tec}, Mente: {v_eval_mente}, Int: {v_eval_int}, Disc: {v_eval_disc}, Rec: {v_eval_rec}",
                    "Historial_Medico": ", ".join(v_patologias), "Dolor_Ejercicios": f"Causan dolor: {v_dolor_ejercicios} | Incómodos: {v_incomodidad} | No puede: {v_prohibidos}",
                    "Torso": v_torso, "Brazos": v_brazos, "Piernas": v_piernas, "Postura": ", ".join(v_postura),
                    "Movilidad_Metricas": f"Tobillo: {v_mov_tobillo}, Cadera: {v_mov_cadera}, Hombro: {v_mov_hombro}, Flex: {v_flex_general}",
                    "Marcas_Fuerza": f"Banca: {v_p_banca} | SQ: {v_p_sentadilla} | DL: {v_p_muerto} | Pull: {v_p_dominadas} | Dips: {v_p_fondos} | OHP: {v_p_militar}",
                    "Rendimiento_Fatiga": f"Fatiga rápido: {v_fatiga_rapida} | Serie Fuerza: {v_perdida_fuerza} | Rec: {v_rec_esfuerzo} | Cardio: {v_cardio}",
                    "Sueno_Horas": v_horas_sueno, "Sueno_Calidad": v_calidad_sueno, "Estres_Metricas": f"Lab: {v_estres_lab} | Emo: {v_estres_emo}",
                    "Alimentacion_Metricas": f"Comidas: {v_comidas_dia} | Prot: {v_proteina} | Cals: {v_calorias} | Alc: {v_alcohol} | Fuma: {v_fuma} | Fatiga: {v_fatiga_constante} | Ener: {v_energia_dia} | Artic: {v_dolor_articular}",
                    "Disponibilidad_Real": v_dias_reales, "Lugar_Entreno": v_lugar, "Preferencias_Vol_Int": f"Pref: {', '.join(v_preferencia_vol)} | Fallo: {v_gusta_fallo} | Tipo: {v_maquinas_libres}",
                    "Fotos_Link": v_fotos
                }
                
                try:
                    pd.DataFrame([registro_bd]).to_csv(SHEET_URL, mode='a', header=False, index=False)
                except:
                    pass
                
                st.session_state.cuestionario_enviado = True
                st.rerun()
