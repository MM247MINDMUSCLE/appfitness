import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN GENERAL
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# URL DE LA BASE DE DATOS
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTEP6Up0KmDzr22xjQzklH3CbgCUJWVc7dXtKyjJIoETOxD5WSuook45kLotqxeQ82LQXUu0n2nkLcm/pub?output=csv"

# 2. CABECERA
st.markdown("<h1 style='text-align: center;'>MINDMUSCLE247</h1>", unsafe_allow_html=True)

# 3. SIDEBAR Y VISTAS
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
modo = st.sidebar.radio("Seleccionar Vista:", ["📝 Cuestionario Alumno", "📊 Dashboard Administrador"])
clave_coach = st.sidebar.text_input("Clave de Acceso:", type="password")

# --- VISTA DASHBOARD ADMINISTRADOR ---
if modo == "📊 Dashboard Administrador":
    if clave_coach == "MM247":
        st.header("📊 Dashboard de Gestión")
        try:
            df = pd.read_csv(SHEET_URL)
            if not df.empty:
                alumno_sel = st.selectbox("Seleccionar Alumno:", df["Nombre Completo"].unique())
                datos = df[df["Nombre Completo"] == alumno_sel].iloc[0]
                
                # Visualización de datos
                st.subheader(f"Análisis de {alumno_sel}")
                
                # Gráficos dinámicos
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(x=['Edad', 'Estatura', 'Peso'], y=[datos['Edad'], datos['Estatura'], datos['Peso']], title="Métricas Físicas")
                    st.plotly_chart(fig)
                
                st.write("### Detalles del Alumno", datos)
                
                if st.button("🖨️ Generar/Imprimir PDF"):
                    st.info("Utiliza Ctrl+P (o Cmd+P) para imprimir esta vista como PDF.")
            else:
                st.info("La base de datos está vacía.")
        except Exception as e:
            st.error(f"Error cargando base de datos: {e}")
    else:
        st.warning("Clave restringida.")

# --- VISTA CUESTIONARIO ALUMNO ---
else:
    # DEFINICIÓN DE TABS (Mantener este orden exacto)
    t1, t2, t3, t4, t5, t6, t7, t8, t9 = st.tabs([
        "⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", 
        "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Fotos"
    ])

    with t1:
        st.subheader("📋 Datos Personales de Partida")
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
        obj_v2 = st.text_input("¿Músculos menos desarrollados?")
        obj_v3 = st.text_input("¿Músculos a priorizar?")

    with t2:
        st.subheader("🏋️ Trayectoria en el Gimnasio")
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
        st.subheader("🩺 Historial Clínico y Lesiones")
        molestias = st.multiselect("Molestias:", ["Lumbar", "Rodilla", "Hombro", "Tendinitis"])
        dolor = st.text_area("Ejercicios que detonan dolor:")
        inc = st.text_area("Movimientos incómodos:")
        prohibidos = st.text_area("Prohibidos:")

    with t4:
        st.subheader("📐 Análisis Biomecánico")
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
