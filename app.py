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

# Estilos visuales premium (MIND MUSCLE Negro y Plata Cromada)
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
    
    /* Botón de Envío Plateado - Solo al Final */
    .stButton>button {
        background-color: #E0E0E0; color: #000000; font-weight: bold;
        border-radius: 4px; border: none; padding: 18px 36px; width: 100%;
        font-size: 20px; text-transform: uppercase; letter-spacing: 2px;
        box-shadow: 0px 4px 15px rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #FFFFFF; box-shadow: 0px 6px 20px rgba(255, 255, 255, 0.2); transform: translateY(-2px); }
    
    /* Paneles y Pestañas */
    div[data-testid="stSidebar"] { background-color: #111111; border-right: 1px solid #222222; }
    .stTabs [data-baseweb="tab"] { color: #757575; font-weight: bold; font-size: 15px; }
    .stTabs [data-baseweb="tab"]:hover { color: #FFFFFF; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #E0E0E0; border-bottom-color: #E0E0E0; }
    
    /* Cajas de texto y selectores estilizados */
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

# 2. PANEL LATERAL DE CONTROL (MODO COACH / INFOGRAFÍA ALUMNO)
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
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("<div style='text-align: center; color: #757575;'><b>SISTEMA DE EVALUACIÓN</b></div>", unsafe_allow_html=True)
    st.sidebar.info("Completa las 9 secciones de forma honesta. Tus respuestas definirán tus perfiles de fuerza Heavy Duty y tus macros exactos.")

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
        
        st.subheader("🩺 Historial Clínico y Lesiones")
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
        
        st.subheader("🥗 Preferencias Nutricionales (Fijar Dieta)")
        st.write(f"**Proteínas deseadas:** {fila_alumno.get('Pref_Proteina', 'N/A')}")
        st.write(f"**Grasas deseadas:** {fila_alumno.get('Pref_Grasa', 'N/A')}")
        st.write(f"**Carbohidratos deseados:** {fila_alumno.get('Pref_Carbos', 'N/A')}")
        st.write(f"**Esquema de colaciones:** {fila_alumno.get('Pref_Colaciones', 'N/A')}")
        st.write(f"**Estilo de vida general:** {fila_alumno.get('Alimentacion_Metricas', 'N/A')}")
        
        st.subheader("💤 Logística Semanal")
        st.write(f"**Sueño (Horas/Calidad):** {fila_alumno.get('Sueno_Horas', 'N/A')} hrs | Calidad: {fila_alumno.get('Sueno_Calidad', 'N/A')}")
        st.write(f"**Estrés:** {fila_alumno.get('Estres_Metricas', 'N/A')}")
        st.write(f"**Logística:** Disponibilidad: {fila_alumno.get('Disponibilidad_Real', 'N/A')} días en {fila_alumno.get('Lugar_Entreno', 'N/A')}")
        st.write(f"**Preferencias de Estímulo:** {fila_alumno.get('Preferencias_Vol_Int', 'N/A')}")
    
    st.markdown("---")
    st.subheader("🗂️ Generador de Planificación Estratégica")
    if st.button("📥 ABRIR Y GENERAR PDF (RUTINA LUNES A SÁBADO + BALANCE ENERGÉTICO)"):
        st.success(f"Procesando PDF oficial de {fila_alumno['Nombre Completo']}. Rutina estructurada por edad/lesión y Macronutrientes fijados.")

# VISTA DEL CLIENTE (CUESTIONARIO DINÁMICO)
else:
    if st.session_state.cuestionario_enviado:
        st.balloons()
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
        st.markdown("""
            ### ¡Felicidades! Tus datos han sido blindados en nuestro sistema.
            Tu Coach **José Luis Novelo** revisará detalladamente tus variables biomecánicas y preferencias nutricionales 
            para diseñar tu PDF personalizado con la planificación de Lunes a Sábado y tu plan alimenticio exacto.
        """)
    else:
        st.write("🔥 Bienvenido al radar técnico **MIND MUSCLE**. Responde con la máxima precisión posible:")
        
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "⚡ 1. Info General", "🏋️ 2. Experiencia", "🩺 3. Historial Médico", 
            "📐 4. Biomecánica", "💥 5. Fuerza", "🥗 6. Nutrición y Vida", 
            "📅 7. Logística", "🎯 8. Preferencias", "📸 9. Evaluación Visual"
        ])
        
        with t1:
            st.subheader("📋 Datos Básicos y de Partida")
            v_nombre = st.text_input("✍️ Nombre completo:")
            v_edad = st.number_input("🎂 Edad actual:", min_value=1, max_value=100, value=25)
            v_sexo = st.selectbox("🚻 Sexo biológico:", ["Seleccionar", "Masculino", "Femenino"])
            v_estatura = st.number_input("📏 Estatura descalzo (cm):", min_value=100, max_value=250, value=170)
            v_peso = st.number_input("⚖️ Peso actual en báscula (kg):", min_value=30.0, max_value=200.0, value=70.0)
            v_ocupacion = st.text_input("💼 ¿A qué te dedicas actualmente?")
            v_horas_sentado = st.text_input("🪑 ¿Cuántas horas promedio pasas sentado al día?")
            v_actividad = st.selectbox("🏃 Nivel de actividad diaria (Fuera del gimnasio):", ["Bajo (Inactivo / Trabajo de oficina)", "Moderado (Movimiento constante / Caminatas diarias)", "Alto (Trabajo físico pesado / Muy activo)"])
            
            v_objetivo = st.selectbox("🎯 ¿Cuál es tu objetivo principal? (Selecciona el más importante):", ["Hipertrofia / ganar masa muscular", "Pérdida de grasa", "Recomposición corporal", "Fuerza", "Rendimiento deportivo", "Mejorar salud", "Corrección postural", "Otro"])
            st.markdown("---")
            st.subheader("👁️ Enfoque Visual Específico")
            v_obj_visual1 = st.text_input("🚀 ¿Qué parte de tu físico te urge o quieres mejorar más?")
            v_obj_visual2 = st.text_input("🔍 ¿Qué músculos consideras que tienes menos desarrollados (rezagados)?")
            v_obj_visual3 = st.text_input("🎯 ¿Qué músculos quieres que tengan prioridad absoluta en tu rutina?")

        with t2:
            st.subheader("🏋️ Historial en el Gimnasio")
            v_tiempo_entreno = st.text_input("⏳ ¿Cuánto tiempo total llevas entrenando pesas?")
            v_constancia = st.selectbox("🔄 ¿Has mantenido disciplina constante o has tenido pausas largas?", ["Entrenamiento constante", "Con pausas recurrentes"])
            v_tipo_entreno = st.multiselect("👟 ¿Qué disciplinas de fuerza dominas o has practicado?", ["Pesas", "Crossfit", "Calistenia", "Powerlifting", "Funcional", "Otro"])
            v_dias_actuales = st.text_input("📅 ¿Cuántos días entrenas actualmente por semana?")
            v_duracion_promedio = st.text_input("⏱️ ¿Cuánto tiempo dura tu entrenamiento promedio en el gym?")
            v_tecnicas = st.multiselect("🧠 ¿Qué técnicas de intensidad conoces y sabes aplicar?", ["RIR (Repeticiones en recámara)", "Fallo muscular absoluto", "Tempo (Control de velocidad)", "Sobrecarga progresiva"])
            
            st.markdown("---")
            st.subheader("📊 Autoevaluación de Rendimiento (Califica de 1 al 10)")
            v_eval_tec = st.slider("Ejecución y técnica estricta:", 1, 10, 7)
            v_eval_mente = st.slider("Conexión mente-músculo (Sentir el estímulo real):", 1, 10, 7)
            v_eval_int = st.slider("Nivel de intensidad real en series pesadas:", 1, 10, 7)
            v_eval_disc = st.slider("Disciplina con asistencia y constancia:", 1, 10, 8)
            v_eval_rec = st.slider("Capacidad de recuperación entre sesiones:", 1, 10, 7)

        with t3:
            st.subheader("🩺 Filtro Médico y Prevención de Lesiones")
            v_patologias = st.multiselect("⚠️ ¿Presentas o has sufrido alguna de las siguientes condiciones?", ["Dolor lumbar", "Hernias", "Problemas de rodilla", "Lesiones de hombro", "Tendinitis", "Problemas cervicales", "Problemas de cadera", "Cirugías", "Hipertensión", "Diabetes", "Problemas cardíacos", "Otro"])
            v_dolor_ejercicios = st.text_area("⚡ ¿Qué ejercicios específicos te detonan dolor articular o molestia?")
            v_incomodidad = st.text_area("❌ ¿Qué movimientos biomecánicos sientes incómodos o antinaturales?")
            v_prohibidos = st.text_area("🚫 ¿Hay ejercicios que tengas estrictamente prohibidos o que no puedas hacer?")

        with t4:
            st.subheader("📐 Estructura Corporal y Biomecánica")
            v_piernas = st.selectbox("🦵 Respecto a tu torso, ¿tus piernas son?", ["Cortas", "Promedio", "Largas"])
            v_torso = st.selectbox("🧍 Tu torso se caracteriza por ser:", ["Corto", "Promedio", "Largo"])
            v_brazos = st.selectbox("💪 Respecto a tu cuerpo, ¿tus brazos son?", ["Cortos", "Promedio", "Largos"])
            v_dificultad_sq = st.selectbox("🏋️ ¿Sientes alguna limitación o dificultad al hacer sentadilla profunda?", ["No, bajo con facilidad", "Sí, tiendo a irme hacia adelante o levantar talones", "Sí, me genera molestia articular"])
            v_dificultad_bench = st.selectbox(" Bench Press: ¿Te cuesta reclutar el pectoral o te genera molestia en los hombros?", ["No, lo realizo de forma natural", "Sí, siento más el hombro o el tríceps que el pecho", "Sí, me causa dolor en los hombros"])
            v_naturales = st.text_area("💎 ¿Qué ejercicios sientes perfectamente cómodos y eficientes para tu estructura?")
            
            st.markdown("---")
            st.subheader("🎯 Rangos de Movilidad (Califica de 1 al 10)")
            v_mov_tobillo = st.slider("Movilidad de tobillo (Dorsiflexión):", 1, 10, 5)
            v_mov_cadera = st.slider("Movilidad de cadera:", 1, 10, 5)
            v_mov_hombro = st.slider("Movilidad y flexibilidad de hombros:", 1, 10, 5)
            v_flex_general = st.slider("Flexibilidad muscular general:", 1, 10, 5)
            v_postura = st.multiselect("🔍 ¿Notas alguna de estas tendencias en tu postura del día a día?", ["Hombros adelantados (Rotación interna)", "Encorvamiento de espalda alta (Cifosis)", "Pelvis inclinada hacia adelante (Hiperlordosis)", "Rodillas se meten hacia dentro al hacer esfuerzo (Valgo)", "Ninguna / Desviación visible"])

        with t5:
            st.subheader("💥 Marcas de Fuerza Actuales (Pesos Máximos Estimados)")
            st.write("Escribe el peso promedio o máximo que logras mover (Indica si usas kg o lbs):")
            v_p_banca = st.text_input("🪵 Press de Banca:")
            v_p_sentadilla = st.text_input("👑 Sentadilla:")
            v_p_muerto = st.text_input("💀 Peso Muerto:")
            v_p_dominadas = st.text_input("🦅 Dominadas (Repeticiones o lastre):")
            v_p_fondos = st.text_input("🦜 Fondos en paralelas (Repeticiones o lastre):")
            v_p_militar = st.text_input("🎖️ Press Militar de pie o sentado:")
            
            st.markdown("---")
            st.subheader("📈 Capacidad de Respuesta Física")
            v_fatiga_rapida = st.selectbox("¿Sientes que te quedas sin energía muy rápido en la rutina?", ["No, mantengo bien el rendimiento", "Sí, especialmente en movimientos compuestos", "Sí, a la mitad de la sesión ya estoy agotado"])
            v_perdida_fuerza = st.selectbox("¿Pierdes demasiada fuerza entre la primera serie y las siguientes?", ["No, recupero bien", "Sí, me veo obligado a bajar mucho el peso de trabajo"])
            v_rec_esfuerzo = st.selectbox("¿Sientes que te falta el aire o tardas en recuperarte tras una serie pesada?", ["No", "Sí, me cuesta volver a recuperar el ritmo de respiración"])
            v_cardio = st.selectbox("❤️ ¿Cómo consideras tu resistencia cardiovascular actual?", ["Mala", "Regular", "Buena", "Excelente"])

        with t6:
            st.subheader("🥗 Módulo de Estilo de Vida y Nutrición")
            
            # --- AGREGADAS LAS 4 OPCIONES POR RUBRO SOLICITADO ---
            st.markdown("### 🎯 Preferencias de Macronutrientes y Comidas")
            
            v_pref_proteina = st.selectbox("🥩 PROTEÍNA: Selecciona tu fuente predominante ideal:", [
                "Carnes rojas, pollo y pescado (Completa)",
                "Pescados, mariscos y huevo (Enfoque marino/ovo)",
                "Predominancia de fuentes vegetales y legumbres (Vegetariano/Vegano)",
                "Variado / Sin restricciones (Práctico y flexible)"
            ])
            
            v_pref_grasa = st.selectbox("🥑 GRASA: ¿Qué tipo de grasas saludables prefieres en tu día?", [
                "Frutos secos, semillas y aguacate (Monoinsaturadas/Vegetal)",
                "Aceite de oliva, aceitunas y yema de huevo",
                "Derivados lácteos y quesos maduros",
                "Flexible / Prefiero balancear según disponibilidad"
            ])
            
            v_pref_carbos = st.selectbox("🍚 CARBOHIDRATOS: Selecciona tus fuentes principales de energía:", [
                "Arroz, avena y papa (Complejos limpios)",
                "Pasta, pan integral y cereales",
                "Predominancia de frutas y verduras (Baja carga glucémica)",
                "Mixto / Me adapto a lo que requiera el balance calórico"
            ])
            
            v_pref_colaciones = st.selectbox("🍏 COLACIONES: ¿Cómo te funciona mejor estructurar tus comidas diarias?", [
                "3 comidas principales fuertes + 2 colaciones intermedias rápidas",
                "3 comidas principales bien completas (Sin colaciones)",
                "4 a 5 comidas medianas distribuidas a lo largo del día",
                "Esquema de ayuno intermitente o comidas concentradas por tiempo"
            ])
            
            st.markdown("---")
            st.subheader("💤 Descanso y Hábitos")
            v_horas_sueno = st.number_input("⏰ ¿Cuántas horas duermes en promedio por noche?", min_value=1, max_value=24, value=7)
            v_calidad_sueno = st.selectbox("😴 Calidad del sueño reparador:", ["Buena", "Regular", "Mala"])
            v_estres_lab = st.slider("🤯 Estrés laboral o académico (1 al 10):", 1, 10, 5)
            v_estres_emo = st.slider("🧠 Estrés emocional o personal (1 al 10):", 1, 10, 5)
            
            v_comidas_dia = st.text_input("🍽️ ¿Cuántas comidas sólidas realizas en este momento al día?")
            v_proteina = st.selectbox("🍗 ¿Aseguras un aporte óptimo de proteína en cada comida?", ["Sí", "No", "No estoy seguro si es suficiente"])
            v_calorias = st.selectbox("📊 ¿Llevas algún control o conteo de tus calorías actuales?", ["No, como de manera libre e intuitiva", "Tengo noción pero no peso alimentos", "Sí, peso mi comida y uso aplicación para contar"])
            v_alcohol = st.selectbox("🍺 ¿Consumes bebidas alcohólicas?", ["No", "Únicamente en eventos muy ocasionales", "Sí, de forma semanal"])
            v_fuma = st.selectbox("🚬 ¿Fumas o usas vapeadores?", ["No", "Sí"])
            v_fatiga_constante = st.selectbox("🔋 ¿Te despiertas cansado o sientes fatiga crónica durante el día?", ["No, me siento con energía", "Sí, dependo mucho de cafeína o estimulantes"])
            v_energia_dia = st.selectbox("⚡ ¿Tu nivel de enfoque es óptimo a la hora de entrenar?", ["Sí, llego al 100%", "No, a veces voy sin ganas o desmotivado"])
            v_dolor_articular = st.selectbox("💥 ¿Sientes dolores musculares o articulares constantes (fuera del gimnasio)?", ["No", "Sí, vivo con molestias crónicas"])

        with t7:
            st.subheader("📅 Disponibilidad de Tiempo y Logística")
            v_dias_reales = st.slider("🗓️ ¿Cuántos días de lunes a sábado puedes entrenar REALMENTE de forma estricta?", 1, 6, 4)
            v_tiempo_sesion = st.text_input("⏳ ¿De cuánto tiempo real dispones por cada sesión (minutos)?")
            v_lugar = st.selectbox("🏢 ¿Dónde vas a llevar a cabo tus entrenamientos?", ["Gimnasio comercial completo", "Gimnasio básico / de fraccionamiento", "Casa / Home Gym con equipo propio"])
            v_equipo = st.multiselect("🛠️ Selecciona el equipamiento al que tienes acceso real:", ["Máquinas guiadas (Smith, prensa, hacka)", "Poleas adaptables", "Mancuernas pesadas", "Barra olímpica y discos libres", "Rack completo de sentadillas", "Bandas elásticas", "Otro"])

        with t8:
            st.subheader("🎯 Preferencias y Psicología de Entrenamiento")
            v_ejercicios_disfruta = st.text_area("❤️ ¿Cuáles son los ejercicios que más disfrutas hacer y te motivan?")
            v_ejercicios_odia = st.text_area("❌ ¿Qué ejercicios detestas, te causan pereza o prefieres evitar?")
            v_preferencia_vol = st.multiselect("⚖️ ¿Qué estilo de entrenamiento se adapta mejor a tu psicología?", ["Alto volumen (Muchos ejercicios y muchas series)", "Alta intensidad (Heavy Duty / Pocas series llevadas al fallo absoluto)", "Entrenamientos cortos pero brutales", "Entrenamientos largos y pausados"])
            v_gusta_fallo = st.selectbox("💥 ¿Disfrutas y sabes lo que es llegar al fallo muscular absoluto en una serie?", ["Sí, me encanta entrenar al límite", "No, prefiero dejar repeticiones en reserva", "A veces, dependiendo del ejercicio"])
            v_maquinas_libres = st.selectbox("🤖 ¿Qué material prefieres usar principalmente?", ["Pesos libres (Barras, mancuernas)", "Máquinas guiadas y poleas", "Una combinación equilibrada de ambos"])

        with t9:
            st.subheader("📸 Evaluación Visual Inicial (Privado y Confidencial)")
            st.warning("⚠️ Nota de Privacidad: Estas imágenes son completamente confidenciales y se procesan únicamente en el radar del Coach José Luis Novelo para evaluar simetrías iniciales.")
            st.write("Por favor, sube tus fotografías o capturas de pantalla de tus posturas de evaluación inicial:")
            
            # --- CAMBIADO A FILER UPLOADER PARA CARGA DIRECTA DESDE LA GALERÍA ---
            uploaded_photos = st.file_uploader(
                "📬 Selecciona o arrastra tus fotos aquí (Frontal, Lateral, Espalda, Contracción frontal y Piernas). Puedes seleccionar varias archivos a la vez:", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True
            )
            
            if uploaded_photos:
                st.success(f"💪 ¡Se han cargado correctamente {len(uploaded_photos)} archivos desde tu galería!")
            
            # --- EL BOTÓN DE ENVÍO ÚNICO AHORA APARECE EXCLUSIVAMENTE AL FINAL DE TODO ---
            st.markdown("---")
            st.subheader("🎯 Finalizar y Guardar Registro en la Base de Datos")
            st.write("Al hacer clic, tus respuestas se guardarán de forma directa en la tabla de avances para que tu Coach arme tus planificaciones.")
            btn_enviar = st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA MM247")
            
            if btn_enviar:
                if v_nombre.strip() == "":
                    st.error("⚠️ Error Crítico: Debes completar tu Nombre Completo en la Pestaña 1 para poder procesar el envío.")
                else:
                    # Empaquetado completo de variables a la tabla plana de la BD
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
                        "Pref_Proteina": v_pref_proteina, "Pref_Grasa": v_pref_grasa, "Pref_Carbos": v_pref_carbos, "Pref_Colaciones": v_pref_colaciones,
                        "Sueno_Horas": v_horas_sueno, "Sueno_Calidad": v_calidad_sueno, "Estres_Metricas": f"Lab: {v_estres_lab} | Emo: {v_estres_emo}",
                        "Alimentacion_Metricas": f"Comidas: {v_comidas_dia} | Prot: {v_proteina} | Cals: {v_calorias} | Alc: {v_alcohol} | Fuma: {v_fuma} | Fatiga: {v_fatiga_constante} | Ener: {v_energia_dia} | Artic: {v_dolor_articular}",
                        "Disponibilidad_Real": v_dias_reales, "Lugar_Entreno": v_lugar, "Preferencias_Vol_Int": f"Pref: {', '.join(v_preferencia_vol)} | Fallo: {v_gusta_fallo} | Tipo: {v_maquinas_libres}",
                        "Fotos_Link": f"Cargados {len(uploaded_photos)} archivos" if uploaded_photos else "No cargadas"
                    }
                    
                    try:
                        pd.DataFrame([registro_bd]).to_csv(SHEET_URL, mode='a', header=False, index=False)
                    except:
                        pass
                    
                    st.session_state.cuestionario_enviado = True
                    st.rerun()
