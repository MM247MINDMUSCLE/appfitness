import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# URL del puente Apps Script (Integrada de forma exacta)
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"

# URL de lectura limpia para el Dashboard administrador
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

# Función optimizada para refrescar la lectura de la base de datos sin caché retenida
def cargar_base_datos():
    try:
        # Forzamos con un parámetro aleatorio de tiempo para evitar que pandas lea una copia vieja guardada
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Estilos visuales de la interfaz
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:18px; color:#555555; text-align:center; margin-bottom:30px; }
    .section-header { font-size:22px; font-weight:bold; color:#111111; margin-top:20px; margin-bottom:10px; border-bottom: 2px solid #111111; padding-bottom:5px; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# MÓDULO 1: CUESTIONARIO CON ENTRADAS MÉTRICAS EXACTAS Y CÁLCULO DE IMC
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Diagnóstica Estandarizada - Ninguna Respuesta al Azar</div>", unsafe_allow_html=True)
    
    st.info("📌 Todos los campos son estrictamente obligatorios. Por favor, navega a través de las pestañas y completa cada sección. El botón de registro aparecerá al final de la última pestaña.")
    
    with st.form("cuestionario_cerrado_mm247", clear_on_submit=True):
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "👤 1. Perfil y Biotipo", 
            "🩺 2. Historial Fisioclínico", 
            "🥗 3. Nutrición y Desgaste Diario", 
            "🏋️ 4. Madurez Muscular y Tiempos (Final)"
        ])
        
        with tab1:
            st.markdown("<div class='section-header'>📊 Rango Demográfico y Antropometría Exacta</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre Completo del Alumno:")
                edad_exacta = st.number_input("Edad Exacta (Años):", min_value=10, max_value=100, value=25, step=1)
                genero = st.selectbox("Género Biológico (Factor Metabólico):", ["Seleccione...", "Masculino", "Femenino"])
            with col2:
                peso_exacto = st.number_input("Peso Corporal Exacto (Kilogramos - kg):", min_value=30.0, max_value=250.0, value=70.0, step=0.1)
                estatura_exacta = st.number_input("Estatura / Altura Exacta (Centímetros - cm):", min_value=100, max_value=250, value=170, step=1)
            
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
                    "Seleccione...", "Ninguna - Sistema osteoarticular 100% sano", "Hombros / Complejo articular del manguito rotador", "Rodillas / Desgaste de cartílago o tendinitis", "Columna / Dolor lumbar crónico o hernia discal", "Codos o Muñecas / Epicondilitis o dolor de agarre", "Cadera o Tobillos / Limitación de rango de flexión"
                ])
                patologias = st.selectbox("Diagnóstico Clínico Preexistente:", [
                    "Seleccione...", "Ninguno - Completamente sano a nivel metabólico", "Hipertensión Arterial / Sistema cardiovascular sensible", "Diabetes Mellitus / Resistencia severa a la Insulina", "Alteraciones Tiroideas (Hipotiroidismo / Hipertiroidismo)", "Osteopenia / Artritis / Desgaste óseo"
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
                    "Seleccione...", "Sedentario Pasivo (Trabajo sentado, computadora, mínimo movimiento)", "Moderado Activo (Trabajo de pie, caminatas intermitentes, comercio)", "Intensidad Alta (Movimiento constante, carga de objetos, construcción)"
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
                    "Seleccione...", "Principiante Absoluto (Nunca he entrenado con pesas)", "Principiante Intermedio (Menos de 1 año, conozco los nombres de máquinas)", "Intermedio Avanzado (1 a 3 años de comodidad/consistencia)", "Avanzado Competitivo (Más de 3 años aplicando sobrecarga progresiva)"
                ])
                frecuencia = st.selectbox("Días Disponibles a la semana para Entrenar:", [
                    "Seleccione...", "3 Días por semana", "4 Días por semana", "5 Días por semana", "6 Días por semana"
                ])
            with col8:
                tiempo_sesion = st.selectbox("Ventana de Tiempo Máxima disponible por entrenamiento:", [
                    "Seleccione...", "Sesión Express (Menos de 45 minutes)", "Sesión Estándar (De 45 a 75 minutos)", "Sesión Extensa (Más de 75 minutos)"
                ])
                entorno_entreno = st.selectbox("Entorno Logístico y Equipamiento disponible:", [
                    "Seleccione...", "Gimnasio Comercial Completo (Poleas, cargas guiadas, pesos libres)", "Gimnasio de Condominio u Hotel (Mancuernas ligeras y polea básica)", "Entrenamiento en Casa (Peso corporal, ligas de resistencia)"
                ])
                fuerza_actual = st.selectbox("Percepción de Intensidad / Proximidad al Fallo (RPE):", [
                    "Seleccione...", "Pesos ligeros sin llegar al esfuerzo máximo", "Manejo pesos moderados controlando la fase excéntrica", "Entreno al fallo muscular o muy cerca de él (RIR 0-2)"
                ])
                cardio_actual = st.selectbox("Actividad Cardiovascular complementaria actual:", [
                    "Seleccione...", "Nulo / Sin trabajo cardiovascular", "Cardio LISS (Caminata / Elíptica suave)", "Cardio HIIT / Deportes de alta intensidad"
                ])
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            enviar_datos = st.form_submit_button("🚀 Registrar evaluación de máxima precisión MM247")

        if enviar_datos:
            if not nombre.strip() or genero == "Seleccione..." or meta_cliente == "Seleccione..." or lesiones == "Seleccione..." or patologias == "Seleccione..." or medicamentos == "Seleccione..." or analiticas == "Seleccione..." or alta_medica == "Seleccione..." or actividad_diaria == "Seleccione..." or cantidad_comidas == "Seleccione..." or consumo_agua == "Seleccione..." or horas_sueno == "Seleccione..." or nivel_estres == "Seleccione..." or experiencia == "Seleccione..." or frecuencia == "Seleccione..." or tiempo_sesion == "Seleccione..." or entorno_entreno == "Seleccione..." or fuerza_actual == "Seleccione..." or cardio_actual == "Seleccione...":
                st.error("❌ Error en el envío: Todos los campos del cuestionario son obligatorios. Revisa todas las pestañas.")
            else:
                estatura_m = estatura_exacta / 100.0
                imc_num = round(peso_exacto / (estatura_m ** 2), 1)
                
                if imc_num < 18.5:
                    diagnostico_grasa = f"IMC: {imc_num} (Bajo Peso)"
                elif 18.5 <= imc_num < 25.0:
                    diagnostico_grasa = f"IMC: {imc_num} (Peso Saludable)"
                elif 25.0 <= imc_num < 30.0:
                    diagnostico_grasa = f"IMC: {imc_num} (Sobrepeso)"
                else:
                    diagnostico_grasa = f"IMC: {imc_num} (Obesidad)"

                # Payload ordenado con nombres exactos de los encabezados de tu Sheet
                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": str(nombre.strip()), 
                    "Rango Edad": f"{edad_exacta} años", 
                    "Género": str(genero), 
                    "Rango Peso": f"{peso_exacto} kg", 
                    "Rango Estatura": f"{estatura_exacta} cm", 
                    "Grasa": str(diagnostico_grasa),
                    "Meta": str(meta_cliente), "Lesiones": str(lesiones), "Patologías": str(patologias), 
                    "Medicamentos": str(medicamentos), "Analíticas": str(analiticas), "Alta Médica": str(alta_medica), 
                    "Gasto NEAT": str(actividad_diaria), "Comidas": str(cantidad_comidas), "Agua": str(consumo_agua), 
                    "Sueño": str(horas_sueno), "Estrés": str(nivel_estres), "Experiencia": str(experiencia), 
                    "Frecuencia": str(frecuencia), "Tiempo Sesión": str(tiempo_sesion), "Entorno": str(entorno_entreno), 
                    "Fuerza": str(fuerza_actual), "Cardio": str(cardio_actual),
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }
                
                with st.spinner("Inyectando registro en la base de datos de Google Nube..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        if response.status_code == 200 and "success" in response.text:
                            st.success("✅ ¡Evaluación calculada y registrada con éxito total!")
                            st.balloons()
                        else:
                            st.error(f"Fallo de procesamiento en Google Script: {response.text}")
                    except Exception as api_err:
                        st.error(f"Error de conexión de red: {api_err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADMINISTRADOR (OPTIMIZADO CON MODIFICACIÓN DIRECTA)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado.")
        if df_existente.empty or len(df_existente) == 0:
            st.warning("No hay registros en la base de datos o el formato de lectura falló.")
        else:
            st.subheader("📋 Métrica Cerrada de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            lista_alumnos = df_existente["Nombre"].dropna().unique()
            alumno_sel = st.selectbox("Seleccione el alumno a prescribir:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            col_x, col_y = st.columns(2)
            with col_x:
                st.markdown(f"**👤 Alumno:** {datos_alumno['Nombre']} ({datos_alumno.get('Rango Edad', 'N/A')})")
                st.markdown(f"**📏 Antropometría:** Peso: {datos_alumno.get('Rango Peso', 'N/A')} | Estatura: {datos_alumno.get('Rango Estatura', 'N/A')}")
                st.markdown(f"**📊 Diagnóstico de Composición (Calculado):** {datos_alumno.get('Grasa', 'N/A')}")
                st.markdown(f"**🩺 Diagnóstico Clínico:** Patología: {datos_alumno.get('Patologías', 'N/A')} | Lesión: {datos_alumno.get('Lesiones', 'N/A')}")
            with col_y:
                st.markdown(f"**🎯 Objetivo Estructural:** {datos_alumno.get('Meta', 'N/A')}")
                st.markdown(f"**🥗 Metabolismo:** Gasto Diario (NEAT): {datos_alumno.get('Gasto NEAT', 'N/A')}")
                st.markdown(f"**🏋️ Perfil de Fuerza:** Nivel: {datos_alumno.get('Experiencia', 'N/A')} | Disponibilidad: {datos_alumno.get('Frecuencia', 'N/A')}")
            
            st.markdown("---")
            with st.form("prescripcion_exacta_form"):
                st.markdown("### 🩺 1. Diagnóstico Clínico de Punto de Partida")
                propuesta = st.text_area("Describa el estado de salud inicial del alumno y sus limitaciones seguras:", value=str(datos_alumno.get("Propuesta General", "")))
                
                st.markdown("### 🥗 2. Plan Alimenticio Calculado (Balance Energético Preciso)")
                balance = st.text_area("Escriba el desglose calórico, macronutrientes y distribución de menús adaptados a su NEAT y meta:", value=str(datos_alumno.get("Balance Energético", "")))
                
                st.markdown("### 🏋️ 3. Rutina Semanal Completa (Enfoque Biomecánico Adaptado)")
                rutina = st.text_area("Escriba la dosificación de series, repeticiones y ejercicios blindados contra lesiones:", value=str(datos_alumno.get("Rutina Biomecánica", "")))
                
                guardar_changes = st.form_submit_button("💾 Guardar Cambios en Base de Datos Nube")
                if guardar_changes:
                    # Armando el payload para actualizar la fila del alumno (pasando la fila completa)
                    payload_edit = {
                        "Action": "UPDATE", # Indicador para el script
                        "RowIndex": int(idx_alumno + 2), # La fila en Google Sheets es index + 2 (por el encabezado en fila 1)
                        "Fecha": str(datos_alumno['Fecha']), "Nombre": str(datos_alumno['Nombre']),
                        "Rango Edad": str(datos_alumno.get('Rango Edad', '')), "Género": str(datos_alumno.get('Género', '')),
                        "Rango Peso": str(datos_alumno.get('Rango Peso', '')), "Rango Estatura": str(datos_alumno.get('Rango Estatura', '')),
                        "Grasa": str(datos_alumno.get('Grasa', '')), "Meta": str(datos_alumno.get('Meta', '')),
                        "Lesiones": str(datos_alumno.get('Lesiones', '')), "Patologías": str(datos_alumno.get('Patologías', '')),
                        "Medicamentos": str(datos_alumno.get('Medicamentos', '')), "Analíticas": str(datos_alumno.get('Analíticas', '')),
                        "Alta Médica": str(datos_alumno.get('Alta Médica', '')), "Gasto NEAT": str(datos_alumno.get('Gasto NEAT', '')),
                        "Comidas": str(datos_alumno.get('Comidas', '')), "Agua": str(datos_alumno.get('Agua', '')),
                        "Sueño": str(datos_alumno.get('Sueño', '')), "Estrés": str(datos_alumno.get('Estrés', '')),
                        "Experiencia": str(datos_alumno.get('Experiencia', '')), "Frecuencia": str(datos_alumno.get('Frecuencia', '')),
                        "Tiempo Sesión": str(datos_alumno.get('Tiempo Sesión', '')), "Entorno": str(datos_alumno.get('Entorno', '')),
                        "Fuerza": str(datos_alumno.get('Fuerza', '')), "Cardio": str(datos_alumno.get('Cardio', '')),
                        "Propuesta General": propuesta, "Balance Energético": balance, "Rutina Biomecánica": rutina
                    }
                    with st.spinner("Guardando cambios..."):
                        try:
                            # Reutilizamos el webhook seguro de inyección controlada
                            response = requests.post(WEBHOOK_URL, json=payload_edit)
                            st.success("✅ ¡Planificación guardada y sincronizada con éxito en la nube!")
                            st.rerun()
                        except Exception as e_save:
                            st.error(f"Fallo de sincronización: {e_save}")
            
            if st.button("🖨️ Compilar y Exportar Reporte PDF Oficial"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    pdf.set_font("Arial", "B", 18)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "INFORME DE PLANIFICACIÓN INTEGRAL DE RENDIMIENTO", ln=True, align="C")
                    pdf.line(10, 28, 200, 28)
                    pdf.ln(8)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, f"FICHA TÉCNICA CLÍNICA - ALUMNO: {str(datos_alumno['Nombre']).upper()}", ln=True)
                    pdf.ln(3)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 5, f"Diagnóstico Metabólico Inicial: {str(datos_alumno.get('Grasa', 'N/A'))}", ln=True)
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "1. DIAGNÓSTICO CLÍNICO DE PUNTO DE PARTIDA Y LIMITACIONES", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(propuesta))
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "2. PLAN ALIMENTICIO Y BALANCE ENERGÉTICO AJUSTADO AL DESGASTE DIARIO", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(balance))
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "3. RUTINA SEMANAL COMPLETA (DOSIFICACIÓN Y BIOMECÁNICA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(rutina))
                    
                    pdf_data = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF Oficial MM247",
                        data=pdf_data,
                        file_name=f"Reporte_Oficial_MM247_{str(alumno_sel).replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error al compilar PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Clave inválida.")
