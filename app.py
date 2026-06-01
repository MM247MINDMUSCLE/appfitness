import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
# =============================================================================
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
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
    .metric-title { font-size: 14px; color: #666666; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 24px; color: #111111; font-weight: bold; margin-top: 5px; }
    
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 45px; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# 2. MOTOR DE INTELIGENCIA Y CÁLCULOS AUTOMÁTICOS
# =============================================================================
def generar_propuesta_inteligente(datos):
    nombre = str(datos.get('Nombre', '')).title()
    grasa = str(datos.get('Grasa', ''))
    lesion = str(datos.get('Lesiones', 'Ninguna'))
    meta = str(datos.get('Meta', ''))
    neat = str(datos.get('Gasto NEAT', ''))
    frec = str(datos.get('Frecuencia', '3 Días por semana'))
    tiempo = str(datos.get('Tiempo Sesión', 'De 45 a 75 minutos'))
    exp = str(datos.get('Experiencia', ''))

    return f"1. DIAGNÓSTICO CLÍNICO DE PUNTO DE PARTIDA Y LIMITACIONES\nALUMNO: {nombre}\nPunto de partida metabólico determinado mediante {grasa}. Presenta una condición de limitaciones catalogada como: {lesion}. Se autoriza entrenamiento de fuerza bajo progresión milimétrica enfocado en corregir desbalances biomecánicos.\n\n2. RESUMEN DEL BALANCE ENERGÉGICO AJUSTADO\nFase asignada: {meta}. Déficit o superávit calculado según gasto diario ({neat}).\n\n3. RESUMEN DE DOSIFICACIÓN SEMANAL\nFrecuencia óptima establecida de: {frec} con sesiones de {tiempo} adaptada a madurez muscular: {exp}."

def generar_rutina_inteligente(datos):
    lesiones = str(datos.get('Lesiones', 'Ninguna'))
    nivel = str(datos.get('Experiencia', 'Intermedio'))

    rutina = f"SISTEMA DE ENTRENAMIENTO BIOMECÁNICO DETALLADO\nNivel: {nivel} | Restricciones de Carga: {lesiones}\n\n"
    rutina += "LUNES [Empuje - Pecho/Hombro/Tríceps]:\n- Press Inclinado con mancuernas: 4 Series x 8-10 reps (RPE 9)\n- Fondos en paralelas guiados: 3 Series x 10 reps\n- Laterales con polea baja: 4 Series x 12 reps\n\n"
    rutina += "MARTES [Tracción - Espalda/Bíceps]:\n- Jalón al pecho con agarre prono: 4 Series x 10 reps\n- Remo con soporte en pecho (Machine): 3 Series x 8-12 reps\n- Curl de bíceps inclinado: 3 Series x 12 reps\n\n"

    if "Rodillas" in lesiones:
        rutina += "MIÉRCOLES [Pierna Completa - Enfoque Terapéutico sin Impacto]:\n- Prensa de piernas (pies bajos, rango controlado): 4 Series x 12 reps\n- Extensión de rodillas (sin bloqueo articular): 3 Series x 15 reps\n- Curl femoral acostado: 4 Series x 10 reps\n\n"
    else:
        rutina += "MIÉRCOLES [Pierna Completa - Enfoque Estabilidad]:\n- Sentadilla Libre o en Hack: 4 Series x 8-10 reps\n- Prensa de piernas: 3 Series x 12 reps\n- Curl femoral acostado: 4 Series x 10 reps\n\n"

    rutina += "JUEVES / VIERNES / SÁBADO:\n[Rotación adaptada a capacidad de recuperación del alumno según su nivel]"
    return rutina

def generar_dieta_inteligente(datos):
    try:
        peso_str = str(datos.get('Rango Peso', '80 kg'))
        peso_kg = float(peso_str.replace(" kg", "").split(" ")[0])
    except:
        peso_kg = 80.0

    meta = str(datos.get('Meta', 'Hipertrofia'))
    neat = str(datos.get('Gasto NEAT', 'Moderado'))

    prot = round(peso_kg * 2.0, 1)
    grasa = round(peso_kg * 1.0, 1)
    carbs = round(peso_kg * 3.0, 1) 
    cals = round((prot * 4) + (grasa * 9) + (carbs * 4), 1)

    return f"ESTRATEGIA NUTRICIONAL Y DIETA DIARIA PERSONALIZADA\nMeta: {meta} | Gasto Energético Base: {neat}\n\nMACRONUTRIENTES OBJETIVO DIARIOS:\nCalorías Totales Estimadas: {cals} kcal | Proteína: {prot}g | Carbohidratos: {carbs}g | Grasas: {grasa}g\n\nDISTRIBUCIÓN DIARIA ESTABLECIDA:\n• COMIDA 1 (Desayuno / Pre-Entreno):\n  - {int(prot*0.3)}g de proteína (Ej. huevos/claras) + {int(carbs*0.3)}g de carbohidratos (Ej. avena).\n• COMIDA 2 (Post-Entreno):\n  - {int(prot*0.35)}g de proteína (Ej. pechuga/pescado) + {int(carbs*0.4)}g de carbohidratos (Ej. arroz blanco) + vegetales.\n• COMIDA 3 (Tarde / Snack):\n  - {int(prot*0.15)}g de proteína (Ej. Whey Protein) + 30g de grasas (Ej. almendras).\n• COMIDA 4 (Cena / Control de Ansiedad):\n  - {int(prot*0.2)}g de proteína magra + {int(carbs*0.3)}g de carbohidratos complejos + ensalada verde libre."

# =============================================================================
# 3. VARIABLES GLOBALES DE FORMULARIO
# =============================================================================
OPCIONES_EDAD = [f"{i} años" for i in range(14, 81)]
OPCIONES_PESO = [f"{round(i * 0.5, 1)} kg" for i in range(80, 401)] 
OPCIONES_ESTATURA = [f"{i} cm" for i in range(120, 221)]

opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

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
                tiempo_sesion = st.selectbox("Ventana de Tiempo Máxima disponible por entrenamiento:", ["Seleccione...", "Sesión Express (Menos de 45 minutes)", "Sesión Estándar (De 45 a 75 minutos)", "Sesión Extensa (Más de 75 minutos)"])
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
            grasa_display = str(datos_alumno.get('Grasa', ''))

            # Control de Estado (Session State) para el Alumno Actual
            if "alumno_actual" not in st.session_state or st.session_state.alumno_actual != alumno_sel:
                st.session_state.alumno_actual = alumno_sel
                st.session_state.v_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
                st.session_state.v_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
                st.session_state.v_balance = str(datos_alumno.get("Balance Energético", "")).strip()

            st.markdown(f"### 👤 Expediente Actualizado: {nombre_display}")
            
            # --- BOTÓN MÁGICO DE GENERACIÓN AUTOMÁTICA ---
            if st.button("🚀 Generar Plan Automático con IA (Cálculo Exacto MM247)"):
                st.session_state.v_propuesta = generar_propuesta_inteligente(datos_alumno)
                st.session_state.v_rutina = generar_rutina_inteligente(datos_alumno)
                st.session_state.v_balance = generar_dieta_inteligente(datos_alumno)
                st.rerun()

            st.markdown("---")
            st.markdown("### 🛠️ Prescripción y Planificación de Sistemas MM247")
            
            with st.form("prescripcion_exacta_form"):
                propuesta = st.text_area("🩺 HOJA 1: Resumen Integral (Ficha, Dieta y Rutina juntas):", value=st.session_state.v_propuesta, height=140)
                rutina = st.text_area("🏋️ HOJA 2: Rutina Semanal Detallada (Músculo, Ejercicio y Series):", value=st.session_state.v_rutina, height=200)
                balance = st.text_area("🥗 HOJA 3: Dieta Diaria Establecida (Comidas y Balance Energético):", value=st.session_state.v_balance, height=200)
                
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
                            # Actualizamos también el estado actual con lo modificado
                            st.session_state.v_propuesta = propuesta
                            st.session_state.v_rutina = rutina
                            st.session_state.v_balance = balance
                            st.success("✅ ¡Planificación guardada y sincronizada exitosamente!")
                        except Exception as e_save: st.error(f"Fallo de sincronización: {e_save}")
            
            # --- COMPILADOR PDF DE ALTA ARMONÍA ---
            if st.button("🖨️ Compilar y Exportar Reporte PDF Premium"):
                try:
                    pdf = FPDF()
                    
                    def limpiar_texto(txt):
                        t = str(txt).replace("•", "-").replace("–", "-").replace("—", "-")
                        return t.encode('latin-1', 'ignore').decode('latin-1')

                    # =========================================================================
                    # HOJA 1: INFOME DE PLANIFICACIÓN INTEGRAL (TODO EN UNA HOJA)
                    # =========================================================================
                    pdf.add_page()
                    pdf.set_fill_color(26, 26, 26) 
                    pdf.rect(0, 0, 210, 38, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 12, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("INFORME DE PLANIFICACIÓN INTEGRAL DE RENDIMIENTO"), ln=True, align="C")
                    
                    pdf.ln(18)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Ficha técnica destacada (Fondo Gris)
                    pdf.set_fill_color(245, 245, 245)
                    pdf.set_draw_color(200, 200, 200)
                    pdf.rect(10, 44, 190, 20, "DF")
                    
                    pdf.set_font("Arial", "B", 11)
                    pdf.set_xy(12, 46)
                    pdf.cell(0, 6, limpiar_texto(f"FICHA TÉCNICA CLÍNICA - ALUMNO: {nombre_display.upper()}"), ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.set_x(12)
                    pdf.cell(0, 6, limpiar_texto(f"Diagnóstico Metabólico Inicial: {grasa_display}"), ln=True)
                    
                    pdf.set_xy(10, 72)
                    pdf.set_font("Arial", "", 10)
                    # Usamos los valores desde session_state para garantizar que imprima lo generado
                    pdf.multi_cell(190, 6, limpiar_texto(st.session_state.v_propuesta))

                    # =========================================================================
                    # HOJA 2: RUTINA SEMANAL DETALLADA POR MÚSCULO, EJERCICIO Y SERIES
                    # =========================================================================
                    pdf.add_page()
                    pdf.set_fill_color(230, 81, 0) # Naranja Deportivo
                    pdf.rect(0, 0, 210, 32, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 20)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("DOSIFICACIÓN DE CARGA Y RUTINA SEMANAL DETALLADA"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Recuadro contenedor de Entrenamiento
                    pdf.set_fill_color(250, 250, 250)
                    pdf.set_draw_color(230, 81, 0) 
                    pdf.set_line_width(0.5)
                    
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(182, 6, limpiar_texto(st.session_state.v_rutina))

                    # =========================================================================
                    # HOJA 3: DIETA DIARIA ESTABLECIDA PARA BALANCE ENERGÉTICO IDEAL
                    # =========================================================================
                    pdf.add_page()
                    pdf.set_fill_color(46, 125, 50) # Verde Salud
                    pdf.rect(0, 0, 210, 32, "F")
                    
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 20)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(0, 4, limpiar_texto("PLAN ALIMENTICIO Y AJUSTE DE BALANCE ENERGÉGICO DIARIO"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    
                    # Recuadro contenedor de Dieta
                    pdf.set_fill_color(248, 249, 248)
                    pdf.set_draw_color(46, 125, 50) 
                    pdf.set_line_width(0.5)
                    
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(182, 6, limpiar_texto(st.session_state.v_balance))
                    
                    # Descargar PDF
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
