import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests
import random

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y BRANDING (SISTEMA MM247)
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    """Carga y limpia de forma segura los datos de Google Sheets evitando de forma estricta fallos de caché"""
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        # Validaciones de seguridad para evitar KeyError en el Dashboard si la hoja está vacía
        if "ID_Alumno" not in df.columns: df["ID_Alumno"] = ""
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = "INICIAL"
        
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Generador de ID Único
def generar_id_unico(nombre):
    iniciales = "".join([p[0].upper() for p in str(nombre).strip().split() if p])[:3]
    if not iniciales: iniciales = "MM"
    numero = random.randint(1000, 9999)
    return f"MM-{iniciales}-{numero}"

# Estilos CSS inyectados de forma segura en Streamlit
st.markdown("""
    <style>
    .main-title { font-size:44px; font-weight:900; color:#111111; text-align:center; letter-spacing: -1px; margin-bottom:0px; }
    .subtitle { font-size:16px; color:#666666; text-align:center; margin-bottom:35px; text-transform: uppercase; letter-spacing: 1px;}
    .section-header { font-size:20px; font-weight:bold; color:#111111; margin-top:25px; margin-bottom:12px; border-bottom: 3px solid #111111; padding-bottom:6px; }
    .metric-card { background: #ffffff; padding: 22px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-left: 6px solid #111111; }
    .metric-title { font-size: 13px; color: #777777; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #111111; font-weight: bold; margin-top: 4px; }
    .profile-box { background-color: #f9f9f9; padding: 18px; border-radius: 6px; border: 1px solid #eeeeee; margin-bottom: 20px;}
    .id-box { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 6px; font-size: 18px; color: #1B5E20; text-align: center; font-weight: bold; margin-top: 15px;}
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 48px; border: none; }
    .stButton>button:hover { background-color: #333333; color: white; }
    
    /* Clases para barras de colores en Dashboard */
    .barra-base { height: 12px; border-radius: 6px; width: 100%; background: #e0e0e0; margin-top: 5px;}
    .barra-verde { background: #22c55e; width: 100%; height: 12px; border-radius: 6px;}
    .barra-roja { background: #ef4444; width: 30%; height: 12px; border-radius: 6px;}
    .barra-amarilla { background: #eab308; width: 60%; height: 12px; border-radius: 6px;}
    .barra-gris { background: #9ca3af; width: 0%; height: 12px; border-radius: 6px;}
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Navegación MM247:", [
    "📝 Cuestionario Integral de Evaluación", 
    "🔄 Cuestionario 2: Revisión de Avance",
    "📊 Dashboard Administrador"
])

# =============================================================================
# 2. MOTOR DE NORMALIZACIÓN FLEXIBLE (TU CÓDIGO ORIGINAL INTACTO)
# =============================================================================
def normalizar_datos_alumno(datos_raw):
    norm = {}
    def buscar_columna(lista_palabras_clave, defecto="", indice_respaldo=None):
        for col in datos_raw.index:
            col_limpia = str(col).lower().strip()
            for kw in lista_palabras_clave:
                if kw.lower() in col_limpia:
                    val = datos_raw[col]
                    if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                        return str(val).strip()
        if indice_respaldo is not None and indice_respaldo < len(datos_raw):
            val = datos_raw.iloc[indice_respaldo]
            if pd.notna(val) and str(val).strip() != "" and str(val).lower() != "nan":
                return str(val).strip()
        return defecto

    norm['Nombre completo'] = buscar_columna(['nombre', 'alumno', 'completo'], 'Alumno', 1)
    norm['Edad'] = buscar_columna(['edad', 'años'], '25', 2)
    norm['Sexo'] = buscar_columna(['sexo', 'género', 'genero'], 'Masculino', 3)
    norm['Estatura'] = buscar_columna(['estatura', 'altura', 'cm'], '175', 4)
    norm['Peso actual'] = buscar_columna(['peso actual', 'peso corporal', 'kg'], '80', 5)
    norm['Peso objetivo'] = buscar_columna(['peso objetivo', 'meta'], '75', 6)
    norm['Nivel de actividad'] = buscar_columna(['nivel de actividad', 'neat', 'actividad'], 'Moderadamente activo')
    norm['Objetivo principal'] = buscar_columna(['meta', 'objetivo principal', 'objetivo'], 'Recomposición corporal')
    norm['Condición médica'] = buscar_columna(['condición médica', 'patología', 'enfermedad', 'medica'], 'Ninguna')
    norm['Tiempo entrenando'] = buscar_columna(['tiempo entrenando', 'experiencia', 'entrenando'], 'Menos de 6 meses')
    norm['Prioridad'] = buscar_columna(['prioridad', 'filtro'], 'Salud')
    norm['Lesión actual'] = buscar_columna(['lesión', 'lesion', 'lastimado'], 'Ninguna')
    norm['Cirugías'] = buscar_columna(['cirugías', 'cirugia', 'operación'], 'No')
    norm['Horas sentado'] = buscar_columna(['horas sentado', 'sentado', 'oficina'], 'No')
    norm['Mala postura'] = buscar_columna(['postura', 'desviación', 'hombros'], 'No')
    norm['Dolor frecuente'] = buscar_columna(['dolor frecuente', 'molestia'], 'No')
    norm['Prohibido ejercicio'] = buscar_columna(['prohibido', 'restricción', 'axial'], 'No')
    norm['Horas sueño'] = buscar_columna(['horas sueño', 'sueño', 'durme'], '7-8 horas')
    norm['Partes mejorar'] = buscar_columna(['partes mejorar', 'priorizar muscular', 'sector'], 'General')
    norm['Músculo desarrollado'] = buscar_columna(['músculo desarrollado', 'genética'], 'Ninguno')
    norm['Días entrenar'] = buscar_columna(['días entrenar', 'semana cuántos', 'dias'], '4 días por semana')
    norm['Equipo disponible'] = buscar_columna(['equipo disponible', 'equipamiento', 'accesorios'], 'Gimnasio completo')
    
    def extraer_numero(lista_kw, defecto=5):
        texto_val = buscar_columna(lista_kw, None)
        if texto_val:
            num = ''.join(filter(str.isdigit, str(texto_val)))
            if num: return int(num)
        return defecto

    norm['P_Estres'] = extraer_numero(['p_estres', 'estrés', 'estres'], 5)
    norm['P_Sueno'] = extraer_numero(['p_sueno', 'sueño eficiencia', 'calidad'], 8)
    norm['P_Recup'] = extraer_numero(['p_recup', 'recuperación', 'velocidad'], 7)
    
    norm['Menu_Proteinas'] = buscar_columna(['menu_proteinas', 'proteínas', 'proteinas'], 'Pechuga de Pollo')
    norm['Menu_Carbohidratos'] = buscar_columna(['menu_carbohidratos', 'carbs', 'carbohidratos'], 'Arroz Blanco')
    norm['Menu_Grasas'] = buscar_columna(['menu_grasas', 'grasas'], 'Aguacate')
    norm['Menu_Frutas'] = buscar_columna(['menu_frutas', 'frutas'], 'Manzana')
    norm['Menu_Verduras'] = buscar_columna(['menu_verduras', 'verduras'], 'Brócoli')
    
    return norm

# =============================================================================
# 3. MOTORES INTERNOS DE CÁLCULO CIENTÍFICO Y FISIOLÓGICO (TU CÓDIGO ORIGINAL)
# =============================================================================
def calcular_motores_automatizados(datos):
    try: peso = float(str(datos.get('Peso actual', '80')).replace(" kg", "").split()[0])
    except Exception: peso = 80.0
    try: estatura = float(str(datos.get('Estatura', '175')).replace(" cm", "").split()[0])
    except Exception: estatura = 175.0
    try: edad = float(str(datos.get('Edad', '25')).replace(" años", "").split()[0])
    except Exception: edad = 25.0
    genero = str(datos.get('Sexo', 'Masculino'))
    
    imc = peso / ((estatura/100)**2)
    
    if imc < 18.5: estado_clinico = "Bajo Peso / Déficit Nutrimental"
    elif imc < 25.0: estado_clinico = "Normopeso / Composición Corporal Saludable"
    elif imc < 30.0: estado_clinico = "Sobrepeso / Alerta de Tejido Adiposo Elevado"
    elif imc < 35.0: estado_clinico = "Obesidad Grado I / Riesgo Cardiovascular Moderado"
    elif imc < 40.0: estado_clinico = "Obesidad Grado II / Riesgo Clínico Alto"
    else: estado_clinico = "Obesidad Grado III (Mórbida) / Alerta Crítica Multiorgánica"
    
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
    
    if "Perder" in meta or "Bajar" in meta or "Déficit" in meta or "grasa" in meta:
        cals_obj = tdee - 450 if edad < 45 else tdee - 350
        balance_str = f"Déficit Calórico Estructurado ({round(cals_obj)} kcal)"
    elif "Ganar" in meta or "Subir" in meta or "Volumen" in meta or "muscular" in meta:
        cals_obj = tdee + 300 if "Diabetes" not in condicion else tdee + 150
        balance_str = f"Superávit Calórico Limpio ({round(cals_obj)} kcal)"
    else:
        cals_obj = tdee
        balance_str = f"Normocalórico de Consolidación ({round(cals_obj)} kcal)"
        
    prot = peso * 2.0  # Regla inmutable MM247
    grasa = peso * 1.0 # Regla inmutable MM247
    cals_restantes = cals_obj - ((prot * 4) + (grasa * 9))
    carbs = max(cals_restantes / 4, 50.0)
    
    return {
        "imc": round(imc, 1), "estado_clinico": estado_clinico, "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals_obj, 0),
        "prot": round(prot, 1), "grasa": round(grasa, 1), "carbs": round(carbs, 1), "balance_str": balance_str,
        "edad": edad, "genero": genero, "condicion": condicion, "peso": peso
    }

def generar_propuesta_integral_mm247(datos):
    m = calcular_motores_automatizados(datos)
    nombre = str(datos.get('Nombre completo', 'Alumno')).title()
    horas_sentado = str(datos.get('Horas sentado', 'No'))
    postura = str(datos.get('Mala postura', 'No'))
    
    analisis_postural = ""
    if "más de 6" in horas_sentado or "Sí" in horas_sentado:
        analisis_postural += "• Alerta Postural: Jornada laboral sedentaria (más de 6 horas sentado). Riesgo de amnesia glútea.\n"
    if "hombros" in postura:
        analisis_postural += "• Desbalance Superior: Rotación interna de hombros (cifosis). Priorizar cadena posterior.\n"
    elif "hiperlordosis" in postura:
        analisis_postural += "• Inestabilidad Lumbar: Anteversión pélvica. Limitar cargas axiales sobre la columna.\n"
    else:
        analisis_postural += "• Estabilidad Ósea: Alineación articular óptima detectada.\n"

    lesion = str(datos.get('Lesión actual', 'Ninguna'))
    cirugias = str(datos.get('Cirugías', 'No'))
    dolor = str(datos.get('Dolor frecuente', 'No'))
    prohibido = str(datos.get('Prohibido ejercicio', 'No'))
    
    analisis_clinico = ""
    if lesion != "Ninguna" or cirugias != "No" or m['condicion'] != "Ninguna":
        analisis_clinico += f"🚨 RESTRICCIONES CLÍNICAS ACTIVADAS:\n"
        analisis_clinico += f"  - Patología Base: {m['condicion']} | Zona Afectada: {lesion}\n"
    else:
        analisis_clinico += "• Diagnóstico de Salud: Sin limitaciones patológicas u óseas declaradas. Apto para sobrecarga.\n"

    res = f"========================================================================\n"
    res += f"        MM247 INFORME DIAGNÓSTICO MAESTRO AVANZADO (100% PERSONALIZADO)\n"
    res += f"========================================================================\n\n"
    res += f"👤 ALUMNO EVALUADO: {nombre} | EDAD: {int(m['edad'])} años | SEXO: {m['genero']}\n"
    res += f"🏥 CLASIFICACIÓN CLÍNICA INICIAL:\n"
    res += f"   - Índice de Masa Corporal (IMC): {m['imc']}\n"
    res += f"   - Estado de Composición: {m['estado_clinico']}\n\n"
    res += f"📊 ANÁLISIS METABÓLICO BASE:\n"
    res += f"   - Tasa Metabólica Basal (TMB): {m['tmb']} kcal\n"
    res += f"   - Gasto Diario Total (TDEE): {m['tdee']} kcal\n"
    res += f"   - Ajuste Prescrito MM247: {m['balance_str']}\n\n"
    res += f"========================================================================\n"
    return res

def generar_rutina_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    dias = str(datos.get('Días entrenar', '4')).split()[0]
    meta = str(datos.get('Objetivo principal', '')).lower()
    
    r = f"========================================================================\n"
    r += f"     CRONOGRAMA DE ENTRENAMIENTO ESTRUCTURADO Y MUTABLE — MM247\n"
    r += f"========================================================================\n"
    r += f"Perfil: {m['genero']} | Frecuencia: {dias} Días | Enfoque: {meta}\n\n"
    r += "📆 LUNES [DÍA 1 - ENFOQUE EMPUJE / TENSIÓN MECÁNICA HEAVY]:\n"
    r += "   - Press de Pecho: 4 x 6-8 reps (RIR 1 | Descanso largo: 120s)\n"
    r += "   - Press Militar con Barra: 3 x 8 reps\n"
    r += "📆 MARTES:\n   ❌ DESCANSO METABÓLICO REPARADOR\n\n"
    r += "📆 MIÉRCOLES [DÍA 2 - ENFOQUE TRACCIÓN]:\n"
    r += "   - Peso Muerto / Remo: 3 x 6 reps pesadas\n"
    r += "📆 JUEVES:\n   ❌ DESCANSO SISTEMA NERVIOSO CENTRAL\n\n"
    r += "📆 VIERNES [DÍA 3 - DESARROLLO DE TREN INFERIOR]:\n"
    r += "   - Sentadilla / Prensa: 4 x 8-10 reps\n"
    r += "📆 SÁBADO Y DOMINGO:\n   ❌ DESCANSO INTEGRAL (Superávit y síntesis proteica)"
    return r

def generar_dieta_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    p_comida = round(m['prot'] / 4, 1)
    g_comida = round(m['grasa'] / 4, 1)
    c_comida = round(m['carbs'] / 4, 1)
    cal_comida = round(m['cals'] / 4, 0)

    d = f"========================================================================\n"
    d += f"     ESTRATEGIA NUTRICIONAL DE ALTA PRECISIÓN MM247 — DIETA AJUSTADA\n"
    d += f"========================================================================\n"
    d += f"🎯 OBJETIVO DIARIO EXACTO (2g Proteína / 1g Grasa por Kg de peso):\n"
    d += f"   🔥 Energía Total: {m['cals']} kcal\n"
    d += f"   💪 Proteínas: {m['prot']}g  |  🍞 Carbohidratos: {m['carbs']}g  |  🥑 Grasas: {m['grasa']}g\n\n"
    d += f"• COMIDA TIPO 1: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"• COMIDA TIPO 2: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"• COMIDA TIPO 3: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"• COMIDA TIPO 4: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"========================================================================\n"
    return d

# =============================================================================
# MÓDULO 1: FORMULARIO MAESTRO INTEGRAL DE EVALUACIÓN (CUESTIONARIO 1)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación de Cargas, Historial Clínico y Selección de Alimentos</div>", unsafe_allow_html=True)
    
    with st.form("formulario_maestro_mm247_cerrado", clear_on_submit=False):
        t1, t2, t3, t4, t5, t6 = st.tabs(["1-2. Datos Generales", "3. Entrenamiento", "4-5. Salud y Postura", "6-7. Estilo de Vida", "8-9. Menú de Alimentos", "10-12. Esfuerzo"])
        
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
            st.markdown("<div class='section-header'>8. MENÚ DE SELECCIÓN CONTROLADA</div>", unsafe_allow_html=True)
            menu_prots = st.multiselect("🥩 PROTEÍNAS:", ["Pechuga de Pollo", "Bisteck de Res magro", "Lomo de Cerdo", "Claras de Huevo", "Atún en agua", "Filete de Pescado"], default=["Pechuga de Pollo", "Claras de Huevo"])
            menu_carbs = st.multiselect("🍞 CARBOHIDRATOS:", ["Arroz Blanco", "Avena en Hojuelas", "Camote asado", "Papa cocida", "Tortilla de Maíz"], default=["Arroz Blanco", "Avena en Hojuelas"])
            menu_grasas = st.multiselect("🥑 GRASAS:", ["Aguacate", "Almendras naturales", "Crema de Cacahuete"], default=["Aguacate"])
            menu_frutas = st.multiselect("🍎 FRUTAS:", ["Plátano", "Manzana", "Fresas / Berries"], default=["Plátano", "Manzana"])
            menu_verds = st.multiselect("🥦 VERDURAS:", ["Brócoli", "Espinacas", "Lechuga / Pepino"], default=["Brócoli", "Espinacas"])
            
            st.markdown("<div class='section-header'>9. COMPORTAMIENTO NUTRICIONAL GENERAL</div>", unsafe_allow_html=True)
            f_obj_nutri = st.selectbox("Preferencia alimenticia:", ["Bajar porcentaje de grasa", "Aumento de masa magra"])
            f_alergias = st.selectbox("¿Alergias alimentarias graves?", ["Ninguna", "Frutos secos", "Mariscos"])
            f_intolerancia = st.selectbox("¿Intolerancias digestivas?", ["Ninguna", "Lactosa", "Gluten"])
            f_tipo_alimentacion = st.selectbox("Estructura dietética:", ["Omnívoro", "Vegetariano"])
            f_no_gustan = st.selectbox("Alimentos que rechaza:", ["Ninguno", "Pescados"])
            f_comer_fuera = st.selectbox("¿Suele comer fuera?", ["Nunca", "1-2 veces por semana"])
            f_presupuesto = st.selectbox("Presupuesto fit:", ["Básico / Económico", "Estándar flexible"])
            f_horarios_fijos = st.selectbox("¿Horarios estrictos?", ["Sí", "No"])
            f_cocinar = st.selectbox("¿Usted cocina?", ["Sí", "No"])

        with t6:
            st.markdown("<div class='section-header'>10. DISPONIBILIDAD LOGÍSTICA</div>", unsafe_allow_html=True)
            f_donde_entrena = st.selectbox("¿Dónde vas a entrenar?", ["Gimnasio comercial completo", "Casa con equipo"])
            f_equipo = st.multiselect("¿De qué equipamiento dispones?", ["Mancuernas", "Barras y Discos", "Poleas"], default=["Mancuernas", "Barras y Discos"])
            f_lim_space = st.selectbox("¿Limitaciones de espacio?", ["No", "Sí"])
            
            st.markdown("<div class='section-header'>11. METAS DE ENFOQUE Y FILTROS</div>", unsafe_allow_html=True)
            f_partes_mejorar = st.selectbox("Sector muscular a corregir:", ["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda", "Brazos", "Abdomen / Definición"])
            f_dificultad = st.selectbox("Mayor limitante previa:", ["Falta de constancia", "Estancamiento en cargas"])
            f_odia_ex = st.selectbox("Ejercicio que rechaces:", ["Ninguno", "Sentadilla Libre"])
            f_disfruta_ex = st.selectbox("Ejercicio con mejor conexión:", ["Prensa de piernas", "Extensiones"])
            f_impide_progresar = st.selectbox("¿Qué saboteó tu avance antes?", ["Falta de tiempo/Trabajo", "Planes aburridos o genéricos"])
            
            st.markdown("<div class='section-header'>12. ESCALAS PSICOMÉTRICAS (1 AL 10)</div>", unsafe_allow_html=True)
            f_p_disciplina = st.slider("Disciplina actual:", 1, 10, 8)
            f_p_estres = st.slider("Estrés mental:", 1, 10, 5)
            f_p_sueno = st.slider("Calidad de sueño:", 1, 10, 8)
            f_p_motivacion = st.slider("Motivación:", 1, 10, 9)
            f_p_energia = st.slider("Energía vital:", 1, 10, 7)
            f_p_hambre = st.slider("Ansiedad/Hambre:", 1, 10, 5)
            f_p_recup = st.slider("Velocidad de recuperación:", 1, 10, 7)
            f_prioridad = st.selectbox("Prioridad del filtro:", ["Salud", "Estética", "Rendimiento"])
            
            enviar_maestro = st.form_submit_button("🚀 REGISTRAR EXPEDIENTE MAESTRO EN MM247")
            
        if enviar_maestro:
            if not f_nombre.strip():
                st.error("❌ El campo de Nombre Completo es obligatorio.")
            else:
                # INTEGRACIÓN: Generar ID único inmutable al dar enviar
                id_nuevo_alumno = generar_id_unico(f_nombre)
                
                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "INICIAL",
                    "ID_Alumno": id_nuevo_alumno,
                    "Nombre completo": str(f_nombre.strip().title()), "Edad": str(f_edad), "Sexo": str(f_sexo), "Estatura": str(f_estatura), "Peso actual": str(f_peso_actual),
                    "Peso objetivo": str(f_peso_obj), "Ocupación": str(f_ocupacion), "Horario laboral": str(f_horario), "Ciudad / País": str(f_ciudad), "Número de contacto": str(f_contacto), "Correo electrónico": str(f_correo),
                    "Objetivo principal": str(f_objetivo), "Tiempo deseado": str(f_tiempoloro), "Compromiso": str(f_compromiso), "Tiempo entrenando": str(f_tiempo_entrenando), "Tipo entreno": ",".join(f_tipo_entreno),
                    "Días entrenar": str(f_dias_semana), "Tiempo por sesión": str(f_tiempo_sesion), "Entrena actualmente": str(f_entrena_act), "Coach anterior": str(f_coach_antes), "Lesión actual": str(f_lesion),
                    "Cirugías": str(f_cirugias), "Dolor frecuente": str(f_dolor_frec), "Medicamentos": str(f_medica), "Condición médica": str(f_cond_diag), "Restricciones": str(f_restriccion), "Prohibido ejercicio": str(f_prohibido),
                    "Molestias movimientos": ",".join(f_molestias_mov), "Movilidad": str(f_movilidad), "Limitaciones movilidad": str(f_lim_mov), "Horas sentado": str(f_sentado), "Mala postura": str(f_postura),
                    "Parte débil": str(f_debil), "Músculo desarrollado": str(f_desarrollado), "Equilibrio": str(f_equilibrio), "Consideración física": str(f_fisico), "Acumula grasa": str(f_acumula_grasa),
                    "Facilidad músculo": str(f_gana_musculo), "Facilidad grasa": str(f_gana_grasa), "Horas sueño": str(f_horas_sueno), "Calificación descanso": str(f_calif_sueno), "Nivel de estrés": str(f_estres_diario),
                    "Comidas al día": str(f_num_comidas), "Agua diaria": str(f_litros_agua), "Alcohol": str(f_alcohol), "Fuma": str(f_fuma), "Pasos día": str(f_pasos), "Nivel de actividad": str(f_nivel_actividad),
                    "Objetivo nutricional": str(f_obj_nutri), "Alergias alimenticias": str(f_alergias), "Intolerancias": str(f_intolerancia), "Tipo alimentación": str(f_tipo_alimentacion), "Alimentos no gustan": str(f_no_gustan),
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
                            # Notificar al cliente su ID y pedirle que lo guarde
                            st.markdown(f"<div class='id-box'>✅ ¡Expediente guardado con éxito!<br>TU ID ÚNICO DE ALUMNO ES:<br><span style='font-size:30px;'>{id_nuevo_alumno}</span><br><small style='color:#333; font-weight:normal;'>Guárdalo. Lo usarás para evaluar tu progreso en el Cuestionario 2.</small></div>", unsafe_allow_html=True)
                            st.balloons()
                        else: st.error(f"Error en servidor: {response.text}")
                    except Exception as api_err: st.error(f"Fallo de comunicación: {api_err}")

# =============================================================================
# MÓDULO 2: CUESTIONARIO 2 DE REVISIÓN COMPARATIVA (ACCESO POR ID)
# =============================================================================
elif opcion == "🔄 Cuestionario 2: Revisión de Avance":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación de Seguimiento Semanal / Mensual</div>", unsafe_allow_html=True)
    
    # 1. Compuerta: Pide el ID y valida que exista en la BD para poder ingresar
    id_ingresado = st.text_input("Ingresa tu ID de Alumno para acceder a tu evaluación (Ej: MM-JUA-1234):").strip().upper()
    
    if id_ingresado:
        if not df_existente.empty and id_ingresado in df_existente["ID_Alumno"].values:
            st.success("Identidad Verificada. Completa tu registro de avances:")
            
            with st.form("form_revision_c2", clear_on_submit=True):
                st.markdown("<div class='section-header'>1. Evaluación Corporal</div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1: peso_rev = st.number_input("Peso Actual en Ayunas (kg):", min_value=30.0, value=70.0, step=0.1)
                with col2: cintura_rev = st.number_input("Contorno de Cintura (cm):", min_value=40.0, value=80.0, step=0.5)
                
                st.markdown("<div class='section-header'>2. Métricas de Progreso y Apego</div>", unsafe_allow_html=True)
                # Opción múltiple para calificar avance/retroceso oculto
                adherencia = st.radio("¿Cuál fue tu nivel de cumplimiento de dieta y macros?", ["Cumplimiento Total (Excelente)", "Cumplimiento Parcial (Aceptable)", "Cumplimiento Bajo (Mal apego)"])
                fuerza = st.radio("¿Cómo sentiste tu nivel de fuerza en los entrenamientos?", ["Incrementé los pesos o repeticiones", "Me mantuve estable", "Me sentí más débil / fatigado"])
                sueno_c2 = st.slider("Calidad del sueño (1-10):", 1, 10, 8)
                comentarios = st.text_area("Comentarios sobre dolores, dudas o sensaciones en general:")
                
                btn_enviar_c2 = st.form_submit_button("🚀 Enviar Evaluación")
                
                if btn_enviar_c2:
                    # Determinación en segundo plano (El cliente no lo ve)
                    puntos = 0
                    if adherencia == "Cumplimiento Total (Excelente)": puntos += 2
                    elif adherencia == "Cumplimiento Parcial (Aceptable)": puntos += 1
                    
                    if fuerza == "Incrementé los pesos o repeticiones": puntos += 2
                    elif fuerza == "Me mantuve estable": puntos += 1
                    
                    # Calificación ciega del estado: Verde, Amarillo, Rojo
                    estado_calculado = "AVANCE"
                    if puntos <= 2: estado_calculado = "RETROCESO"
                    elif puntos == 3: estado_calculado = "LENTO"

                    payload_c2 = {
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro": "REVISION",
                        "ID_Alumno": id_ingresado,
                        "Peso_Revision": str(peso_rev),
                        "Cintura_Revision": str(cintura_rev),
                        "Adherencia_Dieta": adherencia,
                        "Progreso_Fuerza": fuerza,
                        "Energia_SNC": str(sueno_c2),
                        "Comentarios_Evolucion": comentarios,
                        "Estado_Calculado": estado_calculado  # Oculto al usuario, lo lee el Admin
                    }
                    
                    try:
                        requests.post(WEBHOOK_URL, json=payload_c2)
                        # No hay resultados expuestos
                        st.success("✅ Evaluación registrada correctamente. Tu entrenador analizará los resultados.")
                    except Exception as e:
                        st.error(f"Error de red al enviar: {e}")
        else:
            st.error("El ID ingresado no está registrado en el sistema. Verifica mayúsculas o números.")

# =============================================================================
# MÓDULO 3: DASHBOARD ADMINISTRADOR (VISTA LISTA, COLORES, REPORTES PDF)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel de Control MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduzca la clave maestra de acceso de Administrador:", type="password")
    
    if password == "MM247_Admin":
        if df_existente.empty or len(df_existente["ID_Alumno"].dropna().unique()) == 0:
            st.warning("Aún no hay alumnos dados de alta en el sistema.")
        else:
            # Separar Base Inicial y Revisiones
            df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
            df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
            
            # Layout de Lista de Alumnos en Columnas de Streamlit
            st.markdown("### 🗂️ Registro General y Estatus de Alumnos")
            
            # Encabezado de la lista
            h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2.5, 2, 1.5])
            with h1: st.markdown("**ID Alumno**")
            with h2: st.markdown("**Nombre**")
            with h3: st.markdown("**Inicio -> Meta**")
            with h4: st.markdown("**Estatus de Avance**")
            with h5: st.markdown("**Acciones**")
            st.markdown("---")
            
            # Iterar sobre cada alumno único para crear su fila
            ids_unicos = df_c1["ID_Alumno"].replace("", pd.NA).dropna().unique()
            
            for id_al in ids_unicos:
                datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
                revs_al = df_c2[df_c2["ID_Alumno"] == id_al]
                
                # Definir color de barra por último estatus
                clase_barra = "barra-gris"
                texto_barra = "Sin Revisión (Falta C2)"
                
                if not revs_al.empty:
                    # Asumir que la última fila es la revisión más reciente
                    ultima_rev = revs_al.iloc[-1]
                    estado = ultima_rev.get("Estado_Calculado", "AVANCE")
                    if "AVANCE" in estado:
                        clase_barra = "barra-verde"
                        texto_barra = "Avance Correcto"
                    elif "LENTO" in estado:
                        clase_barra = "barra-amarilla"
                        texto_barra = "Avance Lento"
                    elif "RETROCESO" in estado:
                        clase_barra = "barra-roja"
                        texto_barra = "Retroceso"
                
                # Fila visual
                c1, c2, c3, c4, c5 = st.columns([1.5, 2, 2.5, 2, 1.5])
                with c1: st.write(f"`{id_al}`")
                with c2: st.write(str(datos_al.get("Nombre completo", "Alumno")).title())
                with c3: st.write(f"{datos_al.get('Peso actual', '--')} kg -> {datos_al.get('Peso objetivo', '--')} kg")
                with c4: 
                    st.markdown(f"<div style='font-size:12px;'>{texto_barra}</div><div class='barra-base'><div class='{clase_barra}'></div></div>", unsafe_allow_html=True)
                with c5:
                    if st.button("Ver Reporte", key=f"btn_{id_al}"):
                        st.session_state.alumno_seleccionado = id_al
            
            st.markdown("---")
            
            # SECCIÓN: DETALLE Y DESCARGA DEL REPORTE DEL ALUMNO SELECCIONADO
            if "alumno_seleccionado" in st.session_state:
                id_seleccionado = st.session_state.alumno_seleccionado
                st.markdown(f"### 📋 Detalles y Análisis del Alumno: `{id_seleccionado}`")
                
                datos_brutos = df_c1[df_c1["ID_Alumno"] == id_seleccionado].iloc[0]
                datos_normalizados = normalizar_datos_alumno(datos_brutos)
                motores = calcular_motores_automatizados(datos_normalizados)
                
                col_det1, col_det2 = st.columns(2)
                with col_det1:
                    st.markdown("**1. Resumen Cuestionario 1 (Alta)**")
                    st.write(f"- Nombre: {datos_normalizados['Nombre completo']}")
                    st.write(f"- Meta Base: {datos_normalizados['Objetivo principal']}")
                    st.write(f"- Peso Inicial: {motores['peso']} kg")
                    st.write(f"- Macros Asignados: {motores['prot']}g Prot | {motores['grasa']}g Grasa | {motores['carbs']}g Carbs")
                
                revs_seleccionado = df_c2[df_c2["ID_Alumno"] == id_seleccionado]
                with col_det2:
                    st.markdown("**2. Historial de Revisiones (Cuestionario 2)**")
                    if revs_seleccionado.empty:
                        st.write("Aún no ha llenado el Cuestionario 2.")
                    else:
                        for idx, row in revs_seleccionado.iterrows():
                            st.markdown(f"<div style='background:#f4f4f4; padding:10px; margin-bottom:5px; border-left:3px solid #111;'>Fecha: {row['Fecha']}<br>Peso Reportado: {row.get('Peso_Revision', '--')}kg<br>Fuerza: {row.get('Progreso_Fuerza', '--')}</div>", unsafe_allow_html=True)
                
                # GENERACIÓN DE PDF: 3 Hojas + 1 Hoja si existe Avance
                if st.button("🖨️ Descargar Reportes en PDF de este Alumno"):
                    try:
                        pdf = FPDF()
                        def limpiar(txt): return str(txt).replace("•", "-").encode('latin-1', 'ignore').decode('latin-1')
                        
                        # Generamos los textos base usando tus motores originales
                        t_diag = generar_propuesta_integral_mm247(datos_normalizados)
                        t_rut = generar_rutina_detallada_mm247(datos_normalizados)
                        t_diet = generar_dieta_detallada_mm247(datos_normalizados)
                        
                        # Hoja 1: Diagnóstico
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 18)
                        pdf.cell(0, 10, limpiar("HOJA 1: DIAGNOSTICO INICIAL (MM247)"), 0, 1, "C")
                        pdf.set_font("Arial", "", 10)
                        pdf.multi_cell(190, 6, limpiar(t_diag))
                        
                        # Hoja 2: Rutina
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 18)
                        pdf.cell(0, 10, limpiar("HOJA 2: RUTINA SEMANAL (MM247)"), 0, 1, "C")
                        pdf.set_font("Arial", "", 10)
                        pdf.multi_cell(190, 6, limpiar(t_rut))
                        
                        # Hoja 3: Dieta
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 18)
                        pdf.cell(0, 10, limpiar("HOJA 3: DISTRIBUCION NUTRICIONAL (MM247)"), 0, 1, "C")
                        pdf.set_font("Arial", "", 10)
                        pdf.multi_cell(190, 6, limpiar(t_diet))
                        
                        # HOJA 4 CONDICIONAL: Detalles de Avance
                        if not revs_seleccionado.empty:
                            pdf.add_page()
                            pdf.set_font("Arial", "B", 18)
                            pdf.cell(0, 10, limpiar("HOJA 4: REPORTE DE AVANCES Y METRICAS"), 0, 1, "C")
                            pdf.set_font("Arial", "", 10)
                            pdf.ln(5)
                            pdf.cell(190, 6, limpiar(f"ID del Alumno: {id_seleccionado}"), 0, 1)
                            pdf.line(10, 30, 200, 30)
                            pdf.ln(5)
                            
                            for idx, row in revs_seleccionado.iterrows():
                                pdf.set_font("Arial", "B", 11)
                                pdf.cell(190, 6, limpiar(f"Registro: {row['Fecha']}"), 0, 1)
                                pdf.set_font("Arial", "", 10)
                                pdf.cell(190, 6, limpiar(f"  - Peso registrado: {row.get('Peso_Revision')} kg"), 0, 1)
                                pdf.cell(190, 6, limpiar(f"  - Cintura: {row.get('Cintura_Revision')} cm"), 0, 1)
                                pdf.cell(190, 6, limpiar(f"  - Apego a dieta: {row.get('Adherencia_Dieta')}"), 0, 1)
                                pdf.cell(190, 6, limpiar(f"  - Progreso en fuerza: {row.get('Progreso_Fuerza')}"), 0, 1)
                                pdf.cell(190, 6, limpiar(f"  - Estado Dictaminado: {row.get('Estado_Calculado', 'ND')}"), 0, 1)
                                pdf.ln(4)
                        
                        pdf_data = pdf.output(dest='S').encode('latin-1', 'ignore')
                        st.download_button(
                            label=f"⬇️ Clic aquí para guardar Reporte_{id_seleccionado}.pdf",
                            data=pdf_data,
                            file_name=f"Reporte_MM247_{id_seleccionado}.pdf",
                            mime="application/pdf"
                        )
                    except Exception as err:
                        st.error(f"Error al compilar el PDF: {err}")
    elif password != "": 
        st.error("🔑 Clave de acceso inválida.")
