import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

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
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

st.markdown("""
    <style>
    .main-title { font-size:44px; font-weight:900; color:#111111; text-align:center; letter-spacing: -1px; margin-bottom:0px; }
    .subtitle { font-size:16px; color:#666666; text-align:center; margin-bottom:35px; text-transform: uppercase; letter-spacing: 1px;}
    .section-header { font-size:20px; font-weight:bold; color:#111111; margin-top:25px; margin-bottom:12px; border-bottom: 3px solid #111111; padding-bottom:6px; }
    .metric-card { background: #ffffff; padding: 22px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border-left: 6px solid #111111; }
    .metric-title { font-size: 13px; color: #777777; font-weight: bold; text-transform: uppercase; }
    .metric-value { font-size: 26px; color: #111111; font-weight: bold; margin-top: 4px; }
    .profile-box { background-color: #f9f9f9; padding: 18px; border-radius: 6px; border: 1px solid #eeeeee; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; font-weight: bold; height: 48px; border: none; }
    .stButton>button:hover { background-color: #333333; color: white; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Navegación MM247:", ["📝 Cuestionario Integral de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# 2. MOTOR DE NORMALIZACIÓN FLEXIBLE
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
# 3. MOTORES INTERNOS DE CÁLCULO CIENTÍFICO Y FISIOLÓGICO
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
    
    # Diagnóstico clínico basado en rangos clínicos de IMC
    if imc < 18.5:
        estado_clinico = "Bajo Peso / Déficit Nutrimental"
    elif imc < 25.0:
        estado_clinico = "Normopeso / Composición Corporal Saludable"
    elif imc < 30.0:
        estado_clinico = "Sobrepeso / Alerta de Tejido Adiposo Elevado"
    elif imc < 35.0:
        estado_clinico = "Obesidad Grado I / Riesgo Cardiovascular Moderado"
    elif imc < 40.0:
        estado_clinico = "Obesidad Grado II / Riesgo Clínico Alto"
    else:
        estado_clinico = "Obesidad Grado III (Mórbida) / Alerta Crítica Multiorgánica"
    
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
        if "Diabetes" in m['condicion']:
            analisis_clinico += "  - Ajuste Endocrino: Sincronización glucémica avanzada.\n"
        if "Rodilla" in lesion or "sentadillas" in dolor:
            analisis_clinico += "  - Ajuste de Tren Inferior: Sustituir flexión profunda por variantes en polea o prensa.\n"
        if "Espalda" in lesion or "lumbar" in dolor or "columna" in prohibido:
            analisis_clinico += "  - Protección de Columna: Cargas verticales estrictamente restringidas.\n"
    else:
        analisis_clinico += "• Diagnóstico de Salud: Sin limitaciones patológicas u óseas declaradas. Apto para sobrecarga.\n"

    estres_mental = int(datos.get('P_Estres', 5))
    sueno_eficiencia = int(datos.get('P_Sueno', 8))
    
    if estres_mental >= 8 or sueno_eficiencia <= 5:
        capacidad_snc = "CRÍTICA / RESTRIGIDA"
        volumen_recomendado = "8 a 10 Series Efectivas semanales por grupo muscular (Control de fatiga central)"
    else:
        capacidad_snc = "ESTÁNDAR EFICIENTE"
        volumen_recomendado = "12 a 14 Series Efectivas semanales por grupo muscular"

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
    res += f"⚠️ CLASIFICACIÓN BIOMECÁNICA Y RIESGOS POSTURALES:\n{analisis_postural}\n"
    res += f"📋 SINTOMATOLOGÍA CLÍNICA Y ANTECEDENTES RELEVANTES:\n{analisis_clinico}\n"
    res += f"🧠 CAPACIDAD DEL SISTEMA NERVIOSO Y RECOVERY:\n"
    res += f"   - Tolerancia SNC: {capacidad_snc}\n"
    res += f"   - Volumen de Trabajo Semanal Aconsejado: {volumen_recomendado}\n"
    res += f"========================================================================\n"
    return res

# =============================================================================
# 4. MOTOR DE RUTINAS MUTABLES (DÍAS DE DESCANSO Y EJERCICIOS VARIADOS)
# =============================================================================
def generar_rutina_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    dias = str(datos.get('Días entrenar', '4')).split()[0]
    meta = str(datos.get('Objetivo principal', '')).lower()
    lesiones = str(datos.get('Lesión actual', 'Ninguna'))
    
    # Determinar si el perfil es de Pérdida de Grasa (Oxidación/Definición) o Ganancia (Hipertrofia)
    es_deficit = "perder" in meta or "bajar" in meta or "grasa" in meta
    es_mujer = "Femenino" in m['genero']
    
    base_prensa = "Prensa de Piernas Inclinada" if "Rodilla" in lesiones else "Sentadilla Libre Profunda"
    base_pecho = "Press con Mancuernas Inclinado" if "Hombro" in lesiones else "Press de Pecho Plano"

    r = f"========================================================================\n"
    r += f"     CRONOGRAMA DE ENTRENAMIENTO ESTRUCTURADO Y MUTABLE — MM247\n"
    r += f"========================================================================\n"
    r += f"Perfil: {m['genero']} | Frecuencia: {dias} Días | Enfoque: {'Oxidación y Densidad' if es_deficit else 'Hipertrofia Mágnum'}\n\n"

    # ESCENARIO A: 3 DÍAS DE ENTRENAMIENTO
    if "3" in dias:
        if es_deficit:
            r += "📆 LUNES [DÍA 1 - FULLBODY METABÓLICO / ALTA DENSIDAD]:\n"
            r += f"   - {base_prensa}: 3 x 12-15 reps (Descanso corto: 60s)\n"
            r += f"   - {base_pecho}: 3 x 12 reps combinado con Remo invertido\n"
            r += "📆 MARTES:\n   ❌ DESCANSO METABÓLICO REPARADOR (Caminata NEAT ligera)\n\n"
            r += "📆 MIÉRCOLES [DÍA 2 - EMPOWERMENT INFERIOR + ZONA MEDIA]:\n"
            r += "   - Peso Muerto Rumano: 3 x 12 reps\n"
            r += "   - Desplantes Dinámicos: 3 x 15 pasos por lado\n"
            r += "📆 JUEVES:\n   ❌ DESCANSO ABSORCIÓN DE FATIGA CENTRAL\n\n"
            r += "📆 VIERNES [DÍA 3 - CIRCUITOS DE VACIADO DE GLUCÓGENO]:\n"
            r += "   - Flexiones + Jalón al Pecho Polea: 3 x 15 reps continuas\n"
            r += "   - Elevaciones Laterales: 4 x 20 reps buscando bombeo extremo\n"
            r += "📆 SÁBADO Y DOMINGO:\n   ❌ DESCANSO ABSOLUTO (Cero impacto sobre la columna)"
        else:
            r += "📆 LUNES [DÍA 1 - ENFOQUE EMPUJE / TENSIÓN MECÁNICA HEAVY]:\n"
            r += f"   - {base_pecho}: 4 x 6-8 reps (RIR 1 | Descanso largo: 120s)\n"
            r += "   - Press Militar con Barra: 3 x 8 reps\n"
            r += "📆 MARTES:\n   ❌ DESCANSO DE CONSTRUCCIÓN MIOFIBRILAR\n\n"
            r += "📆 MIÉRCOLES [DÍA 2 - ENFOQUE TRACCIÓN Y CADENA POSTERIOR]:\n"
            r += "   - Peso Muerto Convencional: 3 x 6 reps pesadas\n"
            r += "   - Remo Pendlay con Barra: 4 x 8 reps\n"
            r += "📆 JUEVES:\n   ❌ DESCANSO SISTEMA NERVIOSO CENTRAL\n\n"
            r += "📆 VIERNES [DÍA 3 - DESARROLLO DE TREN INFERIOR CUÁDRICEPS]:\n"
            r += f"   - {base_prensa}: 4 x 8-10 reps (Aumentando carga por serie)\n"
            r += "   - Extensiones de Cuádriceps: 3 x 12 reps al fallo técnico\n"
            r += "📆 SÁBADO Y DOMINGO:\n   ❌ DESCANSO INTEGRAL (Superávit y síntesis proteica)"

    # ESCENARIO B: 5 DÍAS DE ENTRENAMIENTO
    elif "5" in dias:
        if es_deficit:
            r += "📆 LUNES [DÍA 1 - TREN SUPERIOR COMPACTO]:\n"
            r += f"   - {base_pecho}: 4 x 12 reps | Fondos en paralelas: 3 x Máximas\n"
            r += "📆 MARTES [DÍA 2 - TREN INFERIOR ÉNFASIS GLÚTEO-FEMORAL]:\n"
            r += "   - Hip Thrust con Barra: 4 x 15 reps pesado | Curl Femoral: 4 x 12\n"
            r += "📆 MIÉRCOLES [DÍA 3 - CARDIO HIIT + CORE ACTIVO DE CONTROL]:\n"
            r += "   - Circuitos funcionales sin barra + Plancas isométricas abdominales\n"
            r += "📆 JUEVES:\n   ❌ DESCANSO OBLIGATORIO DE VACIADO ARTICULAR\n\n"
            r += "📆 VIERNES [DÍA 4 - TRACCIÓN Y HIPERTROFIA DE ESPALDA]:\n"
            r += "   - Jalón al Pecho Polea: 4 x 12 reps | Remo con Mancuerna: 3 x 10\n"
            r += "📆 SÁBADO [DÍA 5 - ESTÉTICA TOTAL: HOMBRO, BRAZO Y PANTORRILLA]:\n"
            r += "   - Elevaciones Laterales: 5 x 15 reps | Copa Tríceps: 3 x 12\n"
            r += "📆 DOMINGO:\n   ❌ DESCANSO TOTAL DE REESTRUCTURACIÓN"
        else:
            r += "📆 LUNES [DÍA 1 - HIPERTROFIA: PECHO Y TRÍCEPS]:\n"
            r += f"   - {base_pecho}: 4 x 8 reps | Press inclinado: 3 x 10 | Copa Tríceps: 4 x 12\n"
            r += "📆 MARTES [DÍA 2 - HIPERTROFIA: PIERNA COMPLETA POTENCIA]:\n"
            r += f"   - {base_prensa}: 4 x 10 reps | Sentadilla Hacka: 3 x 8 | Desplantes: 3 x 10\n"
            r += "📆 MIÉRCOLES [DÍA 3 - HIPERTROFIA: ESPALDA Y BÍCEPS]:\n"
            r += "   - Remo con Barra: 4 x 8 reps | Dominadas Supinas: 3 x Fallo | Curl de Bíceps: 4 x 10\n"
            r += "📆 JUEVES:\n   ❌ DESCANSO ESTRATÉGICO DE REGENERACIÓN ANABÓLICA\n\n"
            r += "📆 VIERNES [DÍA 4 - ESCULTURA DE HOMBRO Y DETALLES]:\n"
            r += "   - Press Militar Mancuernas: 4 x 10 reps | Pájaros Posterior: 4 x 12\n"
            r += "📆 SÁBADO [DÍA 5 - ÉNFASIS ISQUIOS, CADERA Y PANTORRILLA]:\n"
            r += "   - Peso Muerto Rumano: 4 x 8 reps pesadas | Elevación talones: 4 x 20\n"
            r += "📆 DOMINGO:\n   ❌ DESCANSO TOTAL OBLIGATORIO"

    # ESCENARIO C: 4 DÍAS DE ENTRENAMIENTO (POR DEFECTO)
    else:
        if es_deficit:
            r += "📆 LUNES [DÍA 1 - TREN SUPERIOR DENSIDAD ANTAGONISTA]:\n"
            r += f"   - {base_pecho} superserie con Remo Gironda: 4 x 12 reps cada uno.\n"
            r += "📆 MARTES [DÍA 2 - TREN INFERIOR QUEMA METABÓLICA]:\n"
            r += f"   - {base_prensa}: 4 x 15 reps (Descanso rígido de 45 segundos).\n"
            r += "📆 MIÉRCOLES:\n   ❌ DESCANSO MITAD DE SEMANA (SNC activo)\n\n"
            r += "📆 JUEVES [DÍA 3 - TORSO ENFOQUE CONDICIONAMIENTO Y BRAZOS]:\n"
            r += "   - Press Militar + Fondos + Curl: 3 rondas sin descanso continuo.\n"
            r += "📆 VIERNES [DÍA 4 - PIERNA DE DETALLE FISIOLÓGICO]:\n"
            r += "   - Extensión de Cuádriceps + Zancadas estáticas: 4 x 12 reps.\n"
            r += "📆 SÁBADO Y DOMINGO:\n   ❌ DESCANSO DE RESET SISTÉMICO"
        else:
            r += "📆 LUNES [DÍA 1 - DIVISION TORSO COMPLETO F1]:\n"
            r += f"   - {base_pecho}: 4 x 8 reps | Remo con Barra Pecho: 4 x 8 reps pesadas.\n"
            r += "📆 MARTES [DÍA 2 - DIVISION PIERNA FUERZA F1]:\n"
            r += f"   - {base_prensa} o Sentadilla Pesada: 4 x 6-8 reps netas.\n"
            r += "📆 MIÉRCOLES:\n   ❌ DESCANSO CRUCIAL (Permite hipertrofia miofibrilar)\n\n"
            r += "📆 JUEVES [DÍA 3 - TORSO HIPERTROFIA EXTREMA F2]:\n"
            r += "   - Cruces en Poleas: 4 x 12 reps | Jalones al pecho supinos: 4 x 10.\n"
            r += "📆 VIERNES [DÍA 4 - PIERNA DETALLE EN MÁQUINAS F2]:\n"
            r += "   - Curl Femoral Tumbado: 4 x 12 reps | Prensa Inclinada: 3 x 15 reps bomba.\n"
            r += "📆 SÁBADO Y DOMINGO:\n   ❌ DESCANSO COMPLETO (Recuperación estructural profunda)"
        
    return r

# =============================================================================
# 5. MOTOR NUTRICIONAL: PORCIONES AUTOMÁTICAS EN GRAMOS REALES
# =============================================================================
def generar_dieta_detallada_mm247(datos):
    m = calcular_motores_automatizados(datos)
    
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

    if not prots: prots = ["Pechuga de Pollo"]
    if not carbs: carbs = ["Arroz Blanco"]
    if not grasas: grasas = ["Aguacate"]
    if not frutas: frutas = ["Plátano"]
    if not verds: verds = ["Brócoli"]

    p_comida = round(m['prot'] / 4, 1)
    g_comida = round(m['grasa'] / 4, 1)
    c_comida = round(m['carbs'] / 4, 1)
    cal_comida = round(m['cals'] / 4, 0)

    g_alimento_prot = round(p_comida * 4.35)
    g_alimento_carb = round(c_comida * 4.0)
    g_alimento_grasa = round(g_comida * 6.66)

    d = f"========================================================================\n"
    d += f"     ESTRATEGIA NUTRICIONAL DE ALTA PRECISIÓN MM247 — DIETA AJUSTADA\n"
    d += f"========================================================================\n"
    d += f"🎯 OBJETIVO DIARIO EXACTO (2g Proteína / 1g Grasa por Kg de peso):\n"
    d += f"   🔥 Energía Total: {m['cals']} kcal\n"
    d += f"   💪 Proteínas: {m['prot']}g  |  🍞 Carbohidratos: {m['carbs']}g  |  🥑 Grasas: {m['grasa']}g\n\n"
    d += f"🥦 FUENTES SELECCIONADAS DE TUS RESPUESTAS:\n"
    d += f"   - Fuentes Proteicas: {', '.join(prots)}\n"
    d += f"   - Fuentes de Carbohidrato: {', '.join(carbs)}\n"
    d += f"   - Fuentes de Grasas: {', '.join(grasas)}\n\n"
    
    d += f"• COMIDA 1 [Desayuno]: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - {prots[0]}: {g_alimento_prot} gramos (Pesado en Crudo)\n"
    d += f"  - {carbs[0]}: {g_alimento_carb} gramos (Pesado ya Cocinado)\n"
    d += f"  - {frutas[0]}: 1 pieza mediana o 120 gramos netos\n\n"
    
    d += f"• COMIDA 2 [Almuerzo]: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - {prots[-1]}: {g_alimento_prot} gramos (Pesado en Crudo)\n"
    d += f"  - {carbs[-1]}: {g_alimento_carb} gramos (Pesado ya Cocinado)\n"
    d += f"  - {grasas[0]}: {g_alimento_grasa} gramos (Pulpa limpia de aguacate)\n\n"
    
    d += f"• COMIDA 3 [Merienda]: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - {prots[0]}: {g_alimento_prot} gramos (Pesado en Crudo)\n"
    d += f"  - {carbs[0]}: {g_alimento_carb} gramos (Pesado ya Cocinado)\n"
    d += f"  - {frutas[-1]}: 1 pieza mediana o 120 gramos netos\n\n"
    
    d += f"• COMIDA 4 [Cena]: {cal_comida} kcal | {p_comida}g Prot | {c_comida}g Carbs | {g_comida}g Grasa\n"
    d += f"  - {prots[0]}: {g_alimento_prot} gramos (Pesado en Crudo)\n"
    d += f"  - {grasas[-1]}: {g_alimento_grasa} gramos (Pulpa limpia de aguacate)\n"
    d += f"  - Ensalada Libre Acompañante: Mínimo 150 gramos de ({', '.join(verds)})\n"
    d += f"========================================================================\n"
    return d

# =============================================================================
# MÓDULO 1: FORMULARIO MAESTRO INTEGRAL DE EVALUACIÓN (VISTA DEL CLIENTE)
# =============================================================================
if opcion == "📝 Cuestionario Integral de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación de Cargas, Historial Clínico y Selección de Alimentos</div>", unsafe_allow_html=True)
    
    with st.form("formulario_maestro_mm247_cerrado", clear_on_submit=True):
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
            f_dolor_frec = st.selectbox("¿Siete molestias agudas al ejecutar cargas?", ["No", "Sí, al hacer presses", "Sí, al hacer sentadillas", "Sí, dolor lumbar constante"])
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
                            st.success("✅ ¡Expediente guardado con éxito!")
                            st.balloons()
                        else: st.error(f"Error en servidor: {response.text}")
                    except Exception as api_err: st.error(f"Fallo de comunicación: {api_err}")

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
            # --- INTERFAZ DINÁMICA Y GRÁFICOS VISUALES ---
            total_alumnos = len(df_existente)
            col_meta_key = next((c for c in ["Objetivo principal", "Objetivoprincipal", "Objetivo"] if c in df_existente.columns), "")
            
            if col_meta_key:
                perdida_count = df_existente[col_meta_key].astype(str).str.contains('Perder|Bajar|Déficit|grasa', case=False, na=False).sum()
                masa_count = df_existente[col_meta_key].astype(str).str.contains('Ganar|Subir|Volumen|muscular', case=False, na=False).sum()
            else:
                perdida_count, masa_count = 0, 0

            st.markdown("### 📈 Métricas Estatales de Carga Activa")
            k1, k2, k3 = st.columns(3)
            with k1: st.markdown(f"<div class='metric-card'><div class='metric-title'>Expedientes Registrados</div><div class='metric-value'>{total_alumnos} Alumnos Activos</div></div>", unsafe_allow_html=True)
            with k2: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Oxidación de Grasa</div><div class='metric-value'>{perdida_count} Alumnos</div></div>", unsafe_allow_html=True)
            with k3: st.markdown(f"<div class='metric-card'><div class='metric-title'>En Hipertrofia Miofibrilar</div><div class='metric-value'>{masa_count} Alumnos</div></div>", unsafe_allow_html=True)
            
            # Sección de Analíticas Gráficas
            st.markdown("<br>", unsafe_allow_html=True)
            col_chart1, col_chart2 = st.columns([1, 1])
            with col_chart1:
                if col_meta_key and not df_existente[col_meta_key].empty:
                    st.markdown("#### 🎯 Distribución de Objetivos")
                    dist_obj = df_existente[col_meta_key].value_counts()
                    st.bar_chart(dist_obj, color="#111111")
            with col_chart2:
                col_sex_key = next((c for c in ["Sexo", "Género", "Genero"] if c in df_existente.columns), "")
                if col_sex_key and not df_existente[col_sex_key].empty:
                    st.markdown("#### 👥 Demografía por Sexo")
                    dist_sex = df_existente[col_sex_key].value_counts()
                    st.bar_chart(dist_sex, color="#333333")

            st.markdown("---")
            st.markdown("### 🗃️ Registro General de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            col_nombre_key = next((c for c in ["Nombre completo", "Nombre", "Alumno"] if c in df_existente.columns), df_existente.columns[1])
            lista_alumnos = df_existente[col_nombre_key].dropna().unique()
            
            st.markdown("### 🛠️ Constructor de Prescripciones Estructurales")
            alumno_sel = st.selectbox("Seleccione el expediente del alumno a planificar:", lista_alumnos)
            
            idx_alumno = df_existente[df_existente[col_nombre_key] == alumno_sel].index[0]
            datos_alumno_raw = df_existente.loc[idx_alumno]
            
            datos_alumno = normalizar_datos_alumno(datos_alumno_raw)
            nombre_display = str(datos_alumno['Nombre completo']).title()
            
            # Tarjeta de Datos Rápidos del Alumno Seleccionado
            m_previo = calcular_motores_automatizados(datos_alumno)
            st.markdown(f"""
            <div class='profile-box'>
                <strong>Ficha Rápida:</strong> {nombre_display} | 
                <strong>IMC Base:</strong> {m_previo['imc']} ({m_previo['estado_clinico']}) | 
                <strong>Meta Electa:</strong> {datos_alumno['Objetivo principal']} | 
                <strong>Frecuencia Elegida:</strong> {datos_alumno['Días entrenar']}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            if "alumno_actual" not in st.session_state or st.session_state.alumno_actual != alumno_sel:
                st.session_state.alumno_actual = alumno_sel
                
                db_propuesta = str(datos_alumno_raw.get("Propuesta General", "")).strip()
                db_rutina = str(datos_alumno_raw.get("Rutina Biomecánica", "")).strip()
                db_balance = str(datos_alumno_raw.get("Balance Energético", "")).strip()
                
                st.session_state.v_propuesta = db_propuesta if db_propuesta and db_propuesta != "nan" else generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = db_rutina if db_rutina and db_rutina != "nan" else generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = db_balance if db_balance and db_balance != "nan" else generar_dieta_detallada_mm247(datos_alumno)

            if st.button("🚀 Forzar Re-Cálculo de Automatización Dinámica (IMC y Rutina Mutada)"):
                st.session_state.v_propuesta = generar_propuesta_integral_mm247(datos_alumno)
                st.session_state.v_rutina = generar_rutina_detallada_mm247(datos_alumno)
                st.session_state.v_balance = generar_dieta_detallada_mm247(datos_alumno)
                st.rerun()

            st.markdown("---")
            with st.form("prescripcion_maestra_form_mm247"):
                propuesta = st.text_area("🩺 HOJA 1: Informe Diagnóstico Avanzado (Clínico e IMC):", value=st.session_state.v_propuesta, height=280)
                rutina = st.text_area("🏋️ HOJA 2: Programación Semanal Específica e Inteligente:", value=st.session_state.v_rutina, height=350)
                balance = st.text_area("🥗 HOJA 3: Plan Nutricional Ajustado Exacto con Gramajes:", value=st.session_state.v_balance, height=350)
                
                guardar_changes = st.form_submit_button("💾 Guardar y Sincronizar Plan Estructural con Google Sheets")
                if guardar_changes:
                    payload_edit = {"Action": "UPDATE", "RowIndex": int(idx_alumno + 2)}
                    for k in datos_alumno_raw.keys(): payload_edit[k] = str(datos_alumno_raw[k])
                    payload_edit["Propuesta General"] = propuesta
                    payload_edit["Balance Energético"] = balance
                    payload_edit["Rutina Biomecánica"] = rutina
                    
                    with st.spinner("Modificando registros en la base central..."):
                        try:
                            requests.post(WEBHOOK_URL, json=payload_edit)
                            st.session_state.v_propuesta = propuesta
                            st.session_state.v_rutina = rutina
                            st.session_state.v_balance = balance
                            st.success("✅ ¡Plan maestro sincronizado con éxito!")
                        except Exception as e_save: st.error(f"Fallo de guardado: {e_save}")
            
            if st.button("🖨️ Compilar Plan Maestro en PDF"):
                try:
                    pdf = FPDF()
                    def limpiar_texto(txt): return str(txt).replace("•", "-").replace("–", "-").replace("—", "-").replace("º"," ").encode('latin-1', 'ignore').decode('latin-1')

                    # HOJA 1
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 38, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 24)
                    pdf.cell(0, 12, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.ln(18)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 6, limpiar_texto(st.session_state.v_propuesta))

                    # HOJA 2
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
                    pdf.ln(16)
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(190, 5.5, limpiar_texto(st.session_state.v_rutina))

                    # HOJA 3
                    pdf.add_page()
                    pdf.set_fill_color(20, 20, 20)
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.cell(0, 10, limpiar_texto("MINDMUSCLE247"), ln=True, align="C")
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
