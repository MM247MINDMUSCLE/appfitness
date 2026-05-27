# --- MÓDULO 1: CUESTIONARIO INTEGRAL DE EVALUACIÓN ---
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    with st.form("cuestionario_cerrado_mm247", clear_on_submit=True):
        
        # Estructura de pestañas para las 12 secciones
        tab1, tab2, tab3, tab4 = st.tabs(["👤 1. Perfil", "🩺 2. Historial Clínico", "🥗 3. Estilo de Vida", "🏋️ 4. Entrenamiento"])
        
        with tab1:
            st.markdown("<div class='section-header'>1. Datos Generales y Objetivos</div>", unsafe_allow_html=True)
            nombre = st.text_input("Nombre Completo:")
            edad = st.selectbox("Edad:", [f"{i} años" for i in range(14, 81)])
            sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
            peso = st.selectbox("Peso actual:", [f"{i} kg" for i in range(40, 201)])
            meta = st.selectbox("Objetivo principal:", ["Perder grasa", "Ganar masa muscular", "Recomposición", "Rendimiento"])
            compromiso = st.selectbox("Compromiso (1-10):", [str(i) for i in range(1, 11)])

        with tab2:
            st.markdown("<div class='section-header'>2. Salud y Biomecánica</div>", unsafe_allow_html=True)
            lesiones = st.multiselect("¿Alguna lesión?", ["Rodilla", "Hombro", "Espalda", "Cadera", "Ninguna"])
            cirugias = st.radio("¿Cirugías?", ["Sí", "No"])
            condicion = st.selectbox("Condición médica:", ["Ninguna", "Diabetes", "Hipertensión", "Hormonal", "Otro"])
            movilidad = st.selectbox("Movilidad:", ["Mala", "Regular", "Buena", "Excelente"])

        with tab3:
            st.markdown("<div class='section-header'>3. Nutrición y Hábitos</div>", unsafe_allow_html=True)
            sueno = st.selectbox("Calidad del sueño:", ["Malo", "Regular", "Bueno", "Excelente"])
            estres = st.selectbox("Estrés diario:", ["Bajo", "Medio", "Alto"])
            comidas = st.selectbox("Comidas al día:", ["2", "3", "4", "5"])
            actividad = st.selectbox("Actividad física diaria:", ["Sedentario", "Poco activo", "Moderado", "Muy activo"])

        with tab4:
            st.markdown("<div class='section-header'>4. Entrenamiento y Disponibilidad</div>", unsafe_allow_html=True)
            experiencia = st.selectbox("Experiencia:", ["Nunca", "Menos de 6 meses", "1 año", "2-5 años", ">5 años"])
            frecuencia = st.selectbox("Días por semana:", ["3 días", "4 días", "5 días", "6 días"])
            tiempo = st.selectbox("Tiempo por sesión:", ["30 min", "45 min", "60 min", "90 min"])
            entorno = st.selectbox("Entorno:", ["Gimnasio", "Casa", "Exterior"])

        enviar_datos = st.form_submit_button("🚀 Registrar evaluación")
        
        if enviar_datos:
            # Lógica de ID Único
            id_registro = f"MM-{datetime.datetime.now().strftime('%Y%m%d')}-{nombre[:2].upper()}"
            payload = {
                "ID": id_registro, "Nombre": nombre, "Edad": edad, "Meta": meta, 
                "Lesiones": str(lesiones), "Sueño": sueno, "Experiencia": experiencia
            }
            # Tu lógica original de envío
            response = requests.post(WEBHOOK_URL, json=payload)
            st.success(f"¡Evaluación registrada! ID: {id_registro}")
