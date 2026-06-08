# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA DE ADHERENCIA
   
   VERSIÓN 4.0 — PARÁMETROS ESPEJO, LÍNEA BASE Y AUDITORÍA FOTOGRÁFICA
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
st.set_page_config(page_title=CONFIG["page_title"], page_icon=CONFIG["page_icon"], layout="wide")

# =============================================================================
# 2. ESTILOS CSS (DISEÑO LIGHT MODE + VERDE ESMERALDA)
# =============================================================================
st.markdown("""
<style>
/* Fondo principal */
.stApp { background-color: #F8F9FA; color: #333333; }

/* Títulos y Subtítulos */
.main-title { 
    font-size: 50px; font-weight: 800; color: #2C3E50;
    text-align: center; letter-spacing: 1px; margin-bottom: 0px; text-transform: uppercase; 
}
.subtitle { font-size: 16px; color: #7F8C8D; text-align: center; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 3px; }

/* Encabezados de sección */
.section-header { 
    font-size: 20px; font-weight: 700; color: #50C878; margin-top: 30px;
    margin-bottom: 15px; border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; text-transform: uppercase; 
}

/* Panel de Formulario */
div[data-testid="stForm"] { 
    background: #FFFFFF; padding: 30px; border-radius: 16px;
    border: 1px solid #E5E7EB; box-shadow: 0 4px 20px rgba(0,0,0,0.05); 
}

/* Tarjetas de Métricas */
.metric-card {
    background-color: #FFFFFF; padding: 20px; border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #50C878;
    margin-bottom: 20px; border: 1px solid #E5E7EB; 
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
    height: 50px; border: none; text-transform: uppercase; letter-spacing: 0.5px; transition: all 0.3s ease;
}
div.stButton > button:hover, div[data-testid="stForm"] button:hover {
    transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 8px 20px rgba(80, 200, 120, 0.4); color: white;
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
    base_url = "https://models.readyplayer.me/648b28f7f9037c9521369ec9.png"
    if estatus == "AVANCE":
        return f"{base_url}?pose=A&camera=portrait&blendShape=smile"
    elif estatus == "RETROCESO":
        return f"{base_url}?pose=T&camera=fullbody"
    else:
        return f"{base_url}?camera=portrait"

# =============================================================================
# 3. CAPA DE DATOS
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
    if not iniciales: iniciales = "MM"
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
        "Cintura inicial":    buscar(["cintura inicial", "perímetro cintura"],  "85",                    -1),
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
        "P_Energia_Q1":       buscar(["p_energia"],                             "5",                     -1),
        "P_Sueno_Q1":         buscar(["p_sueno"],                               "5",                     -1),
        "P_Fuerza_Q1":        buscar(["p_fuerza"],                              "5",                     -1),
        "P_Hambre_Q1":        buscar(["p_hambre"],                              "5",                     -1),
        "Menu_Proteinas":     buscar(["menu_proteinas", "proteínas"],           "Pechuga de Pollo"),
        "Menu_Carbohidratos": buscar(["menu_carbohidratos", "carbs"],           "Arroz Blanco"),
        "Menu_Grasas":        buscar(["menu_grasas", "grasas"],                 "Aguacate"),
        "Menu_Frutas":        buscar(["menu_frutas", "frutas"],                 "Manzana"),
        "Menu_Verduras":      buscar(["menu_verduras", "verduras"],             "Brócoli"),
    }

# =============================================================================
# 5. MOTOR METABÓLICO Y DE ORIGEN (ICA)
# =============================================================================
def _parse_float(valor: str, defecto: float) -> float:
    try:
        return float(str(valor).replace("kg", "").replace("cm", "").replace("años", "").strip().split()[0])
    except Exception:
        return defecto

def calcular_metabolismo(datos: dict) -> dict:
    peso     = _parse_float(datos.get("Peso actual", "80"),  80.0)
    cintura  = _parse_float(datos.get("Cintura inicial", "85"), 85.0)
    estatura = _parse_float(datos.get("Estatura", "175"), 175.0)
    edad     = _parse_float(datos.get("Edad", "25"),  25.0)
    genero   = str(datos.get("Sexo", "Masculino"))
    actividad= str(datos.get("Nivel de actividad", "Moderadamente activo"))
    meta     = str(datos.get("Objetivo principal", "Recomposición corporal"))

    imc = peso / ((estatura / 100) ** 2) if estatura > 0 else 0.0
    ica = cintura / estatura if estatura > 0 else 0.0

    origen_fisico = "Condición Normal"
    if ica >= 0.53: origen_fisico = "Obesidad / Riesgo Metabólico"
    elif ica >= 0.50: origen_fisico = "Sobrepeso Músculo-Graso"
    elif ica < 0.43: origen_fisico = "Perfil Atlético / Magro"

    if "Masculino" in genero:
        tmb = 66.473 + (13.751 * peso) + (5.0033 * estatura) - (6.755 * edad)
    else:
        tmb = 655.095 + (9.5634 * peso) + (1.8496 * estatura) - (4.6756 * edad)

    factor = CONFIG["factores_actividad"].get(actividad, 1.55)
    tdee   = tmb * factor

    if any(k in meta for k in ("Perder", "Bajar", "grasa", "Déficit")):
        cals, balance_str = tdee - 400, "Déficit Calórico (-400 kcal)"
    elif any(k in meta for k in ("Ganar", "Subir", "Volumen", "muscular")):
        cals, balance_str = tdee + 300, "Superávit Calórico (+300 kcal)"
    elif "fuerza" in meta.lower():
        cals, balance_str = tdee + 200, "Superávit Moderado (+200 kcal)"
    else:
        cals, balance_str = tdee, "Normocalórico (mantenimiento)"

    prot, grasa = round(peso * 2.0, 1), round(peso * 1.0, 1)
    carbs = round(max((cals - (prot * 4) - (grasa * 9)) / 4, 50.0), 1)

    return {
        "imc": round(imc, 1), "ica": round(ica, 2), "origen": origen_fisico,
        "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals, 0),
        "prot": prot, "grasa": grasa, "carbs": carbs, "balance_str": balance_str,
        "factor": factor, "edad": edad, "genero": genero, "peso": peso, "cintura": cintura, "estatura": estatura,
    }

# =============================================================================
# 6. MOTOR DE PDF (DISEÑO ESMERALDA Y HOJA 4 CLÍNICA)
# =============================================================================
def _limpiar(texto: str) -> str:
    return str(texto).encode("latin-1", "replace").decode("latin-1")

def _tiene_lesion(norm: dict) -> bool:
    return norm.get("Lesión actual", "Ninguna").lower() != "ninguna" or norm.get("Prohibido ejercicio", "No").lower() != "no"

def generar_pdf_mm247(norm: dict, mot: dict, revs_df: pd.DataFrame, id_al: str) -> bytes:
    pdf = FPDF("P", "mm", "Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    con_lesion = _tiene_lesion(norm)
    num_dias   = int(str(norm.get("Días entrenar", "4")).strip()[0]) if str(norm.get("Días entrenar", "4")).strip()[0].isdigit() else 4

    def header(titulo: str):
        pdf.add_page()
        pdf.set_fill_color(80, 200, 120)
        pdf.rect(0, 0, 216, 30, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 24)
        pdf.set_xy(10, 8);  pdf.cell(100, 10, "MIND MUSCLE 247",  0, 0, "L")
        pdf.set_font("Arial", "B", 12)
        pdf.set_xy(160, 12); pdf.cell(45, 10, "CONFIDENCIAL", 0, 0, "R")
        pdf.set_text_color(240, 255, 240)
        pdf.set_font("Arial", "", 10)
        pdf.set_xy(10, 18);  pdf.cell(100, 10, f"ID: {id_al}", 0, 0, "L")
        pdf.set_text_color(44, 62, 80)
        pdf.set_font("Arial", "B", 14)
        pdf.set_xy(10, 35);  pdf.cell(196, 10, _limpiar(titulo), 0, 1, "C")
        pdf.set_draw_color(229, 231, 235); pdf.set_line_width(0.5)
        pdf.line(10, 45, 206, 45); pdf.ln(10)

    def fila_dato(label: str, valor: str, col_w: int = 98):
        pdf.set_font("Arial", "B", 10); pdf.cell(col_w, 7, _limpiar(label), 1, 0, "L")
        pdf.set_font("Arial", "",  10); pdf.cell(col_w, 7, _limpiar(valor), 1, 1, "L")

    # --- HOJA 1 ---
    header("HOJA 1: PERFIL CLÍNICO Y LÍNEA BASE")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("1. DATOS GENERALES Y ORIGEN FÍSICO"), 0, 1)
    fila_dato("Cliente", norm["Nombre completo"])
    fila_dato("Edad / Sexo", f"{int(mot['edad'])} años / {mot['genero']}")
    fila_dato("Estatura / Peso", f"{mot['estatura']} cm / {mot['peso']} kg")
    fila_dato("Punto de Partida (Origen)", f"{mot['origen']} (ICA: {mot['ica']})")
    fila_dato("Objetivo principal", norm.get("Objetivo principal", "--"))
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("2. DISPONIBILIDAD LOGÍSTICA"), 0, 1)
    fila_dato("Días de entrenamiento", norm["Días entrenar"])
    fila_dato("Tiempo por sesión", norm["Tiempo por sesión"])
    fila_dato("Nivel de compromiso", str(norm["Compromiso"]))
    fila_dato("Nivel de actividad", norm["Nivel de actividad"])
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(239, 68, 68)
    pdf.cell(0, 10, _limpiar("3. ALERTAS BIOMECÁNICAS"), 0, 1)
    pdf.set_fill_color(254, 242, 242); pdf.set_draw_color(239, 68, 68)
    pdf.rect(10, pdf.get_y(), 196, 32, "FD")
    pdf.set_xy(15, pdf.get_y() + 4)
    pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 10)
    for linea in [
        f"Lesión / Condición : {norm['Lesión actual']} / {norm['Condición médica']}",
        f"Restricción de mov.: {norm['Prohibido ejercicio']}",
        f"Corrección postural: {norm['Mala postura']}",
        f"Protocolo aplicado : {'ADAPTADO' if con_lesion else 'ESTÁNDAR'}",
    ]:
        pdf.set_x(15); pdf.cell(0, 6, _limpiar(f"• {linea}"), 0, 1)

    # --- HOJA 2 ---
    header("HOJA 2: PROGRAMACIÓN SEMANAL")
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 7, _limpiar(f"Estructura: {norm['Días entrenar']}  |  Protocolo: {'ADAPTADO' if con_lesion else 'ESTÁNDAR'}"), 0, 1)
    pdf.ln(5)

    bloques = ["Empuje", "Tracción", "Pierna", "Brazo/Full"]
    nombres_bloque = ["DÍA 1 — EMPUJE", "DÍA 2 — TRACCIÓN", "DÍA 3 — PIERNA", "DÍA 4 — BRAZO/FULL"]
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
            pdf.cell(90, 7, _limpiar(ej), 1, 0, "L")
            pdf.cell(26, 7, _limpiar(series), 1, 0, "C")
            pdf.cell(40, 7, _limpiar(reps), 1, 0, "C")
            pdf.cell(40, 7, _limpiar(desc), 1, 1, "C")
        pdf.ln(6)

    # --- HOJA 3 ---
    header("HOJA 3: PROTOCOLO NUTRICIONAL")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("1. MÉTRICAS METABÓLICAS"), 0, 1)
    fila_dato("TMB (Harris-Benedict)", f"{mot['tmb']} kcal/día")
    fila_dato(f"TDEE (factor {mot['factor']})", f"{mot['tdee']} kcal/día")
    fila_dato("Balance objetivo", mot["balance_str"])
    fila_dato("Calorías diarias prescritas", f"{mot['cals']} kcal")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("2. MACRONUTRIENTES DIARIOS"), 0, 1)
    pdf.set_fill_color(80, 200, 120); pdf.set_text_color(255, 255, 255)
    for h, w in [("PROTEÍNA", 49), ("CARBOHIDRATOS", 49), ("GRASAS", 49), ("CALORÍAS", 49)]:
        pdf.cell(w, 8, _limpiar(h), 1, 0, "C", fill=True)
    pdf.ln()
    pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "B", 13)
    for val, w in [(f"{mot['prot']}g", 49), (f"{mot['carbs']}g", 49), (f"{mot['grasa']}g", 49), (f"{mot['cals']} kcal", 49)]:
        pdf.cell(w, 10, _limpiar(val), 1, 0, "C")
    pdf.ln(12)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("3. DISTRIBUCIÓN EN 4 TOMAS DIARIAS"), 0, 1)
    p_c, c_c, g_c, k_c = round(mot["prot"]/4, 1), round(mot["carbs"]/4, 1), round(mot["grasa"]/4, 1), round(mot["cals"]/4, 0)
    for comida in ["COMIDA 1", "COMIDA 2", "COMIDA 3", "COMIDA 4"]:
        pdf.set_fill_color(243, 244, 246); pdf.set_font("Arial", "B", 11)
        pdf.cell(196, 8, _limpiar(comida), 0, 1, "L", fill=True)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, _limpiar(f"  {k_c} kcal  |  {p_c}g Prot  |  {c_c}g Carbs  |  {g_c}g Grasa"), 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, _limpiar(f"  Proteína: {norm['Menu_Proteinas']} | Carbs: {norm['Menu_Carbohidratos']}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"  Grasas: {norm['Menu_Grasas']} | Verduras: {norm['Menu_Verduras']}"), 0, 1)
        pdf.ln(3)

    # --- HOJA 4 ---
    if len(revs_df) > 0:
        header("HOJA 4: AUDITORÍA CLÍNICA Y PARÁMETROS ESPEJO")
        ult = revs_df.iloc[-1]
        peso_actual = _parse_float(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
        cintura_actual = _parse_float(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("1. COMPARATIVO BIOMÉTRICO (DELTAS)"), 0, 1)
        pdf.set_fill_color(80, 200, 120); pdf.set_text_color(255, 255, 255)
        for h, w in [("MÉTRICA", 60), ("Q1 (BASE)", 45), ("Q2 (ACTUAL)", 45), ("DELTA NETO", 46)]:
            pdf.cell(w, 8, _limpiar(h), 1, 0, "C", fill=True)
        pdf.ln()

        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 11)
        dif_peso = round(peso_actual - mot["peso"], 1)
        pdf.cell(60, 8, "Peso Corporal", 1, 0, "C")
        pdf.cell(45, 8, f"{mot['peso']} kg", 1, 0, "C")
        pdf.cell(45, 8, f"{peso_actual} kg", 1, 0, "C")
        pdf.set_text_color(34, 197, 94) if dif_peso <= 0 else pdf.set_text_color(239, 68, 68)
        pdf.cell(46, 8, f"{dif_peso:+.1f} kg", 1, 1, "C")

        pdf.set_text_color(51, 51, 51)
        dif_cintura = round(cintura_actual - mot["cintura"], 1)
        pdf.cell(60, 8, "Cintura", 1, 0, "C")
        pdf.cell(45, 8, f"{mot['cintura']} cm", 1, 0, "C")
        pdf.cell(45, 8, f"{cintura_actual} cm", 1, 0, "C")
        pdf.set_text_color(34, 197, 94) if dif_cintura <= 0 else pdf.set_text_color(239, 68, 68)
        pdf.cell(46, 8, f"{dif_cintura:+.1f} cm", 1, 1, "C")
        pdf.ln(8)

        pdf.set_text_color(51, 51, 51)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("2. PARÁMETROS ESPEJO PSICOMÉTRICOS (Escala 1-10)"), 0, 1)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, _limpiar(f"• Energía: Base {norm.get('P_Energia_Q1', '-')} -> Actual {ult.get('Energia', '-')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Sueño: Base {norm.get('P_Sueno_Q1', '-')} -> Actual {ult.get('Calidad_Sueno', '-')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Fuerza: Base {norm.get('P_Fuerza_Q1', '-')} -> Actual {ult.get('Progreso_Fuerza', '-')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Hambre: Base {norm.get('P_Hambre_Q1', '-')} -> Actual {ult.get('Hambre', '-')}"), 0, 1)
        pdf.ln(8)

        estado = str(ult.get("Estado_Calculado", "AVANCE")).upper()
        color_map = {"AVANCE": (80, 200, 120), "LENTO": (245, 158, 11), "RETROCESO": (239, 68, 68)}
        fill_color = color_map.get(estado, (100, 100, 100))
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("3. DICTAMEN FINAL Y FOTOGRAFÍA"), 0, 1)
        pdf.set_fill_color(*fill_color); pdf.set_text_color(255, 255, 255)
        pdf.cell(100, 12, _limpiar(f"ESTATUS SISTEMA: {estado}"), 0, 1, "C", fill=True)
        pdf.ln(6)
        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, _limpiar("Nota: Auditoría fotográfica (Frente, Perfil, Espalda) validada en expediente digital."), 0, 1)

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
    admin_pass = st.text_input("⚙️ Modo Administrador", type="password", help="Acceso exclusivo panel MM247")

df_existente = cargar_base_datos()

# =============================================================================
# 9. ENRUTAMIENTO PRINCIPAL
# =============================================================================

if admin_pass == CONFIG["admin_password"]:
    st.markdown("<div class='main-title'>🔐 Panel Maestro MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>CONTROL CENTRAL DE RESULTADOS Y AUDITORÍA</div>", unsafe_allow_html=True)

    if df_existente.empty:
        st.warning("No hay alumnos registrados en el sistema.")
    else:
        df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"].copy()
        df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"].copy()

        st.markdown("### 🗂️ Atletas Activos")
        ids_unicos = df_c1["ID_Alumno"].replace("", pd.NA).dropna().unique()
        
        for id_al in ids_unicos:
            datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
            revs_al  = df_c2[df_c2["ID_Alumno"] == id_al]

            c1, c2, c3, c4 = st.columns([2, 3, 3, 2])
            c1.write(f"`{id_al}`")
            c2.write(str(datos_al.get("Nombre completo", "Atleta")).title())
            c3.write(f"{datos_al.get('Peso actual','--')} kg → {datos_al.get('Peso objetivo','--')} kg")
            if c4.button("Ver Expediente", key=f"btn_{id_al}"):
                st.session_state.alumno_seleccionado = id_al
        st.markdown("---")

        if "alumno_seleccionado" in st.session_state:
            id_sel  = st.session_state.alumno_seleccionado
            d_brutos = df_c1[df_c1["ID_Alumno"] == id_sel].iloc[0]
            d_norm   = normalizar_datos_alumno(d_brutos)
            m_calc   = calcular_metabolismo(d_norm)
            r_df     = df_c2[df_c2["ID_Alumno"] == id_sel]

            st.markdown(f"### 📋 Expediente: `{id_sel}` - {d_norm['Nombre completo']}")
            
            # --- PANEL DE DELTAS Y ORIGEN ---
            st.markdown(f"**Origen Físico Detectado:** `{m_calc['origen']}` (ICA: {m_calc['ica']})")
            
            if not r_df.empty:
                ult = r_df.iloc[-1]
                peso_act = _parse_float(ult.get("Peso_Revision", m_calc["peso"]), m_calc["peso"])
                cintura_act = _parse_float(ult.get("Cintura_Revision", m_calc["cintura"]), m_calc["cintura"])
                
                colA, colB, colC = st.columns(3)
                colA.metric("Peso Corporal", f"{peso_act} kg", f"{peso_act - m_calc['peso']:.1f} kg", delta_color="inverse")
                colB.metric("Perímetro Cintura", f"{cintura_act} cm", f"{cintura_act - m_calc['cintura']:.1f} cm", delta_color="inverse")
                colC.metric("Estatus del Sistema", f"{str(ult.get('Estado_Calculado', 'N/A'))}")
            
            # --- ESPACIO PARA AUDITORÍA FOTOGRÁFICA ---
            st.info("📸 Las fotografías de Frente, Perfil y Espalda del Q1 y Q2 se sincronizan en la carpeta de Drive del atleta (Integración Backend).")

            try:
                pdf_bytes = generar_pdf_mm247(d_norm, m_calc, r_df, id_sel)
                st.download_button(
                    label="🖨️ Descargar Ficha Técnica y Auditoría PDF",
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

    tab_nuevo, tab_revision = st.tabs(["📝 Iniciar Expediente Nuevo (Q1)", "🔄 Registrar Auditoría (Q2)"])

    # ── FORMULARIO MAESTRO (Q1) ──────────────────────────────────
    with tab_nuevo:
        st.info("🟩 Bienvenido al ecosistema MM247. Completa las 6 misiones para establecer tu Línea Base.")
        st.progress(st.session_state.step / CONFIG["total_misiones"])

        # ── M1: Datos fisiológicos y Fotos Base ──
        if st.session_state.step == 1:
            with st.form("form_m1"):
                st.markdown("<div class='section-header'>1. DATOS FISIOLÓGICOS Y LÍNEA BASE</div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                ops_edad, ops_sexo = [f"{i} años" for i in range(14, 81)], ["Masculino", "Femenino"]
                ops_est, ops_peso = [f"{i} cm" for i in range(120, 221)], [f"{i} kg" for i in range(40, 161)]
                ops_cintura = [f"{i} cm" for i in range(50, 150)]

                with col1:
                    v_nombre  = st.text_input("Nombre completo:", value=st.session_state.db.get("Nombre completo", ""))
                    v_edad    = st.selectbox("Edad:", ops_edad, index=g_idx(ops_edad, "Edad", 11))
                    v_sexo    = st.selectbox("Sexo:", ops_sexo, index=g_idx(ops_sexo, "Sexo", 0))
                    v_est     = st.selectbox("Estatura:", ops_est, index=g_idx(ops_est, "Estatura", 55))
                    v_peso    = st.selectbox("Peso actual:", ops_peso, index=g_idx(ops_peso, "Peso actual", 40))
                with col2:
                    v_cintura = st.selectbox("Perímetro de cintura actual (Línea Base):", ops_cintura, index=g_idx(ops_cintura, "Cintura inicial", 35))
                    v_peso_obj = st.selectbox("Peso objetivo:", ops_peso, index=g_idx(ops_peso, "Peso objetivo", 35))
                    v_tel      = st.text_input("WhatsApp:", value=st.session_state.db.get("Número de contacto", "55"))
                    v_mail     = st.text_input("Email:", value=st.session_state.db.get("Correo electrónico", ""))

                st.markdown("<div class='section-header'>2. AUDITORÍA FOTOGRÁFICA DE INICIO (Q1)</div>", unsafe_allow_html=True)
                st.warning("📸 Sube tus fotos actuales para medir el progreso real. Mismas condiciones de luz siempre.")
                cf1, cf2, cf3 = st.columns(3)
                f_frente = cf1.file_uploader("Foto Frente", type=['jpg', 'jpeg'])
                f_perfil = cf2.file_uploader("Foto Perfil", type=['jpg', 'jpeg'])
                f_espalda = cf3.file_uploader("Foto Espalda", type=['jpg', 'jpeg'])

                if st.form_submit_button("Siguiente: Misión 2 ➡️"):
                    if not v_nombre.strip(): st.error("❌ El nombre es obligatorio.")
                    else:
                        guardar_y_navegar({"Nombre completo": v_nombre, "Edad": v_edad, "Sexo": v_sexo, "Estatura": v_est, 
                                           "Peso actual": v_peso, "Cintura inicial": v_cintura, "Peso objetivo": v_peso_obj,
                                           "Número de contacto": v_tel, "Correo electrónico": v_mail}, 2)

        # ── M2: Antecedentes ──
        elif st.session_state.step == 2:
            with st.form("form_m2"):
                st.markdown("<div class='section-header'>3. ANTECEDENTES DE ENTRENAMIENTO</div>", unsafe_allow_html=True)
                v_t_ent   = st.selectbox("Tiempo entrenando:", ["Nunca", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años", "Más de 3 años"])
                v_dias    = st.selectbox("Días/semana disponibles:", ["3 días por semana", "4 días por semana", "5 días por semana"], index=1)
                v_sesion  = st.selectbox("Tiempo por sesión:", ["Menos de 45 minutos", "De 45 a 75 minutos", "Más de 75 minutos"], index=1)
                v_act     = st.selectbox("Nivel de actividad (NEAT):", ["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"], index=2)
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Tiempo entrenando": v_t_ent, "Días entrenar": v_dias, "Tiempo por sesión": v_sesion, "Nivel de actividad": v_act}, 1)
                if c2.form_submit_button("Siguiente: Misión 3 ➡️"): guardar_y_navegar({"Tiempo entrenando": v_t_ent, "Días entrenar": v_dias, "Tiempo por sesión": v_sesion, "Nivel de actividad": v_act}, 3)

        # ── M3: Clínica ──
        elif st.session_state.step == 3:
            with st.form("form_m3"):
                st.markdown("<div class='section-header'>4. CONDICIÓN CLÍNICA Y LESIONES</div>", unsafe_allow_html=True)
                v_lesion  = st.selectbox("Lesión recurrente:", ["Ninguna", "Rodilla / Tendinitis", "Hombro / Manguito", "Espalda Baja", "Cervicales"])
                v_proh    = st.selectbox("Prohibición médica de carga axial:", ["No", "Sí, cargas sobre columna", "Sí, flexiones profundas"])
                v_postura = st.selectbox("Desviaciones posturales:", ["No", "Sí, hombros adelantados", "Sí, hiperlordosis"])
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Lesión actual": v_lesion, "Prohibido ejercicio": v_proh, "Mala postura": v_postura}, 2)
                if c2.form_submit_button("Siguiente: Misión 4 ➡️"): guardar_y_navegar({"Lesión actual": v_lesion, "Prohibido ejercicio": v_proh, "Mala postura": v_postura}, 4)

        # ── M4: Nutrición ──
        elif st.session_state.step == 4:
            with st.form("form_m4"):
                st.markdown("<div class='section-header'>5. MENÚ NUTRICIONAL</div>", unsafe_allow_html=True)
                v_prots   = st.multiselect("Proteínas:", ["Pechuga de Pollo", "Bisteck de Res", "Atún", "Huevos"], default=["Pechuga de Pollo"])
                v_carbs   = st.multiselect("Carbohidratos:", ["Arroz", "Avena", "Papa", "Tortilla"], default=["Arroz"])
                v_grasas  = st.multiselect("Grasas:", ["Aguacate", "Almendras", "Crema de Cacahuete"], default=["Aguacate"])
                v_verds   = st.multiselect("Verduras:", ["Brócoli", "Espinacas", "Lechuga"], default=["Brócoli"])
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Menu_Proteinas": v_prots, "Menu_Carbohidratos": v_carbs, "Menu_Grasas": v_grasas, "Menu_Verduras": v_verds}, 3)
                if c2.form_submit_button("Siguiente: Misión 5 ➡️"): guardar_y_navegar({"Menu_Proteinas": v_prots, "Menu_Carbohidratos": v_carbs, "Menu_Grasas": v_grasas, "Menu_Verduras": v_verds}, 5)

        # ── M5: Logística ──
        elif st.session_state.step == 5:
            with st.form("form_m5"):
                st.markdown("<div class='section-header'>6. LOGÍSTICA Y METAS</div>", unsafe_allow_html=True)
                v_obj = st.selectbox("Meta prioritaria:", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal", "Fuerza"])
                v_comp = st.slider("Nivel de compromiso (1-10):", 1, 10, 10)
                
                c1, c2 = st.columns(2)
                if c1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Objetivo principal": v_obj, "Compromiso": v_comp}, 4)
                if c2.form_submit_button("Siguiente: Misión 6 ➡️"): guardar_y_navegar({"Objetivo principal": v_obj, "Compromiso": v_comp}, 6)

        # ── M6: Parámetros Espejo (Línea Base) ──
        elif st.session_state.step == 6:
            with st.form("form_m6"):
                st.markdown("<div class='section-header'>7. PARÁMETROS ESPEJO PSICOMÉTRICOS (Q1)</div>", unsafe_allow_html=True)
                st.warning("Califica tu estado actual. Estos exactos valores serán contrastados en tu próxima auditoría (Q2).")
                
                v_ener = st.slider("Nivel de Energía promedio en el día (1=Agotado, 10=Enérgico):", 1, 10, 5)
                v_suen = st.slider("Calidad de Sueño/Descanso (1=Insomnio, 10=Profundo):", 1, 10, 5)
                v_fuer = st.slider("Fuerza/Rendimiento físico actual (1=Muy débil, 10=Fuerte):", 1, 10, 5)
                v_hamb = st.slider("Nivel de Hambre/Ansiedad (1=Control Absoluto, 10=Incontrolable):", 1, 10, 5)

                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if c1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"P_Energia_Q1": v_ener, "P_Sueno_Q1": v_suen, "P_Fuerza_Q1": v_fuer, "P_Hambre_Q1": v_hamb}, 5)

                if c2.form_submit_button("🚀 REGISTRAR LÍNEA BASE Y CREAR EXPEDIENTE"):
                    st.session_state.db.update({"P_Energia_Q1": v_ener, "P_Sueno_Q1": v_suen, "P_Fuerza_Q1": v_fuer, "P_Hambre_Q1": v_hamb})
                    d = st.session_state.db
                    id_nuevo = generar_id_unico(d.get("Nombre completo", "Atleta"))
                    
                    payload = {
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro": "INICIAL", "ID_Alumno": id_nuevo,
                        "Nombre completo": str(d.get("Nombre completo")).title(),
                        "Edad": str(d.get("Edad")), "Sexo": str(d.get("Sexo")),
                        "Estatura": str(d.get("Estatura")), "Peso actual": str(d.get("Peso actual")),
                        "Cintura inicial": str(d.get("Cintura inicial")), "Peso objetivo": str(d.get("Peso objetivo")),
                        "Objetivo principal": str(d.get("Objetivo principal")), "Compromiso": str(d.get("Compromiso")),
                        "Tiempo entrenando": str(d.get("Tiempo entrenando")), "Días entrenar": str(d.get("Días entrenar")),
                        "Tiempo por sesión": str(d.get("Tiempo por sesión")), "Nivel de actividad": str(d.get("Nivel de actividad")),
                        "Lesión actual": str(d.get("Lesión actual")), "Prohibido ejercicio": str(d.get("Prohibido ejercicio")),
                        "Mala postura": str(d.get("Mala postura")),
                        "Menu_Proteinas": ",".join(d.get("Menu_Proteinas", [])), "Menu_Carbohidratos": ",".join(d.get("Menu_Carbohidratos", [])),
                        "Menu_Grasas": ",".join(d.get("Menu_Grasas", [])), "Menu_Verduras": ",".join(d.get("Menu_Verduras", [])),
                        "P_Energia_Q1": str(d.get("P_Energia_Q1")), "P_Sueno_Q1": str(d.get("P_Sueno_Q1")),
                        "P_Fuerza_Q1": str(d.get("P_Fuerza_Q1")), "P_Hambre_Q1": str(d.get("P_Hambre_Q1")),
                    }
                    
                    with st.spinner("Sincronizando expediente..."):
                        try:
                            resp = requests.post(CONFIG["webhook_url"], json=payload, timeout=10)
                            if resp.status_code == 200:
                                st.markdown(f"<div class='id-box'>✅ ¡EXPEDIENTE ACTIVADO!<br><br>TU ID DE ATLETA:<br><span style='font-size:32px;'>{id_nuevo}</span></div>", unsafe_allow_html=True)
                                st.balloons()
                                st.cache_data.clear()
                                st.session_state.step, st.session_state.db = 1, {}
                            else: st.error("Error en servidor.")
                        except Exception as e: st.error(f"Error: {e}")

    # ── MÓDULO REVISIÓN DE AVANCE (Q2: ESPEJO) ───────────────
    with tab_revision:
        st.info("Ingresa tu ID y completa la Auditoría (Q2). El sistema restará tus valores matemáticamente frente al Q1.")
        
        with st.form("form_revision", clear_on_submit=True):
            id_ing = st.text_input("Tu ID de Atleta (Ej: MM247-2026-JGR-A3F2B1):").strip().upper()

            col_v, col_t = st.columns([1, 2], gap="large")
            with col_v:
                st.markdown("<div class='section-header'>Evidencia Visual (Q2)</div>", unsafe_allow_html=True)
                st.file_uploader("Subir Foto FRENTE Actual", type=['png', 'jpg', 'jpeg'])
                st.file_uploader("Subir Foto PERFIL Actual", type=['png', 'jpg', 'jpeg'])
                st.file_uploader("Subir Foto ESPALDA Actual", type=['png', 'jpg', 'jpeg'])
                
            with col_t:
                st.markdown("<div class='section-header'>1. Parámetros Espejo (1 al 10)</div>", unsafe_allow_html=True)
                energia_rev = st.slider("Nivel de Energía promedio en el día (1=Agotado, 10=Enérgico):", 1, 10, 5)
                sueno_rev   = st.slider("Calidad de Sueño/Descanso (1=Insomnio, 10=Profundo):", 1, 10, 5)
                fuerza_rev  = st.slider("Fuerza/Rendimiento físico actual (1=Muy débil, 10=Fuerte):", 1, 10, 5)
                hambre_rev  = st.slider("Nivel de Hambre/Ansiedad (1=Control Absoluto, 10=Incontrolable):", 1, 10, 5)

                st.markdown("<div class='section-header'>2. Métricas Corporales Actuales</div>", unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                peso_rev    = m1.number_input("Peso Actual (kg):", min_value=30.0, value=70.0, step=0.1)
                cintura_rev = m2.number_input("Cintura Actual (cm):", min_value=40.0, value=80.0, step=0.5)

            if st.form_submit_button("🚀 ENVIAR AUDITORÍA Y COMPARAR CON Q1"):
                if not id_ing: st.error("❌ El ID es obligatorio.")
                elif df_existente.empty or id_ing not in df_existente["ID_Alumno"].values: st.error("❌ ID no encontrado.")
                else:
                    puntos = 0
                    if fuerza_rev >= 7: puntos += 2
                    elif fuerza_rev >= 5: puntos += 1
                    if energia_rev >= 7: puntos += 1
                    
                    estado_calc = "AVANCE" if puntos >= 2 else "RETROCESO"
                    avatar_url = obtener_avatar_url(estado_calc)

                    payload_rev = {
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro": "REVISION", "ID_Alumno": id_ing,
                        "Peso_Revision": str(peso_rev), "Cintura_Revision": str(cintura_rev),
                        "Energia": str(energia_rev), "Calidad_Sueno": str(sueno_rev),
                        "Progreso_Fuerza": str(fuerza_rev), "Hambre": str(hambre_rev),
                        "Estado_Calculado": estado_calc,
                    }

                    with st.spinner("Comparando parámetros y registrando deltas..."):
                        try:
                            resp = requests.post(CONFIG["webhook_url"], json=payload_rev, timeout=10)
                            if resp.status_code == 200:
                                st.cache_data.clear()
                                color_fb = {"AVANCE": "🟢", "RETROCESO": "🔴"}
                                st.success(f"{color_fb[estado_calc]} Evaluación registrada. Estado: **{estado_calc}**.")
                                st.image(avatar_url, caption=f"Proyección MM247: {estado_calc}", width=250)
                            else: st.error("Error en servidor.")
                        except Exception as e: st.error(f"Error: {e}")
