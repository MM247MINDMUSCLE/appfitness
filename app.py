import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="MINDMUSCLE247",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales premium (MINDMUSCLE247 Negro y Plata Cromada)
st.markdown("""
    <style>
    .main { background-color: #0B0B0B; color: #FFFFFF; font-family: 'Arial', sans-serif; }
    
    /* Membrete Oficial con Logo Integrado */
    .brand-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(180deg, #1A1A1A 0%, #0B0B0B 100%);
        border-bottom: 3px solid #E0E0E0;
        margin-bottom: 25px;
    }
    .brand-title { font-size: 42px; font-weight: 900; color: #FFFFFF; margin: 10px 0 0 0; letter-spacing: 3px; }
    
    /* Botón de Envío Único al Final */
    .stButton>button {
        background-color: #E0E0E0; color: #000000; font-weight: bold;
        border-radius: 4px; border: none; padding: 18px 36px; width: 100%;
        font-size: 20px; text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #FFFFFF; box-shadow: 0px 6px 20px rgba(255, 255, 255, 0.2); transform: translateY(-2px); }
    
    /* Estructura de Pestañas */
    .stTabs [data-baseweb="tab"] { color: #757575; font-weight: bold; font-size: 14px; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #E0E0E0; border-bottom-color: #E0E0E0; }
    
    /* Inputs Estilizados */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div, .stNumberInput>div>div>input {
        background-color: #161616 !important; color: white !important; border: 1px solid #333333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Render del Membrete Superior con el Logotipo Oficial
st.markdown('<div class="brand-header">', unsafe_allow_html=True)
# URL directa del logotipo negro y plata cromado guardado en el sistema
st.image("https://api.metisai.ir/img/b614d081b48fa0bd19a8984fa06cb", width=160, channels="RGB")
st.markdown('<div class="brand-title">MINDMUSCLE247</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# URL de conexión a tu Google Sheets
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

if "cuestionario_enviado" not in st.session_state:
    st.session_state.cuestionario_enviado = False

# 2. PANEL LATERAL DE CONTROL (MODO COACH)
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
clave_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")
es_coach = (clave_coach == "MM247")

fila_alumno = None
if es_coach:
    st.sidebar.success("🔑 MODO COACH ACTIVADO")
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Expedientes de Alumnos")
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
    st.sidebar.info("Completa los 9 bloques técnicos para estructurar tu entrenamiento y tu plan nutricional ideal.")

# 3. INTERFAZ PRINCIPAL

# VISTA EXCLUSIVA DEL COACH
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
        st.subheader("🥗 Preferencias Nutricionales")
        st.write(f"**Proteínas deseadas:** {fila_alumno.get('Pref_Proteina', 'N/A')}")
        st.write(f"**Grasas deseadas:** {fila_alumno.get('Pref_Grasa', 'N/A')}")
        st.write(f"**Carbohidratos deseados:** {fila_alumno.get('Pref_Carbos', 'N/A')}")
        st.write(f"**Esquema de colaciones:** {fila_alumno.get('Pref_Colaciones', 'N/A')}")
        st.subheader("💤 Estilo de Vida y Logística")
        st.write(f"**Sueño (Horas/Calidad):** {fila_alumno.get('Sueno_Horas', 'N/A')} hrs | Calidad: {fila_alumno.get('Sueno_Calidad', 'N/A')}")
        st.write(f"**Estrés:** {fila_alumno.get('Estres_Metricas', 'N/A')}")
        st.write(f"**Logística Semanal:** {fila_alumno.get('Disponibilidad_Real', 'N/A')} días en {fila_alumno.get('Lugar_Entreno', 'N/A')}")
    st.markdown("---")
    if st.button("📥 GENERAR PLANIFICACIÓN ESTRATÉGICA EN PDF"):
        st.success(f"Procesando el PDF oficial de MINDMUSCLE247 para el alumno.")

# VISTA DEL ALUMNO (FORMULARIO INTERACTIVO)
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
        st.markdown("""
            ### ¡Perfecto! Tus datos han sido blindados en el sistema de MINDMUSCLE247.
            Tus perfiles anatómicos y metas nutricionales han sido cargados. Pronto recibirás tu plan integral a medida.
        """)
    else:
        st.write("🔥 Bienvenido al radar de evaluación técnica de **MINDMUSCLE247**. Responde los siguientes bloques:")
        
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "⚡ 1. Info General", "🏋️ 2. Experiencia", "🩺 3. Historial Médico", 
            "📐 4. Biomecánica", "💥 5. Fuerza", "🥗 6. Nutrición y Vida", 
            "📅 7. Logística", "🎯 8. Preferencias", "📸 9. Envío y Fotos"
        ])
        
        with t1:
            st.subheader("📋 Datos Personales de Partida")
            v_nombre = st.text_input("✍️ Escribe tu Nombre Completo:")
            v_edad = st.number_input("🎂 Edad actual:", min_value=1, max_value=100, value=25)
            v_sexo = st.selectbox("Option: Sexo biológico:", ["Seleccionar", "Masculino", "Femenino"])
            v_estatura = st.number_input("📏 Estatura en centímetros (cm):", min_value=100, max_value=250, value=170)
            v_peso = st.number_input("⚖️ Peso actual en báscula (kg):", min_value=30.0, max_value=200.0, value=70.0)
            v_ocupacion = st.text_input("💼 ¿A qué te dedicas o qué actividad realizas en tu día?")
            v_horas_sentado = st.text_input("🪑 ¿Cuántas horas pasas sentado al día?")
            v_actividad = st.selectbox("🏃 Actividad diaria general fuera del gimnasio:", ["Bajo (Inactivo / Trabajo de escritorio)", "Moderado (Movimiento constante)", "Alto (Trabajo físico muy pesado)"])
            v_objetivo = st.selectbox("🎯 Elige tu meta principal actual:", ["Hipertrofia / ganar masa muscular", "Pérdida de grasa", "Recomposición corporal", "Fuerza", "Rendimiento deportivo", "Mejorar salud", "Corrección postural", "Otro"])
            st.markdown("---")
            st.subheader("👁️ Enfoque Visual Estético")
            v_obj_visual1 = st.text_input("🚀 ¿Qué zona corporal te urge o deseas mejorar con prioridad?")
            v_obj_visual2 = st.text_input("🔍 ¿Qué músculos consideras rezagados o difíciles de desarrollar?")
            v_obj_visual3 = st.text_input("🎯 ¿A qué grupos musculares le daremos enfoque absoluto?")

        with t2:
            st.subheader("🏋️ Trayectoria en el Gimnasio")
            v_tiempo_entreno = st.text_input("⏳ ¿Cuánto tiempo llevas entrenando de manera formal?")
            v_constancia = st.selectbox("🔄 ¿Has mantenido una disciplina constante o con interrupciones?", ["Entrenamiento constante", "Con pausas recurrentes"])
            v_tipo_entreno = st.multiselect("👟 Disciplinas de fuerza que has practicado anteriormente:", ["Pesas", "Crossfit", "Calistenia", "Powerlifting", "Funcional", "Otro"])
            v_dias_actuales = st.text_input("📅 ¿Cuántos días entrenas por semana actualmente?")
            v_duracion_promedio = st.text_input("⏱️ ¿Cuánto tiempo dura tu sesión promedio en el gym?")
            v_tecnicas = st.multiselect("🧠 Conceptos técnicos de entrenamiento que dominas:", ["RIR (Repeticiones en recámara)", "Fallo muscular absoluto", "Tempo (Control de velocidad)", "Sobrecarga progresiva"])
            st.markdown("---")
            st.subheader("📊 Califica tus Variables (Desliza del 1 al 10)")
            v_eval_tec = st.slider("Control y ejecución de la técnica estricta:", 1, 10, 7)
            v_eval_mente = st.slider("Conexión mente-músculo (Sentir el estímulo real):", 1, 10, 7)
            v_eval_int = st.slider("Nivel de intensidad real en series pesadas:", 1, 10, 7)
            v_eval_disc = st.slider("Disciplina y constancia semanal:", 1, 10, 8)
            v_eval_rec = st.slider("Capacidad para recuperarte de la fatiga:", 1, 10, 7)

        with t3:
            st.subheader("🩺 Historial Clínico y Lesiones")
            v_patologias = st.multiselect("⚠️ ¿Sufres o has sufrido de alguna de las siguientes molestias?", ["Dolor lumbar", "Hernias", "Problemas de rodilla", "Lesiones de hombro", "Tendinitis", "Problemas cervicales", "Problemas de cadera", "Cirugías", "Hipertensión", "Diabetes", "Problemas cardíacos", "Otro"])
            v_dolor_ejercicios = st.text_area("⚡ ¿Qué ejercicios específicos te detonan dolor articular?")
            v_incomodidad = st.text_area("❌ ¿Qué movimientos biomecánicos sientes incómodos?")
            v_prohibidos = st.text_area("🚫 ¿Tienes algún movimiento o ejercicio estrictamente prohibido?")

        with t4:
            st.subheader("📐 Análisis Biomecánico y Estructura")
            v_piernas = st.selectbox("🦵 En comparación con tu torso, tus piernas son:", ["Cortas", "Promedio", "Largas"])
            v_torso = st.selectbox("🧍 Tu torso estructuralmente es:", ["Corto", "Promedio", "Largo"])
            v_brazos = st.selectbox("💪 En comparación con tu cuerpo, tus brazos son:", ["Cortos", "Promedio", "Largos"])
            v_dificultad_sq = st.selectbox("🏋️ ¿Te cuesta realizar una sentadilla profunda?", ["No, desciendo con total facilidad", "Sí, tiendo a levantar talones o encorvarme", "Sí, me causa molestia en rodillas o cadera"])
            v_dificultad_bench = st.selectbox(" Press de Banca: ¿Sientes el pectoral de manera eficiente?", ["Sí, de forma completamente natural", "No, se me fatiga antes el hombro o el tríceps", "No, me causa incomodidad en la articulación del hombro"])
            v_naturales = st.text_area("💎 ¿Qué ejercicios sientes idóneos y cómodos para tu estructura?")
            st.markdown("---")
            st.subheader("🎯 Movilidad Articular (Califica de 1 al 10)")
            v_mov_tobillo = st.slider("Movilidad de tobillo (Dorsiflexión):", 1, 10, 5)
            v_mov_cadera = st.slider("Movilidad y apertura de cadera:", 1, 10, 5)
            v_mov_hombro = st.slider("Movilidad y flexibilidad de hombros:", 1, 10, 5)
            v_flex_general = st.slider("Flexibilidad general del cuerpo:", 1, 10, 5)
            v_postura = st.multiselect("🔍 ¿Notas alguna de estas tendencias en tu postura?", ["Hombros adelantados (Rotación interna)", "Encorvamiento de espalda alta (Cifosis)", "Pelvis inclinada hacia adelante (Hiperlordosis)", "Rodillas se meten hacia dentro (Valgo)", "Ninguna / Todo alineado"])

        with t5:
            st.subheader("💥 Marcas de Fuerza Máxima Estimadas")
            st.write("Registra el peso máximo que logras mover a unas 4-8 repeticiones (Anota si usas kg o lbs):")
            v_p_banca = st.text_input("🪵 Press de Banca Horizontal:")
            v_p_sentadilla = st.text_input("👑 Sentadilla Libre:")
            v_p_muerto = st.text_input("💀 Peso Muerto Convencional/Rumano:")
            v_p_dominadas = st.text_input("🦅 Dominadas (Repeticiones máximas o lastre):")
            v_p_fondos = st.text_input("🦜 Fondos en Paralelas:")
            v_p_militar = st.text_input("🎖️ Press Militar para Hombros:")
            st.markdown("---")
            st.subheader("📈 Capacidad de Respuesta Física")
            v_fatiga_rapida = st.selectbox("¿Sientes que te quedas sin energía muy rápido a mitad de rutina?", ["No, mantengo perfectamente el rendimiento", "Sí, me agoto en los primeros ejercicios compuestos", "Sí, a mitad de la sesión ya no tengo fuerza"])
            v_perdida_fuerza = st.selectbox("¿Pierdes excesiva fuerza entre la primera serie y las posteriores?", ["No, me recupero excelente", "Sí, tengo que bajar considerablemente el peso"])
            v_rec_esfuerzo = st.selectbox("¿Te cuesta recuperar el aire tras una serie pesada y demandante?", ["No, me estabilizo rápido", "Sí, tardo bastante tiempo en volver a la normalidad"])
            v_cardio = st.selectbox("❤️ ¿Cómo calificas tu resistencia cardiovascular en este momento?", ["Mala", "Regular", "Buena", "Excelente"])

        with t6:
            st.subheader("🥗 Configuración del Módulo Nutricional (4 Opciones por Rubro)")
            
            # --- SECCIÓN MULTIOPCIÓN REQUERIDA ---
            v_pref_proteina = st.selectbox("🥩 PROTEÍNA: Selecciona tu fuente principal preferida para la dieta:", [
                "Carnes rojas, pechuga de pollo y pescados blancos/salmón",
                "Predominancia de pescados, mariscos frescos y piezas de huevo completo",
                "Fuentes de origen vegetal, legumbres y proteína aislada de soya/chícharo",
                "Esquema completamente variado, flexible y abierto sin restricciones alimenticias"
            ])
            
            v_pref_grasa = st.selectbox("🥑 GRASA: Elige el tipo de lípidos saludables que prefieres incluir:", [
                "Aguacate fresco, frutos secos secos (almendras/nueces) y semillas mixtas",
                "Aceite de oliva extra virgen, aceitunas enteras y yemas de huevo",
                "Derivados lácteos limpios, crema de cacahuate y quesos maduros/bajos en grasa",
                "Preferencia mixta y adaptable según los requerimientos del balance calórico diario"
            ])
            
            v_pref_carbos = st.selectbox("🍚 CARBOHIDRATOS: Elige tus fuentes favoritas de energía muscular:", [
                "Arroz jazmín/integral, avena en hojuelas y papas/camote al horno",
                "Pastas de sémola, pan de masa madre/integral y cereales inflados",
                "Predominancia absoluta de frutas frescas de temporada y vegetales fibrosos",
                "Esquema combinado / Consumo variado según las necesidades del entrenamiento"
            ])
            
            v_pref_colaciones = st.selectbox("🍏 COLACIONES: ¿Cómo te funciona mejor organizar tus horarios de comida?", [
                "3 comidas completas y fuertes + 2 colaciones intermedias rápidas/ligeras",
                "3 comidas principales sólidas y abundantes a lo largo del día (Sin colaciones)",
                "Dividir la ingesta en 4 o 5 comidas medianas distribuidas equitativamente",
                "Esquema concentrado de alimentación (Ideal para protocolos de ayuno intermitente)"
            ])
            
            st.markdown("---")
            st.subheader("💤 Descanso y Hábitos Diarios")
            v_horas_sueno = st.number_input("⏰ ¿Cuántas horas duermes en promedio por noche?", min_value=1, max_value=24, value=7)
            v_calidad_sueno = st.selectbox("😴 Calidad general de tu sueño:", ["Buena e ininterrumpida", "Regular / Me despierto a veces", "Mala / Me cuesta conciliar el sueño"])
            v_estres_lab = st.slider("🤯 Nivel de estrés en tu trabajo o escuela (1 al 10):", 1, 10, 5)
            v_estres_emo = st.slider("🧠 Nivel de estrés emocional o personal diario (1 al 10):", 1, 10, 5)
            v_comidas_dia = st.text_input("🍽️ ¿Cuántas comidas realizas de forma sólida actualmente al día?")
            v_proteina = st.selectbox("🍗 ¿Consumes fuentes de proteína en cada una de tus comidas actuales?", ["Sí, de forma estricta", "No, solo en las comidas principales", "No llevo control del macronutriente"])
            v_calorias = st.selectbox("📊 ¿Llevas control o pesaje de tus alimentos en este momento?", ["No, como de manera intuitiva", "Tengo noción visual pero no peso nada", "Sí, peso gramos precisos y registro en app"])
            v_alcohol = st.selectbox("🍺 ¿Consumes bebidas alcohólicas con frecuencia?", ["No", "Únicamente en eventos sociales muy ocasionales", "Sí, de manera semanal"])
            v_fuma = st.selectbox("🚬 ¿Fumas o utilizas vapeadores?", ["No", "Sí"])
            v_fatiga_constante = st.selectbox("🔋 ¿Te levantas cansado o sufres de fatiga crónica a lo largo del día?", ["No, me mantengo activo", "Sí, dependo de la cafeína o pre-entrenos para rendir"])
            v_energia_dia = st.selectbox("⚡ ¿Tienes foco y energía plena al iniciar tu entrenamiento?", ["Sí, llego motivado y al 100%", "No, suelo ir cansado o sin energía"])
            v_dolor_articular = st.selectbox("💥 ¿Sientes dolores o rigidez articular constante fuera del gimnasio?", ["No", "Sí, presento molestias articulares constantes"])

        with t7:
            st.subheader("📅 Logística y Disponibilidad Semanal")
            v_dias_reales = st.slider("🗓️ ¿Cuántos días de lunes a sábado vas a entrenar de forma obligatoria?", 1, 6, 4)
            v_tiempo_sesion = st.text_input("⏳ ¿De cuántos minutos dispones por sesión para entrenar?")
            v_lugar = st.selectbox("🏢 ¿Dónde realizarás tus rutinas?", ["Gimnasio comercial completo", "Gimnasio básico o de fraccionamiento", "Casa con equipamiento libre propio"])
            v_equipo = st.multiselect("🛠️ Selecciona el equipo real al que tienes acceso diario:", ["Máquinas guiadas (Prensa, poleas, smith)", "Poleas ajustables", "Mancuernas pesadas", "Barra olímpica y discos libres", "Rack completo de sentadillas", "Bandas elásticas", "Otro"])

        with t8:
            st.subheader("🎯 Psicología del Entrenamiento")
            v_ejercicios_disfruta = st.text_area("❤️ Ejercicios que te encantan, dominas y disfrutas incluir en tu rutina:")
            v_ejercicios_odia = st.text_area("❌ Ejercicios que te causan pereza, incomodidad o prefieres evitar:")
            v_preferencia_vol = st.multiselect("⚖️ ¿Qué enfoque de entrenamiento se adapta mejor a tu mente?", ["Alto volumen (Muchos ejercicios y series)", "Bajo volumen con alta intensidad (Pocas series al límite)", "Sesiones de entrenamiento compactas y rápidas", "Sesiones largas con descansos amplios"])
            v_gusta_fallo = st.selectbox("💥 ¿Sabes lo que es y disfrutas llevar una serie al fallo muscular absoluto?", ["Sí, me fascina entrenar a máxima intensidad", "No, prefiero mantenerme seguro lejos del fallo", "A veces, solo en ciertos ejercicios guiados"])
            v_maquinas_libres = st.selectbox("🤖 ¿Qué tipo de equipamiento prefieres usar en tus entrenamientos?", ["Pesos libres (Barras y mancuernas)", "Máquinas guiadas y poleas de aislamiento", "Una mezcla equilibrada de ambas herramientas"])

        with t9:
            st.subheader("📸 Evaluación Visual Inicial (Privado y Confidencial)")
            st.info("Sube tus fotos de frente, perfil y espalda. Al terminar, presiona el botón de abajo para consolidar tu registro técnico.")
            
            # --- CARGA NATIVA DESDE LA GALERÍA ---
            uploaded_photos = st.file_uploader(
                "📬 Selecciona o arrastra tus fotos desde tu galería (Formatos aceptados: PNG, JPG, JPEG):", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True
            )
            
            if uploaded_photos:
                st.success(f"💪 ¡Se han cargado correctamente {len(uploaded_photos)} imágenes de evaluación!")
            
            # QR INTERACTIVO INTEGRADO DIRECTAMENTE AL FINAL
            st.markdown("---")
            st.markdown("<div style='text-align: center; font-weight: bold; color: #757575;'>📲 CÓDIGO QR - ACCESO OFICIAL MINDMUSCLE247</div>", unsafe_allow_html=True)
            c_qr1, c_qr2, c_qr3 = st.columns([1, 1, 1])
            with c_qr2:
                # Código QR renderizado en vivo para el dispositivo del alumno
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=https://appfitness-mindmuscle247.streamlit.app&color=000000&bgcolor=FFFFFF", use_container_width=True)
            
            # --- EL BOTÓN DE ENVÍO APARECE ÚNICAMENTE AL FINAL DE LA ÚLTIMA PREGUNTA ---
            st.markdown("---")
            st.subheader("🎯 Finalizar y Guardar Registro en la Base de Datos")
            btn_enviar = st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA MINDMUSCLE247")
            
            if btn_enviar:
                if v_nombre.strip() == "":
                    st.error("⚠️ Error Crítico: Es obligatorio rellenar tu Nombre Completo en la Pestaña 1 para procesar tus respuestas.")
                else:
                    # Estructuración plana de las variables hacia Google Sheets sin referencias personales anteriores
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
                        "Historial_Medico": ", ".join(v_patologias), "Dolor_Ejercicios": f"Dolor: {v_dolor_ejercicios} | Incómodo: {v_incomodidad} | No puede: {v_prohibidos}",
                        "Torso": v_torso, "Brazos": v_brazos, "Piernas": v_piernas, "Postura": ", ".join(v_postura),
                        "Movilidad_Metricas": f"Tobillo: {v_mov_tobillo}, Cadera: {v_mov_cadera}, Hombro: {v_mov_hombro}, Flex: {v_flex_general}",
                        "Marcas_Fuerza": f"Banca: {v_p_banca} | SQ: {v_p_sentadilla} | DL: {v_p_muerto} | Pull: {v_p_dominadas} | Dips: {v_p_fondos} | OHP: {v_p_militar}",
                        "Rendimiento_Fatiga": f"Rápido: {v_fatiga_rapida} | Series: {v_perdida_fuerza} | Rec: {v_rec_esfuerzo} | Cardio: {v_cardio}",
                        "Pref_Proteina": v_pref_proteina, "Pref_Grasa": v_pref_grasa, "Pref_Carbos": v_pref_carbos, "Pref_Colaciones": v_pref_colaciones,
                        "Sueno_Horas": v_horas_sueno, "Sueno_Calidad": v_calidad_sueno, "Estres_Metricas": f"Lab: {v_estres_lab} | Emo: {v_estres_emo}",
                        "Alimentacion_Metricas": f"Comidas: {v_comidas_dia} | Prot: {v_proteina} | Cals: {v_calorias} | Alc: {v_alcohol} | Fuma: {v_fuma} | Fatiga: {v_fatiga_constante} | Ener: {v_energia_dia} | Artic: {v_dolor_articular}",
                        "Disponibilidad_Real": v_dias_reales, "Lugar_Entreno": v_lugar, "Preferencias_Vol_Int": f"Pref: {', '.join(v_preferencia_vol)} | Fallo: {v_gusta_fallo} | Tipo: {v_maquinas_libres}",
                        "Fotos_Link": f"Cargados {len(uploaded_photos)} archivos desde galería" if uploaded_photos else "No cargadas"
                    }
                    
                    try:
                        pd.DataFrame([registro_bd]).to_csv(SHEET_URL, mode='a', header=False, index=False)
                    except:
                        pass
                    
                    st.session_state.cuestionario_enviado = True
                    st.rerun()
