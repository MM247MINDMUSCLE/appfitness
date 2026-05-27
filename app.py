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
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Limpiar los NaN globales de la base de datos para visualización limpia
        df = df.fillna("")
        return df
    except Exception as e:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Estilos visuales avanzados y animaciones CSS para el Dashboard Premium
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:18px; color:#555555; text-align:center; margin-bottom:30px; }
    .section-header { font-size:22px; font-weight:bold; color:#111111; margin-top:20px; margin-bottom:10px; border-bottom: 2px solid #111111; padding-bottom:5px; }
    
    /* Tarjetas de Métricas Animadas */
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #111111;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    .metric-title { font-size: 14px; color: #666666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #111111; font-weight: bold; margin-top: 5px; }
    
    /* Botones */
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# Opciones fijas de números en listas para evitar edición manual de texto
OPCIONES_EDAD = [f"{i} años" for i in range(14, 81)]
OPCIONES_PESO = [f"{round(i * 0.5, 1)} kg" for i in range(80, 401)] # Rango de 40kg a 200kg
OPCIONES_ESTATURA = [f"{i} cm" for i in range(120, 221)]

# =============================================================================
# MÓDULO 1: CUESTIONARIO CON SELECCIÓN DE NÚMEROS ESTRICTA
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Diagnóstica Estandarizada - Ninguna Respuesta al Azar</div>", unsafe_allow_html=True)
    
    st.info("📌 Todos los campos son estrictamente obligatorios. Selecciona tus datos numéricos de las opciones de lista correspondientes.")
    
    with st.form("cuestionario_cerrado_mm247", clear_on_submit=True):
        tab1, tab2, tab3, tab4 = st.tabs(["👤 1. Perfil", "🩺 2. Historial Clínico", "🥗 3. Estilo de Vida", "🏋️ 4. Entrenamiento"])
        
        with tab1:
            st.markdown("<div class='section-header'>📊 Rango Demográfico y Antropometría Exacta</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre Completo del Alumno:")
                edad_sel = st.selectbox("Edad Exacta:", ["Seleccione..."] + OPCIONES_EDAD)
                genero = st.selectbox("Género Biológico:", ["Seleccione...", "Masculino", "Femenino"])
            with col2:
                peso_sel = st.selectbox("Peso Corporal Exacto:", ["Seleccione..."] + OPCIONES_PESO)
                estatura_sel = st.selectbox("Estatura / Altura Exacta:", ["Seleccione..."] + OPCIONES_ESTATURA)
            
            meta_cliente = st.selectbox("🎯 Meta Estructural u Objetivo Clínico Principal:", [
                "Seleccione...",
                "Hipertrofia Muscular (Aumento de masa magra)",
                "Pérdida de Tejido Graso (Definición estética y salud)",
                "Recomposición Corporal (Perder grasa y ganar músculo a la vez)",
                "Acondicionamiento Funcional (Enfoque en longevidad y vitalidad)",
                "Aumento de Fuerza Máxima / Rendimiento Deportivo"
            ])

        with tab2:
            st.markdown("<div class='section-header'>🩺 Seguridad de Carga</div>", unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                lesiones = st.selectbox("Limitación Articular o Lesión Activa:", ["Seleccione...", "Ninguna - Sistema osteoarticular 100% sano", "Hombros / Complejo articular del manguito rotador", "Rodillas / Desgaste de cartílago o tendinitis", "Columna / Dolor lumbar crónico o hernia discal", "Codos o Muñecas / Epicondilitis o dolor de agarre", "Cadera o Tobillos / Limitación de rango de flexión"])
                patologias = st.selectbox("Diagnóstico Clínico Preexistente:", ["Seleccione...", "Ninguno - Completamente sano a nivel metabólico", "Hipertensión Arterial / Sistema cardiovascular sensible", "Diabetes Mellitus / Resistencia severa a la Insulina", "Alteraciones Tiroideas (Hipotiroidismo / Hipertiroidismo)", "Osteopenia / Artritis / Desgaste óseo"])
            with col4:
                medicamentos = st.selectbox("Uso de Medicación Prescrita Diaria:", ["Seleccione...", "No tomo ningún medicamento", "Sí, medicamentos metabólicos (Insulina, Metformina, etc.)", "Sí, medicamentos de presión arterial / cardiovasculares", "Sí, antiinflamatorios / analgésicos recurrentes"])
                analiticas = st.selectbox("Estado de Analíticas de Sangre Recientes:", ["Seleccione...", "Lípidos y glucosa en rangos óptimos", "Colesterol o Triglicéridos elevados", "Glucosa en ayunas elevada / Prediabetes", "Ácido úrico o enzimas hepáticas alteradas", "No cuento con estudios analíticos recientes"])
                alta_medica = st.selectbox("¿Cuenta con dictamen médico/autorización para entrenar fuerza?", ["Seleccione...", "Sí, autorizado para cualquier tipo de carga libre", "Sí, pero restringido a cargas axiales ligeras o máquinas", "No / Entrenando bajo propio riesgo"])

        with tab3:
            st.markdown("<div class='section-header'>🥗 Desgaste Diario y Entorno Nutricional</div>", unsafe_allow_html=True)
            col5, col6 = st.columns(2)
            with col5:
                actividad_diaria = st.selectbox("Desgaste del Día a Día fuera del Gimnasio (Gasto NEAT):", ["Seleccione...", "Sedentario Pasivo (Trabajo sentado, computadora, mínimo movement)", "Moderado Activo (Trabajo de pie, caminatas intermitentes, comercio)", "Intensidad Alta (Movimiento constante, carga de objetos, construcción)"])
                cantidad_comidas = st.selectbox("Disponibilidad logística para distribución de comidas:", ["Seleccione...", "2 comidas grandes al día", "3 comidas estándar al día", "4 comidas distribuidas", "5 comidas o más"])
            with col6:
                consumo_agua = st.selectbox("Consumo diario promedio de agua natural:", ["Seleccione...", "Insuficiente (Menos de 1.5 Litros)", "Adecuado (Entre 1.5 y 3 Litros)", "Óptimo (Más de 3 Litros)"])
                horas_sueno = st.selectbox("Descanso y Recuperación (Sueño):", ["Seleccione...", "Pobre / Insuficiente (Menos de 6 horas)", "Normal / Reparador (6 a 8 horas)", "Excelente (Más de 8 horas profundas)"])
                nivel_estres = st.selectbox("Carga de Estrés Psicológico o Laboral Percibido:", ["Seleccione...", "Bajo / Controlado", "Moderado manejable", "Crónico / Muy alto (Afecta energía)"])

        with tab4:
            st.markdown("<div class='section-header'>🏋️ Experiencia de Fuerza y Ventana de Tiempo</div>", unsafe_allow_html=True)
            col7, col8 = st.columns(2)
            with col7:
                experiencia = st.selectbox("Nivel de Experiencia Práctica en Gimnasio (Madurez Muscular):", ["Seleccione...", "Principiante Absoluto (Nunca he entrenado con pesas)", "Principiante Intermedio (Menos de 1 año, conozco los nombres de máquinas)", "Intermedio Avanzado (1 a 3 años de comodidad/consistencia)", "Avanzado Competitivo (Más de 3 años aplicando sobrecarga progresiva)"])
                frecuencia = st.selectbox("Días Disponibles a la semana para Entrenar:", ["Seleccione...", "3 Días por semana", "4 Días por semana", "5 Días por semana", "6 Días por semana"])
            with col8:
                tiempo_sesion = st.selectbox("Ventana de Tiempo Máxima disponible por entrenamiento:", ["Seleccione...", "Sesión Express (Menos de 45 minutos)", "Sesión Estándar (De 45 a 75 minutos)", "Sesión Extensa (Más de 75 minutos)"])
                entorno_entreno = st.selectbox("Entorno Logístico y Equipamiento disponible:", ["Seleccione...", "Gimnasio Comercial Completo (Poleas, cargas guiadas, pesos libres)", "Gimnasio de Condominio u Hotel (Mancuernas ligeras y polea básica)", "Entrenamiento en Casa (Peso corporal, ligas de resistencia)"])
                fuerza_actual = st.selectbox("Percepción de Intensidad / Proximidad al Fallo (RPE):", ["Seleccione...", "Pesos ligeros sin llegar al esfuerzo máximo", "Manejo pesos moderados controlando la fase excéntrica", "Entreno al fallo muscular o muy cerca de él (RIR 0-2)"])
                cardio_actual = st.selectbox("Actividad Cardiovascular complementaria actual:", ["Seleccione...", "Nulo / Sin trabajo cardiovascular", "Cardio LISS (Caminata / Elíptica suave)", "Cardio HIIT / Deportes de alta intensidad"])
            
            st.markdown("<br><hr>", unsafe_allow_html=True)
            enviar_datos = st.form_submit_button("🚀 Registrar evaluación de máxima precisión MM247")

        if enviar_datos:
            if "Seleccione..." in [edad_sel, peso_sel, estatura_sel, genero, meta_cliente, lesiones, patologias, medicamentos, analiticas, alta_medica, actividad_diaria, cantidad_comidas, consumo_agua, horas_sueno, nivel_estres, experiencia, frecuencia, tiempo_sesion, entorno_entreno, fuerza_actual, cardio_actual] or not nombre.strip():
                st.error("❌ Error en el envío: Todos los campos del cuestionario son obligatorios. Revisa todas las pestañas.")
            else:
                p_num = float(peso_sel.replace(" kg", ""))
                e_num = float(estatura_sel.replace(" cm", "")) / 100.0
                imc_num = round(p_num / (e_num ** 2), 1)
                
                if imc_num < 18.5: diagnostico_grasa = f"IMC: {imc_num} (Bajo Peso)"
                elif 18.5 <= imc_num < 25.0: diagnostico_grasa = f"IMC: {imc_num} (Peso Saludable)"
                elif 25.0 <= imc_num < 30.0: diagnostico_grasa = f"IMC: {imc_num} (Sobrepeso)"
                else: diagnostico_grasa = f"IMC: {imc_num} (Obesidad)"

                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": str(nombre.strip().lower()), 
                    "Rango Edad": str(edad_sel), "Género": str(genero), "Rango Peso": str(peso_sel), "Rango Estatura": str(estatura_sel), "Grasa": str(diagnostico_grasa),
                    "Meta": str(meta_cliente), "Lesiones": str(lesiones), "Patologías": str(patologias), "Medicamentos": str(medicamentos), "Analíticas": str(analiticas), "Alta Médica": str(alta_medica), 
                    "Gasto NEAT": str(actividad_diaria), "Comidas": str(cantidad_comidas), "Agua": str(consumo_agua), "Sueño": str(horas_sueno), "Estrés": str(nivel_estres), "Experiencia": str(experiencia), 
                    "Frecuencia": str(frecuencia), "Tiempo Sesión": str(tiempo_sesion), "Entorno": str(entorno_entreno), "Fuerza": str(fuerza_actual), "Cardio": str(cardio_actual),
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }
                
                with st.spinner("Inyectando registro en la base de datos de Google Nube..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        if response.status_code == 200 and "success" in response.text:
                            st.success("✅ ¡Evaluación calculada y registrada con éxito total!")
                            st.balloons()
                        else: st.error(f"Fallo de procesamiento en Google Script: {response.text}")
                    except Exception as api_err: st.error(f"Error de conexión de red: {api_err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADMINISTRADOR DINÁMICO Y ANIMADO
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado.")
        if df_existente.empty or len(df_existente) == 0:
            st.warning("No hay registros en la base de datos o el formato de lectura falló.")
        else:
            st.markdown("### 📈 Estado Global del Gimnasio")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1:
                st.markdown(f"<div class='metric-card'><div class='metric-title'>Alumnos Totales</div><div class='metric-value'> {len(df_existente)} activos</div></div>", unsafe_allow_html=True)
            with kpi2:
                obesidad_count = df_existente['Grasa'].str.contains('Obesidad|Sobrepeso').sum()
                st.markdown(f"<div class='metric-card'><div class='metric-title'>En Recomposición/Pérdida</div><div class='metric-value'>{obesidad_count} alumnos</div></div>", unsafe_allow_html=True)
            with kpi3:
                hipertrofia_count = df_existente['Meta'].str.contains('Hipertrofia').sum()
                st.markdown(f"<div class='metric-card'><div class='metric-title'>En Fase de Volumen</div><div class='metric-value'>{hipertrofia_count} alumnos</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Métrica Cerrada de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            lista_alumnos = df_existente["Nombre"].dropna().unique()
            alumno_sel = st.selectbox("Seleccione el alumno a prescribir:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            nombre_display = str(datos_alumno['Nombre']).title()
            peso_display = str(datos_alumno.get('Rango Peso', 'No especificado'))
            estatura_display = str(datos_alumno.get('Rango Estatura', 'No especificado'))
            edad_display = str(datos_alumno.get('Rango Edad', 'No especificado'))
            meta_display = str(datos_alumno.get('Meta', 'No especificado'))
            neat_display = str(datos_alumno.get('Gasto NEAT', 'No especificado'))
            lesion_display = str(datos_alumno.get('Lesiones', 'Ninguna'))
            experiencia_display = str(datos_alumno.get('Experiencia', 'No especificado'))
            
            st.markdown(f"### 👤 Expediente Actualizado: {nombre_display}")
            c_info1, c_info2 = st.columns(2)
            with c_info1:
                st.markdown(f"**📏 Antropometría:** Peso: {peso_display} | Estatura: {estatura_display} | Edad: {edad_display}")
                st.markdown(f"**📊 Composición Corporal:** {datos_alumno.get('Grasa', 'Sin datos')}")
                st.markdown(f"**🩺 Limitaciones Clínicas:** {lesion_display}")
            with c_info2:
                st.markdown(f"**🎯 Objetivo Estructural:** {meta_display}")
                st.markdown(f"**🥗 Gasto Diario NEAT:** {neat_display}")
                st.markdown(f"**🏋️ Madurez Muscular:** {experiencia_display}")
            
            v_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
            v_balance = str(datos_alumno.get("Balance Energético", "")).strip()
            v_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
            
            if v_propuesta in ["", "nan"]:
                v_propuesta = (
                    f"ALUMNO: {nombre_display}\n"
                    f"Punto de partida metabólico determinado mediante {datos_alumno.get('Grasa', 'antropometría')}. "
                    f"Presenta una condición de limitaciones catalogada como: {lesion_display}. "
                    f"Se autoriza entrenamiento de fuerza bajo progresión milimétrica enfocado en corregir desbalances biomecánicos."
                )
            
            if v_balance in ["", "nan"]:
                if "Hipertrofia" in meta_display:
                    v_balance = "Fase: Excedente Calórico (Volumen Limpio) [+300 kcal sobre mantenimiento]\n" \
                                "- Proteína: 2.0g por kg de peso corporal diario.\n" \
                                "- Carbohidratos: Enfocados en ventanas pre y post entreno para maximizar glucógeno.\n" \
                                f"- Distribución: Adaptada a {datos_alumno.get('Comidas', '3 comidas')} al día garantizando síntesis proteica óptima."
                elif "Pérdida" in meta_display or "Obesidad" in str(datos_alumno.get('Grasa', '')):
                    v_balance = "Fase: Déficit Calórico Controlado [-500 kcal para oxidación de grasa]\n" \
                                "- Proteína: Alta (2.2g por kg) para blindar y retener la masa muscular magra.\n" \
                                f"- Hidratación: Crítica. Ajustada a requerimiento de {datos_alumno.get('Agua', 'Agua óptima')}.\n" \
                                f"- Control de ansiedad: Organizado en {datos_alumno.get('Comidas', 'comidas pautadas')} cargadas de fibra vegetal."
                else:
                    v_balance = "Fase: Recomposición Corporal / Normocalórica [Mantenimiento Energético]\n" \
                                "- Nutrición balanceada enfocada en recomposición de tejido adiposo a tejido contráctil magro."
            
            if v_rutina in ["", "nan"]:
                v_rutina = f"Planificación Semanal: {datos_alumno.get('Frecuencia', 'Días variables')} ({datos_alumno.get('Tiempo Sesión', 'Tiempo estándar')})\n" \
                           f"Enfoque de Carga: {datos_alumno.get('Fuerza', 'RPE moderado')} adaptado a nivel {experiencia_display}.\n" \
                           "Estructura Biomecánica Recomendada:\n" \
                           "- Priorizar ejercicios multiarticulares estables en máquinas o poleas libres de tensión axial peligrosa.\n" \
                           f"- Cardio complementario obligatorio asignado: {datos_alumno.get('Cardio', 'Cardio moderado LISS')} post-entrenamiento."

            st.markdown("---")
            st.markdown("### 🛠️ Prescripción y Planificación de Sistemas MM247")
            st.caption("💡 Los campos de abajo se han autogenerado inteligentemente basados en los datos del alumno. Puedes editarlos libremente si deseas personalizar algún detalle antes de guardar.")
            
            with st.form("prescripcion_exacta_form"):
                propuesta = st.text_area("🩺 1. Diagnóstico Clínico de Punto de Partida:", value=v_propuesta, height=120)
                balance = st.text_area("🥗 2. Plan Alimenticio Calculado (Balance Energético Preciso):", value=v_balance, height=150)
                rutina = st.text_area("🏋️ 3. Rutina Semanal Completa (Enfoque Biomecánico Adaptado):", value=v_rutina, height=180)
                
                guardar_changes = st.form_submit_button("💾 Guardar y Sincronizar Cambios con Google Sheets")
                if guardar_changes:
                    payload_edit = {
                        "Action": "UPDATE",
                        "RowIndex": int(idx_alumno + 2),
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
                    pdf.cell(0, 6, f"FICHA TÉCNICA CLÍNICA - ALUMNO: {nombre_display.upper()}", ln=True)
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
                    pdf.cell(0, 6, "2. PLAN ALIMENTICIO Y BALANCE ENERGÉTICO AJUSTADO", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(balance))
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "3. RUTINA SEMANAL COMPLETA (DOSIFICACIÓN Y BIOMECÁNICA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(rutina))
                    
                    # RETORNO ARREGLADO: Sin método .encode(), directo a bytes estructurados
                    pdf_data = pdf.output(dest='S')
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF Oficial MM247",
                        data=bytes(pdf_data),
                        file_name=f"Reporte_MM247_{nombre_display.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error al compilar PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Clave inválida.")
