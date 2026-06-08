# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA DE ADHERENCIA
   
   VERSIÓN 3.0 — REDISEÑO LIGHT MODE, AVATARES 3D Y AUDITORÍA CLÍNICA
================================================================================
"""

import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests
import uuid

# =============================================================================
# 0. CONFIGURACIÓN CENTRAL (CONFIG)
# =============================================================================
CONFIG = {
    "page_title": "MINDMUSCLE247",
    "page_icon": "🟩",
    "webhook_url": "https://script.google.com/macros/s/AKfycbx5vDCKmqpe-vsZ2fan0ZQoesLjajIHHHXHOZLtG7-w6-ts3uUl1WkZVHnPnn0F3Cbn/exec",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas",
    "admin_password": "MM247_Admin",
    "total_misiones": 6,
    "factores_actividad": {
        "Sedentario":            1.20,
        "Poco activo":           1.375,
        "Moderadamente activo":  1.55,
        "Muy activo":            1.725,
    },
    "rutinas": {
        "Empuje": {
            "sin_lesion": [
                ("Press Banca con Barra", "4", "6-8", "90s"),
                ("Press Inclinado con Mancuernas", "3", "10-12", "60s"),
                ("Aperturas en Polea Alta", "3", "15-20", "45s"),
                ("Press Militar con Barra", "3", "8-10", "90s"),
                ("Elevaciones Laterales", "4", "12-15", "45s"),
            ],
            "con_lesion": [
                ("Press en Máquina (neutro)", "4", "10-12", "90s"),
                ("Aperturas en Polea Media", "3", "12-15", "60s"),
                ("Press Hombro en Máquina", "3", "12-15", "60s"),
                ("Elevaciones Laterales Cable", "4", "15-20", "45s"),
            ],
        },
        "Tracción": {
            "sin_lesion": [
                ("Dominadas o Jalón al Pecho", "4", "6-10", "90s"),
                ("Remo con Barra", "4", "8-10", "90s"),
                ("Remo en Polea Baja", "3", "12-15", "60s"),
                ("Curl Bíceps con Barra", "3", "10-12", "60s"),
            ],
            "con_lesion": [
                ("Jalón al Pecho Agarre Neutro", "4", "10-12", "90s"),
                ("Remo en Máquina", "3", "12-15", "60s"),
                ("Polea Alta Agarre Neutro", "3", "15-20", "45s"),
                ("Curl Martillo Mancuernas", "3", "12-15", "60s"),
            ],
        },
        "Pierna": {
            "sin_lesion": [
                ("Sentadilla con Barra", "4", "6-8", "120s"),
                ("Prensa de Pierna", "3", "10-12", "90s"),
                ("Extensión de Cuádriceps", "3", "15-20", "60s"),
                ("Curl Femoral", "3", "12-15", "60s"),
                ("Pantorrillas de Pie", "4", "15-20", "45s"),
            ],
            "con_lesion": [
                ("Prensa de Pierna Rango Parcial", "4", "12-15", "90s"),
                ("Extensión Cuádriceps (peso bajo)", "3", "15-20", "60s"),
                ("Hip Thrust con Barra", "4", "10-12", "90s"),
                ("Curl Femoral Tumbado", "3", "15-20", "60s"),
            ],
        },
        "Brazo/Full": {
            "sin_lesion": [
                ("Curl Bíceps con Barra EZ", "4", "10-12", "60s"),
                ("Extensión Tríceps Polea", "4", "12-15", "60s"),
                ("Curl Predicador", "3", "12-15", "45s"),
                ("Press Francés", "3", "10-12", "60s"),
                ("Plancha Abdominal", "3", "30-45s", "45s"),
            ],
            "con_lesion": [
                ("Curl Martillo Cable", "4", "12-15", "60s"),
                ("Tríceps Polea Agarre Neutro", "4", "15-20", "60s"),
                ("Curl Concentrado", "3", "15-20", "45s"),
                ("Extensión Tríceps Mancuerna", "3", "12-15", "60s"),
            ],
        },
    },
}

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(
    page_title=CONFIG["page_title"],
    page_icon=CONFIG["page_icon"],
    layout="wide"
)

# =============================================================================
# 2. ESTILOS CSS (DISEÑO LIGHT MODE + VERDE ESMERALDA)
# =============================================================================
st.markdown("""
<style>
/* Fondo principal */
.stApp { background-color: #F8F9FA; color: #333333; }

/* Títulos y Subtítulos */
.main-title { 
    font-size: 50px; font-weight: 800; 
    color: #2C3E50;
    text-align: center; letter-spacing: 1px; margin-bottom: 0px; text-transform: uppercase; 
}
.subtitle { font-size: 16px; color: #7F8C8D; text-align: center; margin-bottom: 35px;
            text-transform: uppercase; letter-spacing: 3px; }

/* Encabezados de sección */
.section-header { 
    font-size: 20px; font-weight: 700; color: #50C878; margin-top: 30px;
    margin-bottom: 15px; border-bottom: 2px solid #E5E7EB;
    padding-bottom: 5px; text-transform: uppercase; 
}

/* Panel de Formulario */
div[data-testid="stForm"] { 
    background: #FFFFFF; padding: 30px; border-radius: 16px;
    border: 1px solid #E5E7EB; box-shadow: 0 4px 20px rgba(0,0,0,0.05); 
}

/* Tarjetas de Métricas (Metric Cards) */
.metric-card {
    background-color: #FFFFFF; padding: 20px; border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #50C878;
    margin-bottom: 20px; border-top: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB; border-bottom: 1px solid #E5E7EB;
}

/* Caja de ID (Verde Esmeralda) */
.id-box { 
    background: linear-gradient(135deg, #50C878 0%, #3CB371 100%);
    border-left: 5px solid #2E8B57; padding: 25px; border-radius: 12px;
    color: #FFFFFF; text-align: center; font-weight: bold; margin-top: 20px; 
}

/* Botones con Degradado Esmeralda */
div.stButton > button, div[data-testid="stForm"] button {
    background: linear-gradient(90deg, #50C878 0%, #3CB371 100%);
    color: white; width: 100%; border-radius: 8px; font-weight: 700;
    height: 50px; border: none; text-transform: uppercase; letter-spacing: 0.5px;
    transition: all 0.3s ease;
}
div.stButton > button:hover, div[data-testid="stForm"] button:hover {
    transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 8px 20px rgba(80, 200, 120, 0.4);
    color: white;
}

/* Barras de Progreso y Medidores */
.barra-base { height:10px; border-radius:5px; width:100%; background:#E5E7EB; margin-top:5px; }
.barra-verde { background:#50C878; height:10px; border-radius:5px; box-shadow:0 0 10px rgba(80, 200, 120, 0.5); }
.barra-roja  { background:#EF4444; height:10px; border-radius:5px; box-shadow:0 0 10px rgba(239, 68, 68, 0.5); }
.barra-amarilla { background:#F59E0B; height:10px; border-radius:5px; box-shadow:0 0 10px rgba(245, 158, 11, 0.5); }
.barra-gris  { background:#94A3B8; height:10px; border-radius:5px; }
.stProgress > div > div > div > div { background-color: #50C878; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { background-color:#FFFFFF; color:#7F8C8D; border-radius:8px 8px 0 0; border: 1px solid #E5E7EB; border-bottom: none; }
.stTabs [aria-selected="true"] { background-color:#50C878 !important; color:#FFFFFF !important; font-weight:bold; border-color: #50C878; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2.5 LÓGICA DE AVATARES 3D (READY PLAYER ME)
# ==========================================
def obtener_avatar_url(estatus):
    """
    Retorna la URL del avatar 3D dependiendo del estatus del alumno.
    (Utilizamos un ID base que puedes sustituir más adelante por uno dinámico)
    """
    base_url = "https://models.readyplayer.me/648b28f7f9037c9521369ec9.png"
    
    if estatus == "AVANCE":
        # Pose de victoria, cámara cercana, sonrisa
        return f"{base_url}?pose=A&camera=portrait&blendShape=smile"
    elif estatus == "RETROCESO":
        # Pose neutral/reposo, cuerpo entero para análisis
        return f"{base_url}?pose=T&camera=fullbody"
    else:
        # Estándar para Lento/Mantenimiento
        return f"{base_url}?camera=portrait"

# =============================================================================
# 3. CAPA DE DATOS — cacheada para no hacer HTTP en cada recarga
# =============================================================================
@st.cache_data(ttl=60)
def cargar_base_datos() -> pd.DataFrame:
    try:
        url = f"{CONFIG['sheet_url']}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        if "ID_Alumno"    not in df.columns: df["ID_Alumno"]    = ""
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = "INICIAL"
        return df
    except Exception:
        return pd.DataFrame()

def generar_id_unico(nombre: str) -> str:
    iniciales = "".join([p[0].upper() for p in str(nombre).strip().split() if p])[:3]
    if not iniciales:
        iniciales = "MM"
    anio  = datetime.datetime.now().year
    sufijo = str(uuid.uuid4().hex)[:6].upper()
    return f"MM247-{anio}-{iniciales}-{sufijo}"

# =============================================================================
# 4. MOTOR DE NORMALIZACIÓN
# =============================================================================
def normalizar_datos_alumno(datos_raw: pd.Series) -> dict:
    def buscar(keywords: list, defecto: str = "", idx_respaldo: int = None) -> str:
        for col in datos_raw.index:
            col_l = str(col).lower().strip()
            for kw in keywords:
                if kw.lower() in col_l:
                    val = datos_raw[col]
                    if pd.notna(val) and str(val).strip() not in ("", "nan"):
                        return str(val).strip()
        if idx_respaldo is not None and idx_respaldo < len(datos_raw):
            val = datos_raw.iloc[idx_respaldo]
            if pd.notna(val) and str(val).strip() not in ("", "nan"):
                return str(val).strip()
        return defecto

    return {
        "Nombre completo":    buscar(["nombre", "alumno", "completo"],         "Atleta",                1),
        "Edad":               buscar(["edad", "años"],                          "25",                    2),
        "Sexo":               buscar(["sexo", "género", "genero"],              "Masculino",             3),
        "Estatura":           buscar(["estatura", "altura", "cm"],              "175",                   4),
        "Peso actual":        buscar(["peso actual", "peso corporal", "kg"],    "80",                    5),
        "Peso objetivo":      buscar(["peso objetivo", "meta"],                 "75",                    6),
        "Nivel de actividad": buscar(["nivel de actividad", "neat", "actividad"], "Moderadamente activo"),
        "Objetivo principal": buscar(["objetivo principal", "meta", "objetivo"],"Recomposición corporal"),
        "Condición médica":   buscar(["condición médica", "patología"],         "Ninguna"),
        "Tiempo entrenando":  buscar(["tiempo entrenando", "experiencia"],      "Menos de 6 meses"),
        "Lesión actual":      buscar(["lesión", "lesion", "lastimado"],         "Ninguna"),
        "Mala postura":       buscar(["postura", "desviación", "hombros"],      "No"),
        "Prohibido ejercicio":buscar(["prohibido", "restricción", "axial"],     "No"),
        "Días entrenar":      buscar(["días entrenar", "semana cuántos", "dias"],"4 días por semana"),
        "Tiempo por sesión":  buscar(["tiempo por sesión", "disponibilidad"],   "60 minutos"),
        "Compromiso":         buscar(["compromiso"],                            "Alto"),
        "Menu_Proteinas":     buscar(["menu_proteinas", "proteínas", "proteinas"], "Pechuga de Pollo"),
        "Menu_Carbohidratos": buscar(["menu_carbohidratos", "carbs"],           "Arroz Blanco"),
        "Menu_Grasas":        buscar(["menu_grasas", "grasas"],                 "Aguacate"),
        "Menu_Frutas":        buscar(["menu_frutas", "frutas"],                 "Manzana"),
        "Menu_Verduras":      buscar(["menu_verduras", "verduras"],             "Brócoli"),
    }

# =============================================================================
# 5. MOTOR METABÓLICO
# =============================================================================
def _parse_float(valor: str, defecto: float) -> float:
    try:
        return float(str(valor).replace("kg", "").replace("cm", "").replace("años", "").strip().split()[0])
    except Exception:
        return defecto

def calcular_metabolismo(datos: dict) -> dict:
    peso     = _parse_float(datos.get("Peso actual",        "80"),  80.0)
    estatura = _parse_float(datos.get("Estatura",           "175"), 175.0)
    edad     = _parse_float(datos.get("Edad",               "25"),  25.0)
    genero   = str(datos.get("Sexo", "Masculino"))
    actividad= str(datos.get("Nivel de actividad", "Moderadamente activo"))
    meta     = str(datos.get("Objetivo principal", "Recomposición corporal"))

    imc = peso / ((estatura / 100) ** 2) if estatura > 0 else 0.0

    if "Masculino" in genero:
        tmb = 66.473 + (13.751 * peso) + (5.0033 * estatura) - (6.755 * edad)
    else:
        tmb = 655.095 + (9.5634 * peso) + (1.8496 * estatura) - (4.6756 * edad)

    factor = CONFIG["factores_actividad"].get(actividad, 1.55)
    tdee   = tmb * factor

    if any(k in meta for k in ("Perder", "Bajar", "grasa", "Déficit")):
        cals        = tdee - 400
        balance_str = "Déficit Calórico (-400 kcal)"
    elif any(k in meta for k in ("Ganar", "Subir", "Volumen", "muscular")):
        cals        = tdee + 300
        balance_str = "Superávit Calórico (+300 kcal)"
    elif "fuerza" in meta.lower():
        cals        = tdee + 200
        balance_str = "Superávit Moderado (+200 kcal)"
    else:
        cals        = tdee
        balance_str = "Normocalórico (mantenimiento)"

    prot  = round(peso * 2.0, 1)
    grasa = round(peso * 1.0, 1)
    cals_restantes = cals - (prot * 4) - (grasa * 9)
    carbs = round(max(cals_restantes / 4, 50.0), 1)

    return {
        "imc":         round(imc, 1),
        "tmb":         round(tmb, 0),
        "tdee":        round(tdee, 0),
        "cals":        round(cals, 0),
        "prot":        prot,
        "grasa":       grasa,
        "carbs":       carbs,
        "balance_str": balance_str,
        "factor":      factor,
        "edad":        edad,
        "genero":      genero,
        "peso":        peso,
        "estatura":    estatura,
    }

# =============================================================================
# 6. MOTOR DE PDF (ACTUALIZADO A DISEÑO ESMERALDA Y HOJA 4 CLÍNICA)
# =============================================================================
def _limpiar(texto: str) -> str:
    return str(texto).encode("latin-1", "replace").decode("latin-1")

def _tiene_lesion(norm: dict) -> bool:
    lesion = norm.get("Lesión actual", "Ninguna").lower()
    prohibido = norm.get("Prohibido ejercicio", "No").lower()
    return lesion != "ninguna" or prohibido != "no"

def _dias_entrenamiento(norm: dict) -> int:
    try:
        return int(str(norm.get("Días entrenar", "4")).strip()[0])
    except Exception:
        return 4

def generar_pdf_mm247(norm: dict, mot: dict, revs_df: pd.DataFrame, id_al: str) -> bytes:
    pdf = FPDF("P", "mm", "Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    con_lesion = _tiene_lesion(norm)
    num_dias   = _dias_entrenamiento(norm)

    def header(titulo: str):
        pdf.add_page()
        pdf.set_fill_color(80, 200, 120) # Verde Esmeralda
        pdf.rect(0, 0, 216, 30, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 24)
        pdf.set_xy(10, 8);  pdf.cell(100, 10, "MIND MUSCLE 247",  0, 0, "L")
        pdf.set_font("Arial", "B", 12)
        pdf.set_xy(160, 12); pdf.cell(45, 10, "CONFIDENCIAL", 0, 0, "R")
        pdf.set_text_color(240, 255, 240)
        pdf.set_font("Arial", "", 10)
        pdf.set_xy(10, 18);  pdf.cell(100, 10, f"ID: {id_al}", 0, 0, "L")
        pdf.set_text_color(44, 62, 80) # Gris Oscuro
        pdf.set_font("Arial", "B", 14)
        pdf.set_xy(10, 35);  pdf.cell(196, 10, _limpiar(titulo), 0, 1, "C")
        pdf.set_draw_color(229, 231, 235); pdf.set_line_width(0.5)
        pdf.line(10, 45, 206, 45); pdf.ln(10)

    def fila_dato(label: str, valor: str, col_w: int = 98):
        pdf.set_font("Arial", "B", 10); pdf.cell(col_w, 7, _limpiar(label), 1, 0, "L")
        pdf.set_font("Arial", "",  10); pdf.cell(col_w, 7, _limpiar(valor), 1, 1, "L")

    # --- HOJA 1 ---
    header("HOJA 1: PERFIL CLÍNICO Y DIAGNÓSTICO")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("1. DATOS GENERALES"), 0, 1)
    fila_dato("Cliente",         norm["Nombre completo"])
    fila_dato("Edad / Sexo",     f"{int(mot['edad'])} años / {mot['genero']}")
    fila_dato("Estatura / Peso", f"{mot['estatura']} cm / {mot['peso']} kg")
    fila_dato("IMC calculado",   f"{mot['imc']}  |  Objetivo: {norm['Objetivo principal']}")
    fila_dato("Peso objetivo",   norm.get("Peso objetivo", "--"))
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("2. DISPONIBILIDAD LOGÍSTICA"), 0, 1)
    fila_dato("Días de entrenamiento", norm["Días entrenar"])
    fila_dato("Tiempo por sesión",     norm["Tiempo por sesión"])
    fila_dato("Nivel de compromiso",   str(norm["Compromiso"]))
    fila_dato("Nivel de actividad",    norm["Nivel de actividad"])
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(239, 68, 68) # Rojo suave para alertas
    pdf.cell(0, 10, _limpiar("3. ALERTAS BIOMECÁNICAS"), 0, 1)
    pdf.set_fill_color(254, 242, 242); pdf.set_draw_color(239, 68, 68)
    pdf.rect(10, pdf.get_y(), 196, 32, "FD")
    pdf.set_xy(15, pdf.get_y() + 4)
    pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 10)
    for linea in [
        f"Lesión / Condición : {norm['Lesión actual']} / {norm['Condición médica']}",
        f"Restricción de mov.: {norm['Prohibido ejercicio']}",
        f"Corrección postural: {norm['Mala postura']}",
        f"Protocolo aplicado : {'ADAPTADO (sin carga axial / rango reducido)' if con_lesion else 'ESTÁNDAR (sin restricciones)'}",
    ]:
        pdf.set_x(15); pdf.cell(0, 6, _limpiar(f"• {linea}"), 0, 1)

    # --- HOJA 2 ---
    header("HOJA 2: PROGRAMACIÓN SEMANAL DE ENTRENAMIENTO")
    estado_protocolo = "ADAPTADO" if con_lesion else "ESTÁNDAR"
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, _limpiar(f"Estructura: {norm['Días entrenar']}  |  Protocolo: {estado_protocolo}"), 0, 1)
    pdf.ln(5)

    bloques = ["Empuje", "Tracción", "Pierna", "Brazo/Full"]
    nombres_bloque = [
        "DÍA 1 — EMPUJE (Pecho · Hombro · Tríceps)",
        "DÍA 2 — TRACCIÓN (Espalda · Bíceps)",
        "DÍA 3 — PIERNA (Cuádriceps · Femoral · Glúteo)",
        "DÍA 4 — BRAZO / FULL BODY",
    ]
    modo = "con_lesion" if con_lesion else "sin_lesion"

    for i, bloque in enumerate(bloques[:num_dias]):
        ejercicios = CONFIG["rutinas"][bloque][modo]
        pdf.set_fill_color(80, 200, 120); pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(196, 8, _limpiar(nombres_bloque[i]), 0, 1, "L", fill=True)
        pdf.set_fill_color(243, 244, 246); pdf.set_text_color(51, 51, 51)
        for txt, w in [("EJERCICIO", 90), ("SERIES", 26), ("REPS", 40), ("DESCANSO", 40)]:
            pdf.cell(w, 7, _limpiar(txt), 1, 0, "C", fill=True)
        pdf.ln()
        pdf.set_font("Arial", "", 10)
        for ej, series, reps, desc in ejercicios:
            pdf.cell(90, 7, _limpiar(ej),     1, 0, "L")
            pdf.cell(26, 7, _limpiar(series), 1, 0, "C")
            pdf.cell(40, 7, _limpiar(reps),   1, 0, "C")
            pdf.cell(40, 7, _limpiar(desc),   1, 1, "C")
        pdf.ln(6)

    # --- HOJA 3 ---
    header("HOJA 3: PROTOCOLO NUTRICIONAL")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("1. MÉTRICAS METABÓLICAS"), 0, 1)
    fila_dato("TMB (Harris-Benedict)",         f"{mot['tmb']} kcal/día")
    fila_dato(f"TDEE (factor actividad {mot['factor']})", f"{mot['tdee']} kcal/día")
    fila_dato("Balance objetivo",              mot["balance_str"])
    fila_dato("Calorías diarias prescritas",   f"{mot['cals']} kcal")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("2. MACRONUTRIENTES DIARIOS (Regla MM247: 2g Prot · 1g Grasa / kg)"), 0, 1)
    pdf.set_fill_color(80, 200, 120); pdf.set_text_color(255, 255, 255)
    for h, w in [("PROTEÍNA", 49), ("CARBOHIDRATOS", 49), ("GRASAS", 49), ("CALORÍAS", 49)]:
        pdf.cell(w, 8, _limpiar(h), 1, 0, "C", fill=True)
    pdf.ln()
    pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "B", 13)
    for val, w in [(f"{mot['prot']}g", 49), (f"{mot['carbs']}g", 49),
                   (f"{mot['grasa']}g", 49), (f"{mot['cals']} kcal", 49)]:
        pdf.cell(w, 10, _limpiar(val), 1, 0, "C")
    pdf.ln(12)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("3. DISTRIBUCIÓN EN 4 TOMAS DIARIAS"), 0, 1)
    comidas = ["COMIDA 1 — Desayuno", "COMIDA 2 — Post-Entreno",
               "COMIDA 3 — Comida Fuerte", "COMIDA 4 — Cena"]
    p_c = round(mot["prot"]  / 4, 1)
    c_c = round(mot["carbs"] / 4, 1)
    g_c = round(mot["grasa"] / 4, 1)
    k_c = round(mot["cals"]  / 4, 0)

    for comida in comidas:
        pdf.set_fill_color(243, 244, 246); pdf.set_font("Arial", "B", 11)
        pdf.cell(196, 8, _limpiar(comida), 0, 1, "L", fill=True)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, _limpiar(f"  {k_c} kcal  |  {p_c}g Prot  |  {c_c}g Carbs  |  {g_c}g Grasa"), 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, _limpiar(f"  Proteína  : {norm['Menu_Proteinas']}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"  Carbs     : {norm['Menu_Carbohidratos']}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"  Grasas    : {norm['Menu_Grasas']}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"  Verduras  : {norm['Menu_Verduras']}"), 0, 1)
        pdf.ln(3)

    # --- HOJA 4 (AMPLIADA Y ESPECIALIZADA) ---
    if len(revs_df) > 0:
        header("HOJA 4: AUDITORÍA CLÍNICA Y PLAN DE ACCIÓN")
        ult = revs_df.iloc[-1]
        
        try: peso_actual = float(str(ult.get("Peso_Revision", mot["peso"])).replace(",", "."))
        except: peso_actual = mot["peso"]
        
        try: grasa_actual = float(str(ult.get("Grasa_Revision", 0)).replace(",", "."))
        except: grasa_actual = 0.0
        
        try: cintura_actual = float(str(ult.get("Cintura_Revision", 0)).replace(",", "."))
        except: cintura_actual = 0.0

        dif_peso = round(peso_actual - mot["peso"], 1)
        estado   = str(ult.get("Estado_Calculado", "AVANCE")).upper()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("1. COMPARATIVO BIOMÉTRICO EXHAUSTIVO"), 0, 1)
        pdf.set_fill_color(80, 200, 120); pdf.set_text_color(255, 255, 255)
        for h, w in [("MÉTRICA", 60), ("BASE (INICIO)", 45), ("ACTUAL", 45), ("DELTA (+/-)", 46)]:
            pdf.cell(w, 8, _limpiar(h), 1, 0, "C", fill=True)
        pdf.ln()

        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 11)
        
        # Fila Peso
        pdf.cell(60, 8, "Peso Corporal", 1, 0, "C")
        pdf.cell(45, 8, f"{mot['peso']} kg", 1, 0, "C")
        pdf.cell(45, 8, f"{peso_actual} kg", 1, 0, "C")
        pdf.set_text_color(34, 197, 94) if dif_peso <= 0 else pdf.set_text_color(239, 68, 68)
        pdf.cell(46, 8, f"{dif_peso:+.1f} kg", 1, 1, "C")
        pdf.set_text_color(51, 51, 51)
        
        # Fila Grasa
        if grasa_actual > 0:
            pdf.cell(60, 8, "% Grasa Corporal", 1, 0, "C")
            pdf.cell(45, 8, "-- %", 1, 0, "C")
            pdf.cell(45, 8, f"{grasa_actual} %", 1, 0, "C")
            pdf.cell(46, 8, "Reportado", 1, 1, "C")
            
        # Fila Cintura
        if cintura_actual > 0:
            pdf.cell(60, 8, "Perimetro Cintura", 1, 0, "C")
            pdf.cell(45, 8, "-- cm", 1, 0, "C")
            pdf.cell(45, 8, f"{cintura_actual} cm", 1, 0, "C")
            pdf.cell(46, 8, "Reportado", 1, 1, "C")

        pdf.ln(8)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("2. CUESTIONARIO DIAGNÓSTICO (PSICOMETRÍA)"), 0, 1)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, _limpiar(f"• Calidad de Sueño (1-10): {ult.get('Calidad_Sueno', '--')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Nivel de Energía: {ult.get('Energia', '--')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Control de Hambre: {ult.get('Hambre', '--')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Adherencia Reportada: {ult.get('Adherencia_Dieta', '--')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Progresión de Fuerza: {ult.get('Progreso_Fuerza', '--')}"), 0, 1)
        pdf.ln(8)

        color_map = {"AVANCE": (80, 200, 120), "LENTO": (245, 158, 11), "RETROCESO": (239, 68, 68)}
        fill_color = color_map.get(estado, (100, 100, 100))
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("3. DICTAMEN Y PLAN DE ACCIÓN"), 0, 1)
        pdf.set_fill_color(*fill_color); pdf.set_text_color(255, 255, 255)
        pdf.cell(100, 12, _limpiar(f"ESTATUS SISTEMA: {estado}"), 0, 1, "C", fill=True)
        pdf.ln(6)

        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 11)
        # Tomar los comentarios del coach si existen, si no, el default automático.
        dictamen = str(ult.get("Comentarios_Coach", ""))
        if not dictamen or dictamen.lower() == "nan":
            dictamen = {
                "AVANCE":    "El sistema confirma progresión sostenida. Mantener protocolo vigente. Revisar sobrecarga progresiva en ejercicios principales.",
                "LENTO":     "Avance subóptimo detectado. Revisar adherencia nutricional y calidad del sueño. Considerar ajuste calórico de ±100 kcal.",
                "RETROCESO": "ALERTA: Se detecta retroceso. Auditar fugas calóricas, consistencia del entrenamiento y nivel de estrés. Agendar revisión urgente.",
            }.get(estado, "Continuar monitoreo y reportar en la próxima revisión.")

        pdf.set_fill_color(248, 248, 248)
        pdf.rect(10, pdf.get_y(), 196, 22, "F")
        pdf.set_xy(15, pdf.get_y() + 4)
        pdf.multi_cell(186, 6, _limpiar(dictamen))

    return pdf.output(dest="S").encode("latin-1", "ignore")

# =============================================================================
# 7. HELPERS DE FORMULARIO
# =============================================================================
def g_idx(lista: list, clave: str, default: int = 0) -> int:
    val = st.session_state.db.get(clave)
    return lista.index(val) if val in lista else default

def guardar_y_navegar(datos: dict, destino: int):
    st.session_state.db.update(datos)
    st.session_state.step = destino
    st.rerun()

# =============================================================================
# 8. SIDEBAR — ACCESO ADMIN
# =============================================================================
with st.sidebar:
    st.markdown("<br>" * 15, unsafe_allow_html=True)
    admin_pass = st.text_input("⚙️ Modo Administrador", type="password",
                                help="Acceso exclusivo panel MM247")

df_existente = cargar_base_datos()

# =============================================================================
# 9. ENRUTAMIENTO PRINCIPAL
# =============================================================================

# ─── VISTA ADMIN ──────────────────────────────────────────────────────────────
if admin_pass == CONFIG["admin_password"]:
    st.markdown("<div class='main-title'>🔐 Panel Maestro MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>CONTROL CENTRAL DE RESULTADOS</div>", unsafe_allow_html=True)

    if df_existente.empty:
        st.warning("No hay alumnos registrados en el sistema.")
    else:
        df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"].copy()
        df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"].copy()

        st.markdown("### 🗂️ Atletas Activos")
        cols = st.columns([1.5, 2, 2.5, 2, 1.5])
        for col, label in zip(cols, ["ID Atleta", "Nombre", "Inicio → Meta", "Avance", "Acciones"]):
            col.markdown(f"**{label}**")
        st.markdown("---")

        ids_unicos = df_c1["ID_Alumno"].replace("", pd.NA).dropna().unique()

        for id_al in ids_unicos:
            datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
            revs_al  = df_c2[df_c2["ID_Alumno"] == id_al]

            clase_barra = "barra-gris"
            texto_barra = "Esperando reporte"

            if not revs_al.empty:
                estado = str(revs_al.iloc[-1].get("Estado_Calculado", "")).upper()
                if "AVANCE"    in estado: clase_barra, texto_barra = "barra-verde",    "Progresando"
                elif "LENTO"   in estado: clase_barra, texto_barra = "barra-amarilla", "Avance lento"
                elif "RETRO"   in estado: clase_barra, texto_barra = "barra-roja",     "Retroceso"

            c1, c2, c3, c4, c5 = st.columns([1.5, 2, 2.5, 2, 1.5])
            c1.write(f"`{id_al}`")
            c2.write(str(datos_al.get("Nombre completo", "Atleta")).title())
            c3.write(f"{datos_al.get('Peso actual','--')} → {datos_al.get('Peso objetivo','--')}")
            c4.markdown(
                f"<div style='font-size:12px;font-weight:bold;color:#7F8C8D;'>{texto_barra}</div>"
                f"<div class='barra-base'><div class='{clase_barra}'></div></div>",
                unsafe_allow_html=True,
            )
            if c5.button("Ver Expediente", key=f"btn_{id_al}"):
                st.session_state.alumno_seleccionado = id_al

        st.markdown("---")

        if "alumno_seleccionado" in st.session_state:
            id_sel  = st.session_state.alumno_seleccionado
            d_brutos = df_c1[df_c1["ID_Alumno"] == id_sel].iloc[0]
            d_norm   = normalizar_datos_alumno(d_brutos)
            m_calc   = calcular_metabolismo(d_norm)
            r_df     = df_c2[df_c2["ID_Alumno"] == id_sel]

            st.markdown(f"### 📋 Expediente: `{id_sel}`")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("IMC",   f"{m_calc['imc']}")
            col2.metric("TMB",   f"{m_calc['tmb']} kcal")
            col3.metric("TDEE",  f"{m_calc['tdee']} kcal")
            col4.metric("Meta",  f"{m_calc['cals']} kcal")

            try:
                pdf_bytes = generar_pdf_mm247(d_norm, m_calc, r_df, id_sel)
                st.download_button(
                    label="🖨️ Descargar Ficha Técnica PDF",
                    data=pdf_bytes,
                    file_name=f"Ficha_MM247_{id_sel}.pdf",
                    mime="application/pdf",
                )
            except Exception as err:
                st.error(f"Error al compilar el PDF: {err}")

elif admin_pass and admin_pass != CONFIG["admin_password"]:
    st.error("🔑 Clave de acceso inválida.")

# ─── VISTA CLIENTE ────────────────────────────────────────────────────────────
else:
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>SISTEMA DE ALTA INTENSIDAD Y DISCIPLINA</div>", unsafe_allow_html=True)

    if "step" not in st.session_state: st.session_state.step = 1
    if "db"   not in st.session_state: st.session_state.db   = {}

    tab_nuevo, tab_revision = st.tabs([
        "📝 Iniciar Expediente Nuevo",
        "🔄 Registrar Mi Avance (Auditoría)",
    ])

    # ── FORMULARIO MAESTRO (6 Misiones) ──────────────────────────────────
    with tab_nuevo:
        st.info("🟩 Bienvenido al ecosistema MM247. Completa las 6 misiones para activar tu expediente.")
        st.progress(st.session_state.step / CONFIG["total_misiones"])
        st.markdown(
            f"<h4 style='text-align:center;color:#7F8C8D;'>"
            f"MISIÓN {st.session_state.step} DE {CONFIG['total_misiones']}</h4>",
            unsafe_allow_html=True,
        )

        # ── M1: Datos fisiológicos ──────────────────────────────────────
        if st.session_state.step == 1:
            with st.form("form_m1"):
                st.markdown("<div class='section-header'>1. DATOS FISIOLÓGICOS Y DEMOGRÁFICOS</div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                ops_edad  = [f"{i} años" for i in range(14, 81)]
                ops_sexo  = ["Masculino", "Femenino"]
                ops_est   = [f"{i} cm"   for i in range(120, 221)]
                ops_peso  = [f"{i} kg"   for i in range(40, 161)]
                ops_ocup  = ["Sedentaria", "Ligera", "Activa", "Estudiante"]
                ops_hor   = ["Turno Matutino", "Turno Vespertino", "Turno Nocturno", "Horario Variable"]
                ops_ciu   = ["México", "Estados Unidos", "España", "Latinoamérica / Otro"]
                ops_obj   = ["Perder grasa", "Ganar masa muscular", "Recomposición corporal",
                             "Aumentar fuerza", "Mejorar salud general"]
                ops_tiem  = ["1-3 meses", "3-6 meses", "6-12 meses", "Más de 1 año"]

                with col1:
                    v_nombre  = st.text_input("Nombre completo:", value=st.session_state.db.get("Nombre completo", ""))
                    v_edad    = st.selectbox("Edad:", ops_edad,  index=g_idx(ops_edad,  "Edad",     11))
                    v_sexo    = st.selectbox("Sexo:", ops_sexo,  index=g_idx(ops_sexo,  "Sexo",      0))
                    v_est     = st.selectbox("Estatura:", ops_est, index=g_idx(ops_est, "Estatura", 55))
                    v_peso    = st.selectbox("Peso actual:", ops_peso, index=g_idx(ops_peso, "Peso actual", 40))
                with col2:
                    v_peso_obj = st.selectbox("Peso objetivo:", ops_peso, index=g_idx(ops_peso, "Peso objetivo", 35))
                    v_ocup     = st.selectbox("Ocupación:", ops_ocup, index=g_idx(ops_ocup, "Ocupación", 0))
                    v_hor      = st.selectbox("Horario:", ops_hor,  index=g_idx(ops_hor,  "Horario laboral", 0))
                    v_ciu      = st.selectbox("País/Zona:", ops_ciu, index=g_idx(ops_ciu, "Ciudad / País", 0))
                    v_tel      = st.text_input("WhatsApp:", value=st.session_state.db.get("Número de contacto", "55"))
                    v_mail     = st.text_input("Email:",    value=st.session_state.db.get("Correo electrónico", ""))

                st.markdown("<div class='section-header'>2. ENFOQUE PRINCIPAL</div>", unsafe_allow_html=True)
                v_obj    = st.selectbox("Meta prioritaria:", ops_obj, index=g_idx(ops_obj, "Objetivo principal", 0))
                v_tiemp  = st.selectbox("Tiempo para primeros resultados:", ops_tiem, index=g_idx(ops_tiem, "Tiempo deseado", 0))
                v_comp   = st.slider("Nivel de disciplina (1-10):", 1, 10, st.session_state.db.get("Compromiso", 10))

                if st.form_submit_button("Siguiente: Misión 2 ➡️"):
                    if not v_nombre.strip():
                        st.error("❌ El nombre es obligatorio.")
                    elif not v_tel.strip():
                        st.error("❌ El WhatsApp de contacto es obligatorio.")
                    elif not v_mail.strip():
                        st.error("❌ El Correo electrónico es obligatorio.")
                    else:
                        guardar_y_navegar({
                            "Nombre completo": v_nombre, "Edad": v_edad, "Sexo": v_sexo,
                            "Estatura": v_est, "Peso actual": v_peso, "Peso objetivo": v_peso_obj,
                            "Ocupación": v_ocup, "Horario laboral": v_hor, "Ciudad / País": v_ciu,
                            "Número de contacto": v_tel, "Correo electrónico": v_mail,
                            "Objetivo principal": v_obj, "Tiempo deseado": v_tiemp, "Compromiso": v_comp,
                        }, 2)

        # ── M2: Antecedentes de entrenamiento ───────────────────────────
        elif st.session_state.step == 2:
            with st.form("form_m2"):
                st.success("La constancia es la clave de la hipertrofia.")
                st.markdown("<div class='section-header'>3. ANTECEDENTES DE ENTRENAMIENTO</div>", unsafe_allow_html=True)

                ops_t_ent = ["Nunca", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años", "Más de 3 años"]
                ops_d_sem = ["3 días por semana", "4 días por semana", "5 días por semana"]
                ops_t_ses = ["Menos de 45 minutos", "De 45 a 75 minutos", "Más de 75 minutos"]

                v_t_ent   = st.selectbox("Tiempo entrenando:", ops_t_ent, index=g_idx(ops_t_ent, "Tiempo entrenando", 0))
                v_tipo    = st.multiselect("Sistemas practicados:", ["Gimnasio", "Calistenia", "Crossfit", "Deportes", "Funcional", "Ninguno"],
                                           default=st.session_state.db.get("Tipo entreno", ["Gimnasio"]))
                v_dias    = st.selectbox("Días/semana disponibles:", ops_d_sem, index=g_idx(ops_d_sem, "Días entrenar", 1))
                v_sesion  = st.selectbox("Tiempo por sesión:", ops_t_ses, index=g_idx(ops_t_ses, "Tiempo por sesión", 1))
                v_act     = st.selectbox("¿Entrenas actualmente?", ["Sí", "No"], index=g_idx(["Sí", "No"], "Entrena actualmente", 0))
                v_coach   = st.selectbox("¿Tuviste entrenador previo?", ["Sí", "No"], index=g_idx(["Sí", "No"], "Coach anterior", 1))

                c1, c2 = st.columns(2)
                b_back = c1.form_submit_button("⬅️ Atrás")
                b_next = c2.form_submit_button("Siguiente: Misión 3 ➡️")
                datos_m2 = {"Tiempo entrenando": v_t_ent, "Tipo entreno": v_tipo,
                            "Días entrenar": v_dias, "Tiempo por sesión": v_sesion,
                            "Entrena actualmente": v_act, "Coach anterior": v_coach}
                
                if b_back: 
                    guardar_y_navegar(datos_m2, 1)
                if b_next: 
                    if len(v_tipo) == 0:
                        st.error("❌ Selecciona al menos un sistema deportivo practicado (o elige 'Ninguno').")
                    else:
                        guardar_y_navegar(datos_m2, 3)

        # ── M3: Clínica y biomecánica ───────────────────────────────────
        elif st.session_state.step == 3:
            with st.form("form_m3"):
                st.error("⚠️ Reporta lesiones — ajustamos la carga mecánica por tu seguridad.")
                st.markdown("<div class='section-header'>4. CONDICIÓN CLÍNICA Y LESIONES</div>", unsafe_allow_html=True)

                ops_les = ["Ninguna", "Rodilla / Tendinitis", "Hombro / Manguito", "Espalda Baja / Lumbalgia", "Cervicales", "Muñeca / Tobillo"]
                ops_con = ["Ninguna", "Diabetes", "Hipertensión", "Tiroides / Hormonal", "Hernia Discal / Umbilical"]
                ops_pro = ["No", "Sí, cargas sobre columna", "Sí, flexiones profundas"]

                v_lesion  = st.selectbox("Lesión o dolor recurrente:", ops_les, index=g_idx(ops_les, "Lesión actual", 0))
                v_cir     = st.selectbox("Cirugías previas:", ["No", "Sí, miembros inferiores", "Sí, miembros superiores / columna"],
                                         index=g_idx(["No", "Sí, miembros inferiores", "Sí, miembros superiores / columna"], "Cirugías", 0))
                v_dolor   = st.selectbox("Molestias al levantar carga:", ["No", "Sí, al hacer presses", "Sí, en sentadillas", "Sí, lumbar constante"],
                                         index=g_idx(["No", "Sí, al hacer presses", "Sí, en sentadillas", "Sí, lumbar constante"], "Dolor frecuente", 0))
                v_med     = st.selectbox("Medicamentos de prescripción:", ["No", "Sí, presión/glucosa", "Sí, antiinflamatorios"],
                                         index=g_idx(["No", "Sí, presión/glucosa", "Sí, antiinflamatorios"], "Medicamentos", 0))
                v_cond    = st.selectbox("Patología crónica:", ops_con, index=g_idx(ops_con, "Condición médica", 0))
                v_proh    = st.selectbox("Prohibición médica de carga axial:", ops_pro, index=g_idx(ops_pro, "Prohibido ejercicio", 0))

                st.markdown("<div class='section-header'>5. AUTO-EVALUACIÓN BIOMECÁNICA</div>", unsafe_allow_html=True)
                v_molest  = st.multiselect("Dolor en movimientos básicos:", ["Sentadilla", "Press pecho", "Peso muerto", "Press militar", "Ninguno"],
                                           default=st.session_state.db.get("Molestias movimientos", ["Ninguno"]))
                v_movil   = st.selectbox("Flexibilidad general:", ["Mala / Muy rígido", "Regular", "Buena"],
                                         index=g_idx(["Mala / Muy rígido", "Regular", "Buena"], "Movilidad", 1))
                v_postura = st.selectbox("Desviaciones posturales:", ["No", "Sí, hombros adelantados", "Sí, hiperlordosis"],
                                         index=g_idx(["No", "Sí, hombros adelantados", "Sí, hiperlordosis"], "Mala postura", 0))
                v_debil   = st.selectbox("Eslabón muscular más débil:", ["Tren Inferior", "Tren Superior", "Core", "Espalda"],
                                         index=g_idx(["Tren Inferior", "Tren Superior", "Core", "Espalda"], "Parte débil", 0))

                c1, c2 = st.columns(2)
                b_back = c1.form_submit_button("⬅️ Atrás")
                b_next = c2.form_submit_button("Siguiente: Misión 4 ➡️")
                datos_m3 = {"Lesión actual": v_lesion, "Cirugías": v_cir, "Dolor frecuente": v_dolor,
                            "Medicamentos": v_med, "Condición médica": v_cond, "Prohibido ejercicio": v_proh,
                            "Molestias movimientos": v_molest, "Movilidad": v_movil,
                            "Mala postura": v_postura, "Parte débil": v_debil}
                
                if b_back: 
                    guardar_y_navegar(datos_m3, 2)
                if b_next: 
                    if len(v_molest) == 0:
                        st.error("❌ Selecciona si tienes dolor en movimientos básicos (o elige 'Ninguno').")
                    else:
                        guardar_y_navegar(datos_m3, 4)

        # ── M4: Morfología y hábitos ────────────────────────────────────
        elif st.session_state.step == 4:
            with st.form("form_m4"):
                st.warning("El músculo crece fuera del gimnasio. Evalúa tu recuperación.")
                st.markdown("<div class='section-header'>6. MORFOLOGÍA Y HÁBITOS DE VIDA</div>", unsafe_allow_html=True)

                ops_soma  = ["Delgado / Ectomorfo", "Atlético / Mesomorfo", "Robusto / Endomorfo", "Sobrepeso"]
                ops_act   = ["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"]

                v_soma    = st.selectbox("Somatotipo:", ops_soma, index=g_idx(ops_soma, "Consideración física", 1))
                v_grasa   = st.selectbox("Zona de acumulación grasa:", ["Abdomen / Lumbar", "Piernas y Cadera", "General"],
                                         index=g_idx(["Abdomen / Lumbar", "Piernas y Cadera", "General"], "Acumula grasa", 0))
                v_sueno   = st.selectbox("Horas de sueño:", ["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"],
                                         index=g_idx(["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"], "Horas sueño", 2))
                v_estres  = st.selectbox("Estrés diario:", ["Bajo / Controlado", "Medio", "Alto"],
                                         index=g_idx(["Bajo / Controlado", "Medio", "Alto"], "Nivel de estrés", 1))
                v_agua    = st.selectbox("Agua diaria:", ["Menos de 1.5 L", "1.5 a 3 L", "Más de 3 L"],
                                         index=g_idx(["Menos de 1.5 L", "1.5 a 3 L", "Más de 3 L"], "Agua diaria", 1))
                v_alcohol = st.selectbox("Alcohol:", ["No / Nunca", "Ocasional", "Frecuente fines de semana"],
                                         index=g_idx(["No / Nunca", "Ocasional", "Frecuente fines de semana"], "Alcohol", 1))
                v_fuma    = st.selectbox("Tabaco:", ["No", "Sí"], index=g_idx(["No", "Sí"], "Fuma", 0))
                v_act_niv = st.selectbox("Actividad fuera del gym:", ops_act, index=g_idx(ops_act, "Nivel de actividad", 2))

                c1, c2 = st.columns(2)
                b_back = c1.form_submit_button("⬅️ Atrás")
                b_next = c2.form_submit_button("Siguiente: Misión 5 ➡️")
                datos_m4 = {"Consideración física": v_soma, "Acumula grasa": v_grasa,
                            "Horas sueño": v_sueno, "Nivel de estrés": v_estres,
                            "Agua diaria": v_agua, "Alcohol": v_alcohol,
                            "Fuma": v_fuma, "Nivel de actividad": v_act_niv}
                
                if b_back: guardar_y_navegar(datos_m4, 3)
                if b_next: guardar_y_navegar(datos_m4, 5)

        # ── M5: Menú nutricional ─────────────────────────────────────────
        elif st.session_state.step == 5:
            with st.form("form_m5"):
                st.info("Elige el combustible de tu plan. Mantente apegado.")
                st.markdown("<div class='section-header'>7. MENÚ DE SELECCIÓN CONTROLADA</div>", unsafe_allow_html=True)

                v_prots   = st.multiselect("🥩 Proteínas:", ["Pechuga de Pollo", "Bisteck de Res magro", "Lomo de Cerdo",
                                            "Claras de Huevo", "Atún en agua", "Filete de Pescado"],
                                           default=st.session_state.db.get("Menu_Proteinas", ["Pechuga de Pollo", "Claras de Huevo"]))
                v_carbs   = st.multiselect("🍞 Carbohidratos:", ["Arroz Blanco", "Avena", "Camote", "Papa cocida", "Tortilla de Maíz"],
                                           default=st.session_state.db.get("Menu_Carbohidratos", ["Arroz Blanco", "Avena"]))
                v_grasas  = st.multiselect("🥑 Grasas saludables:", ["Aguacate", "Almendras", "Crema de Cacahuete"],
                                           default=st.session_state.db.get("Menu_Grasas", ["Aguacate"]))
                v_frutas  = st.multiselect("🍎 Frutas:", ["Plátano", "Manzana", "Fresas / Berries"],
                                           default=st.session_state.db.get("Menu_Frutas", ["Plátano", "Manzana"]))
                v_verds   = st.multiselect("🥦 Verduras:", ["Brócoli", "Espinacas", "Lechuga / Pepino"],
                                           default=st.session_state.db.get("Menu_Verduras", ["Brócoli", "Espinacas"]))

                st.markdown("<div class='section-header'>8. PERFIL NUTRICIONAL</div>", unsafe_allow_html=True)
                v_alerg   = st.text_input("Alergias alimentarias:", value=st.session_state.db.get("Alergias alimenticias", ""))
                v_intol   = st.text_input("Intolerancias digestivas:", value=st.session_state.db.get("Intolerancias", ""))
                v_tipo_al = st.selectbox("Estructura dietética:", ["Omnívoro", "Vegetariano"],
                                         index=g_idx(["Omnívoro", "Vegetariano"], "Tipo alimentación", 0))
                v_no_gust = st.text_input("Alimentos que rechazas:", value=st.session_state.db.get("Alimentos no gustan", ""))

                c1, c2 = st.columns(2)
                b_back = c1.form_submit_button("⬅️ Atrás")
                b_next = c2.form_submit_button("Siguiente: Misión 6 ➡️")
                datos_m5 = {"Menu_Proteinas": v_prots, "Menu_Carbohidratos": v_carbs,
                            "Menu_Grasas": v_grasas, "Menu_Frutas": v_frutas, "Menu_Verduras": v_verds,
                            "Alergias alimenticias": v_alerg, "Intolerancias": v_intol,
                            "Tipo alimentación": v_tipo_al, "Alimentos no gustan": v_no_gust}
                
                if b_back: 
                    guardar_y_navegar(datos_m5, 4)
                if b_next: 
                    if len(v_prots) == 0: st.error("❌ Elige al menos una fuente de PROTEÍNAS.")
                    elif len(v_carbs) == 0: st.error("❌ Elige al menos una fuente de CARBOHIDRATOS.")
                    elif len(v_grasas) == 0: st.error("❌ Elige al menos una fuente de GRASAS.")
                    elif len(v_frutas) == 0: st.error("❌ Elige al menos una FRUTA.")
                    elif len(v_verds) == 0: st.error("❌ Elige al menos una VERDURA.")
                    else:
                        guardar_y_navegar(datos_m5, 6)

        # ── M6: Logística y psicometría ──────────────────────────────────
        elif st.session_state.step == 6:
            with st.form("form_m6"):
                st.markdown("<div class='section-header'>9. LOGÍSTICA DE ENTRENAMIENTO</div>", unsafe_allow_html=True)

                v_lugar   = st.selectbox("¿Dónde entrenas?", ["Gimnasio comercial completo", "Casa con equipo"],
                                         index=g_idx(["Gimnasio comercial completo", "Casa con equipo"], "Donde entrenará", 0))
                v_equipo  = st.multiselect("Equipo disponible:", ["Mancuernas", "Barras y Discos", "Poleas"],
                                           default=st.session_state.db.get("Equipo disponible", ["Mancuernas", "Barras y Discos"]))
                v_partes  = st.selectbox("Músculo prioritario:", ["Glúteos / Femorales", "Cuádriceps",
                                          "Hombros y Espalda", "Brazos", "Abdomen / Definición"],
                                         index=g_idx(["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda",
                                                      "Brazos", "Abdomen / Definición"], "Partes mejorar", 2))
                v_impide  = st.text_area("¿Qué saboteó tu avance antes?", value=st.session_state.db.get("Impedido progresar", ""))
                v_odia    = st.text_input("Ejercicio que odias:", value=st.session_state.db.get("Ejercicio odia", ""))
                v_gusta   = st.text_input("Ejercicio favorito:", value=st.session_state.db.get("Ejercicio disfruta", ""))

                st.markdown("<div class='section-header'>10. ESCALAS PSICOMÉTRICAS</div>", unsafe_allow_html=True)
                v_disc = st.slider("Disciplina:", 1, 10, st.session_state.db.get("P_Disciplina", 8))
                v_estr = st.slider("Estrés mental:", 1, 10, st.session_state.db.get("P_Estres", 5))
                v_suen = st.slider("Calidad de sueño:", 1, 10, st.session_state.db.get("P_Sueno", 8))
                v_moti = st.slider("Motivación:", 1, 10, st.session_state.db.get("P_Motivacion", 9))
                v_ener = st.slider("Energía diaria:", 1, 10, st.session_state.db.get("P_Energia", 7))
                v_hamb = st.slider("Ansiedad por comida:", 1, 10, st.session_state.db.get("P_Hambre", 5))
                v_recu = st.slider("Recuperación muscular:", 1, 10, st.session_state.db.get("P_Recup", 7))
                v_prio = st.selectbox("Prioridad de entrenamiento:", ["Salud", "Estética", "Rendimiento"],
                                      index=g_idx(["Salud", "Estética", "Rendimiento"], "Prioridad", 1))

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                b_back  = c1.form_submit_button("⬅️ Atrás")
                b_envia = c2.form_submit_button("🚀 REGISTRAR EXPEDIENTE")

                datos_m6 = {"Donde entrenará": v_lugar, "Equipo disponible": v_equipo,
                            "Partes mejorar": v_partes, "Impedido progresar": v_impide,
                            "Ejercicio odia": v_odia, "Ejercicio disfruta": v_gusta,
                            "P_Disciplina": v_disc, "P_Estres": v_estr, "P_Sueno": v_suen,
                            "P_Motivacion": v_moti, "P_Energia": v_ener, "P_Hambre": v_hamb,
                            "P_Recup": v_recu, "Prioridad": v_prio}

                if b_back:
                    guardar_y_navegar(datos_m6, 5)

                if b_envia:
                    if len(v_equipo) == 0:
                        st.error("❌ Selecciona el equipo de entrenamiento del que dispones.")
                    elif not v_impide.strip() or not v_odia.strip() or not v_gusta.strip():
                        st.error("❌ Responde las preguntas de texto sobre tus obstáculos y ejercicios (o escribe 'Ninguno').")
                    else:
                        st.session_state.db.update(datos_m6)
                        nombre_final = st.session_state.db.get("Nombre completo", "").strip()
                        
                        id_nuevo = generar_id_unico(nombre_final)
                        d = st.session_state.db

                        payload = {
                            "Fecha":            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Tipo_Registro":    "INICIAL",
                            "ID_Alumno":        id_nuevo,
                            "Nombre completo":  str(d.get("Nombre completo")).title(),
                            "Edad":             str(d.get("Edad")),
                            "Sexo":             str(d.get("Sexo")),
                            "Estatura":         str(d.get("Estatura")),
                            "Peso actual":      str(d.get("Peso actual")),
                            "Peso objetivo":    str(d.get("Peso objetivo")),
                            "Ocupación":        str(d.get("Ocupación")),
                            "Horario laboral":  str(d.get("Horario laboral")),
                            "Ciudad / País":    str(d.get("Ciudad / País")),
                            "Número de contacto": str(d.get("Número de contacto")),
                            "Correo electrónico": str(d.get("Correo electrónico")),
                            "Objetivo principal": str(d.get("Objetivo principal")),
                            "Tiempo deseado":   str(d.get("Tiempo deseado")),
                            "Compromiso":       str(d.get("Compromiso")),
                            "Tiempo entrenando": str(d.get("Tiempo entrenando")),
                            "Tipo entreno":     ",".join(d.get("Tipo entreno", [])),
                            "Días entrenar":    str(d.get("Días entrenar")),
                            "Tiempo por sesión": str(d.get("Tiempo por sesión")),
                            "Entrena actualmente": str(d.get("Entrena actualmente")),
                            "Coach anterior":   str(d.get("Coach anterior")),
                            "Lesión actual":    str(d.get("Lesión actual")),
                            "Cirugías":         str(d.get("Cirugías")),
                            "Dolor frecuente":  str(d.get("Dolor frecuente")),
                            "Medicamentos":     str(d.get("Medicamentos")),
                            "Condición médica": str(d.get("Condición médica")),
                            "Prohibido ejercicio": str(d.get("Prohibido ejercicio")),
                            "Molestias movimientos": ",".join(d.get("Molestias movimientos", [])),
                            "Movilidad":        str(d.get("Movilidad")),
                            "Mala postura":     str(d.get("Mala postura")),
                            "Parte débil":      str(d.get("Parte débil")),
                            "Consideración física": str(d.get("Consideración física")),
                            "Acumula grasa":    str(d.get("Acumula grasa")),
                            "Horas sueño":      str(d.get("Horas sueño")),
                            "Nivel de estrés":  str(d.get("Nivel de estrés")),
                            "Agua diaria":      str(d.get("Agua diaria")),
                            "Alcohol":          str(d.get("Alcohol")),
                            "Fuma":             str(d.get("Fuma")),
                            "Nivel de actividad": str(d.get("Nivel de actividad")),
                            "Alergias alimenticias": str(d.get("Alergias alimenticias")),
                            "Intolerancias":    str(d.get("Intolerancias")),
                            "Tipo alimentación": str(d.get("Tipo alimentación")),
                            "Alimentos no gustan": str(d.get("Alimentos no gustan")),
                            "Donde entrenará":  str(d.get("Donde entrenará")),
                            "Equipo disponible": ",".join(d.get("Equipo disponible", [])),
                            "Partes mejorar":   str(d.get("Partes mejorar")),
                            "Impedido progresar": str(d.get("Impedido progresar")),
                            "Ejercicio odia":   str(d.get("Ejercicio odia")),
                            "Ejercicio disfruta": str(d.get("Ejercicio disfruta")),
                            "P_Disciplina":     str(d.get("P_Disciplina")),
                            "P_Estres":         str(d.get("P_Estres")),
                            "P_Sueno":          str(d.get("P_Sueno")),
                            "P_Motivacion":     str(d.get("P_Motivacion")),
                            "P_Energia":        str(d.get("P_Energia")),
                            "P_Hambre":         str(d.get("P_Hambre")),
                            "P_Recup":          str(d.get("P_Recup")),
                            "Prioridad":        str(d.get("Prioridad")),
                            "Menu_Proteinas":   ",".join(d.get("Menu_Proteinas", [])),
                            "Menu_Carbohidratos": ",".join(d.get("Menu_Carbohidratos", [])),
                            "Menu_Grasas":      ",".join(d.get("Menu_Grasas", [])),
                            "Menu_Frutas":      ",".join(d.get("Menu_Frutas", [])),
                            "Menu_Verduras":    ",".join(d.get("Menu_Verduras", [])),
                        }

                        with st.spinner("Sincronizando expediente..."):
                            try:
                                resp = requests.post(CONFIG["webhook_url"], json=payload, timeout=10)
                                if resp.status_code == 200 and "success" in resp.text.lower():
                                    st.markdown(
                                        f"<div class='id-box'>"
                                        f"✅ ¡EXPEDIENTE ACTIVADO!<br><br>"
                                        f"TU ID DE ATLETA:<br>"
                                        f"<span style='font-size:32px;color:#FFFFFF;'>{id_nuevo}</span><br><br>"
                                        f"<small style='color:#E5E7EB;font-weight:normal;'>"
                                        f"Guárdalo. Lo necesitarás para reportar tu avance.</small>"
                                        f"</div>",
                                        unsafe_allow_html=True,
                                    )
                                    st.balloons()
                                    st.cache_data.clear() # Limpia caché para que el Admin lo vea al instante
                                    st.session_state.step = 1
                                    st.session_state.db   = {}
                                else:
                                    st.error(f"Error en servidor: {resp.text[:200]}")
                            except requests.exceptions.Timeout:
                                st.error("⏱️ El servidor tardó demasiado. Intenta de nuevo.")
                            except Exception as e:
                                st.error(f"Error de conexión: {e}")

    # ── MÓDULO REVISIÓN DE AVANCE (NUEVO DISEÑO CON AVATAR) ───────────────
    with tab_revision:
        st.info("La constancia se mide en datos. Ingresa tu ID y reporta tu estado clínico.")

        with st.form("form_revision", clear_on_submit=True):
            id_ing = st.text_input("Tu ID de Atleta (Ej: MM247-2026-JGR-A3F2B1):").strip().upper()

            col_v, col_t = st.columns([1, 2], gap="large")
            
            with col_v:
                st.markdown("<div class='section-header'>Evidencia Visual</div>", unsafe_allow_html=True)
                st.file_uploader("Subir Foto INICIO", type=['png', 'jpg', 'jpeg'])
                st.file_uploader("Subir Foto AUDITORÍA ACTUAL", type=['png', 'jpg', 'jpeg'])
                
            with col_t:
                st.markdown("<div class='section-header'>1. Cuestionario Clínico</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    sueno_rev = st.slider("Calidad de sueño esta semana (1-10):", 1, 10, 8)
                    energia_rev = st.select_slider("Nivel de Energía Post-Entreno:", options=["Agotado", "Normal", "Óptimo"])
                with c2:
                    hambre_rev = st.select_slider("Ansiedad por comida:", options=["Alta", "Controlada", "Baja"])
                    adherencia = st.radio("Cumplimiento de dieta:", ["Cumplimiento Total (Excelente)", "Cumplimiento Parcial (Aceptable)", "Cumplimiento Bajo (Mal apego)"])
                
                fuerza = st.radio("Rendimiento en fuerza:", ["Incrementé pesos o repeticiones", "Me mantuve estable", "Me sentí más débil / fatigado"])

                st.markdown("<div class='section-header'>2. Métricas Corporales</div>", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                peso_rev    = m1.number_input("Peso (kg):", min_value=30.0, value=70.0, step=0.1)
                grasa_rev   = m2.number_input("% Grasa:", min_value=0.0, value=15.0, step=0.1)
                cintura_rev = m3.number_input("Cintura (cm):", min_value=40.0, value=80.0, step=0.5)

                comentarios = st.text_area("Observaciones, dudas o sensaciones para tu Coach:")

            if st.form_submit_button("🚀 ENVIAR AUDITORÍA"):
                if not id_ing:
                    st.error("❌ El ID es obligatorio.")
                elif df_existente.empty or id_ing not in df_existente["ID_Alumno"].values:
                    st.error("❌ ID no encontrado. Verifica mayúsculas y guiones.")
                else:
                    # Lógica para Avatar Dinámico
                    puntos = 0
                    if adherencia == "Cumplimiento Total (Excelente)": puntos += 2
                    elif adherencia == "Cumplimiento Parcial (Aceptable)": puntos += 1
                    if fuerza == "Incrementé pesos o repeticiones": puntos += 2
                    elif fuerza == "Me mantuve estable": puntos += 1

                    if puntos >= 3: estado_calc = "AVANCE"
                    elif puntos == 2: estado_calc = "LENTO"
                    else: estado_calc = "RETROCESO"

                    # Generamos el Avatar según el dictamen automático
                    avatar_url = obtener_avatar_url(estado_calc)

                    payload_rev = {
                        "Fecha":                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro":        "REVISION",
                        "ID_Alumno":            id_ing,
                        "Peso_Revision":        str(peso_rev),
                        "Grasa_Revision":       str(grasa_rev),
                        "Cintura_Revision":     str(cintura_rev),
                        "Adherencia_Dieta":     adherencia,
                        "Progreso_Fuerza":      fuerza,
                        "Calidad_Sueno":        str(sueno_rev),
                        "Energia":              energia_rev,
                        "Hambre":               hambre_rev,
                        "Comentarios_Evolucion": comentarios,
                        "Estado_Calculado":     estado_calc,
                    }

                    with st.spinner("Registrando métricas..."):
                        try:
                            resp = requests.post(CONFIG["webhook_url"], json=payload_rev, timeout=10)
                            if resp.status_code == 200 and "success" in resp.text.lower():
                                st.cache_data.clear()
                                color_fb = {"AVANCE": "🟢", "LENTO": "🟡", "RETROCESO": "🔴"}
                                st.success(
                                    f"{color_fb[estado_calc]} Evaluación registrada. "
                                    f"Estado del sistema: **{estado_calc}**."
                                )
                                # Mostramos el avatar como retroalimentación visual al enviar
                                st.image(avatar_url, caption=f"Tu Proyección Actual: {estado_calc}", width=250)
                            else:
                                st.error(f"Error en servidor: {resp.text[:200]}")
                        except Exception as e:
                            st.error(f"Error: {e}")
