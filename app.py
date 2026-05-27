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
# MÓDULO 1: CUESTIONARIO 100% OPCIÓN MÚLTIPLE (30 VARIABLES ESTÁNDAR)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Diagnóstica Estandarizada - Ninguna Respuesta al Azar</div>", unsafe_allow_html=True)
    
    st.info("📌 Todas las preguntas son obligatorias y de selección cerrada para garantizar la máxima precisión en el cálculo de tu balance energético y diseño biomecánico.")
    
    with st.form("cuestionario_cerrado_mm247", clear_on_submit=True):
        
        tab1, tab2, tab3, tab4 = st.tabs(["👤 Perfil y Biotipo", "🩺 Historial Fisioclínico", "🥗 Nutrición y Desgaste Diario", "🏋️ Madurez Muscular y Tiempos"])
        
        with tab1:
            st.markdown("<div class='section-header'>📊 Rango Demográfico y Antropometría</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre Completo del Alumno:")
                rango_edad = st.selectbox("Rango de Edad (Segmento Poblacional):", [
                    "Seleccione...",
                    "Joven Adolescente (12 a 17 años)",
                    "Adulto Joven (18 a 29 años)",
                    "Adulto Contemporáneo (30 a 49 años)",
                    "Adulto Mayor / Madurez (50 a 64 años)",
                    "Tercera Edad / Longevidad Avanzada (65 años o más)"
                ])
                genero = st.selectbox("Género Biológico (Factor Metabólico):", ["Seleccione...", "Masculino", "Femenino"])
            with col2:
                rango_peso = st.selectbox("Rango de Peso Corporal Actual:", [
                    "Seleccione...", "Menos de 50 kg", "De 50 a 60 kg", "De 61 a 70 kg", "De 71 a 80 kg", "De 81 a 90 kg", "De 91 a 100 kg", "Más de 100 kg"
                ])
                rango_estatura = st.selectbox("Rango de Estatura / Altura:", [
                    "Seleccione...", "Menos de 150 cm", "De 150 a 160 cm", "De 161 a 170 cm", "De 171 a 180 cm", "De 181 a 190 cm", "Más de 190 cm"
                ])
                porcentaje_grasa = st.selectbox("Estimación de Composición Corporal (Porcentaje Grasa):", [
                    "Seleccione...", "Bajo / Definido (<12% H / <20% M)", "Normal / Saludable (12-18% H / 20-27% M)", "Moderado / Sobrepeso leve (19-24% H / 28-34% M)", "Alto / Exceso de Grasa (>25% H / >35% M)"
                ])
            meta_cliente = st.selectbox("🎯 Meta Estructural u Objetivo Clínico Principal:", [
                "Seleccione...",
                "Hipertrofia Muscular (Aumento de masa magra)",
                "Pérdida de Tejido Graso (Definición estética y salud)",
                "Recomposición Corporal (Perder grasa y ganar músculo a la vez)",
                "Acondicionamiento Funcional (Enfoque en longevidad y vitalidad)",
                "Aumento de Fuerza Máxima / Rendimiento Deportivo"
            ])

        with tab2:
            st.markdown("<div class='section-header'>🩺 Punto de Partida Clínico y Seguridad de Carga</div>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                lesiones = st.selectbox("Limitación Articular o Lesión Activa:", [
                    "Seleccione...",
                    "Ninguna - Sistema osteoarticular 100% sano",
                    "Hombros / Complejo articular del manguito rotador",
                    "Rodillas / Desgaste de cartílago o tendinitis",
                    "Columna / Dolor lumbar crónico o hernia discal",
                    "Codos o Muñecas / Epicondilitis o dolor de agarre",
                    "Cadera o Tobillos / Limitación de rango de flexión"
                ])
                patologias = st.selectbox("Diagnóstico Clínico Preexistente:", [
                    "Seleccione...",
                    "Ninguno - Completamente sano a nivel metabólico",
                    "Hipertensión Arterial / Sistema cardiovascular sensible",
                    "Diabetes Mellitus / Resistencia severa a la Insulina",
                    "Alteraciones Tiroideas (Hipotiroidismo / Hipertiroidismo)",
                    "Osteopenia / Artritis / Desgaste óseo"
                ])
            with col4:
                medicamentos = st.selectbox("Uso de Medicación Prescrita Diaria:", [
                    "Seleccione...", "No tomo ningún medicamento", "Sí, medicamentos metabólicos (Insulina, Metformina, etc.)", "Sí, medicamentos de presión arterial / cardiovasculares", "Sí, antiinflamatorios / analgésicos recurrentes"
                ])
                analiticas = st.selectbox("Estado de Analíticas de Sangre Recientes (Últimos 6 meses):", [
                    "Seleccione...", "Lípidos y glucosa en rangos óptimos", "Colesterol o Triglicéridos elevados", "Glucosa en ayunas elevada / Prediabetes", "Ácido úrico o enzimas hepáticas alteradas", "No cuento con estudios analíticos recientes"
                ])
                alta_medica = st.selectbox("¿Cuenta con dictamen médico/autorización para entrenar fuerza?", [
                    "Seleccione...", "Sí, autorizado para cualquier tipo de carga libre", "Sí, pero restringido a cargas axiales ligeras o máquinas", "No / Entrenando bajo propio riesgo"
                ])

        with tab3:
            st.markdown("<div class='section-header'>🥗 Desgaste Diario, NEAT y Entorno Nutricional</div>", unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            with col5:
                actividad_diaria = st.selectbox("Desgaste del Día a Día fuera del Gimnasio (Gasto NEAT):", [
                    "Seleccione...",
                    "Sedentario Pasivo (Trabajo sentado, computadora, mínimo movimiento)",
                    "Moderado Activo (Trabajo de pie, caminatas intermitentes, comercio)",
                    "Intensidad Alta (Movimiento constante, carga de objetos, construcción)"
                ])
                cantidad_comidas = st.selectbox("Disponibilidad logística para distribución de comidas:", [
                    "Seleccione...", "2 comidas grandes al día", "3 comidas estándar al día", "4 comidas distribuidas", "5 comidas o más"
                ])
            with col6:
                consumo_agua = st.selectbox("Consumo diario promedio de agua natural:", [
                    "Seleccione...", "Insuficiente (Menos de 1.5 Litros)", "Adecuado (Entre 1.5 y 3 Litros)", "Óptimo (Más de 3 Litros)"
                ])
                horas_sueno = st.selectbox("Descanso y Recuperación del Sistema Nervioso (Sueño):", [
                    "Seleccione...", "Pobre / Insuficiente (Menos de 6 horas)", "Normal / Reparador (6 a 8 horas)", "Excelente (Más de 8 horas profundas)"
                ])
                nivel_estres = st.selectbox("Carga de Estrés Psicológico o Laboral Percibido:", [
                    "Seleccione...", "Bajo / Controlado", "Moderado manejable", "Crónico / Muy alto (Afecta energía)"
                ])

        with tab4:
            st.markdown("<div class='section-header'>🏋️ Experiencia de Fuerza y Ventana de Tiempo</div>", unsafe_allow_html=True)
            col7, col8 = st.columns(2)
            with col7:
                experiencia = st.selectbox("Nivel de Experiencia Práctica en Gimnasio (Madurez Muscular):", [
                    "Seleccione...",
                    "Principiante Absoluto (Nunca he entrenado con pesas)",
                    "Principiante Intermedio (Menos de 1 año, conozco los nombres de máquinas)",
                    "Intermedio Avanzado (1 a 3 años de consistencia, sé entrenar con intensidad)",
                    "Avanzado Competitivo (Más de 3 años aplicando sobrecarga progresiva)"
                ])
                frecuencia = st.selectbox("Días Disponibles a la semana para Entrenar:", [
                    "Seleccione...", "3 Días por semana", "4 Días por semana", "5 Días por semana", "6 Días por semana"
                ])
            with col8:
                tiempo_sesion = st.selectbox("Ventana de Tiempo Máxima disponible por entrenamiento:", [
                    "Seleccione...", "Sesión Express (Menos de 45 minutos)", "Sesión Estándar (De 45 a 75 minutos)", "Sesión Extensa (Más de 75 minutos)"
                ])
                entorno_entreno = st.selectbox("Entorno Logístico y Equipamiento disponible:", [
                    "Seleccione...",
                    "Gimnasio Comercial Completo (Poleas, cargas guiadas, pesos libres)",
                    "Gimnasio de Condominio u Hotel (Mancuernas ligeras y polea básica)",
                    "Entrenamiento en Casa (Peso corporal, ligas de resistencia)"
                ])
                fuerza_actual = st.selectbox("Percepción de Intensidad / Proximidad al Fallo (RPE):", [
                    "Seleccione...", "Pesos ligeros sin llegar al esfuerzo máximo", "Manejo pesos moderados controlando la fase excéntrica", "Entreno al fallo muscular o muy cerca de él (RIR 0-2)"
                ])
                cardio_actual = st.selectbox("Actividad Cardiovascular complementaria actual:", [
                    "Seleccione...", "Nulo / Sin trabajo cardiovascular", "Cardio LISS (Caminata / Elíptica suave)", "Cardio HIIT / Deportes de alta intensidad"
                ])

        st.markdown("<br>", unsafe_allow_html=True)
        enviar_datos = st.form_submit_button("🚀 Registrar Evaluación de Máxima Precisión MM247")
        
        if enviar_datos:
            # Validación estricta en bloque de que ningún campo se quede en el valor por defecto
            if (not nombre.strip() or rango_edad == "Seleccione..." or genero == "Seleccione..." or 
                rango_peso == "Seleccione..." or rango_estatura == "Seleccione..." or porcentaje_grasa == "Seleccione..." or
                meta_cliente == "Seleccione..." or lesiones == "Seleccione..." or patologias == "Seleccione..." or 
                medicamentos == "Seleccione..." or analiticas == "Seleccione..." or alta_medica == "Seleccione..." or 
                actividad_diaria == "Seleccione..." or cantidad_comidas == "Seleccione..." or consumo_agua == "Seleccione..." or 
                horas_sueno == "Seleccione..." or nivel_estres == "Seleccione..." or experiencia == "Seleccione..." or 
                frecuencia == "Seleccione..." or tiempo_sesion == "Seleccione..." or entorno_entreno == "Seleccione..." or 
                fuerza_actual == "Seleccione..." or cardio_actual == "Seleccione..."):
                st.error("❌ Error en el envío: Todos los campos desplegables son obligatorios para garantizar un reporte sin margen de error.")
            else:
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre.strip(), "Rango Edad": rango_edad, "Género": genero, "Rango Peso": rango_peso, 
                    "Rango Estatura": rango_estatura, "Grasa": porcentaje_grasa, "Meta": meta_cliente, "Lesiones": lesiones, 
                    "Patologías": patologias, "Medicamentos": medicamentos, "Analíticas": analiticas, "Alta Médica": alta_medica, 
                    "Gasto NEAT": actividad_diaria, "Comidas": cantidad_comidas, "Agua": consumo_agua, "Sueño": horas_sueno, 
                    "Estrés": nivel_estres, "Experiencia": experiencia, "Frecuencia": frecuencia, "Tiempo Sesión": tiempo_sesion, 
                    "Entorno": entorno_entreno, "Fuerza": fuerza_actual, "Cardio": cardio_actual,
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }])
                
                try:
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Respuestas", data=df_final)
                    st.success("✅ ¡Evaluación estandarizada inyectada en la base de datos con éxito!")
                    st.balloons()
                except Exception as err:
                    st.error(f"Error de base de datos: {err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADM Y COMPILADOR PDF PROFESIONAL
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado.")
        if df_existente.empty or len(df_existente) == 0:
            st.warning("No hay registros en la base de datos.")
        else:
            st.subheader("📋 Métrica Cerrada de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            lista_alumnos = df_existente["Nombre"].unique()
            alumno_sel = st.selectbox("Seleccione el alumno a prescribir:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            # Panel Analítico de Datos de Entrada para el Diagnóstico del Coach
            col_x, col_y = st.columns(2)
            with col_x:
                st.markdown(f"**👤 Alumno:** {datos_alumno['Nombre']} ({datos_alumno['Rango Edad']}) | **Género:** {datos_alumno['Género']}")
                st.markdown(f"**📏 Antropometría:** Peso: {datos_alumno['Rango Peso']} | Estatura: {datos_alumno['Rango Estatura']} | Grasa: {datos_alumno['Grasa']}")
                st.markdown(f"**🩺 Diagnóstico Clínico:** Patología: {datos_alumno['Patologías']} | Lesión: {datos_alumno['Lesiones']}")
                st.markdown(f"**💊 Control Médico:** Medicación: {datos_alumno['Medicamentos']} | Autorización: {datos_alumno['Alta Médica']}")
            with col_y:
                st.markdown(f"**🎯 Objetivo Estructural:** {datos_alumno['Meta']}")
                st.markdown(f"**🥗 Metabolismo y Desgaste:** Gasto Diario (NEAT): {datos_alumno['Gasto NEAT']} | Comidas: {datos_alumno['Comidas']}")
                st.markdown(f"**🏋️ Perfil de Fuerza:** Nivel: {datos_alumno['Experiencia']} | Disponibilidad: {datos_alumno['Frecuencia']} | Tiempo: {datos_alumno['Tiempo Sesión']}")
                st.markdown(f"**🧠 Entorno Nervioso:** Estrés: {datos_alumno['Estrés']} | Descanso: {datos_alumno['Sueño']} | Entorno: {datos_alumno['Entorno']}")
            
            st.markdown("---")
            with st.form("prescripcion_exacta_form"):
                st.markdown("### 🩺 1. Diagnóstico Clínico de Punto de Partida")
                propuesta = st.text_area("Describa el estado de salud inicial del alumno y sus limitaciones seguras:", value=str(datos_alumno.get("Propuesta General", "")))
                
                st.markdown("### 🥗 2. Plan Alimenticio Calculado (Balance Energético Preciso)")
                balance = st.text_area("Escriba el desglose calórico, macronutrientes y distribución de menús adaptados a su NEAT y meta:", value=str(datos_alumno.get("Balance Energético", "")))
                
                st.markdown("### 🏋️ 3. Rutina Semanal Completa (Enfoque Biomecánico Adaptado)")
                rutina = st.text_area("Escriba la dosificación de series, repeticiones y ejercicios blindados contra lesiones:", value=str(datos_alumno.get("Rutina Biomecánica", "")))
                
                guardar_cambios = st.form_submit_button("💾 Guardar Cambios en Base de Datos Nube")
                if guardar_cambios:
                    try:
                        df_existente.at[idx_alumno, "Propuesta General"] = propuesta
                        df_existente.at[idx_alumno, "Balance Energético"] = balance
                        df_existente.at[idx_alumno, "Rutina Biomecánica"] = rutina
                        conn.update(worksheet="Respuestas", data=df_existente)
                        st.success("Plan guardado con éxito. Listo para compilar en PDF.")
                        st.rerun()
                    except Exception as e_save:
                        st.error(f"Fallo de sincronización: {e_save}")
            
            # COMPILACIÓN DEL PDF OFICIAL DE PRECISIÓN MM247
            if st.button("🖨️ Compilar y Exportar Reporte PDF Oficial"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Encabezado Corporativo
                    pdf.set_font("Arial", "B", 18)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "INFORME DE PLANIFICACIÓN INTEGRAL DE RENDIMIENTO", ln=True, align="C")
                    pdf.line(10, 28, 200, 28)
                    pdf.ln(8)
                    
                    # Bloque Fijo de Métricas Estandarizadas
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, f"FICHA TÉCNICA CLÍNICA - ALUMNO: {datos_alumno['Nombre'].upper()}", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 5, f"Grupo de Edad: {datos_alumno['Rango Edad']}  |  Genero: {datos_alumno['Género']}", ln=True)
                    pdf.cell(0, 5, f"Segmento de Peso: {datos_alumno['Rango Peso']}  |  Estatura: {datos_alumno['Rango Estatura']}  |  Grasa: {datos_alumno['Grasa']}", ln=True)
                    pdf.cell(0, 5, f"Madurez en Fuerza: {datos_alumno['Experiencia']}  |  Disponibilidad: {datos_alumno['Frecuencia']} en {datos_alumno['Entorno']}", ln=True)
                    pdf.cell(0, 5, f"Gasto Diario Fuera del Gym (NEAT): {datos_alumno['Gasto NEAT']}", ln=True)
                    pdf.cell(0, 5, f"Meta Establecida: {datos_alumno['Meta']}", ln=True)
                    pdf.ln(5)
                    
                    # 1. Diagnóstico Clínico
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "1. DIAGNÓSTICO CLÍNICO DE PUNTO DE PARTIDA Y LIMITACIONES", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Propuesta General"]))
                    pdf.ln(5)
                    
                    # 2. Plan Alimenticio
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "2. PLAN ALIMENTICIO Y BALANCE ENERGÉTICO AJUSTADO AL DESGASTE DIARIO", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Balance Energético"]))
                    pdf.ln(5)
                    
                    # 3. Rutina Semanal
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "3. RUTINA SEMANAL COMPLETA (DOSIFICACIÓN Y BIOMECÁNICA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Rutina Biomecánica"]))
                    
                    pdf_data = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF Oficial MM247",
                        data=pdf_data,
                        file_name=f"Reporte_Oficial_MM247_{alumno_sel.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error al compilar PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Clave inválida.")
