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
            frecuencia_display = str(datos_alumno.get('Frecuencia', '3 Días por semana'))
            tiempo_display = str(datos_alumno.get('Tiempo Sesión', 'De 45 a 75 minutos'))
            grasa_display = str(datos_alumno.get('Grasa', ''))

            st.markdown(f"### 👤 Expediente Actualizado: {nombre_display}")
            c_info1, c_info2 = st.columns(2)
            with c_info1:
                st.markdown(f"**📏 Antropometría:** Peso: {peso_display} | Estatura: {estatura_display} | Edad: {edad_display}")
                st.markdown(f"**📊 Composición Corporal:** {grasa_display}")
                st.markdown(f"**🩺 Limitaciones Clínicas:** {lesion_display}")
            with c_info2:
                st.markdown(f"**🎯 Objetivo Estructural:** {meta_display}")
                st.markdown(f"**🥗 Gasto Diario NEAT:** {neat_display}")
                st.markdown(f"**🏋️ Disponibilidad:** {frecuencia_display} | {tiempo_display}")
            
            v_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
            v_balance = str(datos_alumno.get("Balance Energético", "")).strip()
            v_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
            
            # --- GENERACIÓN INTELIGENTE AUTOMÁTICA HOJA 1: DIAGNÓSTICO ---
            if v_propuesta in ["", "nan"]:
                v_propuesta = (
                    f"ALUMNO: {nombre_display}\n\n"
                    f"• ANÁLISIS DE PARTIDA: Diagnóstico metabólico calculado mediante {grasa_display}. Objetivo: {meta_display}.\n"
                    f"• HISTORIAL DE RIESGO: Presenta vulnerabilidad catalogada en: '{lesion_display}'.\n"
                    f"• DIRECTRIZ DE CARGA: Se restringen cargas axiales directas. Todo ejercicio se ejecutará bajo condiciones de total estabilidad mecánica en poleas y máquinas guiadas para eliminar el perfil de riesgo lesivo y optimizar el estímulo del tejido contráctil."
                )
            
            # --- GENERACIÓN INTELIGENTE AUTOMÁTICA HOJA 2: RUTINA BIOMECÁNICA ---
            if v_rutina in ["", "nan"]:
                # Ajuste biomecánico según lesiones
                filtro_maquinas = "Evitar Sentadillas libres o Prensa profunda. Usar Extensión de Rodillas en máquina (perfil de fuerza acortado) y Curl Femoral sentado." if "Rodillas" in lesion_display else \
                                  "Evitar Press Militar con barra o cargas sobre la cabeza. Usar Cruces en Polea Media y elevaciones laterales en máquina/polea." if "Hombros" in lesion_display else \
                                  "Evitar Peso Muerto convencional y Sentadilla libre. Priorizar Prensa de Piernas inclinada con espalda fija y remo en máquina apoyado en el pecho." if "Columna" in lesion_display else \
                                  "Priorizar ejercicios multiarticulares estables en máquinas guiadas y sistemas de poleas libres de vectores de torque destructivo."
                
                # Distribución según días disponibles
                if "3 Días" in frecuencia_display:
                    distribucion_dias = (
                        "• DÍA 1: Torso Completo (Énfasis empujes estables y tracciones en máquina) - Tiempo: " + tiempo_display + "\n"
                        "  - Press en Máquina Guiada (Pectoral): 3 series x 8-12 reps\n"
                        "  - Remo en Máquina con Soporte al Pecho (Dorsal): 3 series x 10-12 reps\n"
                        "  - Elevaciones Laterales en Polea (Deltoides): 3 series x 12-15 reps\n\n"
                        "• DÍA 2: Pierna Completa (Enfoque en estabilidad biomecánica) - Tiempo: " + tiempo_display + "\n"
                        "  - " + filtro_maquinas + "\n"
                        "  - Curl Femoral Tumbado o Sentado: 3 series x 10-12 reps\n"
                        "  - Prensa de Piernas (Rango seguro sin flexión lumbar): 3 series x 10-12 reps\n\n"
                        "• DÍA 3: Full Body de Estímulo Metabólico Continuo - Tiempo: " + tiempo_display + "\n"
                        "  - Jalón al Pecho en Polea Alta: 3 series x 10 reps\n"
                        "  - Extensión de Tríceps + Curl de Bíceps en Polea: 3 series x 12 reps"
                    )
                elif "4 Días" in frecuencia_display:
                    distribucion_dias = (
                        "• DÍA 1: Torso - Empujes y Deltoides (Estabilidad Controlada) - Tiempo: " + tiempo_display + "\n"
                        "  - Press de Pecho en Máquina Convergente: 4 series x 8-11 reps\n"
                        "  - Aperturas en Polea Alta (Pectoral Bajo): 3 series x 12 reps\n"
                        "  - Elevaciones Laterales en Máquina o Polea: 4 series x 12-15 reps\n\n"
                        "• DÍA 2: Tren Inferior - Cadera Anterior/Posterior - Tiempo: " + tiempo_display + "\n"
                        "  - " + filtro_maquinas + "\n"
                        "  - Prensa de Pierna (Pies altos y separados): 4 series x 10-12 reps\n\n"
                        "• DÍA 3: Torso - Tracciones y Brazos - Tiempo: " + tiempo_display + "\n"
                        "  - Jalón al Pecho en Polea Neutra: 4 series x 10 reps\n"
                        "  - Remo con Cable en Polea Baja: 3 series x 10-12 reps\n\n"
                        "• DÍA 4: Tren Inferior Especializado (Estímulo Isquiotibial/Glúteo) - Tiempo: " + tiempo_display + "\n"
                        "  - Curl Femoral Sentado (Máxima tensión en estiramiento): 4 series x 10-12 reps\n"
                        "  - Extensión de Cuádriceps (Fase excéntrica de 3 segundos): 3 series x 12 reps"
                    )
                else: # 5 o 6 Días (Como el caso de José Luis Novelo)
                    distribucion_dias = (
                        "• DÍA 1: Pectoral y Deltoides Anterior (Líneas de Fuerza Convergentes)\n"
                        "  - Press en Máquina Plana (Alineado con fibras medias): 4 series x 8-10 reps\n"
                        "  - Cruces en Polea Media (Máxima contracción): 3 series x 12 reps\n"
                        "  - Elevaciones Laterales en Polea Baja: 4 series x 12-15 reps\n\n"
                        "• DÍA 2: Dorsal y Deltoides Posterior (Tracciones Planas y Verticales)\n"
                        "  - Remo con Soporte en Pecho (Enfoque en Dorsal Ancho): 4 series x 10 reps\n"
                        "  - Jalón al Pecho Agarre Abierto en Polea: 3 series x 10-12 reps\n"
                        "  - Face Pulls en Polea con Cuerda: 4 series x 15 reps\n\n"
                        "• DÍA 3: Tren Inferior (Enfoque de Protección Articular Estricta)\n"
                        "  - " + filtro_maquinas + "\n"
                        "  - Prensa Inclinada Mecánicamente Estable: 4 series x 10-12 reps\n"
                        "  - Extensión de Pantorrilla en Máquina Costal: 4 series x 15 reps\n\n"
                        "• DÍA 4: Brazos Completos (Bíceps y Tríceps en Polea Continua)\n"
                        "  - Extensión de Tríceps con Cuerda sobre la cabeza: 4 series x 12 reps\n"
                        "  - Curl de Bíceps en Polea Baja con Barra Recta: 4 series x 10-12 reps\n\n"
                        "• DÍA 5: Estímulo Específico de Eslabones Débiles\n"
                        "  - Remo Gironda en Polea Baja: 3 series x 12 reps\n"
                        "  - Aperturas de Pectoral en Peck Deck: 3 series x 12 reps"
                    )

                # Cardio distribuido según la meta y perfil metabólico
                if "Obesidad" in grasa_display or "Pérdida" in meta_display:
                    cardio_estrategia = "• DOSIFICACIÓN CARDIOVASCULAR COMPLEMENTARIA MANDATORIA:\n  - Tipo: LISS (Caminata a Paso Firme / Inclinación Controlada sin impacto activo).\n  - Volumen: 35 a 45 minutos continuos al terminar cada entrenamiento de fuerza.\n  - Razón Biomecánica: Proteger cartílago de rodillas evitando el trote, maximizando oxidación lipídica por vía aeróbica limpia."
                else:
                    cardio_estrategia = "• DOSIFICACIÓN CARDIOVASCULAR COMPLEMENTARIA REGENERATIVA:\n  - Tipo: Cardio LISS Ligero (Caminata o Bicicleta Estática de baja resistencia).\n  - Volumen: 15 a 20 minutos post-entrenamiento.\n  - Razón Biomecánica: Optimizar retorno venoso, remoción de lactato y acelerar la recuperación mitocondrial."

                v_rutina = (
                    f"PLANIFICACIÓN DE CARGA ESTABLECIDA: {frecuencia_display} | Ventana por Sesión: {tiempo_display}\n"
                    f"SISTEMA DE ENTRENAMIENTO BASADO EN PRINCIPIOS DE BIOMECÁNICA APLICADA\n\n"
                    f"{distribucion_dias}\n\n"
                    f"{cardio_estrategia}"
                )

            # --- GENERACIÓN INTELIGENTE AUTOMÁTICA HOJA 3: DIETA NO VIOLENTA ---
            if v_balance in ["", "nan"]:
                if "Obesidad" in grasa_display or "Pérdida" in meta_display or "Recomposición" in meta_display:
                    v_balance = (
                        "ESTRATEGIA NUTRICIONAL: DÉFICIT CALÓRICO MODERADO NO VIOLENTO\n"
                        "Diseñado con base en tu gasto energético estimado para ver avances constantes sin inducir ansiedad severa ni frenar el metabolismo basal.\n\n"
                        "• CONSTANTES MACRONUTRICIONALES DIARIAS:\n"
                        "  - Proteína Base: 2.0g a 2.2g por kilogramo de peso corporal (Blindaje de masa muscular magra).\n"
                        "  - Carbohidratos Complejos: Moderados, concentrados estratégicamente en torno al entrenamiento.\n"
                        "  - Grasas Saludables: Esenciales para mantener balance hormonal óptimo.\n\n"
                        "• MENÚ DIARIO PROPUESTO (Ejemplo Flexible de Distribución):\n"
                        "  - DESAYUNO: 3 a 4 claras de huevo + 1 huevo entero revuelto con espinacas y verduras libres. 1 porción de avena integral en hojuelas cocida en agua con canela.\n"
                        "  - COMIDA: 150g a 180g de pechuga de pollo o filete de pescado blanco a la plancha. 100g de arroz blanco o integral cocido. Ensalada verde grande aliñada con 1 cucharadita de aceite de oliva virgen.\n"
                        "  - MERIENDA (Pre/Post Entreno): 1 scoop de proteína de suero aislada (Whey) mezclada con agua + 1 manzana mediana o 100g de fresas fresqueras.\n"
                        "  - CENA: 150g de filete de res magro o atún en agua. Taza de brócoli o calabacitas al vapor. 1/3 de pieza de aguacate mediano para aporte lipídico limpio.\n\n"
                        "• LÍQUIDOS: Mínimo 3 litros de agua natural distribuidos a lo largo del día para mantener la tasa de filtración y mitigar el hambre artificial."
                    )
                else: # Hipertrofia o Fuerza
                    v_balance = (
                        "ESTRATEGIA NUTRICIONAL: SUPERÁVIT CALÓRICO LIMPIO CONTROLADO\n"
                        "Enfoque en crear un balance energético positivo controlado no violento, maximizando síntesis proteica sin acumulación masiva de tejido graso.\n\n"
                        "• CONSTANTES MACRONUTRICIONALES DIARIAS:\n"
                        "  - Proteína Base: 2.0g por kilogramo para reparación fibrilar.\n"
                        "  - Carbohidratos: Altos para mantener repletos los depósitos de glucógeno muscular.\n\n"
                        "• MENÚ DIARIO PROPUESTO (Ejemplo Estructurado):\n"
                        "  - DESAYUNO: 3 huevos enteros con tortilla de maíz o pan integral. 1 plátano maduro.\n"
                        "  - COMIDA: 200g de carne de res magra o pechuga de pollo. 150g de arroz pesado ya cocido + taza de frijoles enteros.\n"
                        "  - MERIENDA: Licuado de 1 scoop de proteína + 50g de avena molida + 1 cucharada de crema de cacahuate natural.\n"
                        "  - CENA: 150g de pollo o pescado a la plancha + 150g de papa o camote al horno + vegetales libres al gusto."
                    )

            st.markdown("---")
            st.markdown("### 🛠️ Prescripción y Planificación de Sistemas MM247")
            st.caption("💡 Los campos de abajo se han autogenerado inteligentemente basados en los datos del alumno. Puedes editarlos libremente si deseas personalizar algún detalle antes de guardar.")
            
            with st.form("prescripcion_exacta_form"):
                propuesta = st.text_area("🩺 HOJA 1: Diagnóstico Clínico de Punto de Partida y Limitaciones:", value=v_propuesta, height=140)
                rutina = st.text_area("🏋️ HOJA 2: Rutina Semanal Completa, Máquinas y Cardio (Biomecánica):", value=v_rutina, height=220)
                balance = st.text_area("🥗 HOJA 3: Plan Alimenticio Calculado (Dieta Diaria No Violenta):", value=v_balance, height=220)
                
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
            
            if st.button("🖨️ Compilar y Exportar Reporte PDF Oficial de 3 Hojas"):
                try:
                    pdf = FPDF()
                    
                    # ---------------- PAGE 1: DIAGNÓSTICO ----------------
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 20)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 6, "INFORME DE EVALUACIÓN Y PRESCIPCIÓN DE RENDIMIENTO", ln=True, align="C")
                    pdf.line(10, 28, 200, 28)
                    pdf.ln(10)
                    
                    pdf.set_font("Arial", "B", 13)
                    pdf.cell(0, 6, f"HOJA 1: DIAGNÓSTICO DE INGRESO - ALUMNO: {nombre_display.upper()}", ln=True)
                    pdf.line(10, 39, 110, 39)
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 5, f"• Edad: {edad_display}  |  Peso: {peso_display}  |  Estatura: {estatura_display}", ln=True)
                    pdf.cell(0, 5, f"• Condición Inicial: {grasa_display}", ln=True)
                    pdf.cell(0, 5, f"• Meta Declarada: {meta_display}", ln=True)
                    pdf.cell(0, 5, f"• Historial Articular/Riesgo: {lesion_display}", ln=True)
                    pdf.ln(8)
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 6, "ANÁLISIS CLÍNICO E INTEGRAL DE INICIO:", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(propuesta))
                    
                    # ---------------- PAGE 2: ENTRENAMIENTO BIOMECÁNICO ----------------
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 13)
                    pdf.cell(0, 6, "HOJA 2: PLANIFICACIÓN SEMANAL Y DOSIFICACIÓN BIOMECÁNICA", ln=True, align="C")
                    pdf.line(10, 28, 200, 28)
                    pdf.ln(8)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(rutina))
                    
                    # ---------------- PAGE 3: NUTRICIÓN NO VIOLENTA ----------------
                    pdf.add_page()
                    pdf.set_font("Arial", "B", 16)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 13)
                    pdf.cell(0, 6, "HOJA 3: INTERVENCIÓN NUTRICIONAL Y DIETA DIARIA", ln=True, align="C")
                    pdf.line(10, 28, 200, 28)
                    pdf.ln(8)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(balance))
                    
                    # Descarga directa y limpia libre de codificaciones obsoletas
                    pdf_data = pdf.output(dest='S')
                    st.download_button(
                        label="⬇️ Descargar Reporte PDF de 3 Hojas Oficinales",
                        data=bytes(pdf_data),
                        file_name=f"Plan_MM247_3Hojas_{nombre_display.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error al compilar el reporte de 3 hojas: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Clave inválida.")
