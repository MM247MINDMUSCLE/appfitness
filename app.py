import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="MINDMUSCLE247",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos visuales
st.markdown("""
    <style>
    .main { background-color: #0B0B0B; color: #FFFFFF; }
    .brand-title-main { font-size: 52px; font-weight: 900; color: #FFFFFF; text-align: center; }
    .stButton>button { background-color: #E0E0E0; color: #000000; font-weight: bold; width: 100%; padding: 18px; }
    </style>
""", unsafe_allow_html=True)

# 2. CABECERA
st.markdown('<h1 class="brand-title-main">MINDMUSCLE247</h1>', unsafe_allow_html=True)

SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/export?format=csv"

# 3. LÓGICA DE CONTROL
if "cuestionario_enviado" not in st.session_state: st.session_state.cuestionario_enviado = False

st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
modo = st.sidebar.radio("Seleccionar Vista:", ["📝 Cuestionario Alumno", "📊 Dashboard Administrador"])
clave_coach = st.sidebar.text_input("Clave de Acceso:", type="password")

if modo == "📊 Dashboard Administrador":
    if clave_coach == "MM247":
        st.header("📊 Dashboard de Gestión")
        try:
            df = pd.read_csv(SHEET_URL)
            st.metric("Total Alumnos", len(df))
            alumno_sel = st.selectbox("Seleccionar Alumno:", df["Nombre Completo"].unique())
            datos = df[df["Nombre Completo"] == alumno_sel].iloc[0]
            st.write(datos)
        except:
            st.error("Error cargando base de datos.")
    else:
        st.warning("Acceso restringido.")
else:
    if st.session_state.cuestionario_enviado:
        st.success("✅ ¡Cuestionario Enviado con Éxito!")
    else:
        # DEFINICIÓN CORRECTA DE TABS (No eliminar ni modificar este bloque)
        t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
            "⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", 
            "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Fotos"
        ])

        with t1:
            st.subheader("📋 Datos Personales de Partida")
            v_nombre = st.text_input("✍ Escribe tu Nombre Completo:")
            v_edad = st.number_input("🎂 Edad actual:", min_value=1, max_value=100, value=25)
            v_sexo = st.selectbox("Sexo biológico:", ["Seleccionar", "Masculino", "Femenino"])
            v_estatura = st.number_input("📏 Estatura (cm):", min_value=100, max_value=250, value=170)
            v_peso = st.number_input("⚖ Peso actual (kg):", min_value=30.0, max_value=200.0, value=70.0)
            v_ocupacion = st.text_input("💼 Ocupación:")
            v_horas_sentado = st.text_input("🪑 Horas sentado al día:")
            v_actividad = st.selectbox("🏃 Actividad diaria:", ["Bajo", "Moderado", "Alto"])
            v_objetivo = st.selectbox("🎯 Objetivo principal:", ["Hipertrofia", "Pérdida de grasa", "Recomposición", "Fuerza", "Rendimiento", "Salud", "Otro"])
            v_obj_visual1 = st.text_input("🚀 ¿Qué parte física mejorar más?")
            v_obj_visual2 = st.text_input("🔍 ¿Músculos menos desarrollados?")
            v_obj_visual3 = st.text_input("🎯 ¿Músculos a priorizar?")

        with t2:
            st.subheader("🏋️ Trayectoria en el Gimnasio")
            v_tiempo_entreno = st.text_input("⏳ Tiempo entrenando:")
            v_constancia = st.selectbox("🔄 Constancia:", ["Entrenamiento constante", "Con pausas recurrentes"])
            v_tipo_entreno = st.multiselect("👟 Disciplinas:", ["Pesas", "Crossfit", "Calistenia", "Powerlifting", "Funcional"])
            v_dias_actuales = st.text_input("📅 Días por semana:")
            v_duracion_promedio = st.text_input("⏱ Duración sesión:")
            v_tecnicas = st.multiselect("🧠 Técnicas:", ["RIR", "Fallo muscular", "Tempo", "Sobrecarga"])
            v_eval_tec = st.slider("Control técnica (1-10):", 1, 10, 7)
            v_eval_mente = st.slider("Conexión mente-músculo (1-10):", 1, 10, 7)
            v_eval_int = st.slider("Intensidad (1-10):", 1, 10, 7)
            v_eval_disc = st.slider("Disciplina (1-10):", 1, 10, 8)
            v_eval_rec = st.slider("Recuperación (1-10):", 1, 10, 7)

        with t3:
            st.subheader("🩺 Historial Clínico y Lesiones")
            v_patologias = st.multiselect("⚠️ Molestias:", ["Lumbar", "Rodilla", "Hombro", "Tendinitis", "Otros"])
            v_dolor_ejercicios = st.text_area("⚡ Ejercicios que detonan dolor:")
            v_incomodidad = st.text_area("❌ Movimientos incómodos:")
            v_prohibidos = st.text_area("🚫 Prohibidos:")

        with t4:
            st.subheader("📐 Análisis Biomecánico")
            v_piernas = st.selectbox("🦵 Piernas:", ["Cortas", "Promedio", "Largas"])
            v_torso = st.selectbox("🧍 Torso:", ["Corto", "Promedio", "Largo"])
            v_brazos = st.selectbox("💪 Brazos:", ["Cortos", "Promedio", "Largos"])
            v_dificultad_sq = st.selectbox("🏋️ Sentadilla profunda:", ["Fácil", "Difícil"])
            v_dificultad_bench = st.selectbox("Press Banca:", ["Natural", "Incomodidad"])
            v_naturales = st.text_area("💎 Ejercicios idóneos:")
            v_mov_tobillo = st.slider("Movilidad tobillo:", 1, 10, 5)
            v_mov_cadera = st.slider("Movilidad cadera:", 1, 10, 5)
            v_mov_hombro = st.slider("Movilidad hombro:", 1, 10, 5)
            v_flex_general = st.slider("Flexibilidad general:", 1, 10, 5)
            v_postura = st.multiselect("🔍 Postura:", ["Hombros adelantados", "Cifosis", "Hiperlordosis", "Valgo"])

        with t5:
            st.subheader("💥 Marcas de Fuerza")
            v_p_banca = st.text_input("🪵 Banca:")
            v_p_sentadilla = st.text_input("👑 Sentadilla:")
            v_p_muerto = st.text_input("💀 Peso Muerto:")
            v_p_dominadas = st.text_input("🦅 Dominadas:")
            v_p_fondos = st.text_input("🦜 Fondos:")
            v_p_militar = st.text_input("🎖️ Militar:")
            v_fatiga_rapida = st.selectbox("¿Fatiga rápida?", ["No", "Sí"])
            v_perdida_fuerza = st.selectbox("¿Pérdida fuerza series?", ["No", "Sí"])
            v_rec_esfuerzo = st.selectbox("¿Recuperación aire?", ["No", "Sí"])
            v_cardio = st.selectbox("❤️ Cardio:", ["Mala", "Regular", "Buena", "Excelente"])

        with t6:
            st.subheader("🥗 Nutrición")
            v_pref_proteina = st.selectbox("🥩 Proteína:", ["Carnes", "Pescados", "Vegetal", "Variado"])
            v_pref_grasa = st.selectbox("🥑 Grasas:", ["Aguacate/Frutos", "Aceite/Yemas", "Lácteos", "Mixto"])
            v_pref_carbos = st.selectbox("🍚 Carbos:", ["Arroz/Avena", "Pastas", "Frutas", "Mixto"])
            v_pref_colaciones = st.selectbox("🍏 Colaciones:", ["5 comidas", "3 comidas", "Ayuno"])
            v_horas_sueno = st.number_input("⏰ Sueño (hrs):", 1, 24, 7)
            v_calidad_sueno = st.selectbox("😴 Calidad sueño:", ["Buena", "Regular", "Mala"])
            v_estres_lab = st.slider("🤯 Estrés trabajo:", 1, 10, 5)
            v_estres_emo = st.slider("🧠 Estrés emocional:", 1, 10, 5)
            v_comidas_dia = st.text_input("🍽 Comidas sólidas:")
            v_proteina = st.selectbox("🍗 ¿Proteína en cada comida?", ["Sí", "No"])
            v_calorias = st.selectbox("📊 ¿Pesaje de alimentos?", ["No", "Visual", "Preciso"])
            v_alcohol = st.selectbox("🍺 Alcohol:", ["No", "Social", "Semanal"])
            v_fuma = st.selectbox("🚬 ¿Fuma?", ["No", "Sí"])
            v_fatiga_constante = st.selectbox("🔋 ¿Fatiga crónica?", ["No", "Sí"])
            v_energia_dia = st.selectbox("⚡ ¿Energía entreno?", ["Sí", "No"])
            v_dolor_articular = st.selectbox("💥 ¿Dolor articular?", ["No", "Sí"])

        with t7:
            st.subheader("📅 Logística")
            v_dias_reales = st.slider("🗓 Días entreno:", 1, 6, 4)
            v_tiempo_sesion = st.text_input("⏳ Minutos sesión:")
            v_lugar = st.selectbox("🏢 Lugar:", ["Gimnasio", "Casa"])
            v_equipo = st.multiselect("🛠 Equipo:", ["Máquinas", "Poleas", "Mancuernas", "Barra", "Rack", "Bandas"])

        with t8:
            st.subheader("🎯 Psicología")
            v_ejercicios_disfruta = st.text_area("❤️ Ejercicios favoritos:")
            v_ejercicios_odia = st.text_area("❌ Ejercicios que evita:")
            v_preferencia_vol = st.multiselect("⚖ Enfoque:", ["Alto volumen", "Bajo volumen", "Corto", "Largo"])
            v_gusta_fallo = st.selectbox("💥 Fallo muscular:", ["Sí", "No", "A veces"])
            v_maquinas_libres = st.selectbox("🤖 Preferencia equipo:", ["Libres", "Máquinas", "Mezcla"])

        with t9:
            st.subheader("📸 Envío")
            btn_enviar = st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA")
            if btn_enviar:
                st.session_state.cuestionario_enviado = True
                st.rerun()
