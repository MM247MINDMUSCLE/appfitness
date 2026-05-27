import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# URL del puente Apps Script 
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"

# URL de lectura limpia para el Dashboard administrador
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
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
    
    .metric-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #111111;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15 rgba(0,0,0,0.1); }
    .metric-title { font-size: 14px; color: #666666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #111111; font-weight: bold; margin-top: 5px; }
    
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

OPCIONES_EDAD = [f"{i} años" for i in range(14, 81)]
OPCIONES_PESO = [f"{round(i * 0.5, 1)} kg" for i in range(80, 401)] 
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
                actividad_diaria = st.selectbox("Desgaste del Día a Día fuera del Gimnasio (Gasto NEAT):", ["Seleccione...", "Sedentario Pasivo (Trabajo sentado, computadora, mínimo movimiento)", "Moderado Activo (Trabajo de pie, caminatas intermitentes, comercio)", "Intensidad Alta (Movimiento constante, carga de objetos, construcción)"])
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
                st.error("❌ Error en el envío: Todos los campos del cuestionario son obligatorios.")
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
                
                with st.spinner("Inyectando registro en Google Nube..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        if response.status_code == 200 and "success" in response.text:
                            st.success("✅ ¡Evaluación registrada con éxito total!")
                            st.balloons()
                        else: st.error(f"Fallo de procesamiento: {response.text}")
                    except Exception as api_err: st.error(f"Error de red: {api_err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADMINISTRADOR DINÁMICO
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado.")
        if df_existente.empty or len(df_existente) == 0:
            st.warning("No hay registros en la base de datos.")
        else:
            st.markdown("### 📈 Estado Global")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1: st.markdown(f"<div class='metric-card'><div class='metric-title'>Alumnos Totales</div><div class='metric-value'> {len(df_existente)} activos</div></div>", unsafe_allow_html=True)
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
            frecuencia_display = str(datos_alumno.get('Frecuencia', '3 Días por semana'))
            tiempo_display = str(datos_alumno.get('Tiempo Sesión', 'De 45 a 75 minutos'))
            grasa_display = str(datos_alumno.get('Grasa', ''))

            st.markdown(f"### 👤 Expediente Actualizado: {nombre_display}")
            
            v_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
            v_balance = str(datos_alumno.get("Balance Energético", "")).strip()
            v_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
            
            # --- HOJA 1 ORIGINAL RESTAURADA ---
            if v_propuesta in ["", "nan"]:
                v_propuesta = (
                    f"ALUMNO: {nombre_display}\n"
                    f"Diagnóstico Metabólico Inicial: {grasa_display}\n\n"
                    f"1. DIAGNÓSTICO CLÍNICO DE PUNTO DE PARTIDA Y LIMITACIONES\n"
                    f"ALUMNO: {nombre_display}\n"
                    f"Punto de partida metabólico determinado mediante {grasa_display}. Presenta una condición de limitaciones catalogada como: {lesion_display}. Se autoriza entrenamiento de fuerza bajo progresión milimétrica enfocado en corregir desbalances biomecánicos."
                )
            
            # --- HOJA 2 ORIGINAL ---
            if v_rutina in ["", "nan"]:
                v_rutina = (
                    f"3. RUTINA SEMANAL COMPLETA (DOSIFICACIÓN Y BIOMECÁNICA)\n"
                    f"Planificación Semanal: {frecuencia_display}\n"
                    f"Enfoque de Carga: Manejo de pesos moderados controlando la fase excéntrica adaptado a nivel {experiencia_display}.\n"
                    f"Estructura Biomecánica Recomendada:\n"
                    f"- Priorizar ejercicios multiarticulares estables en máquinas o poleas libres de tensión axial peligrosa.\n"
                    f"- Cardio complementario obligatorio asignado: Moderado LISS post-entrenamiento para control lipídico activo."
                )

            # --- HOJA 3 ORIGINAL ---
            if v_balance in ["", "nan"]:
                v_balance = (
                    f"2. PLAN ALIMENTICIO Y BALANCE ENERGÉTICO AJUSTADO\n"
                    f"Fase: Ajuste calórico limpio enfocado en {meta_display}.\n"
                    f"- Proteína: 2.0g por kg de peso corporal diario.\n"
                    f"- Carbohidratos: Enfocados en ventanas pre y post entreno para maximizar glucógeno.\n"
                    f"- Distribución: Adaptada de manera inteligente para garantizar síntesis proteica óptima sin picos de ansiedad."
                )

            st.markdown("---")
            st.markdown("### 🛠️ Prescripción y Planificación de Sistemas MM247")
            
            with st.form("prescripcion_exacta_form"):
                propuesta = st.text_area("🩺 HOJA 1: Diagnóstico Clínico (Original):", value=v_propuesta, height=140)
                balance = st.text_area("🥗 HOJA 3: Plan Alimenticio:", value=v_balance, height=160)
                rutina = st.text_area("🏋️ HOJA 2: Rutina Semanal Biomecánica:", value=v_rutina, height=160)
                
                guardar_changes = st.form_submit_button("💾 Guardar y Sincronizar Cambios con Google Sheets")
                if guardar_changes:
                    payload_edit = {
                        "Action": "UPDATE", "RowIndex": int(idx_alumno + 2),
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
                            requests.post(WEBHOOK_URL, json=payload_edit)
                            st.success("✅ ¡Planificación guardada!")
                            st.rerun()
                        except Exception as e_save: st.error(f"Fallo de sincronización: {e_save}")
            
            # --- COMPILADOR PDF DE ALTA ARMONÍA, COLORES Y RECUADROS ---
            if st.button("🖨️ Compilar y Exportar Reporte PDF Premium"):
                try:
                    pdf = FPDF()
                    
                    def limpiar_texto(txt):
                        t = str(txt).replace("•", "-").replace("–", "-").replace("—", "-")
                        return t.encode('latin-1', 'ignore').decode('latin-1')

                    # ---------------- HOJA 1: FORMATO ORIGINAL CON BRANDING ELEVADO ----------------
                    pdf.add_page()
                    # Encabezado corporativo (Gris Oscuro / Negro)
                    pdf.set_fill_color(26, 26, 26) 
                    pdf.rect(0, 0, 210, 38, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 12, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("INFORME DE PLANIFICACIÓN INTEGRAL DE RENDIMIENTO"), ln=True, align="C")
                    
                    pdf.ln(18)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Ficha técnica destacada de entrada (Fondo Gris Claro)
                    pdf.set_fill_color(245, 245, 245)
                    pdf.set_draw_color(200, 200, 200)
                    pdf.rect(10, 44, 190, 20, "DF")
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.set_xy(12, 46)
                    pdf.cell(0, 6, limpiar_texto(f"FICHA TÉCNICA CLÍNICA - ALUMNO: {nombre_display.upper()}"), ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.set_x(12)
                    pdf.cell(0, 6, limpiar_texto(f"Diagnóstico Metabólico Inicial: {grasa_display}"), ln=True)
                    
                    # Bloque de texto fluido original
                    pdf.set_xy(10, 72)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 6, limpiar_texto(propuesta))

                    # ---------------- HOJA 2: RUTINA BIOMECÁNICA (DISEÑO AUTODIDACTA EN RECUADROS) ----------------
                    pdf.add_page()
                    # Banner Superior Naranja/Rojo Deportivo para distinguir Entrenamiento
                    pdf.set_fill_color(230, 81, 0) 
                    pdf.rect(0, 0, 210, 32, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 20)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("SISTEMA DE ENTRENAMIENTO BIOMECÁNICO ADAPTADO"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Recuadro de diseño armónico para la rutina
                    pdf.set_fill_color(250, 250, 250)
                    pdf.set_draw_color(230, 81, 0) # Borde naranja elegante
                    pdf.set_linewidth(0.5)
                    
                    # Dibujamos un contenedor estilizado para la información de entrenamiento
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    
                    pdf.set_font("Arial", "", 10.5)
                    pdf.multi_cell(182, 6.5, limpiar_texto(rutina))

                    # ---------------- HOJA 3: DIETA Y NUTRICIÓN (DISEÑO EN RECUADROS VERDES) ----------------
                    pdf.add_page()
                    # Banner Superior Verde Salud para Nutrición
                    pdf.set_fill_color(46, 125, 50) 
                    pdf.rect(0, 0, 210, 32, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 20)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("ESTRATEGIA NUTRICIONAL Y BALANCE ENERGÉTICO"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Recuadro de diseño armónico para la nutrición
                    pdf.set_fill_color(248, 249, 248)
                    pdf.set_draw_color(46, 125, 50) # Borde verde elegante
                    
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    
                    pdf.set_font("Arial", "", 10.5)
                    pdf.multi_cell(182, 6.5, limpiar_texto(balance))
                    
                    # Descarga directa del archivo PDF
                    pdf_data = pdf.output(dest='S')
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF Premium de 3 Hojas",
                        data=bytes(pdf_data),
                        file_name=f"Plan_Premium_MM247_{nombre_display.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error al compilar el reporte premium: {err_pdf}")
                    
    elif password != "": st.error("🔑 Clave inválida.")
