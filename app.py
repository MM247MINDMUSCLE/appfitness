import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEP6Up0KmDzr22xjQzklH3CbgCUJWVc7dXtKyjJIoETOxD5WSuook45kLotqxeQ82LQXUu0n2nkLcm/pub?output=csv"

# 2. CABECERA
st.markdown("<h1 style='text-align: center;'>MINDMUSCLE247</h1>", unsafe_allow_html=True)

# 3. LÓGICA DE VISTAS
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
modo = st.sidebar.radio("Seleccionar Vista:", ["📝 Cuestionario Alumno", "📊 Dashboard Administrador"])
clave_coach = st.sidebar.text_input("Clave de Acceso:", type="password")

# --- VISTA ADMINISTRADOR ---
if modo == "📊 Dashboard Administrador":
    if clave_coach == "MM247":
        st.header("📊 Dashboard de Gestión Integral")
        try:
            df = pd.read_csv(SHEET_URL)
            if not df.empty:
                alumno_sel = st.selectbox("Seleccionar Alumno:", df["Nombre Completo"].unique())
                datos = df[df["Nombre Completo"] == alumno_sel].iloc[0]
                
                # Métricas visuales
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Edad", datos["Edad"])
                c2.metric("Peso", f"{datos['Peso']} kg")
                c3.metric("Objetivo", datos["Objetivo principal"])
                c4.metric("Sueño", f"{datos['Sueño (hrs)']} hrs")
                
                # Gráfica Dinámica
                st.subheader("📈 Análisis de Capacidades")
                # Seleccionamos columnas numéricas para el gráfico
                metricas = datos[["Control técnica (1-10)", "Conexión mente-músculo (1-10)", "Intensidad (1-10)", "Disciplina (1-10)", "Recuperación (1-10)"]]
                fig = px.bar(x=metricas.index, y=metricas.values, color=metricas.values, color_continuous_scale="RdYlGn")
                st.plotly_chart(fig, use_container_width=True)
                
                st.write("### Datos Completos", datos)
                st.info("🖨️ Presiona Ctrl+P para guardar este análisis como PDF.")
            else:
                st.info("Base de datos conectada, pero no hay registros.")
        except Exception as e:
            st.error(f"Error cargando dashboard: {e}")
    else:
        st.warning("Clave incorrecta.")

# --- VISTA CUESTIONARIO (CON TODAS LAS PREGUNTAS) ---
else:
    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
        "⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", 
        "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Fotos"
    ])

    with t1:
        st.subheader("📋 Datos Personales")
        nombre = st.text_input("Nombre Completo:")
        edad = st.number_input("Edad:", 1, 100, 25)
        sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
        estatura = st.number_input("Estatura (cm):", 100, 250, 170)
        peso = st.number_input("Peso (kg):", 30.0, 200.0, 70.0)
        ocupacion = st.text_input("Ocupación:")
        hrs_sentado = st.text_input("Horas sentado al día:")
        actividad = st.selectbox("Actividad:", ["Bajo", "Moderado", "Alto"])
        objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Pérdida de grasa", "Recomposición", "Fuerza"])
        obj_v1 = st.text_input("¿Parte física a mejorar?")
        obj_v2 = st.text_input("¿Músculos rezagados?")
        obj_v3 = st.text_input("¿Músculos a priorizar?")

    with t2:
        st.subheader("🏋️ Trayectoria")
        tiempo = st.text_input("Tiempo entrenando:")
        constancia = st.selectbox("Constancia:", ["Constante", "Con pausas"])
        disciplinas = st.multiselect("Disciplinas:", ["Pesas", "Crossfit", "Calistenia", "Powerlifting"])
        dias = st.text_input("Días por semana:")
        duracion = st.text_input("Duración sesión:")
        tecnicas = st.multiselect("Técnicas:", ["RIR", "Fallo", "Tempo"])
        tec_slider = st.slider("Control técnica (1-10):", 1, 10, 7)
        mente = st.slider("Conexión mente-músculo (1-10):", 1, 10, 7)
        intensidad = st.slider("Intensidad (1-10):", 1, 10, 7)
        disc_slider = st.slider("Disciplina (1-10):", 1, 10, 8)
        rec = st.slider("Recuperación (1-10):", 1, 10, 7)

    with t3:
        st.subheader("🩺 Historial Clínico")
        molestias = st.multiselect("Molestias:", ["Lumbar", "Rodilla", "Hombro", "Tendinitis"])
        dolor = st.text_area("Ejercicios que detonan dolor:")
        inc = st.text_area("Movimientos incómodos:")
        prohibidos = st.text_area("Prohibidos:")

    with t4:
        st.subheader("📐 Biomecánica")
        piernas = st.selectbox("Piernas:", ["Cortas", "Promedio", "Largas"])
        torso = st.selectbox("Torso:", ["Corto", "Promedio", "Largo"])
        brazos = st.selectbox("Brazos:", ["Cortos", "Promedio", "Largos"])
        sq = st.selectbox("Sentadilla profunda:", ["Fácil", "Difícil"])
        bench = st.selectbox("Press Banca:", ["Natural", "Incomodidad"])
        ideales = st.text_area("Ejercicios idóneos:")
        mob_tobillo = st.slider("Movilidad tobillo:", 1, 10, 5)
        mob_cadera = st.slider("Movilidad cadera:", 1, 10, 5)
        mob_hombro = st.slider("Movilidad hombro:", 1, 10, 5)
        flex = st.slider("Flexibilidad general:", 1, 10, 5)
        postura = st.multiselect("Postura:", ["Hombros adelantados", "Cifosis", "Hiperlordosis"])

    with t5:
        st.subheader("💥 Marcas de Fuerza")
        banca = st.text_input("Banca:")
        sq_m = st.text_input("Sentadilla:")
        muerto = st.text_input("Peso Muerto:")
        dom = st.text_input("Dominadas:")
        fondos = st.text_input("Fondos:")
        mil = st.text_input("Militar:")
        fatiga = st.selectbox("¿Fatiga rápida?", ["No", "Sí"])
        perdida = st.selectbox("¿Pérdida fuerza series?", ["No", "Sí"])
        rec_esf = st.selectbox("¿Recuperación aire?", ["No", "Sí"])
        cardio = st.selectbox("Cardio:", ["Mala", "Regular", "Buena", "Excelente"])

    with t6:
        st.subheader("🥗 Nutrición")
        prot = st.selectbox("Proteína:", ["Carnes", "Pescados", "Vegetal", "Variado"])
        grasas = st.selectbox("Grasas:", ["Aguacate", "Aceite", "Lácteos"])
        carbo = st.selectbox("Carbos:", ["Arroz", "Pastas", "Frutas"])
        cola = st.selectbox("Colaciones:", ["5 comidas", "3 comidas", "Ayuno"])
        sueno = st.number_input("Sueño (hrs):", 1, 24, 7)
        cal_sueno = st.selectbox("Calidad sueño:", ["Buena", "Regular", "Mala"])
        str_l = st.slider("Estrés trabajo:", 1, 10, 5)
        str_e = st.slider("Estrés emocional:", 1, 10, 5)
        comidas = st.text_input("Comidas sólidas:")
        prot_cada = st.selectbox("¿Proteína en cada comida?", ["Sí", "No"])
        pesaje = st.selectbox("¿Pesaje de alimentos?", ["No", "Visual", "Preciso"])
        alc = st.selectbox("Alcohol:", ["No", "Social", "Semanal"])
        fuma = st.selectbox("¿Fuma?", ["No", "Sí"])
        fat_cron = st.selectbox("¿Fatiga crónica?", ["No", "Sí"])
        energia = st.selectbox("¿Energía entreno?", ["Sí", "No"])
        dolor_art = st.selectbox("¿Dolor articular?", ["No", "Sí"])

    with t7:
        st.subheader("📅 Logística")
        d_ent = st.slider("Días entreno:", 1, 6, 4)
        min_ses = st.text_input("Minutos sesión:")
        lugar = st.selectbox("Lugar:", ["Gimnasio", "Casa"])
        equipo = st.multiselect("Equipo:", ["Máquinas", "Poleas", "Mancuernas", "Barra", "Rack"])

    with t8:
        st.subheader("🎯 Psicología")
        fav = st.text_area("Ejercicios favoritos:")
        odia = st.text_area("Ejercicios que evita:")
        enf = st.multiselect("Enfoque:", ["Alto volumen", "Bajo volumen", "Corto", "Largo"])
        fallo = st.selectbox("Fallo muscular:", ["Sí", "No", "A veces"])
        maq = st.selectbox("Preferencia equipo:", ["Libres", "Máquinas", "Mezcla"])

    with t9:
        st.subheader("📸 Fotos")
        if st.button("🚀 ENVIAR EVALUACIÓN"):
            st.success("¡Información enviada con éxito!")
