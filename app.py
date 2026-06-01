import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y BRANDING (SISTEMA MM247)
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# Configuración de URLs de sincronización de datos
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    """Carga y limpia de forma segura los datos de Google Sheets evitando KeyErrors"""
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        # Eliminar columnas fantasma o sin nombre
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        # Limpieza absoluta de espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Estilos visuales de la interfaz minimalista de MM247
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

opcion = st.sidebar.selectbox("Navegación MM247:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# 2. MOTORES INTERNOS DE CÁLCULO CIENTÍFICO Y FISIOLÓGICO
# =============================================================================
def procesar_metricas_base(datos):
    try: peso = float(str(datos.get('Peso actual', '80')).replace(" kg", "").split()[0])
    except Exception: peso = 80.0
    try: estatura = float(str(datos.get('Estatura', '175')).replace(" cm", "").split()[0])
    except Exception: estatura = 175.0
    try: edad = float(str(datos.get('Edad', '25')).replace(" años", "").split()[0])
    except Exception: edad = 25.0
    genero = str(datos.get('Sexo', 'Masculino'))
    return peso, estatura, edad, genero

def calcular_motores_automatizados(datos):
    peso, estatura, edad, genero = procesar_metricas_base(datos)
    
    # Ecuación de Harris-Benedict revisada para Tasa Metabólica Basal
    if "Masculino" in genero:
        tmb = 66.473 + (13.751 * peso) + (5.0033 * estatura) - (6.755 * edad)
    else:
        tmb = 655.095 + (9.5634 * peso) + (1.8496 * estatura) - (4.6756 * edad)
        
    neat_str = str(datos.get('Nivel de actividad', 'Moderadamente activo'))
    factores = {"Sedentario": 1.2, "Poco activo": 1.375, "Moderadamente activo": 1.55, "Muy activo": 1.725}
    factor = factores.get(neat_str.split()[0], 1.55)
    tdee = tmb * factor
    
    meta = str(datos.get('Objetivo principal', 'Recomposición corporal'))
    condicion = str(datos.get('Condición médica', 'Ninguna'))
    
    # Ajustes calóricos inteligentes adaptados a la salud
    if "Perder" in meta or "Bajar" in meta or "Déficit" in meta or "grasa" in meta:
        cals_obj = tdee - 450 if edad < 45 else tdee - 350
        balance_str = f"Déficit Calórico Estructurado ({round(cals_obj)} kcal)"
    elif "Ganar" in meta or "Subir" in meta or "Volumen" in meta or "muscular" in meta:
        cals_obj = tdee + 300 if "Diabetes" not in condicion else tdee + 150
        balance_str = f"Superávit Calórico Limpio ({round(cals_obj)} kcal)"
    else:
        cals_obj = tdee
        balance_str = f"Normocalórico de Consolidación ({round(cals_obj)} kcal)"
        
    # Leyes nutricionales fijas del entrenador: 2g Proteína y 1g Grasa por kg de peso
    prot = peso * 2.0  
    grasa = peso * 1.0 
    cals_restantes = cals_obj - ((prot * 4) + (grasa * 9))
    carbs = max(cals_restantes / 4, 50.0)
    
    return {
        "imc": round(peso / ((estatura/100)**2), 1), "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals_obj, 0),
        "prot": round(prot, 1), "grasa": round(grasa, 1), "carbs": round(carbs, 1), "balance_str": balance_str,
        "edad": edad, "genero": genero, "condicion": condicion, "peso": peso
    }

# =============================================================================
# 3. NUEVO MOTOR DE TEXTO DINÁMICO (SISTEMA DE CORRECCIÓN DE AMBIGÜEDAD)
# =============================================================================
def generar_propuesta_integral_mm247(datos):
    m = calcular_motores_automatizados(datos)
    nombre = str(datos.get('Nombre completo', 'Alumno')).title()
    experiencia = str(datos.get('Tiempo entrenando', 'Menos de 6 meses'))
    prioridad = str(datos.get('Prioridad', 'Salud'))
    lesion = str(datos.get('Lesión actual', 'Ninguna'))
    cirugias = str(datos.get('Cirugías', 'No'))
    
    # Análisis dinámico de postura y estilo de vida laboral
    horas_sentado = str(datos.get('Horas sentado', 'No'))
    postura = str(datos.get('Mala postura', 'No'))
    
    analisis_postural = ""
    if "más de 6 horas" in horas_sentado:
        analisis_postural += "• Alerta Postural: Jornada laboral sedentaria (más de 6 horas sentado). Riesgo latente de amnesia glútea y acortamiento del psoas ilíaco. Obligatorio realizar aproximaciones dinámicas.\n"
    if "hombros adelantados" in postura:
        analisis_postural += "• Desbalance Biomecánico Superior: Rotación interna de hombros detectada (cifosis). Se limita el volumen de empujes planos en barra; priorizar trabajo de deltoides posterior y tracciones.\n"
    elif "hiperlordosis" in postura:
        analisis_postural += "• Inestabilidad Lumbar: Anteversión pélvica marcada. Limitar cargas axiales libres e incorporar ejercicios estabilizadores de core.\n"
    else:
        analisis_postural += "• Estabilidad Ósea: Sin desviaciones posturales graves evidentes. Alineación articular óptima.\n"

    # Diagnóstico clínico cruzado con dolores y antecedentes
    dolor = str(datos.get('Dolor frecuente', 'No'))
    prohibido = str(datos.get('Prohibido ejercicio', 'No'))
    
    analisis_clinico = ""
    if lesion != "Ninguna" or cirugias != "No" or m['condicion'] != "Ninguna":
        analisis_clinico += f"🚨 RESTRICCIONES CLÍNICAS ACTIVADAS:\n"
        analisis_clinico += f"  - Patología Base: {m['condicion']} | Región estructural afectada: {lesion}\n"
        if "Diabetes" in m['condicion']:
            analisis_clinico += "  - Ajuste Endocrino: Plan nutricional adaptado con carbohidratos de bajo índice glucémico y alto aporte de fibra para mitigar picos de insulina.\n"
        if "Hipertensión" in m['condicion']:
            analisis_clinico += "  - Seguridad Hemodinámica: Prohibido trabajar a intensidades máximas prolongadas que requieran bloqueo respiratorio extremo (Valsalva).\n"
        if "Rodilla" in lesion or "sentadillas" in dolor:
            analisis_clinico += "  - Modificación de Tren Inferior: Sustituir sentadillas libres profundas por variantes controladas en poleas o prensa inclinada con rango seguro.\n"
        if "Espalda" in lesion or "lumbar" in dolor or "columna" in prohibido:
            analisis_clinico += "  - Protección de Columna: Restricción estricta de cargas verticales o compresivas. Trabajo de fuerza enfocado en vectores horizontales.\n"
    else:
        analisis_clinico += "• Diagnóstico de Salud: Sin limitaciones patológicas ni óseas declaradas. Apto para protocolos estándar de fuerza.\n"

    # Medición psicométrica de fatiga del Sistema Nervioso Central (SNC)
    estres_mental = int(datos.get('P_Estres', 5))
    sueno_eficiencia = int(datos.get('P_Sueno', 8))
    horas_sueno = str(datos.get('Horas sueño', '7-8 horas'))
    
    if estres_mental >= 8 or sueno_eficiencia <= 5 or "4-5 horas" in horas_sueno:
        capacidad_snc = "CRÍTICA / RESTRIGIDA (Carga laboral o insomnio severo)"
        volumen_recomendado = "8 a 10 Series Efectivas semanales por grupo muscular (Rutina optimizada para evitar fatiga crónica)"
        pauta_recup = "Evitar entrenamientos extenuantes al fallo muscular absoluto. Priorizar la consistencia sobre la intensidad."
    elif estres_mental <= 4 and sueno_eficiencia >= 8:
        capacidad_snc = "MÁXIMA / ÓPTIMA (Excelente entorno anabólico)"
        volumen_recomendado = "14 a 18 Series Efectivas semanales por grupo muscular"
        pauta_recup = "Sistemas energéticos listos para soportar alta densidad de entrenamiento y sobrecarga progresiva lineal."
    else:
        capacidad_snc = "ESTÁNDAR EFICIENTE"
        volumen_recomendado = "11 a 13 Series Efectivas semanales por grupo muscular"
        pauta_recup = "Tolerancia de carga regular. Mantener progresión convencional."

    res = f"========================================================================\n"
    res += f"        MM247 INFORME DIAGNÓSTICO MAESTRO AVANZADO (100% PERSONALIZADO)\n"
    res += f"========================================================================\n\n"
    res += f"👤 ALUMNO EVALUADO: {nombre} | EDAD: {int(m['edad'])} años | SEXO: {m['genero']}\n"
    res += f"📊 ANÁLISIS METABÓLICO BASE:\n"
    res += f"   - Tasa Metabólica Basal (TMB): {m['tmb']} kcal\n"
    res += f"   - Gasto Diario Total (TDEE): {m['tdee']} kcal\n"
    res += f"   - Ajuste Prescrito MM247: {m['balance_str']}\n\n"
    res += f"⚠️ CLASIFICACIÓN BIOMECÁNICA Y RIESGOS POSTURALES:\n{analisis_postural}\n"
    res += f"📋 SINTOMATOLOGÍA CLÍNICA Y ANTECEDENTES RELEVANTES:\n{analisis_clinico}\n"
    res += f"🧠 CAPACIDAD DEL SISTEMA NERVIOSO Y RECOVIERY:\n"
    res += f"   - Tolerancia SNC: {capacidad_snc}\n"
    res += f"   - Volumen de Trabajo Semanal Aconsejado: {volumen_recomendado}\n"
    res += f"   - Estrategia de Control de Fatiga: {pauta_recup}\n\n"
    res += f"🎯 OBJETIVO ESTÉTICO LOCALIZADO:\n"
    res += f"   - Zona prioritaria elegida: {datos.get('Partes mejorar', 'General')}\n"
    res += f"   - Dominancia genética reportada: {datos.get('Músculo desarrollado', 'Ninguno')}\n"
    res += f"========================================================================\n"
    return res

def generar_rutina_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    dias = str(datos.get('Días entrenar', '4')).split()[0]
    equipo = str(datos.get('Equipo disponible', 'Gimnasio completo'))
    lesiones = str(datos.get('Lesión actual', 'Ninguna'))
    
    es_adulto_mayor = m['edad'] >= 50
    es_mujer = "Femenino" in m['genero']
    
    # Ajustes automáticos de ejercicios por seguridad biomecánica
    base_prensa = "Prensa de Piernas Inclinada (Ejecución controlada)" if ("Rodilla" in lesiones or es_adulto_mayor) else "Sentadilla Libre Profunda"
    base_pecho = "Press con Mancuernas en Banco Inclinado" if ("Hombro" in lesiones) else "Press de Pecho Plano con Barra"
    
    ej_gluteo_fem = "Hip Thrust con Barra Pesado + Peso Muerto Rumano" if es_mujer else "Peso Muerto Convencional con Barra"
    ej_brazo_torso = "Elevaciones Laterales + Jalón al Pecho Polea" if es_mujer else "Press Militar con Barra + Remo Pendlay"

    r = f"========================================================================\n"
    r += f"     CRONOGRAMA SEMANAL DE 7 DÍAS REALES (SIN AMBIGÜEDADES) — MM247\n"
    r += f"========================================================================\n"
    r += f"Programación para perfil: {m['genero']} | Edad: {int(m['edad'])} años | Cargas en: {equipo}\n"
    r += f"Cuidado articular por lesión en: {lesiones}\n\n"

    if "3" in dias:
        r += "📆 LUNES [DÍA 1 - ESTÍMULO FULLBODY GLOBAL]:\n"
        r += f"   - {base_prensa}: 3 x 10-12 reps (Tempo 3-1-1-0). RIR 2.\n"
        r += f"   - {base_pecho}: 3 x 8-10 reps.\n"
        r += f"   - Curl de Piernas Sentado (Polea): 3 x 12 reps.\n\n"
        r += "📆 MARTES:\n   ❌ DESCANSO OBLIGATORIO - Recuperación del Sistema Nervioso Central.\n\n"
        r += "📆 MIÉRCOLES [DÍA 2 - ESTÍMULO FULLBODY GLOBAL]:\n"
        r += f"   - {ej_gluteo_fem}: 3 x 10 reps (Controlando la bajada excéntrica).\n"
        r += f"   - {ej_brazo_torso}: 3 x 12 reps.\n\n"
        r += "📆 JUEVES:\n   ❌ DESCANSO OBLIGATORIO - Procesamiento y síntesis proteica.\n\n"
        r += "📆 VIERNES [DÍA 3 - ESTÍMULO FULLBODY GLOBAL]:\n"
        r += f"   - Zancadas Estáticas con Mancuerna: 3 x 12 reps por pierna.\n"
        r += f"   - Cruces de Poleas desde Abajo (Pectoral): 3 x 15 reps.\n"
        r += "   - Plank Abdominal Isométrico: 3 x 45 segundos.\n\n"
        r += "📆 SÁBADO:\n   ❌ DESCANSO OBLIGATORIO.\n\n"
        r += "📆 DOMINGO:\n   ❌ DESCANSO OBLIGATORIO — Reset metabólico semanal."
        
    elif "5" in dias:
        r += "📆 LUNES [DÍA 1 - ENFOQUE CADENA INFERIOR / POSTERIOR]:\n"
        r += f"   - {base_prensa}: 4 x 10 reps.\n"
        r += f"   - {ej_gluteo_fem}: 4 x 12 reps.\n\n"
        r += "📆 MARTES [DÍA 2 - ENFOQUE TREN SUPERIOR (EMPUJE / TRACCIÓN)]:\n"
        r += f"   - {base_pecho}: 4 x 10 reps.\n"
        r += f"   - {ej_brazo_torso}: 3 x 12 reps.\n\n"
        r += "📆 MIÉRCOLES:\n   ❌ DESCANSO OBLIGATORIO EN MITAD DE SEMANA - Vaciado de fatiga.\n\n"
        r += "📆 JUEVES [DÍA 3 - AISLAMIENTO METABÓLICO E HIPERTROFIA]:\n"
        r += "   - Extensiones de Cuádriceps en Máquina: 4 x 15 reps (Última serie al fallo técnico).\n"
        r += "   - Jalón al Pecho con Agarre Prono Abierto: 4 x 12 reps.\n\n"
        r += "📆 VIERNES [DÍA 4 - ÉNFASIS EN CADENA POSTERIOR Y GLÚTEO]:\n"
        r += "   - Hip Thrust en Máquina o Barra Libre: 4 x 10 reps (Sostener 2 segundos arriba).\n"
        r += "   - Curl Femoral Tumbado: 4 x 12 reps.\n\n"
        r += "📆 SÁBADO [DÍA 5 - DETALLE ESTÉTICO: HOMBROS, BRAZO Y CORE]:\n"
        r += "   - Elevaciones Laterales con Mancuerna: 4 x 15 reps.\n"
        r += "   - Curl de Bíceps con Polea + Copa de Tríceps (Superserie): 3 x 12 reps.\n\n"
        r += "📆 DOMINGO:\n   ❌ DESCANSO OBLIGATORIO — Recuperación integral profunda."
        
    else: # 4 Días
        r += "📆 LUNES [DÍA 1 - TORSO COMPLETO]:\n"
        r += f"   - {base_pecho}: 4 x 8-10 reps.\n"
        r += f"   - {ej_brazo_torso}: 4 x 10 reps.\n\n"
        r += "📆 MARTES [DÍA 2 - PIERNA ENFOQUE GLOBAL]:\n"
        r += f"   - {base_prensa}: 4 x 10-12 reps.\n"
        r += f"   - {ej_gluteo_fem}: 4 x 12 reps.\n\n"
        r += "📆 MIÉRCOLES:\n   ❌ DESCANSO OBLIGATORIO - Pausa de recuperación de articulaciones.\n\n"
        r += "📆 JUEVES [DÍA 3 - TORSO ENFOQUE HIPERTROFIA]:\n"
        r += "   - Aperturas en Contractor (Peck Deck): 4 x 12 reps.\n"
        r += "   - Remo Sentado en Polea Baja con Agarre Gironda: 4 x 10 reps.\n\n"
        r += "📆 VIERNES [DÍA 4 - PIERNA DETALLE Y VOLUMEN DE TRABAJO]:\n"
        r += "   - Extensión de Cuádriceps + Curl Femoral Tumbado (Superserie): 4 x 12 reps.\n"
        r += "   - Elevación de Pantorrillas de Pie: 4 x 15 reps.\n\n"
        r += "📆 SÁBADO:\n   ❌ DESCANSO OBLIGATORIO.\n\n"
        r += "📆 DOMINGO:\n   ❌ DESCANSO OBLIGATORIO."
        
    return r

def generar_dieta_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    
    # Extracción automatizada de los checkboxes marcados por el cliente
    prots_sel = str(datos.get('Menu_Proteinas', 'Pechuga de Pollo')).split(',')
    carbs_sel = str(datos.get('Menu_Carbohidratos', 'Arroz Blanco')).split(',')
    grasas_sel = str(datos.get('Menu_Grasas', 'Aguacate')).split(',')
    frutas_sel = str(datos.get('Menu_Frutas', 'Manzana')).split(',')
    verd_sel = str(datos.get('Menu_Verduras', 'Brócoli')).split(',')
    
    prots = [p.strip() for p in prots_sel if p.strip() and p.strip() != "nan"]
    carbs = [c.strip() for c in carbs_sel if c.strip() and c.strip() != "nan"]
    grasas = [g.strip() for g in grasas_sel if g.strip() and g.strip() != "nan"]
    frutas = [f.strip() for f in frutas_sel if f.strip() and f.strip() != "nan"]
    verds = [v.strip() for v in verd_sel if v.strip() and v.strip() != "nan"]

    # Alimentos por defecto si el cliente dejó el casillero en blanco
    if not prots: prots = ["Pechuga de Pollo", "Claras de Huevo"]
    if not carbs: carbs = ["Arroz Blanco", "Avena en Hojuelas"]
    if not grasas: grasas = ["Aguacate", "Almendras"]
    if not frutas: frutas = ["Plátano", "Manzana"]
    if not verds: verds = ["Brócoli", "Espinacas"]

    # División milimétrica de macros exactos en 4 comidas estructuradas
    p_comida = round(m['prot'] / 4, 1)
    g_comida = round(m['grasa'] / 4, 1)
    c_comida = round(m['carbs'] / 4, 1)
    cal_comida = round(m['cals'] / 4, 0)

    d = f"========================================================================\n"
    d += f"     ESTRATEGIA NUTRICIONAL DE ALTA PRECISIÓN MM247 — DIETA AJUSTADA\n"
    d += f"========================================================================\n"
    d += f"🎯 OBJETIVO DIARIO EXACTO (Fijo: 2g Proteína / 1g Grasa por Kg de peso):\n"
    d += f"   🔥 Energía Total: {m['cals']} kcal\n"
    d += f"   💪 Proteínas: {m['prot']}g  |  🍞 Carbohidratos: {m['carbs']}g  |  🥑 Grasas: {m['grasa']}g\n\n"
    d += f"🥦 FUENTES SELECCIONADAS POR EL CLIENTE EN EL CUESTIONARIO:\n"
    d += f"   - Proteínas: {', '.join(prots)}\n"
    d += f"   - Carbohidratos: {', '.join(carbs)}\n"
    d += f"   - Grasas Saludables: {', '.join(grasas)}\n"
    d += f"   - Fibras y Micronutrientes: {', '.join(frutas)} | {', '.join(verds)}\n\n"
    d += f"📋 DISTRIBUCIÓN HORARIA DEL TIMING NUTRICIONAL:\n\n"
    
    d += f"• COMIDA 1 [Desayuno / Carga de Energía Inicial]:\n"
    d += f"  - Macronutrientes: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - MENÚ ESTRUCTURADO: Cocinado de {prots[0]} acompañado con {carbs[0]} y una porción fresca de {frutas[0]}. Fibra: {verds[0]}.\n\n"
    
    d += f"• COMIDA 2 [Almuerzo Central de Consolidación]:\n"
    d += f"  - Macronutrientes: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - MENÚ ESTRUCTURADO: {prots[-1]} preparado a la plancha (pesado en crudo) + porción de {carbs[-1]} cocido + aderezo graso de {grasas[0]}.\n\n"
    
    d += f"• COMIDA 3 [Merienda / Post-Entrenamiento de Absorción]:\n"
    d += f"  - Macronutrientes: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - MENÚ ESTRUCTURADO: Preparación rápida de {prots[0]} combinada de forma exacta con {carbs[0]} y una fruta mediana ({frutas[-1]}).\n\n"
    
    d += f"• COMIDA 4 [Cena Reparadora y Control de Ansiedad Nocturna]:\n"
    d += f"  - Macronutrientes: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - MENÚ ESTRUCTURADO: {prots[1] if len(prots)>1 else prots[0]} + {grasas[-1]} + Ensalada libre y abundante de {', '.join(verds)}.\n\n"
    
    d += "========================================================================\n"
    d += "⚠️ REGLAS OBLIGATORIAS: Pesar los alimentos de forma consistente y asegurar 4 Litros de agua purificada al día."
    return d

# =============================================================================
# MÓDULO 1: FORMULARIO MAESTRO INTEGRAL DE EVALUACIÓN (VISTA DEL CLIENTE)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación de Cargas, Historial Clínico y Selección de Alimentos</div>", unsafe_allow_html=True)
    
    with st.form("formulario_maestro_mm247_cerrado", clear_on_submit=True):
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "1-2. Datos Generales", 
            "3. Entrenamiento", 
            "4-5. Salud y Postura", 
            "6-7. Estilo de Vida", 
            "8-9. Menú de Alimentos", 
            "10-12. Esfuerzo"
        ])
        
        with t1:
            st.markdown("<div class='section-header'>1. DATOS FISIOLÓGICOS Y DEMOGRÁFICOS</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                f_nombre = st.text_input("Nombre completo:")
                f_edad = st.selectbox("Edad:", [f"{i} años" for i in range(14, 81)], index=11)
                f_sexo = st.selectbox("Sexo asignado al nacer:", ["Masculino", "Femenino"])
                f_estatura = st.selectbox("Estatura base:", [f"{i} cm" for i in range(120, 221)], index=55)
                f_peso_actual = st.selectbox("Peso corporal actual:", [f"{i} kg" for i in range(40, 161)], index=40)
            with col2:
                f_peso_obj = st.selectbox("Peso corporal objetivo:", [f"{i} kg" for i in range(40, 161)], index=35)
                f_ocupacion = st.selectbox("Ocupación de rutina:", ["Sedentaria", "Ligera", "Activa", "Estudiante"])
                f_horario = st.selectbox("Horario diario habitual:", ["Turno Matutino", "Turno Vespertino", "Turno Nocturno", "Horario Variable"])
                f_ciudad = st.selectbox("Zona geográfica:", ["México", "Estados Unidos", "España", "Latinoamérica / Otro"])
                f_contacto = st.text_input("WhatsApp de contacto:", value="55")
                f_correo = st.text_input("Correo electrónico de contacto:")
                
            st.markdown("<div class='section-header'>2. ENFOQUE PRINCIPAL</div>", unsafe_allow_html=True)
            f_objetivo = st.selectbox("¿Cuál es la meta prioritaria actual?", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal", "Aumentar fuerza", "Mejorar salud general"])
            f_tiempoloro = st.selectbox("¿En cuánto tiempo esperas ver resultados iniciales?", ["1-3 meses", "3-6 meses", "6-12 meses", "Más de 1 año"])
            f_compromiso = st.slider("Grado de compromiso real declarado (1 al 10):", 1, 10, 10)

        with t2:
            st.markdown("<div class='section-header'>3. ANTECEDENTES DE ENTRENAMIENTO</div>", unsafe_allow_html=True)
            f_tiempo_entrenando = st.selectbox("Tiempo entrenando de forma ininterrumpida:", ["Nunca", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años", "Más de 3 años"])
            f_tipo_entreno = st.multiselect("Sistemas deportivos practicados con anterioridad:", ["Gimnasio", "Calistenia", "Crossfit", "Deportes", "Funcional", "Ninguno"], default=["Gimnasio"])
            f_dias_semana = st.selectbox("¿Cuántos días a la semana vas a entrenar?", ["3 días por semana", "4 días por semana", "5 días por semana"])
            f_tiempo_sesion = st.selectbox("Disponibilidad de tiempo por sesión:", ["Menos de 45 minutos", "De 45 a 75 minutos", "Más de 75 minutos"])
            f_entrena_act = st.selectbox("¿Se encuentra entrenando actualmente?", ["Sí", "No"])
            f_coach_antes = st.selectbox("¿Ha tenido entrenadores personales previos?", ["Sí", "No"])

        with t3:
            st.markdown("<div class='section-header'>4. CONDICIÓN CLÍNICA Y LESIONES</div>", unsafe_allow_html=True)
            f_lesion = st.selectbox("¿Sufre de alguna lesión o dolor recurrente?", ["Ninguna", "Rodilla / Desgaste / Tendinitis", "Hombro / Manguito rotador", "Espalda Baja / Lumbalgia", "Cervicales", "Muñeca / Tobillo"])
            f_cirugias = st.selectbox("¿Cuenta con cirugías o intervenciones médicas quirúrgicas?", ["No", "Sí, en miembros inferiores", "Sí, en miembros superiores / columna"])
            f_dolor_frec = st.selectbox("¿Siente molestias agudas al ejecutar cargas?", ["No", "Sí, al hacer presses", "Sí, al hacer sentadillas", "Sí, dolor lumbar constante"])
            f_medica = st.selectbox("¿Consume medicamentos de prescripción de forma diaria?", ["No", "Sí, para presión / glucosa", "Sí, antiinflamatorios"])
            f_cond_diag = st.selectbox("¿Tiene alguna patología crónica diagnosticada?", ["Ninguna", "Diabetes", "Hipertensión", "Problemas de Tiroides / Hormonales", "Hernia Discal / Umbilical"])
            f_restriccion = st.selectbox("¿Tiene prohibiciones médicas explícitas?", ["No", "Sí"])
            f_prohibido = st.selectbox("¿Le han prohibido entrenamientos pesados de columna (Carga axial)?:", ["No", "Sí, cargas sobre la columna", "Sí, flexiones profundas"])
            
            st.markdown("<div class='section-header'>5. AUTO-EVALUACIÓN BIOMECÁNICA PRESETADA</div>", unsafe_allow_html=True)
            f_molestias_mov = st.multiselect("¿Tiene limitaciones o dolor al realizar estos movimientos básicos?:", ["Sentadilla", "Press de pecho", "Peso muerto", "Press militar", "Ninguno"], default=["Ninguno"])
            f_movilidad = st.selectbox("¿Cómo evalúa su flexibilidad articular general?", ["Mala / Muy rígido", "Regular", "Buena"])
            f_lim_mov = st.selectbox("¿Nota acortamientos evidentes de movimiento?", ["No", "Sí, en tobillos/cadera", "Sí, en hombros"])
            f_sentado = st.selectbox("¿Cuántas horas pasa sentado a causa de sus labores?", ["Sí, más de 6 horas", "Moderado (3 a 6 horas)", "No"])
            f_postura = st.selectbox("¿Tiene alguna de estas desviaciones posturales conocidas?", ["No", "Sí, hombros adelantados", "Sí, hiperlordosis lumbar"])
            f_debil = st.selectbox("¿Cuál considera que es su punto muscular más débil?:", ["Tren Inferior", "Tren Superior", "Zona Media / Core", "Espalda"])
            f_desarrollado = st.selectbox("¿Qué grupo muscular responde mejor por genética?:", ["Ninguno", "Piernas", "Pectoral / Brazos", "Espalda"])
            f_equilibrio = st.selectbox("¿Tiene problemas de coordinación mecánica o equilibrio?:", ["No", "Sí"])

        with t4:
            st.markdown("<div class='section-header'>6. MORFOLOGÍA Y ESTRUCTURA</div>", unsafe_allow_html=True)
            f_fisico = st.selectbox("¿Con qué somatotipo se identifica de forma visual?", ["Delgado / Ectomorfo", "Atlético / Mesomorfo", "Robusto / Endomorfo", "Sobrepeso"])
            f_acumula_grasa = st.selectbox("¿En qué sector del cuerpo tiende a acumular tejido graso?:", ["Abdomen / Zona lumbar", "Piernas y Cadera", "Distribución General"])
            f_gana_musculo = st.selectbox("¿Qué tanta facilidad muestra para construir masa muscular?", ["Muy difícil", "Ritmo Normal", "Fácil"])
            f_gana_grasa = st.selectbox("¿Qué tan rápido aumenta su peso graso en periodos libres?", ["Muy fácil", "Ritmo Normal", "Difícil"])
            
            st.markdown("<div class='section-header'>7. CALIDAD DE HÁBITOS Y DESCANSO</div>", unsafe_allow_html=True)
            f_horas_sueno = st.selectbox("Promedio de horas de sueño por noche:", ["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"])
            f_calif_sueno = st.selectbox("Calidad percibida de su descanso nocturno:", ["Malo", "Regular", "Excelente"])
            f_estres_diario = st.selectbox("Nivel de estrés psicológico o laboral cotidiano:", ["Bajo / Controlado", "Medio", "Alto"])
            f_num_comidas = st.selectbox("¿Cuántas comidas sólidas completas realiza al día?", ["2 comidas", "3 comidas", "4 comidas", "5 comidas o más"])
            f_litros_agua = st.selectbox("Consumo diario estimado de agua simple:", ["Menos de 1.5 Litros", "Entre 1.5 y 3 Litros", "Más de 3 Litros"])
            f_alcohol = st.selectbox("Frecuencia de consumo de bebidas alcohólicas:", ["No / Nunca", "Solo Ocasional", "Frecuente fines de semana"])
            f_fuma = st.selectbox("¿Consume tabaco de forma regular?", ["No", "Sí"])
            f_pasos = st.selectbox("Estimación diaria de actividad de movimiento (Pasos/NEAT):", ["Menos de 5k", "5k a 10k", "Más de 10k"])
            f_nivel_actividad = st.selectbox("Nivel de actividad cotidiana fuera del gimnasio:", ["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"])

        with t5:
            st.markdown("<div class='section-header'>8. MENÚ DE SELECCIÓN CONTROLADA (CHECKBOXES DE ALIMENTOS)</div>", unsafe_allow_html=True)
            st.write("Marque únicamente los alimentos que está dispuesto a comer cotidianamente para armar su menú exacto:")
            
            menu_prots = st.multiselect("🥩 FUENTES PROTEICAS:", ["Pechuga de Pollo", "Bisteck de Res magro", "Lomo de Cerdo", "Claras de Huevo", "Huevo Entero", "Atún en agua", "Filete de Pescado Blanco", "Queso Panela bajo en grasa", "Tofu / Fuentes Veganas"], default=["Pechuga de Pollo", "Claras de Huevo", "Atún en agua"])
            menu_carbs = st.multiselect("🍞 FUENTES DE CARBOHIDRATOS:", ["Arroz Blanco", "Avena en Hojuelas", "Camote asado", "Papa cocida", "Tortilla de Maíz", "Pan Integral", "Pasta Integral", "Quinoa"], default=["Arroz Blanco", "Avena en Hojuelas", "Tortilla de Maíz"])
            menu_grasas = st.multiselect("🥑 GRASAS SALUDABLES REQUERIDAS:", ["Aguacate", "Almendras naturales", "Nueces de pecana", "Crema de Cacahuete pura", "Aceite de Oliva Extra Virgen"], default=["Aguacate", "Almendras naturales"])
            menu_frutas = st.multiselect("🍎 FRUTAS SELECCIONADAS:", ["Plátano", "Manzana", "Fresas / Berries", "Piña", "Papaya", "Melón"], default=["Plátano", "Manzana"])
            menu_verds = st.multiselect("🥦 VERDURAS Y APORTE DE FIBRA:", ["Brócoli", "Espinacas", "Calabacita", "Champiñones", "Espárragos", "Lechuga / Pepino"], default=["Brócoli", "Espinacas", "Lechuga / Pepino"])
            
            st.markdown("<div class='section-header'>9. COMPORTAMIENTO NUTRICIONAL GENERAL</div>", unsafe_allow_html=True)
            f_obj_nutri = st.selectbox("Preferencia de control alimenticio:", ["Bajar porcentaje de grasa", "Aumento de masa magra", "Recomposición"])
            f_alergias = st.selectbox("¿Padece de alergias alimentarias graves?", ["Ninguna", "Frutos secos", "Mariscos", "Huevo / Gluten"])
            f_intolerancia = st.selectbox("¿Tiene intolerancias digestivas marcadas?", ["Ninguna", "Lactosa", "Gluten", "Legumbres"])
            f_tipo_alimentacion = st.selectbox("Estructura dietética general de preferencia:", ["Omnívoro", "Vegetariano", "Vegano", "Keto"])
            f_no_gustan = st.selectbox("Alimentos que rechaza por completo por sabor/palatabilidad:", ["Ninguno", "Pescados", "Verduras amargas", "Lácteos"])
            f_comer_fuera = st.selectbox("¿Suele realizar comidas comerciales fuera de casa?", ["Nunca", "1-2 veces por semana", "3 o más veces"])
            f_presupuesto = st.selectbox("Presupuesto de inversión asignado para despensa fit:", ["Básico / Económico", "Estándar flexible", "Premium"])
            f_horarios_fijos = st.selectbox("¿Cuenta con facilidad para comer a horarios estrictos?", ["Sí", "No", "Solo a veces"])
            f_cocinar = st.selectbox("¿Usted mismo se encarga de la preparación y cocina?", ["Sí", "No", "Básico"])
            
            f_recup_post, f_cansado_freq, f_fatiga_dia, f_dolores_const, f_energia_diaria = "Regular", "No", "Leve", "No", "Normal"

        with t6:
            st.markdown("<div class='section-header'>10. DISPONIBILIDAD LOGÍSTICA DE INSTALACIONES</div>", unsafe_allow_html=True)
            f_donde_entrena = st.selectbox("¿En qué instalaciones vas a entrenar?", ["Gimnasio comercial completo", "Gimnasio de edificio", "Casa con equipo", "Exterior / Calistenia"])
            f_equipo = st.multiselect("¿De qué equipamiento dispones de forma inmediata?", ["Mancuernas", "Barras y Discos", "Poleas", "Máquinas de aislamiento", "Banco regulable", "Rack / Smith"], default=["Mancuernas", "Barras y Discos", "Poleas"])
            f_lim_space = st.selectbox("¿Tienes limitaciones severas de espacio en tus zonas de entreno?", ["No", "Sí"])
            
            st.markdown("<div class='section-header'>11. METAS DE ENFOQUE Y FILTROS</div>", unsafe_allow_html=True)
            f_partes_mejorar = st.selectbox("Sector muscular estético prioritario que deseas corregir:", ["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda", "Brazos", "Abdomen / Definición"])
            f_dificultad = st.selectbox("¿Cuál ha sido tu mayor limitante en proyectos previos?", ["Falta de constancia", "Estancamiento en cargas", "No saber comer", "Lesiones recurrentes"])
            f_odia_ex = st.selectbox("Ejercicio que te cause dolor o que rechaces por completo:", ["Ninguno", "Sentadilla Libre", "Press Militar Barra", "Zancadas Walking"])
            f_disfruta_ex = st.selectbox("Ejercicio donde experimentas la mejor conexión mente-músculo:", ["Prensa de piernas", "Extensiones", "Jalones en polea", "Press inclinado"])
            f_impide_progresar = st.selectbox("¿Qué factor saboteó tus intenciones de entrenamiento antes?", ["Falta de tiempo/Trabajo", "Planes aburridos o genéricos", "Falta de un guía experto"])
            
            st.markdown("<div class='section-header'>12. COMPORTAMIENTO Y ESCALAS PSICOMÉTRICAS (1 AL 10)</div>", unsafe_allow_html=True)
            f_p_disciplina = st.slider("Autoevaluación de disciplina actual:", 1, 10, 8)
            f_p_estres = st.slider("Percepción de carga de estrés mental:", 1, 10, 5)
            f_p_sueno = st.slider("Eficiencia real detectada en sus horas de sueño:", 1, 10, 8)
            f_p_motivacion = st.slider("Nivel de motivación para arrancar el proceso:", 1, 10, 9)
            f_p_energia = st.slider("Nivel de energía vital promedio durante el día:", 1, 10, 7)
            f_p_hambre = st.slider("Nivel de ansiedad o hambre diurna recurrente:", 1, 10, 5)
            f_p_recup = st.slider("Velocidad de recuperación muscular percibida:", 1, 10, 7)
            
            f_prioridad = st.selectbox("Prioridad del filtro de cargas estructurales:", ["Salud", "Estética", "Rendimiento", "Fuerza"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            enviar_maestro = st.form_submit_button("🚀 REGISTRAR EXPEDIENTE MAESTRO EN MM247")
            
        if enviar_maestro:
            if not f_nombre.strip():
                st.error("❌ El campo de Nombre Completo es completamente obligatorio para el registro.")
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
                    "Recuperación post": str(f_recup_post), "Cansado frecuente": str(f_cansado_freq), "Fatiga durante el día": str(f_fatiga_dia), "Dolores constantes": str(f_dolores_const), "Energía diaria": str(f_energia_diaria),
                    "Donde entrenará": str(f_donde_entrena), "Equipo disponible": ",".join(f_equipo), "Limitación espacio": str(f_lim_space), "Partes mejorar": str(f_partes_mejorar), "Dificultades físicas": str(f_dificultad),
                    "Ejercicio odia": str(f_odia_ex), "Ejercicio disfruta": str(f_disfruta_ex), "Impedido progresar": str(f_impide_progresar), "P_Disciplina": str(f_p_disciplina), "P_Estres": str(f_p_estres),
                    "P_Sueno": str(f_p_sueno), "P_Motivacion": str(f_p_motivacion), "P_Energia": str(f_p_energia), "P_Hambre": str(f_p_hambre), "P_Recup": str(f_p_recup), "Prioridad": str(f_prioridad),
                    "Menu_Proteinas": ",".join(menu_prots), "Menu_Carbohidratos": ",".join(menu_carbs), "Menu_Grasas": ",".join(menu_grasas), "Menu_Frutas": ",".join(menu_frutas), "Menu_Verduras": ",".join(menu_verds),
                    "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                }
                with st.spinner("Subiendo expediente estructurado..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        if response.status_code == 200 and "success" in response.text:
                            st.success("✅ ¡Expediente y Menú de Alimentos guardados con éxito en la base de datos de MM247!")
                            st.balloons()
                        else: st.error(f"Error de procesamiento en servidor de hojas: {response.text}")
                    except Exception as api_err: st.error(f"Fallo crítico de comunicación externa: {api_err}")

# =============================================================================
# MÓDULO 2: PANEL DE CONTROL ADMINISTRATIVO AVANZADO (VISTA DEL ENTRENADOR)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel de Control MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave maestra de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        st.success("Acceso autorizado con credenciales válidas.")
        if df_existente.empty:
            st.warning("No se detectan alumnos registrados en la base de datos actual.")
        else:
            st.markdown("### 📈 Métricas de Control General")
            total_alumnos = len(df_existente)
            
            # Buscador seguro de columnas dinámicas para evitar fallos de Pandas
            col_meta_key = next((c for c in ["Objetivo principal", "Objetivoprincipal", "Objetivo"] if c in df_existente.columns), "")
            
            if col_meta_key:
                perdida_count = df_existente[col_meta_key].astype(str).str.contains('Perder|Bajar|Déficit|grasa', case=False, na=False).sum()
                masa_count = df_existente[col_meta_key].astype(str).str.contains('Ganar|Subir|Volumen|muscular', case=False, na=False).sum()
            else:
                perdida_count, masa_count = 0, 0

            k1, k2, k3 = st.columns(3)
            with k1: st.markdown(f"<div class='metric-card'><div class='metric-title'>Expedientes Registrados</div><div class='metric-value'>{total_alumnos} alumnos</div></div>", unsafe_allow_html=True)
            with k2: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Enfoque Oxidación / Grasa</div><div class='metric-value'>{perdida_count} alumnos</div></div>", unsafe_allow_html=True)
            with k3: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Enfoque Hipertrofia Magra</div><div class='metric-value'>{masa_count} alumnos</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            col_nombre_key = "Nombre completo" if "Nombre completo" in df_existente.columns else df_existente.columns[1]
            lista_alumnos = df_existente[col_nombre_key].dropna().unique()
            alumno_sel = st.selectbox("Seleccione el expediente del alumno a planificar:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente[col_nombre_key] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            nombre_display = str(datos_alumno[col_nombre_key]).title()

            # Gestión inteligente de estados de la sesión para mantener las ediciones del entrenador
            if "alumno_actual" not in st.session_state or st.session_state.alumno_actual != alumno_sel:
                st.session_state.alumno_actual = alumno_sel
                db_propuesta = str(datos_alumno.get("Propuesta General", "")).strip()
                db_rutina = str(datos_alumno.get("Rutina Biomecánica", "")).strip()
                db_balance = str(datos_alumno.get("Balance Energético", "")).strip()
                
                st.session_state.v_propuesta = db_propuesta if db_propuesta and db_propuesta != "nan" else generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = db_rutina if db_rutina and db_rutina != "nan" else generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = db_balance if db_balance and db_balance != "nan" else generar_dieta_detallada_mm247(datos_alumno)

            st.markdown(f"### 👤 Gestión de Carga Activa: {nombre_display}")
            
            if st.button("🚀 Forzar Re-Cálculo de Automatización con Alimentos Reales"):
                st.session_state.v_propuesta = generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = generar_dieta_detallada_mm247(datos_alumno)
                st.rerun()

            st.markdown("---")
            with st.form("prescripcion_maestra_form_mm247"):
                propuesta = st.text_area("🩺 HOJA 1: Informe Diagnóstico Avanzado (Clínico, Postural y Fisiológico):", value=st.session_state.v_propuesta, height=280)
                rutina = st.text_area("🏋️ HOJA 2: Programación Semanal Específica de 7 Días (Cronograma con Descansos):", value=st.session_state.v_rutina, height=350)
                balance = st.text_area("🥗 HOJA 3: Plan Nutricional Ajustado Exacto (Filtro por Checkboxes):", value=st.session_state.v_balance, height=350)
                
                guardar_changes = st.form_submit_button("💾 Guardar y Sincronizar Plan Estructural con Google Sheets")
                if guardar_changes:
                    payload_edit = {"Action": "UPDATE", "RowIndex": int(idx_alumno + 2)}
                    for k in datos_alumno.keys(): payload_edit[k] = str(datos_alumno[k])
                    payload_edit["Propuesta General"] = propuesta
                    payload_edit["Balance Energético"] = balance
                    payload_edit["Rutina Biomecánica"] = rutina
                    
                    with st.spinner("Modificando registros en la base central..."):
                        try:
                            requests.post(WEBHOOK_URL, json=payload_edit)
                            st.session_state.v_propuesta = propuesta
                            st.session_state.v_rutina = rutina
                            st.session_state.v_balance = balance
                            st.success("✅ ¡Plan maestro y dieta de precisión sincronizados con éxito!")
                        except Exception as e_save: st.error(f"Fallo de guardado en la red: {e_save}")
            
            if st.button("🖨️ Compilar Plan Maestro en PDF Profesional de 3 Hojas"):
                try:
                    pdf = FPDF()
                    def limpiar_texto(txt): return str(txt).replace("•", "-").replace("–", "-").replace("—", "-").replace("º"," ").encode('latin-1', 'ignore').decode('latin-1')

                    # HOJA 1: Diagnóstico Integral
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 38, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 24)
                    pdf.cell(0, 12, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("INFORME DE PLANIFICACIÓN INTEGRAL DE RENDIMIENTO"), ln=True, align="C")
                    pdf.ln(18)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 6, limpiar_texto(st.session_state.v_propuesta))

                    # HOJA 2: Entrenamiento Cronológico
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("PROGRAMACIÓN SEMANAL DETALLADA (CRONOGRAMA DE 7 DÍAS)"), ln=True, align="C")
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 5.5, limpiar_texto(st.session_state.v_rutina))

                    # HOJA 3: Nutrición Flexible con Checkboxes
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(0, 4, limpiar_texto("ESTRATEGIA NUTRICIONAL DE ALTA PRECISIÓN (MACROS EXACTOS)"), ln=True, align="C")
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 5.5, limpiar_texto(st.session_state.v_balance))
                    
                    pdf_data = pdf.output(dest='S')
                    st.download_button(
                        label="⬇️ Descargar Plan Estructural Completo en PDF",
                        data=bytes(pdf_data),
                        file_name=f"Plan_Estructural_MM247_{nombre_display.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf: st.error(f"Fallo mecánico al compilar el PDF: {err_pdf}")
                    
    elif password != "": st.error("🔑 Clave de acceso inválida.")
