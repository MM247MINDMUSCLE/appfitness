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
# MÓDULO 1: CUESTIONARIO INTEGRAL AVANZADO (30 VARIABLES ANALÍTICAS)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Diagnóstica de Máxima Personalización - Ficha Clínica, Nutrición & Biomecánica</div>", unsafe_allow_html=True)
    
    st.info("📌 Este cuestionario recopila métricas avanzadas para segmentar tu plan si eres principiante, avanzado, joven o adulto mayor. Responde con la mayor precisión posible.")
    
    with st.form("cuestionario_ultra_avanzado_mm247", clear_on_submit=True):
        
        # Uso de pestañas visuales para que no se vea kilométrico el formulario
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Perfil y Biotipo", "🩺 Historial Fisioclínico", "🥗 Nutrición y Estilo de Vida", "🏋️ Madurez Muscular y Entorno"])
        
        with tab1:
            st.markdown("<div class='section-header'>📊 Datos Antropométricos y Grupo Poblacional</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre Completo:")
                edad = st.number_input("Edad Actual (Años):", min_value=12, max_value=100, step=1, value=25)
                genero = st.selectbox("Género Biológico:", ["Seleccione...", "Masculino", "Femenino"])
                estatura = st.number_input("Estatura / Altura Exacta (en cm):", min_value=100, max_value=250, step=1, value=170)
            with col2:
                peso = st.number_input("Peso Corporal Actual (en kg):", min_value=30.0, max_value=250.0, step=0.1, value=70.0)
                porcentaje_grasa = st.selectbox("Estimación visual de grasa corporal o rango actual:", [
                    "Seleccione...", "Bajo / Delgado (Atleta)", "Normal / Promedio", "Moderado / Con sobrepeso", "Alto / Obesidad"
                ])
                perimetro_cintura = st.text_input("Perímetro de cintura en cm (Opcional - Escribe N/A si no lo sabes):", value="N/A")
                meta_cliente = st.selectbox("Objetivo Principal del Plan:", [
                    "Seleccione...", "Hipertrofia Muscular", "Pérdida de Tejido Graso", "Acondicionamiento Físico y Salud (Longevidad)", "Aumento de Fuerza / Rendimiento"
                ])

        with tab2:
            st.markdown("<div class='section-header'>🩺 Ficha Médica y Limitaciones de Carga</div>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                lesiones = st.selectbox("¿Sufres de alguna lesión o molestia articular/muscular?", [
                    "Seleccione...", "Ninguna", "Hombros", "Rodillas", "Columna / Lumbar", "Muñecas / Codos", "Cadera / Tobillos"
                ])
                detalles_lesiones = st.text_area("Describe qué movimientos específicos te detonan dolor físico o limitan tu rango de movimiento:")
                patologias = st.selectbox("Diagnóstico clínico preexistente (Metabólico / Cardiovascular):", [
                    "Seleccione...", "Ninguna patología", "Hipertensión", "Diabetes / Resistencia a la Insulina", "Hipotiroidismo / Hipertiroidismo", "Artritis / Osteoporosis (Adulto Mayor)"
                ])
            with col4:
                medicamentos = st.text_input("Medicamentos tomados habitualmente (Si no, escribe 'Ninguno'):")
                analiticas = st.selectbox("¿Tienes alguna alteración en tus analíticas de sangre recientes?", [
                    "Seleccione...", "Todo en rango saludable", "Colesterol / Triglicéridos altos", "Ácido úrico elevado", "Glucosa elevada", "No me he hecho estudios recientes"
                ])
                alta_medica = st.selectbox("¿Tienes autorización médica definitiva para cargar peso libre?", ["Seleccione...", "Sí, completamente autorizado", "No / En proceso de revisión"])

        with tab3:
            st.markdown("<div class='section-header'>🥗 Hábitos Alimenticios, Sueño y Estrés</div>", unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            with col5:
                actividad_diaria = st.selectbox("Nivel de Actividad Diaria fuera del Gym (Biotipo/NEAT):", [
                    "Seleccione...", "Sedentario (Oficina / Sentado)", "Moderado (De pie / Caminatas moderadas)", "Muy Activo (Trabajo físico / Movimiento constante)"
                ])
                cantidad_comidas = st.selectbox("¿Cuántas comidas sólidas al día se adaptan a tu agenda actual?", [
                    "Seleccione...", "1 a 2 comidas", "3 comidas", "4 comidas", "5 comidas"
                ])
                alergias_evitar = st.text_area("Alergias o alimentos que por presupuesto, gusto o digestión prefieras omitir:")
            with col6:
                consumo_agua = st.selectbox("Consumo diario de agua natural:", ["Seleccione...", "Menos de 1.5L", "Entre 1.5L y 3L", "Más de 3L"])
                horas_sueno = st.selectbox("Calidad y promedio de sueño por noche:", ["Seleccione...", "Mala (Menos de 6 horas)", "Regular (6 a 7 horas)", "Excelente (7 a 9 horas)"])
                nivel_estres = st.selectbox("Nivel de estrés psicológico o laboral diario:", ["Seleccione...", "Bajo / Controlado", "Moderado", "Muy Alto (Afecta mi energía)"])

        with tab4:
            st.markdown("<div class='section-header'>🏋️ Madurez Muscular y Disponibilidad Logística</div>", unsafe_allow_html=True)
            col7, col8 = st.columns(2)
            with col7:
                experiencia = st.selectbox("Nivel de experiencia real en entrenamientos de fuerza:", [
                    "Seleccione...", "Principiante Absoluto (Nunca he entrenado)", "Principiante (Menos de 1 año conociendo la técnica)", "Intermedio (1 a 3 años de entrenamiento constante)", "Avanzado (Más de 3 años entrenando pesado e intenso)"
                ])
                frecuencia = st.selectbox("Días por semana que puedes entrenar:", ["Seleccione...", "3 Días", "4 Días", "5 Días", "6 Días"])
                tiempo_sesion = st.selectbox("Tiempo máximo por sesión de gimnasio:", ["Seleccione...", "Menos de 45 min", "45 a 70 min", "Más de 70 min"])
            with col8:
                entorno_entreno = st.selectbox("¿Dónde entrenarás?", ["Seleccione...", "Gym Comercial completo", "Gym Básico", "En Casa / Calistenia"])
                fuerza_actual = st.selectbox("¿Conoces tu nivel de fuerza actual en ejercicios básicos (Sentadilla, Prensa, etc.)?", [
                    "Seleccione...", "No lo conozco (Manejo pesos muy ligeros)", "Intermedio (Conozco mis límites de peso)", "Alto (Entreno cerca del fallo muscular / RPE alto)"
                ])
                cardio_actual = st.selectbox("¿Realizas alguna actividad cardiovascular actualmente?", ["Seleccione...", "No realizo cardio", "Caminata ligera / Trote", "Ciclismo / Natación / Hit de alta intensidad"])

        st.markdown("<br>", unsafe_allow_html=True)
        enviar_datos = st.form_submit_button("🚀 Registrar Evaluación Diagnóstica Completa en MINDMUSCLE247")
        
        if enviar_datos:
            # Validación estricta en el Frontend
            if (not nombre.strip() or genero == "Seleccione..." or meta_cliente == "Seleccione..." or 
                lesiones == "Seleccione..." or patologias == "Seleccione..." or actividad_diaria == "Seleccione..." or 
                cantidad_comidas == "Seleccione..." or consumo_agua == "Seleccione..." or experiencia == "Seleccione..." or 
                frecuencia == "Seleccione..." or entorno_entreno == "Seleccione..." or tiempo_sesion == "Seleccione..." or
                porcentaje_grasa == "Seleccione..." or analiticas == "Seleccione..." or alta_medica == "Seleccione..." or
                horas_sueno == "Seleccione..." or nivel_estres == "Seleccione..." or fuerza_actual == "Seleccione..." or
                cardio_actual == "Seleccione..."):
                st.error("❌ Error en el envío: Todas las preguntas desplegables son obligatorias para poder armar la estrategia avanzada.")
            else:
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre.strip(), "Edad": int(edad), "Peso (kg)": float(peso), "Estatura (cm)": int(estatura),
                    "Género": genero, "Porcentaje Grasa": porcentaje_grasa, "Cintura (cm)": perimetro_cintura.strip(), "Meta": meta_cliente,
                    "Lesiones": lesiones, "Detalles Lesión": detalles_lesiones.strip(), "Patologías": patologias, "Medicamentos": medicamentos.strip(),
                    "Analíticas": analiticas, "Alta Médica": alta_medica, "Gasto NEAT": actividad_diaria, "Comidas por Día": cantidad_comidas,
                    "Alimentos Evitar": allergies_evitar.strip(), "Consumo Agua": consumo_agua, "Horas Sueño": horas_sueno, "Nivel Estrés": nivel_estres,
                    "Experiencia": experiencia, "Frecuencia Semanal": frecuencia, "Tiempo Sesión": tiempo_sesion, "Entorno": entorno_entreno,
                    "Fuerza Actual": fuerza_actual, "Cardio Actual": cardio_actual,
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }])
                
                try:
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Respuestas", data=df_final)
                    st.success("✅ ¡Evaluación de 30 variables guardada con éxito!")
                    st.balloons()
                except Exception as err:
                    st.error(f"Error crítico de base de datos: {err}")

# =============================================================================
# MÓDULO 2: PANEL DE ADMINISTRACIÓN Y EXPORTADOR AVANZADO
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso seguro autorizado.")
        if df_existente.empty or len(df_existente) == 0:
            st.warning("Aún no existen registros clínicos completados en la base de datos.")
        else:
            st.subheader("📋 Base de Datos Completa de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            lista_alumnos = df_existente["Nombre"].unique()
            alumno_sel = st.selectbox("Seleccione el alumno a evaluar en esta sesión:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            # Desglose Metodológico Completo para el Entrenador
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**👤 Perfil:** {datos_alumno['Nombre']} ({datos_alumno['Edad']} años) | **Biotipo:** {datos_alumno['Porcentaje Grasa']}")
                st.markdown(f"**⚖️ Métricas:** {datos_alumno['Peso (kg)']} kg | {datos_alumno['Estatura (cm)']} cm | Cintura: {datos_alumno.get('Cintura (cm)', 'N/A')}")
                st.markdown(f"**🩺 Salud Clínico:** Patologías: {datos_alumno['Patologías']} | Lesión: {datos_alumno['Lesiones']} ({datos_alumno.get('Detalles Lesión','')})")
                st.markdown(f"**💊 Analíticas / Medicinas:** {datos_alumno.get('Analíticas','')} | {datos_alumno.get('Medicamentos','')}")
            with col_b:
                st.markdown(f"**🏋️ Nivel Muscular:** Experiencia: {datos_alumno['Experiencia']} | Percepción de Fuerza: {datos_alumno.get('Fuerza Actual','')}")
                st.markdown(f"**⏱️ Logística:** {datos_alumno['Frecuencia Semanal']} por semana | {datos_alumno['Tiempo Sesión']} por sesión en {datos_alumno['Entorno']}")
                st.markdown(f"**🥗 Recuperación:** Sueño: {datos_alumno.get('Horas Sueño','')} | Estrés: {datos_alumno.get('Nivel Estrés','')} | Cardio: {datos_alumno.get('Cardio Actual','')}")
            
            with st.form("planificacion_coach_ultra_avanzada"):
                propuesta = st.text_area("1. Propuesta General de Mejora y Saludable:", value=str(datos_alumno.get("Propuesta General", "")))
                balance = st.text_area("2. Balance Energético Inicial y Ajuste Dieta Diaria:", value=str(datos_alumno.get("Balance Energético", "")))
                rutina = st.text_area("3. Planificación Semanal de Gym (Fundamentos Biomecánicos e Hipertrofia):", value=str(datos_alumno.get("Rutina Biomecánica", "")))
                
                guardar_cambios = st.form_submit_button("💾 Guardar e Inyectar Planificación en la Nube")
                if guardar_cambios:
                    try:
                        df_existente.at[idx_alumno, "Propuesta General"] = propuesta
                        df_existente.at[idx_alumno, "Balance Energético"] = balance
                        df_existente.at[idx_alumno, "Rutina Biomecánica"] = rutina
                        conn.update(worksheet="Respuestas", data=df_existente)
                        st.success("Ficha actualizada correctamente.")
                        st.rerun()
                    except Exception as e_save:
                        st.error(f"Fallo de sincronización: {e_save}")
            
            # EXPORTACIÓN PDF EN LATIN-1 CON PARSEO SEGURO
            if st.button("🖨️ Compilar Reporte PDF Avanzado"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 8, "PLANIFICACIÓN INTEGRAL DE RENDIMIENTO Y SALUD", ln=True, align="C")
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, f"FICHA TÉCNICA DEL ALUMNO: {datos_alumno['Nombre']}", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 5, f"Edad: {datos_alumno['Edad']} anos | Peso: {datos_alumno['Peso (kg)']} kg | Estatura: {datos_alumno['Estatura (cm)']} cm | Grasa: {datos_alumno['Porcentaje Grasa']}", ln=True)
                    pdf.cell(0, 5, f"Experiencia: {datos_alumno['Experiencia']} | Frecuencia: {datos_alumno['Frecuencia Semanal']} | Entorno: {datos_alumno['Entorno']}", ln=True)
                    pdf.cell(0, 5, f"Salud/Lesiones: {datos_alumno['Patologías']} / {datos_alumno['Lesiones']} ({datos_alumno.get('Detalles Lesión','')})", ln=True)
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "1. ENFOQUE METODOLÓGICO Y PROPUESTA GENERAL DE MEJORA", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Propuesta General"]))
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "2. BALANCE ENERGÉTICO INICIAL Y DISEÑO DE PLAN ALIMENTICIO", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Balance Energético"]))
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "3. PROGRAMACIÓN SEMANAL DE GYM (AJUSTE BIOMECÁNICO)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Rutina Biomecánica"]))
                    
                    pdf_data = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Descargar Ficha PDF",
                        data=pdf_data,
                        file_name=f"Ficha_MINDMUSCLE247_{alumno_sel.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error técnico al construir el PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Contraseña incorrecta.")
