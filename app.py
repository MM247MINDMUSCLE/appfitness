import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# 2. CONEXIÓN DIRECTA Y SEGURA A GOOGLE SHEETS
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_existente = conn.read(worksheet="Respuestas", ttl=0)
except Exception as e:
    st.error("Error de conexión con la base de datos. Verifica la configuración de Secrets.")
    df_existente = pd.DataFrame()

# Estilos visuales de la interfaz
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:18px; color:#555555; text-align:center; margin-bottom:30px; }
    .section-header { font-size:22px; font-weight:bold; color:#111111; margin-top:20px; margin-bottom:10px; border-bottom: 2px solid #111111; padding-bottom:5px; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Menú lateral de navegación
opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# MÓDULO 1: CUESTIONARIO INTEGRAL COMPLETO (CAMPOS REQUERIDOS PARA DIETA Y RUTINA)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Diagnóstica Avanzada - Ficha Clínica, Nutrición & Biomecánica</div>", unsafe_allow_html=True)
    
    st.info("📌 Por favor, responde con la mayor honestidad posible. Todos los datos son obligatorios y esenciales para calcular tu balance calórico exacto y dosificar tus cargas de entrenamiento de forma segura.")
    
    with st.form("cuestionario_avanzado_mm247", clear_on_submit=True):
        
        # --- BLOQUE 1: DATOS ANTROPOMÉTRICOS Y OBJETIVO ---
        st.markdown("<div class='section-header'>📊 1. Datos Antropométricos Perfil General</div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:")
            edad = st.number_input("Edad Actual (Años):", min_value=12, max_value=90, step=1, value=25)
        with col2:
            peso = st.number_input("Peso Corporal Actual (en kg):", min_value=30.0, max_value=250.0, step=0.1, value=70.0)
            estatura = st.number_input("Estatura / Altura Exacta (en cm):", min_value=100, max_value=250, step=1, value=170)
        with col3:
            genero = st.selectbox("Género Biológico:", ["Seleccione...", "Masculino", "Femenino"])
            meta_cliente = st.selectbox("Objetivo Estructural Principal (Meta):", [
                "Seleccione...",
                "Hipertrofia Muscular Eficiente (Ganar masa)",
                "Pérdida de Tejido Graso / Definición Estética",
                "Acondicionamiento Físico General y Salud",
                "Recomposición Corporal Inteligente (Músculo/Grasa)"
            ])
            
        # --- BLOQUE 2: HISTORIAL CLÍNICO Y BIOMECÁNICA DE LESIONES ---
        st.markdown("<div class='section-header'>🩺 2. Historial Clínico, Lesiones y Limitaciones</div>", unsafe_allow_html=True)
        col4, col5 = st.columns(2)
        with col4:
            lesiones = st.selectbox("¿Sufres o has sufrido de alguna lesión articular o muscular?", [
                "Seleccione...",
                "Ninguna (Completamente Sano/a)",
                "Lesión en Hombros / Manguito Rotador",
                "Lesión o dolor crónico en Rodillas",
                "Hernia discal / Molestias en zona Lumbar",
                "Lesión en Muñecas / Codos",
                "Múltiples lesiones / Limitaciones combinadas"
            ])
            detalles_lesiones = st.text_area("Si seleccionaste alguna molestia, describe detalladamente qué movimientos o ejercicios te causan dolor mecánico:")
        with col5:
            patologias = st.selectbox("¿Cuentas con algún diagnóstico médico o patología clínica?", [
                "Seleccione...",
                "Ninguna patología",
                "Hipertensión Arterial / Problemas cardiacos",
                "Diabetes / Resistencia a la Insulina",
                "Hipotiroidismo / Hipertiroidismo",
                "Asma / Problemas respiratorios crónicos"
            ])
            medicamentos = st.text_input("¿Tomas actualmente algún medicamento prescrito? (Si no, escribe 'Ninguno'):")

        # --- BLOQUE 3: HISTORIAL NUTRICIONAL Y HABITOS ---
        st.markdown("<div class='section-header'>🥗 3. Perfil Nutricional e Historial Alimenticio</div>", unsafe_allow_html=True)
        col6, col7 = st.columns(2)
        with col6:
            actividad_diaria = st.selectbox("Nivel de Actividad Diaria fuera del Gimnasio (Gasto NEAT):", [
                "Seleccione...",
                "Muy Bajo (Sedentario, trabajo de oficina/sentado)",
                "Moderado (De pie gran parte del día, maestros, cajeros)",
                "Alto (Movimiento constante, caminatas largas diarios)",
                "Muy Alto (Trabajo físico pesado, construcción, mudanzas)"
            ])
            cantidad_comidas = st.selectbox("¿Cuántas comidas sólidas realizas normalmente al día?", [
                "Seleccione...", "1 a 2 comidas", "3 comidas", "4 comidas", "5 o más comidas"
            ])
        with col7:
            alergias_evitar = st.text_area("¿Tienes alguna alergia alimentaria o alimentos que te desagraden/prefieras evitar por completo?:")
            consumo_agua = st.selectbox("¿Cuánta agua natural consumes aproximadamente al día?", [
                "Seleccione...", "Menos de 1 Litro", "Entre 1 y 2 Litros", "Entre 2 y 3 Litros", "Más de 3 Litros"
            ])

        # --- BLOQUE 4: PLANIFICACIÓN DEL ENTRENAMIENTO ---
        st.markdown("<div class='section-header'>🏋️ 4. Historial, Disponibilidad y Entorno de Entrenamiento</div>", unsafe_allow_html=True)
        col8, col9 = st.columns(2)
        with col8:
            experiencia = st.selectbox("¿Cuánto tiempo llevas entrenando de forma continua en gimnasio?", [
                "Seleccione...", "Ninguna experiencia / Absoluto principiante", "Menos de 1 año", "1 a 3 años", "Más de 3 años continuos"
            ])
            frecuencia = st.selectbox("¿De cuántos días dispones a la semana para ir al Gimnasio?", [
                "Seleccione...", "3 Días", "4 Días", "5 Días", "6 Días"
            ])
        with col9:
            entorno_entreno = st.selectbox("¿Dónde vas a realizar tus rutinas de ejercicio?", [
                "Seleccione...",
                "Gimnasio Comercial Completo (Máquinas, poleas, pesos libres)",
                "Gimnasio de Unidad Habitacional / Básico (Mancuernas limitadas)",
                "En casa (Solo peso corporal / Bandas elásticas)"
            ])
            tiempo_sesion = st.selectbox("¿Cuánto tiempo máximo le puedes dedicar a cada sesión?", [
                "Seleccione...", "Menos de 45 minutos", "Entre 45 y 60 minutos", "Entre 60 y 90 minutos", "Más de 90 minutos"
            ])

        enviar_datos = st.form_submit_button("🚀 Registrar Evaluación Completa en MINDMUSCLE247")
        
        if enviar_datos:
            # Control estricto del Frontend para campos tipo selectbox obligatorios
            if (not nombre.strip() or genero == "Seleccione..." or meta_cliente == "Seleccione..." or 
                lesiones == "Seleccione..." or patologias == "Seleccione..." or actividad_diaria == "Seleccione..." or 
                cantidad_comidas == "Seleccione..." or consumo_agua == "Seleccione..." or experiencia == "Seleccione..." or 
                frecuencia == "Seleccione..." or entorno_entreno == "Seleccione..." or tiempo_sesion == "Seleccione..."):
                st.error("❌ Error en el envío: Para poder diseñar tu estrategia biomecánica y calórica, todos los menús desplegables son obligatorios.")
            else:
                # Estructura idéntica y expandida para evitar rechazos en el Google Sheet
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre.strip(),
                    "Edad": int(edad),
                    "Peso (kg)": float(peso),
                    "Estatura (cm)": int(estatura),
                    "Género": genero,
                    "Meta": meta_cliente,
                    "Lesiones": lesiones,
                    "Detalles Lesión": detalles_lesiones.strip(),
                    "Patologías": patologias,
                    "Medicamentos": medicamentos.strip(),
                    "Gasto NEAT": actividad_diaria,
                    "Comidas por Día": cantidad_comidas,
                    "Alimentos Evitar": allergies_evitar.strip(),
                    "Consumo Agua": consumo_agua,
                    "Experiencia": experiencia,
                    "Frecuencia Semanal": frecuencia,
                    "Entorno": entorno_entreno,
                    "Tiempo Sesión": tiempo_sesion,
                    "Propuesta General": "",      # Espacios reservados para las respuestas del Administrador
                    "Balance Energético": "",
                    "Rutina Biomecánica": ""
                }])
                
                try:
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Respuestas", data=df_final)
                    st.success("✅ ¡Evaluación de 22 variables procesada con éxito! Tu información ya se encuentra disponible para análisis biomecánico.")
                    st.balloons()
                except Exception as err:
                    st.error(f"Error crítico de base de datos: {err}. Reporta este problema.")

# =============================================================================
# MÓDULO 2: PANEL DE ADMINISTRACIÓN COMPLETO Y EXPORTADOR
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso seguro autorizado.")
        
        if df_existente.empty or len(df_existente) == 0:
            st.warning("Aún no existen registros clínicos completados en la base de datos.")
        else:
            st.subheader("📋 Métrica y Base de Datos Completa de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🛠️ Prescripción de Planes Basada en Evidencia y Variables")
            
            lista_alumnos = df_existente["Nombre"].unique()
            alumno_sel = st.selectbox("Seleccione el alumno a evaluar en esta sesión:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            # Desglose de información analítica capturada para la toma de decisiones del Coach
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**⚖️ Peso:** {datos_alumno['Peso (kg)']} kg | **📏 Estatura:** {datos_alumno['Estatura (cm)']} cm")
                st.markdown(f"**🎯 Meta:** {datos_alumno['Meta']}")
                st.markdown(f"**🏃 Gasto Diario Fuera del Gym:** {datos_alumno['Gasto NEAT']}")
                st.markdown(f"**🩺 Lesiones Reportadas:** {datos_alumno['Lesiones']} ({datos_alumno.get('Detalles Lesión', 'Sin detalles')})")
            with col_b:
                st.markdown(f"**⏱️ Disponibilidad:** {datos_alumno['Frecuencia Semanal']} | **⏰ Duración:** {datos_alumno['Tiempo Sesión']}")
                st.markdown(f"**🏢 Entorno de Trabajo:** {datos_alumno['Entorno']}")
                st.markdown(f"**🥗 Hábitos:** {datos_alumno['Comidas por Día']} comidas | Evita: {datos_alumno.get('Alimentos Evitar', 'Ninguno')}")
            
            # Formulario técnico para rellenar observaciones del Coach
            with st.form("planificacion_coach_avanzada"):
                st.markdown("### 📋 1. Propuesta General de Mejora y Saludable")
                propuesta = st.text_area("Establecer la estrategia general del plan:", 
                                         value=str(datos_alumno.get("Propuesta General", "")))
                
                st.markdown("### 🥗 2. Balance Energético Inicial y Ajuste Dieta Diaria")
                balance = st.text_area("Pauta alimenticia basada en macronutrientes, calorías meta y distribución diaria:", 
                                       value=str(datos_alumno.get("Balance Energético", "")))
                
                st.markdown("### 🏋️ 3. Planificación Semanal de Gym (Fundamentos Biomecánicos e Hipertrofia)")
                rutina = st.text_area("Dosificación de la rutina, selección de ejercicios adaptados a sus lesiones y volumen de series:", 
                                      value=str(datos_alumno.get("Rutina Biomecánica", "")))
                
                guardar_cambios = st.form_submit_button("💾 Guardar y Vincular Cambios con Google Sheets")
                
                if guardar_cambios:
                    try:
                        df_existente.at[idx_alumno, "Propuesta General"] = propuesta
                        df_existente.at[idx_alumno, "Balance Energético"] = balance
                        df_existente.at[idx_alumno, "Rutina Biomecánica"] = rutina
                        
                        conn.update(worksheet="Respuestas", data=df_existente)
                        st.success(f"Ficha de {alumno_sel} actualizada correctamente en la nube.")
                        st.rerun()
                    except Exception as e_save:
                        st.error(f"Fallo de sincronización: {e_save}")
            
            # GENERACIÓN COMPLETA DEL DOCUMENTO EN PDF
            st.markdown("---")
            st.subheader("📄 Exportación de Ficha PDF Oficial")
            
            if st.button("🖨️ Compilar Reporte PDF Avanzado"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    pdf.set_font("Arial", "B", 18)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "PLANIFICACIÓN INTEGRAL DE RENDIMIENTO Y SALUD", ln=True, align="C")
                    pdf.set_font("Arial", "I", 9)
                    pdf.cell(0, 6, f"Fecha de Emisión: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True, align="C")
                    pdf.line(10, 36, 200, 36)
                    pdf.ln(12)
                    
                    # Datos Clínicos
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, f"1. DIAGNÓSTICO METABÓLICO Y ARTICULAR DEL ALUMNO: {datos_alumno['Nombre']}", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 6, f"Edad: {datos_alumno['Edad']} anos  |  Peso: {datos_alumno['Peso (kg)']} kg  |  Estatura: {datos_alumno['Estatura (cm)']} cm", ln=True)
                    pdf.cell(0, 6, f"Objetivo: {datos_alumno['Meta']}  |  Nivel NEAT: {datos_alumno['Gasto NEAT']}", ln=True)
                    pdf.cell(0, 6, f"Patologias/Medicamentos: {datos_alumno['Patologías']} / {datos_alumno.get('Medicamentos', 'Ninguno')}", ln=True)
                    pdf.cell(0, 6, f"Limitacion Articular: {datos_alumno['Lesiones']} - {datos_alumno.get('Detalles Lesión', '')}", ln=True)
                    pdf.ln(6)
                    
                    # Propuesta General
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "2. ENFOQUE METODOLÓGICO Y PROPUESTA GENERAL DE MEJORA", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Propuesta General"]))
                    pdf.ln(6)
                    
                    # Balance Energético
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "3. BALANCE ENERGÉTICO INICIAL Y DISEÑO DE PLAN ALIMENTICIO", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Balance Energético"]))
                    pdf.ln(6)
                    
                    # Rutina Semanal
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "4. PROGRAMACIÓN SEMANAL DE GYM (AJUSTE BIOMECÁNICO E HIPERTROFIA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Rutina Biomecánica"]))
                    
                    pdf_data = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Descargar Ficha PDF Completa",
                        data=pdf_data,
                        file_name=f"Ficha_Avanzada_MM247_{alumno_sel.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error técnico al construir el PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Contraseña incorrecta. Acceso restringido al sistema MINDMUSCLE247.")
