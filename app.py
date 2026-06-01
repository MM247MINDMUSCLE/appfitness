import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (BRANDING AUTOMATIZADO MM247)
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Limpieza estricta de espacios en los nombres de las columnas para evitar KeyErrors
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Inyección de Estilos CSS Personalizados
st.markdown("""
    <style>
    .main-title { font-size:44px; font-weight:900; color:#111111; text-align:center; letter-spacing: -1px; margin-bottom:0px; }
    .subtitle { font-size:16px; color:#666666; text-align:center; margin-bottom:35px; text-transform: uppercase; letter-spacing: 1px;}
    .section-header { font-size:20px; font-weight:bold; color:#111111; margin-top:25px; margin-bottom:12px; border-bottom: 3px solid #111111; padding-bottom:6px; }
    .metric-card { background: #ffffff; padding: 22px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-left: 6px solid #111111; }
    .metric-title { font-size: 13px; color: #777777; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #111111; font-weight: bold; margin-top: 4px; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 48px; border: none; }
    .stButton>button:hover { background-color: #333333; color: white; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# MENU DE NAVEGACIÓN
# =============================================================================
opcion = st.sidebar.selectbox(
    "Navegación del Sistema MM247:",
    ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"]
)

# =============================================================================
# 2. MOTOR DE INTELIGENCIA CLÍNICA, BIOMECÁNICA Y METABÓLICA
# =============================================================================
def procesar_metricas_base(datos):
    """Extrae de forma segura los valores numéricos de peso, estatura y edad."""
    try:
        peso = float(str(datos.get('Peso actual', '80')).replace(" kg", "").split()[0])
    except Exception: peso = 80.0
    try:
        estatura = float(str(datos.get('Estatura', '175')).replace(" cm", "").split()[0])
    except Exception: estatura = 175.0
    try:
        edad = float(str(datos.get('Edad', '25')).replace(" años", "").split()[0])
    except Exception: edad = 25.0
    
    genero = str(datos.get('Sexo', 'Masculino'))
    return peso, estatura, edad, genero

def calcular_motores_automatizados(datos):
    peso, estatura, edad, genero = procesar_metricas_base(datos)
    
    # METABOLISMO BASE (Harris-Benedict)
    if "Masculino" in genero:
        tmb = 66.473 + (13.751 * peso) + (5.0033 * estatura) - (6.755 * edad)
    else:
        tmb = 655.095 + (9.5634 * peso) + (1.8496 * estatura) - (4.6756 * edad)
        
    # Factor NEAT
    neat_str = str(datos.get('Nivel de actividad', 'Moderadamente activo'))
    factores = {"Sedentario": 1.2, "Poco activo": 1.375, "Moderadamente activo": 1.55, "Muy activo": 1.725}
    factor = factores.get(neat_str.split()[0], 1.55)
    tdee = tmb * factor
    
    # Balance Objetivo según Meta
    meta = str(datos.get('Objetivo principal', 'Recomposición corporal'))
    if "Perder" in meta or "Bajar" in meta or "Déficit" in meta:
        cals_obj = tdee - 500
        balance_str = "Déficit Calórico Restrictivo Controlado (-500 kcal)"
    elif "Ganar" in meta or "Subir" in meta or "Volumen" in meta:
        cals_obj = tdee + 350
        balance_str = "Superávit Calórico Limpio Progresivo (+350 kcal)"
    else:
        cals_obj = tdee
        balance_str = "Normocalórico Estandarizado Normorregulado"
        
    # Macronutrientes Estrictos de Precisión MM247
    prot = peso * 2.0  
    grasa = peso * 1.0 
    cals_restantes = cals_obj - ((prot * 4) + (grasa * 9))
    carbs = max(cals_restantes / 4, 50.0)
    
    # CAPACIDAD DE RECUPERACIÓN Y VOLUMEN TOLERABLE
    try:
        estres = float(str(datos.get('P_Estres', '5')))
        sueno = float(str(datos.get('P_Sueno', '5')))
        
        score_recup = (11 - estres) + sueno
        if "Sí" in str(datos.get('Dolores constantes', 'No')) or score_recup < 8:
            cap_recup = "Baja Tolerancia / Sistema Nervioso Estresado"
            vol_por_musculo = "10-12 Series efectivas semanales"
            rir_sugerido = "RIR 2 fijo (Evitar fallo sistémico)"
        elif score_recup > 14:
            cap_recup = "Alta Capacidad de Adaptación / Recuperación Rápida"
            vol_por_musculo = "16-20 Series efectivas semanales"
            rir_sugerido = "RIR 0-1 (Alta intensidad e impacto)"
        else:
            cap_recup = "Media Estandarizada"
            vol_por_musculo = "12-16 Series efectivas semanales"
            rir_sugerido = "RIR 1-2 (Progresión estándar)"
    except Exception:
        cap_recup, vol_por_musculo, rir_sugerido = "Media Estandarizada", "12-16 Series", "RIR 1-2"

    # RIESGO BIOMECÁNICO Y RESTRICCIONES ARTICULARES
    lesion = str(datos.get('Lesión actual', 'Ninguna'))
    molestias_mov = str(datos.get('Molestias movimientos', ''))
    
    riesgo = "Bajo"
    restricciones = "Ninguna"
    if "Rodilla" in lesion or "Sentadilla" in molestias_mov:
        riesgo = "Alto en Tren Inferior"
        restricciones = "Prohibido extensiones pesadas a rangos máximos y cargas axiales compresivas en rodilla."
    if "Hombro" in lesion or "Press de pecho" in molestias_mov or "Press militar" in molestias_mov:
        riesgo = "Moderado/Alto en Tren Superior"
        restricciones = "Modificar presses planos con barra por mancuernas en ángulos neutros o poleas."

    return {
        "imc": round(peso / ((estatura/100)**2), 1),
        "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals_obj, 0),
        "prot": round(prot, 1), "grasa": round(grasa, 1), "carbs": round(carbs, 1),
        "balance_str": balance_str, "cap_recup": cap_recup, "volumen": vol_por_musculo,
        "rir": rir_sugerido, "riesgo": riesgo, "restricciones": restricciones
    }

def generar_propuesta_integral_mm247(datos):
    m = calcular_motores_automatizados(datos)
    nombre = str(datos.get('Nombre completo', 'Alumno')).title()
    experiencia = str(datos.get('Tiempo entrenando', 'Menos de 6 meses'))
    tiempo_sesion = str(datos.get('Tiempo por sesión', '45 a 75 minutos'))
    prioridad = str(datos.get('Prioridad', 'Salud'))
    
    res = f"========================================================================\n"
    res += f"         MM247 FICHA DE EVALUACIÓN CLÍNICA, BIOMECÁNICA Y METABÓLICA\n"
    res += f"========================================================================\n\n"
    res += f"👤 ALUMNO VALORADO: {nombre}\n"
    res += f"📊 ÍNDICE DE MASA CORPORAL (IMC): {m['imc']} | NIVEL OPERATIVO: {experiencia}\n"
    res += f"🛡️ ENFOQUE DE PRIORIDAD ASIGNADO: {prioridad.upper()}\n\n"
    res += f"1. CLASIFICACIÓN FÍSICA, METABÓLICA Y CONSUMO DE ENERGÍA:\n"
    res += f"   - Tasa Metabólica Basal (TMB): {m['tmb']} kcal\n"
    res += f"   - Gasto Energético Total Diario (TDEE): {m['tdee']} kcal\n"
    res += f"   - Intervención Planificada: {m['balance_str']}\n\n"
    res += f"2. CLASIFICACIÓN BIOMECÁNICA Y EVALUACIÓN DE RIESGOS:\n"
    res += f"   - Diagnóstico de Riesgo de Lesión: {m['riesgo']}\n"
    res += f"   - Limitaciones y Restricciones Estrictas: {m['restricciones']}\n\n"
    res += f"3. CAPACIDAD DE RECUPERACIÓN SISTÉMICA Y VOLUMEN DE CARGA:\n"
    res += f"   - Capacidad Nerviosa: {m['cap_recup']}\n"
    res += f"   - Volumen de Trabajo Semanal Recomendado: {m['volumen']}\n"
    res += f"   - Intensidad de Esfuerzo Target: {m['rir']} (Escala RPE correlativa)\n"
    res += f"   - Ventana de Tiempo Límite Ejecutable por Sesión: {tiempo_sesion} por disponibilidad."
    return res

def generar_rutina_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    dias = str(datos.get('Días entrenar', '4')).split()[0]
    tiempo = str(datos.get('Tiempo por sesión', '1 hora'))
    equipo = str(datos.get('Equipo disponible', 'Gimnasio completo'))
    lesiones = str(datos.get('Lesión actual', 'Ninguna'))
    
    ex_prensa = "Prensa de Piernas de forma controlada" if "Rodilla" in lesiones else "Sentadilla Hack Profunda"
    ex_pecho = "Press de Pecho Inclinado con Mancuernas (Agarre semineutro)" if "Hombro" in lesiones else "Press de Pecho Plano con Barra"
    ex_hombro = "Elevaciones Laterales con Polea por detrás" if "Hombro" in lesiones else "Press Militar con Barra"

    r = f"========================================================================\n"
    r += f"     SISTEMA DE ENTRENAMIENTO PERSONALIZADO MM247 — PLANIFICACIÓN SEMANAL\n"
    r += f"========================================================================\n"
    r += f"Disponibilidad de Tiempo Semanal: {dias} días | Capacidad Límite de Sesión: {tiempo}\n"
    r += f"Centro Operativo Logístico: {equipo} | Gestión de Intensidad: {m['rir']}\n\n"

    if "3" in dias:
        r += "DIVISIÓN DISPUESTA: FULLBODY COMPLETO (Frecuencia 3 Semanal)\n\n"
        r += f"• DÍA 1 [LUNES - Estímulo Completo Global]:\n  - {ex_prensa}: 3 series efectivas x 10-12 reps (Tempo 3-1-1-0)\n  - {ex_pecho}: 3 series efectivas x 8-10 reps\n  - Jalón al Pecho con agarre Supino: 3 series x 10 reps\n  - Descanso pautado: 120 segundos reales entre series.\n\n"
        r += f"• DÍA 2 [MIÉRCOLES - Estímulo Completo Global]:\n  - Peso Muerto Rumano con Mancuernas: 3 series x 10 reps\n  - {ex_hombro}: 3 series x 12 reps\n  - Remo con Soporte en Pecho: 3 series x 8-10 reps\n  - Descanso pautado: 90-120 segundos.\n\n"
        r += f"• DÍA 3 [VIERNES - Estímulo Completo Global]:\n  - Zancadas Estáticas con Mancuernas: 3 series x 12 reps por pierna\n  - Cruces de Polea para Pectoral: 3 series x 15 reps\n  - Curl de Bíceps en Banco Inclinado + Extensión de Tríceps en Polea: 3 series x 12 reps (Superserie)"
    elif "5" in dias:
        r += "DIVISIÓN DISPUESTA: SUPERIOR / INFERIOR / EMPUJE / TRACCIÓN / PIERNA (Frecuencia Variable Avanzada)\n\n"
        r += f"• DÍA 1 [LUNES - Tren Superior]:\n  - {ex_pecho}: 4 series x 8-10 reps\n  - Remo con Barra para Dorsal: 4 series x 10 reps\n  - {ex_hombro}: 3 series x 12 reps\n\n"
        r += f"• DÍA 2 [MARTES - Tren Inferior Biomecánico]:\n  - {ex_prensa}: 4 series x 10-12 reps\n  - Curl Femoral Sentado: 4 series x 12 reps\n  - Elevación de Talones en Máquina: 4 series x 15 reps\n\n"
        r += f"• DÍA 3 [MIÉRCOLES - Enfoque Empuje (Pecho/Hombro/Tríceps)]:\n  - Press de Hombro con Mancuernas: 3 series x 10 reps\n  - Aperturas en Contractor Peck-Deck: 3 series x 12 reps\n  - Fondos en Paralelas (Máquina asistida): 3 series x 12 reps\n\n"
        r += f"• DÍA 4 [JUEVES - Enfoque Tracción (Espalda/Bícep/Core)]:\n  - Jalón al Pecho Agarre Abierto: 4 series x 10 reps\n  - Remo con Mancuerna a una mano: 3 series x 12 reps\n  - Curl de Bíceps de pie con Barra Z: 3 series x 10 reps\n\n"
        r += f"• DÍA 5 [VIERNES - Tren Inferior de Aislamiento e Hipertrofia]:\n  - Extensión de Rodillas en Máquina: 4 series x 15 reps\n  - Peso Muerto Rumano con Barra: 3 series x 10 reps\n  - Abductores en Máquina Sentado: 3 series x 20 reps"
    elif "6" in dias:
        r += "DIVISIÓN DISPUESTA: PUSH / PULL / LEG (Frecuencia 2 Estricta de Bodybuilding)\n\n"
        r += f"• DÍA 1 [LUNES - PUSH 1]: {ex_pecho} 4x10, {ex_hombro} 3x12, Fondos 3x10.\n"
        r += f"• DÍA 2 [MARTES - PULL 1]: Jalón Prono 4x10, Remo Sentado 3x12, Curl Inclinado 3x12.\n"
        r += f"• DÍA 3 [MIÉRCOLES - LEG 1]: {ex_prensa} 4x12, Curl Femoral 4x10, Extensiones 3x15.\n"
        r += f"• DÍA 4 [JUEVES - PUSH 2]: Press con Mancuernas 4x10, Cruces en Poleas 3x12, Copa de Tríceps 3x12.\n"
        r += f"• DÍA 5 [VIERNES - PULL 2]: Dominadas asistidas 4x10, Remo en Polea Baja 3x12, Curl Martillo 3x12.\n"
        r += f"• DÍA 6 [SÁBADO - LEG 2]: Peso Muerto Rumano 4x10, Zancadas con Mancuerna 3x12, Pantorrilla en Máquina 4x15."
    else: 
        r += "DIVISIÓN DISPUESTA: TORSO / PIERNA ORIGINAL (Frecuencia 2 Óptima)\n\n"
        r += f"• DÍA 1 [LUNES - Torso Enfoque Fuerza]:\n  - {ex_pecho}: 4 series efectivas x 6-8 reps (2 mins descanso)\n  - Remo con Barra con agarre Supino: 4 series x 8 reps\n  - Press Militar con Mancuernas: 3 series x 10 reps\n  - Jalón al Pecho Cerrado Neutro: 3 series x 10 reps\n\n"
        r += f"• DÍA 2 [MARTES - Pierna Enfoque Desarrollo Estructural]:\n  - {ex_prensa}: 4 series x 10-12 reps\n  - Peso Muerto Rumano con Mancuernas: 4 series x 10 reps\n  - Extensión de Cuádriceps: 3 series x 15 reps\n  - Curl Femoral Acostado: 3 series x 12 reps\n\n"
        r += f"• DÍA 3 [JUEVES - Torso Enfoque Hipertrofia y Detalle]:\n  - Press Inclinado con Mancuernas: 4 series x 10-12 reps\n  - Remo con Polea Baja con triángulo: 4 series x 12 reps\n  - Elevaciones Laterales con Mancuerna: 4 series x 15 reps\n  - Curl de Bíceps en Polea Baja + Extensión de Tríceps Cuerda: 3 series x 12 reps\n\n"
        r += f"• DÍA 4 [VIERNES - Pierna de Estabilidad y Aislamiento]:\n  - Sentadilla Búlgara con Mancuernas: 3 series x 10 reps por pierna\n  - Prensa de Piernas: 3 series x 12 reps\n  - Elevación de Talones de pie: 4 series x 15 reps\n\n"
        r += "SÁBADO Y DOMINGO [Descanso Completo / Recuperación Nerviosa]"

    r += "\n\n========================================================================\n"
    r += "🛡️ PROTOCOLO DE PROGRESIÓN SEMANAL AUTOMÁTICA Y CONTROL DE FATIGA:\n"
    r += f"Aplica Sobrecarga Progresiva de Doble Entrada: Si completas las repeticiones objetivo con el RIR establecido ({m['rir']}), sube un 5% de carga para la siguiente semana."
    return r

def generar_dieta_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    tipo_dieta = str(datos.get('Tipo alimentación', 'Omnívoro'))
    comidas = str(datos.get('Comidas al día', '4')).split()[0]
    alergias = str(datos.get('Alergias alimenticias', 'Ninguna'))
    no_gustan = str(datos.get('Alimentos no gustan', 'Ninguno'))

    d = f"========================================================================\n"
    d += f"     ESTRATEGIA NUTRICIONAL DE ALTA PRECISIÓN MM247 — DIETA CALCULADA\n"
    d += f"========================================================================\n"
    d += f"Estructura Logística: {comidas} ingestas fijas distribuidas | Enfoque: {tipo_dieta}\n"
    d += f"Exclusiones de Alimentos: {alergias} | Restricciones por palatabilidad: {no_gustan}\n\n"
    d += f"🔥 MACRONUTRIENTES DIARIOS CALCULADOS CON PRECISIÓN MATEMÁTICA:\n"
    d += f"   - CALORÍAS TARGET: {m['cals']} kcal al día\n"
    d += f"   - PROTEÍNAS (2g/kg): {m['prot']} g\n"
    d += f"   - GRASAS (1g/kg): {m['grasa']} g\n"
    d += f"   - CARBOHIDRATOS: {m['carbs']} g\n\n"
    d += f"📋 DISTRIBUCIÓN ESPECÍFICA DE TIMING SEGÚN TUS HORARIOS DE COMIDA:\n\n"

    try: c_num = int(comidas)
    except Exception: c_num = 4

    p_por_comida = round(m['prot'] / c_num, 1)
    g_por_comida = round(m['grasa'] / c_num, 1)
    c_por_comida = round(m['carbs'] / c_num, 1)
    cal_por_comida = round(m['cals'] / c_num, 0)

    fuente_p = "Pechuga de Pollo / Claras de Huevo / Lomo de Cerdo Magro"
    fuente_g = "Aguacate / Almendras naturales / Aceite de Oliva Extra Virgen"
    if "Vegetariano" in tipo_dieta:
        fuente_p = "Tofu firme / Tempeh / Queso Cottage bajo en grasa"
    elif "Vegano" in tipo_dieta:
        fuente_p = "Proteína aislada de guisante/arroz / Seitan / Lentejas"
        fuente_g = "Nueces / Semillas de Chía / Crema de Cacahuete pura"

    for i in range(1, c_num + 1):
        if i == 1:
            d += f"• COMIDA 1 [Desayuno Metatónico]:\n"
            d += f"  - Macronutrientes: {p_por_comida}g Prot | {c_por_comida}g Carbs | {g_por_comida}g Grasa ({cal_por_comida} kcal)\n"
            d += f"  - Menú: Tortilla de Claras de huevo + Avena en hojuelas cocida con agua y canela.\n\n"
        elif i == 2:
            d += f"• COMIDA 2 [Almuerzo / Post-Entrenamiento]:\n"
            d += f"  - Macronutrientes: {p_por_comida}g Prot | {c_por_comida}g Carbs | {g_por_comida}g Grasa ({cal_por_comida} kcal)\n"
            d += f"  - Menú: {fuente_p.split(' / ')[0]} a la plancha + Arroz blanco al vapor + Ensalada verde.\n\n"
        elif i == c_num:
            d += f"• COMIDA {i} [Cena de Control Nocturno]:\n"
            d += f"  - Macronutrientes: {p_por_comida}g Prot | {c_por_comida}g Carbs | {g_por_comida}g Grasa ({cal_por_comida} kcal)\n"
            d += f"  - Menú: Pescado blanco magro o Atún en agua + Bloque de {fuente_g.split(' / ')[0]} + Brócoli asado.\n\n"
        else:
            d += f"• COMIDA {i} [Incentivo Metabólico Intermedio]:\n"
            d += f"  - Macronutrientes: {p_por_comida}g Prot | {c_por_comida}g Carbs | {g_por_comida}g Grasa ({cal_por_comida} kcal)\n"
            d += f"  - Menú: Batido de Proteína Isolate + {fuente_g.split(' / ')[1]}.\n\n"

    d += "========================================================================\n"
    d += f"Consumo de agua de 3.5 a 4 Litros diarios."
    return d

# =============================================================================
# MÓDULO 1: FORMULARIO MAESTRO TOTALMENTE OPTIMIZADO A OPCIÓN MÚLTIPLE
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Formulario Maestro — Evaluación Inicial y Diagnóstico Integral de Cargas</div>", unsafe_allow_html=True)
    
    st.info("🚨 FORMULARIO TOTALMENTE ESTANDARIZADO: Todas las respuestas son controladas para garantizar reportes de precisión absoluta.")
    
    with st.form("formulario_maestro_mm247_cerrado", clear_on_submit=True):
        t1, t2, t3, t4, t5, t6 = st.tabs(["1-2. General y Objetivos", "3. Experiencia", "4-5. Salud y Biomecánica", "6-7. Estructura y Hábitos", "8-9. Alimentación y Fatiga", "10-12. Equipo y Métricas"])
        
        with t1:
            st.markdown("<div class='section-header'>1. INFORMACIÓN GENERAL Y DATOS DEMOGRÁFICOS</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                f_nombre = st.text_input("Nombre completo (Ingresa Nombre y Apellido):")
                f_edad = st.selectbox("Edad:", [f"{i} años" for i in range(14, 81)])
                f_sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
                f_estatura = st.selectbox("Estatura:", [f"{i} cm" for i in range(120, 221)], index=55) # 175 cm def
                f_peso_actual = st.selectbox("Peso actual:", [f"{i} kg" for i in range(40, 161)], index=40) # 80 kg def
            with col2:
                f_peso_obj = st.selectbox("Peso objetivo:", [f"{i} kg" for i in range(40, 161)], index=35)
                f_ocupacion = st.selectbox("Ocupación predominante:", ["Sedentaria (Oficina / Escritorio)", "Ligera (Profesor / Ventas)", "Activa (Construcción / Trabajo manual)", "Estudiante"])
                f_horario = st.selectbox("Horario laboral / Actividad:", ["Turno Matutino", "Turno Vespertino", "Turno Nocturno", "Horario Partido / Rolar turnos"])
                f_ciudad = st.selectbox("Región geográfica:", ["México (Centro)", "México (Norte)", "México (Sur)", "Estados Unidos", "España", "Latinoamérica / Otro"])
                f_contacto = st.text_input("Número de WhatsApp (Solo números):", value="55")
                f_correo = st.text_input("Correo electrónico corporativo / personal:")
                
            st.markdown("<div class='section-header'>2. OBJETIVO PRINCIPAL</div>", unsafe_allow_html=True)
            f_objetivo = st.selectbox("¿Cuál es tu objetivo principal?", [
                "Perder grasa", "Ganar masa muscular", "Recomposición corporal", 
                "Mejorar condición física", "Aumentar fuerza", "Mejorar salud general"
            ])
            f_tiempoloro = st.selectbox("¿Cuánto tiempo deseas entrenar para lograr tu objetivo?", ["1-3 meses", "3-6 meses", "6-12 meses", "Más de 1 año"])
            f_compromiso = st.slider("¿Qué tan comprometido estás del 1 al 10?", 1, 10, 10)

        with t2:
            st.markdown("<div class='section-header'>3. EXPERIENCIA EN ENTRENAMIENTO</div>", unsafe_allow_html=True)
            f_tiempo_entrenando = st.selectbox("¿Cuánto tiempo llevas entrenando de forma constante?", ["Nunca / Principiante", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años (Intermedio)", "Más de 3 años (Avanzado)"])
            f_tipo_entreno = st.multiselect("¿Qué tipo de entrenamiento has realizado previamente? (Elige opciones):", ["Gimnasio", "Calistenia", "Crossfit", "Deportes de conjunto", "Funcional", "Ninguno"])
            if not f_tipo_entreno: f_tipo_entreno = ["Gimnasio"]
            f_dias_semana = st.selectbox("¿Cuántos días puedes entrenar por semana?", ["3 días por semana", "4 días por semana", "5 días por semana", "6 días por semana"])
            f_tiempo_sesion = st.selectbox("¿Cuánto tiempo puedes dedicar por sesión?", ["Sesión corta (Menos de 45 minutos)", "Sesión Estándar (De 45 a 75 minutos)", "Sesión Extendida (Más de 75 minutos)"])
            f_entrena_act = st.selectbox("¿Entrenas actualmente?", ["Sí", "No"])
            f_coach_antes = st.selectbox("¿Has trabajado antes con un asesor en línea o coach?", ["Sí", "No"])

        with t3:
            st.markdown("<div class='section-header'>4. CONDICIONES DE SALUD Y RESTRICCIONES</div>", unsafe_allow_html=True)
            f_lesion = st.selectbox("¿Tienes alguna lesión diagnosticada o molestia crónica?", ["Ninguna", "Rodilla / Desgaste / Tendinitis", "Hombro / Manguito rotador", "Espalda Baja / Lumbalgia", "Cervicales", "Muñeca / Tobillo"])
            f_cirugias = st.selectbox("¿Has tenido cirugías de importancia en el aparato locomotor?", ["No", "Sí, en miembros inferiores", "Sí, en miembros superiores / columna"])
            f_dolor_frec = st.selectbox("¿Tienes dolor frecuente durante las sesiones?", ["No", "Sí, al hacer presses pesados", "Sí, al hacer sentadillas", "Sí, dolor lumbar constante"])
            f_medica = st.selectbox("¿Tomas medicamentos prescritos de forma regular?", ["No", "Sí, para presión / glucosa", "Sí, antiinflamatorios frecuentemente"])
            f_cond_diag = st.selectbox("¿Tienes alguna condición médica diagnosticada?", ["Ninguna", "Diabetes", "Hipertensión", "Problemas de Tiroides / Hormonales", "Hernia Discal / Umbilical"])
            f_restriccion = st.selectbox("¿Tu médico ha puesto limitaciones directas a tu esfuerzo?", ["No", "Sí"])
            f_prohibido = st.selectbox("¿Te han prohibido ejercicios de carga axial (como sentadilla libre u hombros)?", ["No", "Sí, cargas sobre la columna", "Sí, flexiones profundas de rodilla"])
            
            st.markdown("<div class='section-header'>5. EVALUACIÓN BIOMECÁNICA PRESETADA</div>", unsafe_allow_html=True)
            f_molestias_mov = st.multiselect("¿Sientes molestias en alguno de estos movimientos clave?:", ["Sentadilla", "Press de pecho", "Peso muerto", "Press militar", "Zancadas", "Ninguno"])
            if not f_molestias_mov: f_molestias_mov = ["Ninguno"]
            f_movilidad = st.selectbox("¿Cómo describirías tu movilidad articular general?", ["Mala / Muy rígido", "Regular", "Buena / Rangos completos"])
            f_lim_mov = st.selectbox("¿Tienes acortamiento evidente (ej. no bajas en sentadilla)?", ["No", "Sí, en tobillos/cadera", "Sí, en hombros"])
            f_sentado = st.selectbox("¿Pasas muchas horas en posición sedente al día?", ["Sí, más de 6 horas continuas", "Moderado (3 a 6 horas)", "No, paso el día activo/parado"])
            f_postura = st.selectbox("¿Presentas desviaciones posturales notables?", ["No", "Sí, hombros adelantados / hipercifosis", "Sí, hiperlordosis lumbar"])
            f_debil = st.selectbox("¿Qué sección corporal consideras que es tu mayor punto débil?:", ["Tren Inferior (Piernas/Glúteos)", "Tren Superior (Brazos/Hombros)", "Zona Media / Core", "Espalda completa"])
            f_desarrollado = st.selectbox("¿Qué músculos tienes más avanzados por genética o historial?:", ["Ninguno", "Piernas", "Pectoral / Brazos", "Espalda"])
            f_equilibrio = st.selectbox("¿Presentas problemas de coordinación motriz o equilibrio?:", ["No", "Sí, en movimientos unilaterales"])

        with t4:
            st.markdown("<div class='section-header'>6. ESTRUCTURA FÍSICA AUTOPERÇIBIDA</div>", unsafe_allow_html=True)
            f_fisico = st.selectbox("¿Cómo te consideras morfológicamente en este momento?", ["Delgado / Ectomorfo", "Atlético / Mesomorfo", "Robusto / Endomorfo", "Sobrepeso / Obesidad"])
            f_acumula_grasa = st.selectbox("¿En qué zona corporal acumulas grasa con mayor facilidad?:", ["Abdomen / Zona lumbar", "Piernas y Cadera", "Distribución General uniforme"])
            f_gana_musculo = st.selectbox("¿Qué tanta facilidad posees para desarrollar masa muscular?", ["Muy difícil", "Ritmo Normal", "Fácil"])
            f_gana_grasa = st.selectbox("¿Qué tan rápido aumentas tu porcentaje de grasa?", ["Muy fácil", "Ritmo Normal", "Difícil"])
            
            st.markdown("<div class='section-header'>7. HÁBITOS Y ESTILO DE VIDA</div>", unsafe_allow_html=True)
            f_horas_sueno = st.selectbox("¿Cuántas horas duermes en promedio por noche?", ["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"])
            f_calif_sueno = st.selectbox("¿Cómo calificas la calidad de tu descanso?", ["Malo (Despierto cansado)", "Regular", "Excelente (Reparador profundo)"])
            f_estres_diario = st.selectbox("¿Qué nivel de estrés psicológico o laboral manejas diariamente?", ["Bajo / Controlado", "Medio", "Alto / Trabajo bajo presión"])
            f_num_comidas = st.selectbox("¿Cuántas comidas sólidas realizas habitualmente al día?", ["2 comidas", "3 comidas", "4 comidas", "5 comidas o más"])
            f_litros_agua = st.selectbox("¿Cuánta agua simple ingieres diariamente?", ["Menos de 1.5 Litros", "Entre 1.5 y 3 Litros", "Más de 3 Litros"])
            f_alcohol = st.selectbox("¿Consumes bebidas alcohólicas?", ["No / Nunca", "Solo en eventos / Ocasional", "Frecuente fines de semana"])
            f_fuma = st.selectbox("¿Fumas de forma activa?", ["No", "Sí"])
            f_pasos = st.selectbox("Estimación de pasos diarios (NEAT):", ["Menos de 5k (Sedentario)", "5k a 10k (Activo moderado)", "Más de 10k (Altamente activo)"])
            f_nivel_actividad = st.selectbox("¿Cómo describirías tu nivel de actividad diaria fuera del gimnasio?", ["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"])

        with t5:
            st.markdown("<div class='section-header'>8. COMPORTAMIENTO ALIMENTICIO</div>", unsafe_allow_html=True)
            f_obj_nutri = st.selectbox("¿Cuál es tu prioridad nutricional inmediata?", ["Bajar porcentaje de grasa", "Aumento de masa magra", "Recomposición / Mantener"])
            f_alergias = st.selectbox("¿Sufres de alergias alimenticias diagnosticadas?", ["Ninguna", "Frutos secos", "Mariscos / Pescados", "Huevo / Gluten"])
            f_intolerancia = st.selectbox("¿Presentas intolerancias digestivas severas?", ["Ninguna", "Lactosa", "Gluten / Trigo", "Legumbres"])
            f_tipo_alimentacion = st.selectbox("¿Qué tipo de patrón dietético sigues?", ["Omnívoro", "Vegetariano (Consumo huevo/lácteos)", "Vegano (Estricto origen vegetal)", "Keto / Low Carb"])
            f_no_gustan = st.selectbox("Alimentos que prefieres evitar por completo en tus menús:", ["Ninguno", "Pescados / Mariscos", "Verduras amargas", "Lácteos"])
            f_consumo_freq = st.selectbox("¿Cuál es la base proteica de tu dieta actual?", ["Pollo y Res", "Huevo y Quesos", "Pescados y Legumbres", "Variada completa"])
            f_comer_fuera = st.selectbox("¿Cuántas veces consumes alimentos preparados fuera de casa?", ["Nunca / Preparo todo", "1-2 veces por semana", "3 o más veces (Frecuente)"])
            f_presupuesto = st.selectbox("Presupuesto asignado a tu despensa fitness mensual:", ["Básico / Económico", "Estándar flexible", "Premium / Alimentos selectos"])
            f_horarios_fijos = st.selectbox("¿Tienes la estructura para comer a horas fijas?", ["Sí, todos los días", "No, mis horarios varían demasiado", "Solo a veces"])
            f_cocinar = st.selectbox("¿Tienes control o conocimiento en la cocina?", ["Sí, cocino mis platillos", "No, alguien cocina por mí", "Conocimiento básico (Fácil/Rápido)"])
            
            st.markdown("<div class='section-header'>9. CAPACIDAD DE RECUPERACIÓN Y FATIGA</div>", unsafe_allow_html=True)
            f_recup_post = st.selectbox("¿Cómo es tu tasa de recuperación tras un entrenamiento intenso?", ["Mala (Dolor por más de 3 días)", "Regular / Estándar", "Excelente (Listo al día siguiente)"])
            f_cansado_freq = st.selectbox("¿Te despiertas o te sientes fatigado crónicamente?", ["Sí, casi todos los días", "Solo a mitad de la semana", "No, energía estable"])
            f_fatiga_dia = st.selectbox("¿Experimentas bajones severos de energía por la tarde?", ["Muy alta fatiga", "Normal / Leve", "Baja / Sin bajones"])
            f_dolores_const = st.selectbox("¿Sientes dolores articulares recurrentes (no musculares)?", ["No", "Sí, rodillas/codos constantemente"])
            f_energia_diaria = st.selectbox("Calificación de tu enfoque y energía mental diaria:", ["Muy baja", "Normal estable", "Alta / Enfoque total"])

        with t6:
            st.markdown("<div class='section-header'>10. DISPONIBILIDAD LOGÍSTICA DE EQUIPO</div>", unsafe_allow_html=True)
            f_donde_entrena = st.selectbox("¿Dónde se ejecutarán los entrenamientos?", ["Gimnasio comercial completo", "Gimnasio de edificio / Semi-equipado", "Casa con mancuernas y bandas", "Exterior / Calistenia"])
            f_equipo = st.multiselect("Selecciona el equipamiento al que tienes acceso real (Elige opciones):", ["Mancuernas", "Barras y Discos", "Poleas ajustables", "Máquinas de aislamiento", "Banco regulable", "Rack / Smith"])
            if not f_equipo: f_equipo = ["Mancuernas", "Barras y Discos"]
            f_lim_espacio = st.selectbox("¿Tienes limitaciones críticas de espacio o equipo?", ["No", "Sí, entreno en espacio muy reducido"])
            
            st.markdown("<div class='section-header'>11. METAS ESPECÍFICAS DE ENFOQUE</div>", unsafe_allow_html=True)
            f_partes_mejorar = st.selectbox("Eslabón muscular estético que urge priorizar:", ["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda", "Brazos (Bíceps/Tríceps)", "Abdomen / Definición"])
            f_dificultad = st.selectbox("Tu mayor limitante histórica en el fitness:", ["Falta de constancia", "Estancamiento en cargas", "No saber comer adecuadamente", "Lesiones recurrentes"])
            f_odia_ex = st.selectbox("Ejercicio que te genera excesivo estrés articular o desagrado:", ["Ninguno", "Sentadilla Libre", "Press Militar Barra", "Desplantes / Zancadas Walking"])
            f_disfruta_ex = st.selectbox("Ejercicio donde sientes la mejor conexión mente-músculo:", ["Prensa de piernas", "Extensiones", "Jalones en polea", "Press inclinado mancuernas"])
            f_impide_progresar = st.selectbox("¿Qué factor saboteó tus planes de entrenamiento anteriores?", ["Falta de tiempo/Trabajo", "Planes aburridos o genéricos", "Falta de un guía experto"])
            
            st.markdown("<div class='section-header'>12. ESCALAS PSICOMÉTRICAS DE ESFUERZO (Control Operativo 1 al 10)</div>", unsafe_allow_html=True)
            f_p_disciplina = st.slider("Nivel de disciplina autoimpuesta:", 1, 10, 8)
            f_p_estres = st.slider("Nivel de carga de estrés mental:", 1, 10, 5)
            f_p_sueno = st.slider("Eficiencia real del sueño:", 1, 10, 8)
            f_p_motivacion = st.slider("Nivel de motivación actual de arranque:", 1, 10, 9)
            f_p_energia = st.slider("Energía promedio diaria percibida:", 1, 10, 7)
            f_p_hambre = st.slider("Sensación de ansiedad / Hambre diurna:", 1, 10, 5)
            f_p_recup = st.slider("Velocidad de recuperación muscular percibida:", 1, 10, 7)
            
            f_prioridad = st.selectbox("Prioridad del Filtro Automatizado de Carga:", ["Salud", "Estética", "Rendimiento", "Fuerza"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            enviar_maestro = st.form_submit_button("🚀 ENVIAR EXPEDIENTE ESTANDARIZADO A MM247")
            
        if enviar_maestro:
            if not f_nombre.strip():
                st.error("❌ El campo de Nombre Completo es totalmente obligatorio.")
            else:
                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre completo": str(f_nombre.strip().lower()), "Edad": str(f_edad), "Sexo": str(f_sexo), "Estatura": str(f_estatura), "Peso actual": str(f_peso_actual),
                    "Peso objetivo": str(f_peso_obj), "Ocupación": str(f_ocupacion), "Horario laboral": str(f_horario), "Ciudad / País": str(f_ciudad), "Número de contacto": str(f_contacto), "Correo electrónico": str(f_correo),
                    "Objetivo principal": str(f_objetivo), "Tiempo deseado": str(f_tiempoloro), "Compromiso": str(f_compromiso), "Tiempo entrenando": str(f_tiempo_entrenando), "Tipo entreno": ",".join(f_tipo_entreno),
                    "Días entrenar": str(f_dias_semana), "Tiempo por sesión": str(f_tiempo_sesion), "Entrena actualmente": str(f_entrena_act), "Coach anterior": str(f_coach_antes), "Lesión actual": str(f_lesion),
                    "Cirugías": str(f_cirugias), "Dolor frecuente": str(f_dolor_frec), "Medicamentos": str(f_medica), "Condición médica": str(f_cond_diag), "Restricciones": str(f_restriccion), "Prohibido ejercicio": str(f_prohibido),
                    "Molestias movimientos": ",".join(f_molestias_mov), "Movilidad": str(f_movilidad), "Limitaciones movilidad": str(f_lim_mov), "Horas sentado": str(f_sentado), "Mala postura": str(f_postura),
                    "Parte débil": str(f_debil), "Músculo desarrollado": str(f_desarrollado), "Equilibrio": str(f_equilibrio), "Consideración física": str(f_fisico), "Acumula grasa": str(f_acumula_grasa),
                    "Facilidad músculo": str(f_gana_musculo), "Facilidad grasa": str(f_gana_grasa), "Horas sueño": str(f_horas_sueno), "Calificación descanso": str(f_calif_sueno), "Nivel de estrés": str(f_estres_diario),
                    "Comidas al día": str(f_num_comidas), "Agua diaria": str(f_litros_agua), "Alcohol": str(f_alcohol), "Fuma": str(f_fuma), "Pasos día": str(f_pasos), "Nivel de actividad": str(f_nivel_actividad),
                    "Objetivo nutricional": str(f_obj_nutri), "Alergias alimenticias": str(f_alergias), "Intolerancias": str(f_intolerancia), "Tipo alimentación": str(f_tipo_alimentacion), "Alimentos no gustan": str(f_no_gustan),
                    "Consumo frecuente": str(f_consumo_freq), "Comer fuera": str(f_comer_fuera), "Presupuesto": str(f_presupuesto), "Horarios fijos": str(f_horarios_fijos), "Sabe cocinar": str(f_cocinar),
                    "Recuperación post": str(f_recup_post), "Cansado frecuente": str(f_cansado_freq), "Fatiga durante el día": str(f_fatiga_dia), "Dolores constantes": str(f_dolores_const), "Energía diaria": str(f_energia_diaria),
                    "Donde entrenará": str(f_donde_entrena), "Equipo disponible": ",".join(f_equipo), "Limitación espacio": str(f_lim_espacio), "Partes mejorar": str(f_partes_mejorar), "Dificultades físicas": str(f_dificultad),
                    "Ejercicio odia": str(f_odia_ex), "Ejercicio disfruta": str(f_disfruta_ex), "Impedido progresar": str(f_impide_progresar), "P_Disciplina": str(f_p_disciplina), "P_Estres": str(f_p_estres),
                    "P_Sueno": str(f_p_sueno), "P_Motivacion": str(f_p_motivacion), "P_Energia": str(f_p_energia), "P_Hambre": str(f_p_hambre), "P_Recup": str(f_p_recup), "Prioridad": str(f_prioridad),
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }
                with st.spinner("Subiendo expediente estructurado..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        if response.status_code == 200 and "success" in response.text:
                            st.success("✅ ¡Expediente guardado con éxito absoluto en Google Sheets de forma estructurada!")
                            st.balloons()
                        else: st.error(f"Error de procesamiento de datos: {response.text}")
                    except Exception as api_err: st.error(f"Fallo de conexión externa: {api_err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADMINISTRADOR AVANZADO (CORREGIDO DE KEYERRORS)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel de Control MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado de forma segura.")
        if df_existente.empty:
            st.warning("No se detectan alumnos en la base de datos de Google Sheets.")
        else:
            st.markdown("### 📈 Métricas de Control General")
            
            # CONTROL CRÍTICO ANTI-KEYERROR: Se valida si las columnas objetivo existen antes de procesar conteos
            total_alumnos = len(df_existente)
            perdida_count = 0
            masa_count = 0
            
            col_meta_key = ""
            for c in ["Objetivo principal", "Objetivoprincipal", "Objetivo"]:
                if c in df_existente.columns:
                    col_meta_key = c
                    break
            
            if col_meta_key != "":
                perdida_count = df_existente[col_meta_key].astype(str).str.contains('Perder|Bajar|Déficit|grasa', case=False, na=False).sum()
                masa_count = df_existente[col_meta_key].astype(str).str.contains('Ganar|Subir|Volumen|muscular', case=False, na=False).sum()
            else:
                # Si las columnas no concuerdan en absoluto, evitamos crasheo contando por descarte o asignando 0
                perdida_count = 0
                masa_count = 0

            k1, k2, k3 = st.columns(3)
            with k1: st.markdown(f"<div class='metric-card'><div class='metric-title'>Expedientes Totales</div><div class='metric-value'>{total_alumnos} alumnos</div></div>", unsafe_allow_html=True)
            with k2: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Enfoque Pérdida / Grasa</div><div class='metric-value'>{perdida_count} alumnos</div></div>", unsafe_allow_html=True)
            with k3: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Enfoque Hipertrofia</div><div class='metric-value'>{masa_count} alumnos</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("📋 Matriz Completa de Alumnos (Sincronizada)")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            
            # Buscar llave del nombre del alumno de forma segura
            col_nombre_key = "Nombre completo" if "Nombre completo" in df_existente.columns else df_existente.columns[1]
            lista_alumnos = df_existente[col_nombre_key].dropna().unique()
            alumno_sel = st.selectbox("Seleccione el expediente del alumno a planificar:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente[col_nombre_key] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            nombre_display = str(datos_alumno[col_nombre_key]).title()

            if "alumno_actual" not in st.session_state or st.session_state.alumno_actual != alumno_sel:
                st.session_state.alumno_actual = alumno_sel
                
                db_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
                db_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
                db_balance = str(datos_alumno.get("Balance Energético", "")).strip()
                
                st.session_state.v_propuesta = db_propuesta if db_propuesta and db_propuesta != "nan" else generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = db_rutina if db_rutina and db_rutina != "nan" else generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = db_balance if db_balance and db_balance != "nan" else generar_dieta_detallada_mm247(datos_alumno)

            st.markdown(f"### 👤 Gestión de Carga Activa: {nombre_display}")
            
            if st.button("🚀 Forzar Re-Cálculo de Automatización (IA Base)"):
                st.session_state.v_propuesta = generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = generar_dieta_detallada_mm247(datos_alumno)
                st.rerun()

            st.markdown("---")
            st.markdown("### 🛠️ Sistema de Edición y Prescripción de Hojas MM247")
            
            with st.form("prescripcion_maestra_form_mm247"):
                propuesta = st.text_area("🩺 HOJA 1: Informe Diagnóstico Avanzado (Metabólico, Clínico y Biomecánico):", value=st.session_state.v_propuesta, height=220)
                rutina = st.text_area("🏋️ HOJA 2: Programación Semanal Estricta (Distribución Completa de Ejercicios y Series):", value=st.session_state.v_rutina, height=320)
                balance = st.text_area("🥗 HOJA 3: Dieta Detallada de Ingestas Múltiples (Macros y Menú Específico):", value=st.session_state.v_balance, height=320)
                
                guardar_changes = st.form_submit_button("💾 Guardar y Sincronizar Cambios con Google Sheets")
                if guardar_changes:
                    payload_edit = {"Action": "UPDATE", "RowIndex": int(idx_alumno + 2)}
                    for k in datos_alumno.keys():
                        payload_edit[k] = str(datos_alumno[k])
                    
                    payload_edit["Propuesta General"] = propuesta
                    payload_edit["Balance Energético"] = balance
                    payload_edit["Rutina Biomecánica"] = rutina
                    
                    with st.spinner("Modificando fila en Google Sheets..."):
                        try:
                            requests.post(WEBHOOK_URL, json=payload_edit)
                            st.session_state.v_propuesta = propuesta
                            st.session_state.v_rutina = rutina
                            st.session_state.v_balance = balance
                            st.success("✅ ¡Prescripción guardada y sincronizada de forma impecable!")
                        except Exception as e_save: st.error(f"Fallo crítico de sincronización: {e_save}")
            
            if st.button("🖨️ Compilar Plan Maestro en PDF de 3 Hojas"):
                try:
                    pdf = FPDF()
                    def limpiar_texto(txt):
                        return str(txt).replace("•", "-").replace("–", "-").replace("—", "-").replace("º"," ").encode('latin-1', 'ignore').decode('latin-1')

                    # HOJA 1
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20) 
                    pdf.rect(0, 0, 210, 38, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 24)
                    pdf.cell(0, 12, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("INFORME DE PLANIFICACIÓN INTEGRAL CLÍNICA Y METABÓLICA"), ln=True, align="C")
                    
                    pdf.ln(18)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_fill_color(245, 245, 245)
                    pdf.set_draw_color(180, 180, 180)
                    pdf.rect(10, 44, 190, 16, "DF")
                    pdf.set_font("Arial", "B", 11)
                    pdf.set_xy(12, 49)
                    pdf.cell(0, 6, limpiar_texto(f"FICHA TÉCNICA OPERATIVA — ALUMNO: {nombre_display.upper()}"), ln=True)
                    
                    pdf.set_xy(10, 68)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 6, limpiar_texto(st.session_state.v_propuesta))

                    # HOJA 2
                    pdf.add_page()
                    pdf.set_fill_color(220, 70, 0) 
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("DOSIFICACIÓN DE CARGAS Y PROGRAMACIÓN SEMANAL DE FUERZA"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_fill_color(252, 252, 252)
                    pdf.set_draw_color(220, 70, 0) 
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(182, 5.5, limpiar_texto(st.session_state.v_rutina))

                    # HOJA 3
                    pdf.add_page()
                    pdf.set_fill_color(35, 115, 40) 
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("AJUSTE DE BALANCE ENERGÉTICO Y ESTRATEGIA NUTRICIONAL DIARIA"), ln=True, align="C")
                    
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_fill_color(248, 249, 248)
                    pdf.set_draw_color(35, 115, 40) 
                    pdf.rect(10, 42, 190, 235, "DF")
                    pdf.set_xy(14, 46)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(182, 5.5, limpiar_texto(st.session_state.v_balance))
                    
                    pdf_data = pdf.output(dest='S')
                    st.download_button(
                        label="⬇️ Descargar Reporte Completo en PDF Premium",
                        data=bytes(pdf_data),
                        file_name=f"Plan_Estructural_MM247_{nombre_display.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Fallo al construir el compilador PDF: {err_pdf}")
                    
    elif password != "": st.error("🔑 Clave inválida.")
