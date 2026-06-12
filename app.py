# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA CLÍNICA
   
   VERSIÓN 5.0 — CRUCE CLÍNICO, PLAN DE ACCIÓN Y DASHBOARD ANIMADO
================================================================================
"""

import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests
import uuid
import tempfile
import os

# =============================================================================
# 0. CONFIGURACIÓN CENTRAL (CONFIG) Y RUTINAS
# =============================================================================
CONFIG = {
    "page_title": "MM247",
    "page_icon": "🟩",
    "webhook_url": "https://script.google.com/macros/s/AKfycbx5vDCKmqpe-vsZ2fan0ZQoesLjajIHHHXHOZLtG7-w6-ts3uUl1WkZVHnPnn0F3Cbn/exec",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas",
    "admin_password": "MM247_Admin",
    "total_misiones": 7,
    "factores_actividad": {
        "Sedentario":            1.20,
        "Poco activo":           1.375,
        "Moderadamente activo":  1.55,
        "Muy activo":            1.725,
    },
    "rutinas": {
        "Inducción (1 Mes)": {
            "sin_lesion": [
                ("Sentadilla Goblet (Prevención y Fortalecimiento)", "3", "12-15", "60s"),
                ("Flexiones Asistidas o Regulares", "3", "8-12", "60s"),
                ("Remo con Mancuernas Soporte", "3", "10-12", "60s"),
                ("Puente de Glúteo", "3", "15-20", "45s"),
                ("Plancha Abdominal Estática", "3", "30-45s", "45s"),
            ],
            "con_lesion": [
                ("Prensa de Piernas (Carga Ligera)", "3", "15-20", "60s"),
                ("Press de Pecho en Máquina", "3", "12-15", "60s"),
                ("Jalón al Pecho Agarre Neutro", "3", "12-15", "60s"),
                ("Extensión de Cuádriceps Lenta", "3", "15-20", "45s"),
                ("Crunch Abdominal Suelo", "3", "15-20", "45s"),
            ]
        },
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
    },
}

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA
# =============================================================================
st.set_page_config(page_title=CONFIG["page_title"], page_icon=CONFIG["page_icon"], layout="wide")

# =============================================================================
# 2. ESTILOS CSS ANIMADOS
# =============================================================================
st.markdown("""
<style>
/* Animaciones */
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(80, 200, 120, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(80, 200, 120, 0); } 100% { box-shadow: 0 0 0 0 rgba(80, 200, 120, 0); } }

/* Fondo y textos base */
.stApp { background-color: #F8F9FA; color: #333333; }

/* Corrección de visibilidad de Labels en Modo Oscuro */
label[data-testid="stWidgetLabel"] p, div[data-testid="stForm"] label p { color: #2C3E50 !important; font-weight: 700 !important; }

/* Títulos y Subtítulos (Diseño MM247 con Mancuerna de fondo) */
.main-title-container { text-align: center; position: relative; margin-bottom: 0px; animation: fadeIn 0.8s ease-out; }
.main-title-bg { 
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
    font-size: 80px; opacity: 0.05; z-index: 0; 
}
.main-title { 
    font-size: 60px; font-weight: 900; color: #2C3E50; position: relative; 
    z-index: 1; letter-spacing: 2px; text-transform: uppercase; margin: 0;
}
.subtitle { font-size: 16px; color: #7F8C8D; text-align: center; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 3px; animation: fadeIn 1s ease-out; }

/* Encabezados de sección */
.section-header { 
    font-size: 20px; font-weight: 700; color: #50C878; margin-top: 30px; margin-bottom: 15px; 
    border-bottom: 2px solid #E5E7EB; padding-bottom: 5px; text-transform: uppercase; 
}

/* Paneles y Tarjetas */
div[data-testid="stForm"] { 
    background: #FFFFFF; padding: 30px; border-radius: 16px; border: 1px solid #E5E7EB; 
    box-shadow: 0 8px 30px rgba(0,0,0,0.04); animation: fadeIn 0.5s ease-out;
}

.metric-card {
    background-color: #FFFFFF; padding: 20px; border-radius: 12px; text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03); border-bottom: 4px solid #50C878;
    margin-bottom: 20px; border-top: 1px solid #E5E7EB; border-left: 1px solid #E5E7EB; border-right: 1px solid #E5E7EB;
    transition: transform 0.3s ease;
}
.metric-card:hover { transform: translateY(-5px); }
.metric-title { font-size: 12px; color: #7F8C8D; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
.metric-value { font-size: 28px; color: #2C3E50; font-weight: 900; margin-top: 5px; }

/* Caja de ID (Verde Esmeralda) */
.id-box { 
    background: linear-gradient(135deg, #50C878 0%, #3CB371 100%); border-left: 5px solid #2E8B57; 
    padding: 25px; border-radius: 12px; color: #FFFFFF; text-align: center; font-weight: bold; margin-top: 20px; 
    animation: pulse 2s infinite;
}

/* Botones con Degradado Esmeralda */
div.stButton > button, div[data-testid="stForm"] button {
    background: linear-gradient(90deg, #50C878 0%, #3CB371 100%); color: white; width: 100%; 
    border-radius: 8px; font-weight: 700; height: 50px; border: none; text-transform: uppercase; 
    letter-spacing: 1px; transition: all 0.3s ease;
}
div.stButton > button:hover, div[data-testid="stForm"] button:hover {
    transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 8px 20px rgba(80, 200, 120, 0.4); color: white;
}

/* Status Cards */
.status-avance { background: #E8F5E9; border-left: 5px solid #4CAF50; padding: 15px; border-radius: 8px; color: #2E7D32; font-weight: bold;}
.status-lento { background: #FFF8E1; border-left: 5px solid #FFC107; padding: 15px; border-radius: 8px; color: #F57F17; font-weight: bold;}
.status-retroceso { background: #FFEBEE; border-left: 5px solid #F44336; padding: 15px; border-radius: 8px; color: #C62828; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2.5 LÓGICA DE AVATARES (SISTEMA DINÁMICO ROBUSTO)
# =============================================================================
def obtener_avatar_url(estatus, nombre="Atleta"):
    nom_formateado = str(nombre).replace(" ", "+")
    if estatus == "AVANCE": bg = "50C878"
    elif estatus == "RETROCESO": bg = "EF4444"
    else: bg = "F59E0B"
    # Generador de Avatar garantizado que no se cae
    return f"https://ui-avatars.com/api/?name={nom_formateado}&background={bg}&color=fff&size=256&font-size=0.4&bold=true&rounded=true"

# =============================================================================
# 3. CAPA DE DATOS (NORMALIZACIÓN EXACTA)
# =============================================================================
@st.cache_data(ttl=60)
def cargar_base_datos() -> pd.DataFrame:
    try:
        url = f"{CONFIG['sheet_url']}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        if "ID_Alumno" not in df.columns: df["ID_Alumno"] = ""
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = "INICIAL"
        return df
    except Exception:
        return pd.DataFrame()

def generar_id_unico(nombre: str) -> str:
    iniciales = "".join([p[0].upper() for p in str(nombre).strip().split() if p])[:3]
    if not iniciales: iniciales = "MM"
    sufijo = str(uuid.uuid4().hex)[:6].upper()
    return f"MM247-{datetime.datetime.now().year}-{iniciales}-{sufijo}"

def normalizar_datos_alumno(datos_raw: pd.Series) -> dict:
    def buscar(key: str, defecto: str = "") -> str:
        if key in datos_raw.index:
            val = datos_raw[key]
            if pd.notna(val) and str(val).strip() not in ("", "nan"):
                return str(val).strip()
        return defecto

    return {
        "Nombre completo":    buscar("Nombre completo", "Atleta"),
        "Edad":               buscar("Edad", "25"),
        "Sexo":               buscar("Sexo", "Masculino"),
        "Estatura":           buscar("Estatura", "175"),
        "Peso actual":        buscar("Peso actual", "80"),
        "Cintura inicial":    buscar("Cintura inicial", "85"),
        "Peso objetivo":      buscar("Peso objetivo", "75"),
        "Nivel de actividad": buscar("Nivel de actividad", "Moderadamente activo"),
        "Objetivo principal": buscar("Objetivo principal", "Recomposición corporal"),
        "Tiempo entrenando":  buscar("Tiempo entrenando", "Menos de 6 meses"),
        "Lesión actual":      buscar("Lesión actual", "Ninguna"),
        "Prohibido ejercicio":buscar("Prohibido ejercicio", "No"),
        "Mala postura":       buscar("Mala postura", "No"),
        "Días entrenar":      buscar("Días entrenar", "4 días por semana"),
        "Tiempo por sesión":  buscar("Tiempo por sesión", "60 minutos"),
        "Compromiso":         buscar("Compromiso", "10"),
        "Menu_Proteinas":     buscar("Menu_Proteinas", "Pechuga de Pollo"),
        "Menu_Carbohidratos": buscar("Menu_Carbohidratos", "Arroz Blanco"),
        "Menu_Grasas":        buscar("Menu_Grasas", "Aguacate"),
        "Menu_Verduras":      buscar("Menu_Verduras", "Brócoli"),
        "P_Energia_Q1":       buscar("P_Energia_Q1", "5"),
        "P_Sueno_Q1":         buscar("P_Sueno_Q1", "5"),
        "P_Fuerza_Q1":        buscar("P_Fuerza_Q1", "5"),
        "P_Hambre_Q1":        buscar("P_Hambre_Q1", "5"),
        "Historial_Est":      buscar("Historial de Estancamiento", "Menos de 1 mes"),
        "Recuperacion_Base":  buscar("Capacidad de Recuperación Base", "Normal"),
        "Biofeedback_Dig":    buscar("Biofeedback Digestivo", "Sin molestias"),
        "Estres_Ext":         buscar("Carga de Estrés Externo", "5"),
    }

# =============================================================================
# 4. MOTOR METABÓLICO Y PLAN DE ACCIÓN CLÍNICO
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

def generar_plan_accion(q1_datos: dict, ult_rev: pd.Series, estado: str) -> list:
    plan = []
    adherencia = str(ult_rev.get("Adherencia Real al Sistema", "100%"))
    sobrecarga = str(ult_rev.get("Sobrecarga Progresiva", "Sí, en la mayoría"))
    tolerancia = str(ult_rev.get("Tolerancia Metabólica", "Digestión rápida y normal"))
    
    if "menos del 50%" in adherencia.lower() or "50%" in adherencia:
        plan.append("ADHERENCIA CRÍTICA: Reducir la complejidad del menú actual. Priorizar alimentos de fácil preparación y revisar picos de ansiedad.")
    if estado == "RETROCESO" and "No" in sobrecarga:
        plan.append("AJUSTE NEUROMUSCULAR: Descarga programada (Deload) de 1 semana. Reducir volumen de entrenamiento un 30% para disipar fatiga sistémica.")
    if "pesadez" in tolerancia.lower() or "inflamación" in tolerancia.lower():
        plan.append("BIOFEEDBACK: Ajuste en fuentes de carbohidratos. Rotar arroz/papa por avena/vegetales fibrosos para mejorar digestibilidad.")
    if estado == "AVANCE" and "Sí" in sobrecarga:
        plan.append("LUZ VERDE (INTENSIDAD): Mantener superávit/déficit intacto. Autorizado para aumentar cargas en ejercicios compuestos en un 5%.")
    
    if not plan:
        plan.append("MANTENIMIENTO ÓPTIMO: Parámetros estables. Continuar protocolo actual sin modificaciones agresivas.")
    return plan

# =============================================================================
# 5. MOTOR DE PDF (DISEÑO ESMERALDA Y HOJA 4 CLÍNICA AVANZADA)
# =============================================================================
def _limpiar(texto: str) -> str:
    return str(texto).encode("latin-1", "replace").decode("latin-1")

def _tiene_lesion(norm: dict) -> bool:
    return norm.get("Lesión actual", "Ninguna").lower() != "ninguna" or norm.get("Prohibido ejercicio", "No").lower() != "no"

def generar_pdf_mm247(norm: dict, mot: dict, revs_df: pd.DataFrame, id_al: str) -> bytes:
    pdf = FPDF("P", "mm", "Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    con_lesion = _tiene_lesion(norm)
    
    t_ent = norm.get("Tiempo entrenando", "Menos de 6 meses")
    aplica_induccion = "Nunca" in t_ent or "Menos de 6 meses" in t_ent
    num_dias = int(str(norm.get("Días entrenar", "4")).strip()[0]) if str(norm.get("Días entrenar", "4")).strip()[0].isdigit() else 4

    def header(titulo: str):
        pdf.add_page()
        pdf.set_fill_color(80, 200, 120)
        pdf.rect(0, 0, 216, 30, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 24)
        pdf.set_xy(10, 8);  pdf.cell(100, 10, "MM247",  0, 0, "L")
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

    # --- HOJA 1: CLÍNICA ---
    header("HOJA 1: PERFIL CLÍNICO Y LÍNEA BASE")
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, _limpiar("1. DATOS GENERALES Y ORIGEN FÍSICO"), 0, 1)
    fila_dato("Cliente", norm["Nombre completo"])
    fila_dato("Edad / Sexo", f"{int(mot['edad'])} años / {mot['genero']}")
    fila_dato("Estatura / Peso Base", f"{mot['estatura']} cm / {mot['peso']} kg")
    fila_dato("Punto de Partida (Origen)", f"{mot['origen']} (ICA: {mot['ica']})")
    fila_dato("Objetivo principal", norm.get("Objetivo principal", "--"))
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(239, 68, 68)
    pdf.cell(0, 10, _limpiar("2. ALERTAS BIOMECÁNICAS Y CLÍNICAS"), 0, 1)
    pdf.set_fill_color(254, 242, 242); pdf.set_draw_color(239, 68, 68)
    pdf.rect(10, pdf.get_y(), 196, 38, "FD")
    pdf.set_xy(15, pdf.get_y() + 4)
    pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 10)
    for linea in [
        f"Lesión Base : {norm['Lesión actual']}",
        f"Restricción Axial : {norm['Prohibido ejercicio']}",
        f"Corrección Postural : {norm['Mala postura']}",
        f"Estancamiento Prev: {norm['Historial_Est']}",
        f"Recuperación Base : {norm['Recuperacion_Base']}",
    ]:
        pdf.set_x(15); pdf.cell(0, 6, _limpiar(f"• {linea}"), 0, 1)

    # --- HOJA 2: PROGRAMACIÓN ---
    header("HOJA 2: PROGRAMACIÓN NEUROMUSCULAR")
    modo = "con_lesion" if con_lesion else "sin_lesion"
    
    if aplica_induccion:
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(46, 139, 87)
        pdf.cell(0, 7, _limpiar("PROTOCOLO ACTIVO: SISTEMA DE INDUCCIÓN (1 MES) - PREVENCIÓN Y FORTALECIMIENTO"), 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(51, 51, 51)
        pdf.cell(0, 6, _limpiar("Estructura adaptada para acondicionamiento articular y corrección técnica antes de carga pesada."), 0, 1)
        pdf.ln(5)
        bloques = ["Inducción (1 Mes)"] * num_dias
        nombres_bloque = [f"DÍA {i+1} — FULL BODY ACONDICIONAMIENTO" for i in range(num_dias)]
    else:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, _limpiar(f"Estructura: {num_dias} Días | Protocolo: {'ADAPTADO' if con_lesion else 'ESTÁNDAR (HIPERTROFIA)'}"), 0, 1)
        pdf.ln(5)
        bloques = ["Empuje", "Tracción", "Pierna", "Empuje", "Tracción"][:num_dias]
        nombres_bloque = [f"DÍA {i+1} — {b.upper()}" for i, b in enumerate(bloques)]

    for i, bloque in enumerate(bloques):
        if bloque in CONFIG["rutinas"]:
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

    # --- HOJA 3: NUTRICIÓN ---
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

    # --- HOJA 4: AUDITORÍA CLÍNICA Y PLAN DE ACCIÓN ---
    if len(revs_df) > 0:
        header("HOJA 4: AUDITORÍA CLÍNICA, DELTAS Y PLAN DE ACCIÓN (Q2)")
        ult = revs_df.iloc[-1]
        peso_actual = _parse_float(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
        cintura_actual = _parse_float(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])
        estado = str(ult.get("Estado_Calculado", "AVANCE")).upper()

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("1. CRUCE BIOMÉTRICO (DELTAS Q1 vs Q2)"), 0, 1)
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

        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("2. PARÁMETROS ESPEJO Y ADHERENCIA"), 0, 1)
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, _limpiar(f"• Fuerza y Recuperación: Base {norm.get('P_Fuerza_Q1', '-')} -> Actual {ult.get('Progreso_Fuerza', '-')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Adherencia Real Declarada: {ult.get('Adherencia Real al Sistema', '--')}"), 0, 1)
        pdf.cell(0, 6, _limpiar(f"• Tolerancia Metabólica: {ult.get('Tolerancia Metabólica', '--')}"), 0, 1)
        pdf.ln(5)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("3. PLAN DE ACCIÓN CLÍNICO AUTOMATIZADO"), 0, 1)
        pdf.set_fill_color(243, 244, 246); pdf.rect(10, pdf.get_y(), 196, 30, "F")
        pdf.set_xy(15, pdf.get_y() + 4)
        pdf.set_font("Arial", "B", 10); pdf.set_text_color(44, 62, 80)
        plan_accion = generar_plan_accion(norm, ult, estado)
        for accion in plan_accion:
            pdf.set_x(15); pdf.multi_cell(180, 6, _limpiar(f"-> {accion}"), 0, "L")
        pdf.set_y(pdf.get_y() + 10)

        color_map = {"AVANCE": (80, 200, 120), "LENTO": (245, 158, 11), "RETROCESO": (239, 68, 68)}
        fill_color = color_map.get(estado, (100, 100, 100))
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, _limpiar("4. DICTAMEN FINAL Y FOTOGRAFÍA CRUZADA"), 0, 1)
        pdf.set_fill_color(*fill_color); pdf.set_text_color(255, 255, 255)
        pdf.cell(100, 12, _limpiar(f"ESTATUS SISTEMA: {estado}"), 0, 1, "C", fill=True)
        pdf.ln(6)
        pdf.set_text_color(51, 51, 51); pdf.set_font("Arial", "", 10)
        pdf.cell(0, 6, _limpiar("[ FOTOGRAFÍAS ALMACENADAS EN EXPEDIENTE DIGITAL ]"), 0, 1)
        pdf.cell(0, 6, _limpiar("Evidencia de Frente, Perfil y Espalda (Q1 vs Q2) verificada en base de datos central."), 0, 1)

    return pdf.output(dest="S").encode("latin-1", "ignore")

# =============================================================================
# 6. HELPERS DE NAVEGACIÓN STATE
# =============================================================================
def g_idx(lista: list, clave: str, default: int = 0) -> int:
    val = st.session_state.db.get(clave)
    return lista.index(val) if val in lista else default

def guardar_y_navegar(datos: dict, destino: int):
    st.session_state.db.update(datos)
    st.session_state.step = destino
    st.rerun()

# =============================================================================
# 7. INTERFAZ MAESTRA (SIDEBAR ADMIN Y ENRUTAMIENTO)
# =============================================================================
with st.sidebar:
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2936/2936886.png", width=100)
    admin_pass = st.text_input("⚙️ Acceso Maestro", type="password", help="Panel de Control MM247")

df_existente = cargar_base_datos()

# ─── VISTA ADMINISTRADOR (DASHBOARD) ─────────────────────────────────────────
if admin_pass == CONFIG["admin_password"]:
    st.markdown("""
    <div class='main-title-container'>
        <div class='main-title-bg'>🏋️‍♂️</div>
        <div class='main-title'>MM247</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>CONTROL CLÍNICO, CRUCES Y AVATARES 3D</div>", unsafe_allow_html=True)

    if df_existente.empty:
        st.warning("Base de datos en blanco. Esperando registros Q1.")
    else:
        df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"].copy()
        df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"].copy()

        ids_unicos = df_c1["ID_Alumno"].replace("", pd.NA).dropna().unique()
        
        col_list, col_det = st.columns([1, 2])
        
        with col_list:
            st.markdown("### 🗂️ Atletas Activos")
            for id_al in ids_unicos:
                datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
                if st.button(f"🔍 {id_al} - {datos_al.get('Nombre completo', 'Atleta')[:15]}", key=f"btn_{id_al}", use_container_width=True):
                    st.session_state.alumno_seleccionado = id_al

        with col_det:
            if "alumno_seleccionado" in st.session_state:
                id_sel = st.session_state.alumno_seleccionado
                d_brutos = df_c1[df_c1["ID_Alumno"] == id_sel].iloc[0]
                d_norm   = normalizar_datos_alumno(d_brutos)
                m_calc   = calcular_metabolismo(d_norm)
                r_df     = df_c2[df_c2["ID_Alumno"] == id_sel]

                st.markdown(f"### 📋 Expediente Clínico: `{id_sel}`")
                
                estado_actual = "SIN AUDITORÍA (SOLO Q1)"
                if not r_df.empty:
                    ult = r_df.iloc[-1]
                    estado_actual = str(ult.get("Estado_Calculado", "AVANCE")).upper()
                
                # Renderizado de Avatar y Status
                c_av, c_st = st.columns([1, 2])
                with c_av:
                    nombre_atleta = d_norm.get("Nombre completo", "Atleta")
                    st.image(obtener_avatar_url(estado_actual if not r_df.empty else "AVANCE", nombre_atleta), width=150)
                with c_st:
                    if estado_actual == "AVANCE": st.markdown(f"<div class='status-avance'>ESTADO: {estado_actual}<br>El sistema reporta sobrecarga positiva y buena adherencia.</div>", unsafe_allow_html=True)
                    elif estado_actual == "RETROCESO": st.markdown(f"<div class='status-retroceso'>ESTADO: {estado_actual}<br>Alerta de estancamiento. Revisar plan de acción en PDF.</div>", unsafe_allow_html=True)
                    else: st.markdown(f"<div class='status-lento'>ESTADO: {estado_actual}</div>", unsafe_allow_html=True)

                st.markdown("#### ⚖️ Deltas Biométricos (Q1 vs Actual)")
                peso_act = _parse_float(r_df.iloc[-1].get("Peso_Revision", m_calc["peso"]) if not r_df.empty else m_calc["peso"], m_calc["peso"])
                cintura_act = _parse_float(r_df.iloc[-1].get("Cintura_Revision", m_calc["cintura"]) if not r_df.empty else m_calc["cintura"], m_calc["cintura"])
                
                mA, mB, mC = st.columns(3)
                mA.markdown(f"<div class='metric-card'><div class='metric-title'>Peso Corporal</div><div class='metric-value'>{peso_act} kg</div><div style='color: {'#e74c3c' if peso_act > m_calc['peso'] else '#2ecc71'}; font-weight:bold;'>{peso_act - m_calc['peso']:+.1f} kg</div></div>", unsafe_allow_html=True)
                mB.markdown(f"<div class='metric-card'><div class='metric-title'>Cintura</div><div class='metric-value'>{cintura_act} cm</div><div style='color: {'#e74c3c' if cintura_act > m_calc['cintura'] else '#2ecc71'}; font-weight:bold;'>{cintura_act - m_calc['cintura']:+.1f} cm</div></div>", unsafe_allow_html=True)
                mC.markdown(f"<div class='metric-card'><div class='metric-title'>TDEE Prescrito</div><div class='metric-value'>{m_calc['cals']}</div><div style='color: #7f8c8d;'>kcal/día</div></div>", unsafe_allow_html=True)

                # =============================================================
                # NUEVO: VISUALIZACIÓN DE IMÁGENES DEL Q1 (PLACEHOLDERS DE DRIVE)
                # =============================================================
                st.markdown("#### 📸 Evidencia Visual (Registro Q1)")
                st.info("Las imágenes almacenadas en el sistema central para evaluación y cruce físico.")
                img_col1, img_col2, img_col3 = st.columns(3)
                
                # Usamos placeholders de estructura anatómica para mostrar dónde irían las fotos
                img_col1.image("https://dummyimage.com/200x300/2C3E50/ffffff.png&text=Frente+Q1", caption="Foto: Frente", use_container_width=True)
                img_col2.image("https://dummyimage.com/200x300/2C3E50/ffffff.png&text=Perfil+Q1", caption="Foto: Perfil", use_container_width=True)
                img_col3.image("https://dummyimage.com/200x300/2C3E50/ffffff.png&text=Espalda+Q1", caption="Foto: Espalda", use_container_width=True)

                try:
                    pdf_bytes = generar_pdf_mm247(d_norm, m_calc, r_df, id_sel)
                    st.download_button("🖨️ GENERAR Y DESCARGAR EXPEDIENTE PDF", data=pdf_bytes, file_name=f"MM247_Clinica_{id_sel}.pdf", mime="application/pdf")
                except Exception as err:
                    st.error(f"Error generando PDF: {err}")

elif admin_pass and admin_pass != CONFIG["admin_password"]:
    st.error("🔑 Clave maestra incorrecta.")

# ─── VISTA CLIENTE (FORMULARIOS Q1 Y Q2) ─────────────────────────────────────
else:
    st.markdown("""
    <div class='main-title-container'>
        <div class='main-title-bg'>🏋️‍♂️</div>
        <div class='main-title'>MM247</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>LÍNEA BASE (Q1) Y AUDITORÍA DE AVANCE (Q2)</div>", unsafe_allow_html=True)

    if "step" not in st.session_state: st.session_state.step = 1
    if "db"   not in st.session_state: st.session_state.db   = {}

    tab_q1, tab_q2 = st.tabs(["📝 CREAR EXPEDIENTE INICIAL (Q1)", "🔄 REGISTRAR AUDITORÍA (Q2)"])

    # ── FORMULARIO EXPEDIENTE INICIAL (Q1) ──────────────────────────────────
    with tab_q1:
        st.progress(st.session_state.step / CONFIG["total_misiones"])

        if st.session_state.step == 1:
            with st.form("f_m1"):
                st.markdown("<div class='section-header'>1. DATOS FISIOLÓGICOS BASE</div>", unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    v_nom = st.text_input("Nombre completo:", value=st.session_state.db.get("Nombre completo", ""))
                    v_edad = st.selectbox("Edad:", [f"{i} años" for i in range(14, 81)], index=11)
                    v_sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
                    v_est = st.selectbox("Estatura:", [f"{i} cm" for i in range(120, 221)], index=55)
                with c2:
                    v_peso = st.selectbox("Peso actual:", [f"{i} kg" for i in range(40, 161)], index=40)
                    v_cint = st.selectbox("Cintura actual:", [f"{i} cm" for i in range(50, 150)], index=35)
                    v_meta_p = st.selectbox("Peso objetivo:", [f"{i} kg" for i in range(40, 161)], index=35)
                    v_mail = st.text_input("Correo electrónico:", value=st.session_state.db.get("Correo electrónico", ""))

                if st.form_submit_button("Siguiente ➡️"):
                    if not v_nom.strip(): st.error("El nombre es requerido.")
                    else: guardar_y_navegar({"Nombre completo": v_nom, "Edad": v_edad, "Sexo": v_sexo, "Estatura": v_est, "Peso actual": v_peso, "Cintura inicial": v_cint, "Peso objetivo": v_meta_p, "Correo electrónico": v_mail}, 2)

        elif st.session_state.step == 2:
            with st.form("f_m2"):
                st.markdown("<div class='section-header'>2. EVIDENCIA VISUAL (FOTOGRAFÍAS Q1)</div>", unsafe_allow_html=True)
                st.warning("📸 Sube tus fotos iniciales. Estas se cruzarán con tus resultados en la Auditoría Q2.")
                f1, f2, f3 = st.columns(3)
                f_frente = f1.file_uploader("Frente (Obligatorio)", type=['jpg', 'jpeg', 'png'])
                f_perfil = f2.file_uploader("Perfil (Obligatorio)", type=['jpg', 'jpeg', 'png'])
                f_espalda = f3.file_uploader("Espalda (Obligatorio)", type=['jpg', 'jpeg', 'png'])
                
                c_b1, c_b2 = st.columns(2)
                if c_b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({}, 1)
                if c_b2.form_submit_button("Siguiente ➡️"): 
                    st.session_state.db["fotos_q1"] = "Cargadas" if (f_frente and f_perfil and f_espalda) else "Pendientes"
                    guardar_y_navegar({}, 3)

        elif st.session_state.step == 3:
            with st.form("f_m3"):
                st.markdown("<div class='section-header'>3. ANTECEDENTES Y ESTANCAMIENTO</div>", unsafe_allow_html=True)
                v_t_ent = st.selectbox("Tiempo entrenando:", ["Nunca", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años", "Más de 3 años"])
                v_dias = st.selectbox("Días disponibles/semana:", ["3 días por semana", "4 días por semana", "5 días por semana"])
                v_estancamiento = st.selectbox("Historial de Estancamiento (Sin ver cambios):", ["No estoy estancado", "Menos de 1 mes", "1 a 3 meses", "Más de 6 meses"])
                
                c_b1, c_b2 = st.columns(2)
                if c_b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Tiempo entrenando": v_t_ent, "Días entrenar": v_dias, "Historial de Estancamiento": v_estancamiento}, 2)
                if c_b2.form_submit_button("Siguiente ➡️"): guardar_y_navegar({"Tiempo entrenando": v_t_ent, "Días entrenar": v_dias, "Historial de Estancamiento": v_estancamiento}, 4)

        elif st.session_state.step == 4:
            with st.form("f_m4"):
                st.markdown("<div class='section-header'>4. PERFIL CLÍNICO Y BIOFEEDBACK</div>", unsafe_allow_html=True)
                v_lesion = st.selectbox("Lesión actual:", ["Ninguna", "Rodilla", "Hombro", "Espalda Baja", "Cervicales"])
                v_proh = st.selectbox("Prohibición carga axial:", ["No", "Sí, sobre columna", "Sí, flexiones profundas"])
                v_recup = st.selectbox("Capacidad de Recuperación Base (DOMS):", ["Recuperación rápida (Sin dolor excesivo)", "Normal", "Llego muy adolorido a la siguiente sesión"])
                v_dig = st.selectbox("Biofeedback Digestivo general:", ["Sin molestias", "Inflamación ocasional", "Gases y pesadez frecuente"])
                v_estres = st.slider("Carga de Estrés Externo (1=Mínimo, 10=Extremo):", 1, 10, 5)

                c_b1, c_b2 = st.columns(2)
                if c_b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Lesión actual": v_lesion, "Prohibido ejercicio": v_proh, "Capacidad de Recuperación Base": v_recup, "Biofeedback Digestivo": v_dig, "Carga de Estrés Externo": str(v_estres)}, 3)
                if c_b2.form_submit_button("Siguiente ➡️"): guardar_y_navegar({"Lesión actual": v_lesion, "Prohibido ejercicio": v_proh, "Capacidad de Recuperación Base": v_recup, "Biofeedback Digestivo": v_dig, "Carga de Estrés Externo": str(v_estres)}, 5)

        elif st.session_state.step == 5:
            with st.form("f_m5"):
                st.markdown("<div class='section-header'>5. NUTRICIÓN Y METAS</div>", unsafe_allow_html=True)
                v_obj = st.selectbox("Objetivo principal:", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal"])
                v_prots = st.multiselect("Proteínas preferidas:", ["Pechuga de Pollo", "Bisteck", "Atún", "Huevos"], default=["Pechuga de Pollo"])
                v_carbs = st.multiselect("Carbohidratos:", ["Arroz", "Avena", "Papa", "Tortilla"], default=["Arroz"])
                v_grasas = st.multiselect("Grasas:", ["Aguacate", "Almendras", "Crema de Cacahuete"], default=["Aguacate"])
                v_verds = st.multiselect("Verduras:", ["Brócoli", "Espinacas", "Lechuga"], default=["Brócoli"])
                
                c_b1, c_b2 = st.columns(2)
                if c_b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Objetivo principal": v_obj, "Menu_Proteinas": v_prots, "Menu_Carbohidratos": v_carbs, "Menu_Grasas": v_grasas, "Menu_Verduras": v_verds}, 4)
                if c_b2.form_submit_button("Siguiente ➡️"): guardar_y_navegar({"Objetivo principal": v_obj, "Menu_Proteinas": v_prots, "Menu_Carbohidratos": v_carbs, "Menu_Grasas": v_grasas, "Menu_Verduras": v_verds}, 6)

        elif st.session_state.step == 6:
            with st.form("f_m6"):
                st.markdown("<div class='section-header'>6. PARÁMETROS ESPEJO (LÍNEA BASE)</div>", unsafe_allow_html=True)
                v_ener = st.slider("Energía promedio en el día (1-10):", 1, 10, 5)
                v_suen = st.slider("Calidad de Sueño (1-10):", 1, 10, 5)
                v_fuer = st.slider("Fuerza actual (1-10):", 1, 10, 5)
                v_hamb = st.slider("Nivel de Hambre/Ansiedad (1-10):", 1, 10, 5)

                c_b1, c_b2 = st.columns(2)
                if c_b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"P_Energia_Q1": v_ener, "P_Sueno_Q1": v_suen, "P_Fuerza_Q1": v_fuer, "P_Hambre_Q1": v_hamb}, 5)
                if c_b2.form_submit_button("🚀 ACTIVAR EXPEDIENTE MM247"):
                    d = st.session_state.db
                    d.update({"P_Energia_Q1": v_ener, "P_Sueno_Q1": v_suen, "P_Fuerza_Q1": v_fuer, "P_Hambre_Q1": v_hamb})
                    
                    id_nuevo = generar_id_unico(d.get("Nombre completo", "Atleta"))
                    
                    payload = {
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro": "INICIAL", "ID_Alumno": id_nuevo,
                        "Nombre completo": str(d.get("Nombre completo")), "Edad": str(d.get("Edad")), "Sexo": str(d.get("Sexo")),
                        "Estatura": str(d.get("Estatura")), "Peso actual": str(d.get("Peso actual")), "Cintura inicial": str(d.get("Cintura inicial")),
                        "Peso objetivo": str(d.get("Peso objetivo")), "Correo electrónico": str(d.get("Correo electrónico")),
                        "Tiempo entrenando": str(d.get("Tiempo entrenando")), "Días entrenar": str(d.get("Días entrenar")),
                        "Lesión actual": str(d.get("Lesión actual")), "Prohibido ejercicio": str(d.get("Prohibido ejercicio")),
                        "Menu_Proteinas": ",".join(d.get("Menu_Proteinas", [])), "Menu_Carbohidratos": ",".join(d.get("Menu_Carbohidratos", [])),
                        "Menu_Grasas": ",".join(d.get("Menu_Grasas", [])), "Menu_Verduras": ",".join(d.get("Menu_Verduras", [])),
                        "Objetivo principal": str(d.get("Objetivo principal")),
                        "P_Energia_Q1": str(d.get("P_Energia_Q1")), "P_Sueno_Q1": str(d.get("P_Sueno_Q1")), 
                        "P_Fuerza_Q1": str(d.get("P_Fuerza_Q1")), "P_Hambre_Q1": str(d.get("P_Hambre_Q1")),
                        "Historial de Estancamiento": str(d.get("Historial de Estancamiento")),
                        "Capacidad de Recuperación Base": str(d.get("Capacidad de Recuperación Base")),
                        "Biofeedback Digestivo": str(d.get("Biofeedback Digestivo")),
                        "Carga de Estrés Externo": str(d.get("Carga de Estrés Externo")),
                        "Foto_Frente_Q1": "Recibida", "Foto_Perfil_Q1": "Recibida", "Foto_Espalda_Q1": "Recibida"
                    }
                    
                    with st.spinner("Compilando ecosistema..."):
                        try:
                            resp = requests.post(CONFIG["webhook_url"], json=payload, timeout=10)
                            if resp.status_code == 200:
                                st.markdown(f"<div class='id-box'>✅ EXPEDIENTE ACTIVO<br>TU ID: {id_nuevo}</div>", unsafe_allow_html=True)
                                st.balloons()
                                st.cache_data.clear()
                                st.session_state.step, st.session_state.db = 1, {}
                            else: st.error("Error conectando con la base.")
                        except Exception as e: st.error(f"Error: {e}")

    # ── FORMULARIO AUDITORÍA (Q2) ───────────────────────────────────────────
    with tab_q2:
        st.info("Ingresa tu ID y completa el cruce clínico. Se generará un plan de acción dictaminado.")
        with st.form("f_auditoria", clear_on_submit=True):
            id_ing = st.text_input("ID de Atleta (Ej: MM247-2026-ABC-123456):").strip().upper()

            st.markdown("<div class='section-header'>1. EVIDENCIA VISUAL (Q2)</div>", unsafe_allow_html=True)
            fq1, fq2, fq3 = st.columns(3)
            fq1.file_uploader("Frente Actual", type=['png', 'jpg'])
            fq2.file_uploader("Perfil Actual", type=['png', 'jpg'])
            fq3.file_uploader("Espalda Actual", type=['png', 'jpg'])

            st.markdown("<div class='section-header'>2. MÉTRICAS Y ADHERENCIA</div>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            peso_rev = m1.number_input("Peso Actual (kg):", min_value=30.0, value=70.0, step=0.1)
            cint_rev = m2.number_input("Cintura Actual (cm):", min_value=40.0, value=80.0, step=0.5)
            
            adherencia = st.selectbox("Adherencia Real al Sistema:", ["100% Perfecto", "80-90% Con fallos mínimos", "Cerca del 50%", "Menos del 50% / Abandoné"])
            sobrecarga = st.selectbox("Sobrecarga Progresiva:", ["Sí, subí peso/reps", "Me mantuve igual", "No, perdí fuerza"])
            tolerancia = st.selectbox("Tolerancia Metabólica:", ["Digestión rápida y normal", "Ligera pesadez", "Mucha pesadez / Inflamación constante"])

            st.markdown("<div class='section-header'>3. PARÁMETROS ESPEJO ACTUALES (1-10)</div>", unsafe_allow_html=True)
            c_p1, c_p2 = st.columns(2)
            e_rev = c_p1.slider("Energía:", 1, 10, 5)
            s_rev = c_p2.slider("Sueño:", 1, 10, 5)
            f_rev = c_p1.slider("Fuerza:", 1, 10, 5)
            h_rev = c_p2.slider("Hambre:", 1, 10, 5)

            if st.form_submit_button("🚀 AUDITAR Y GENERAR PLAN DE ACCIÓN"):
                if not id_ing: st.error("El ID es obligatorio para cruzar los datos.")
                elif df_existente.empty or id_ing not in df_existente["ID_Alumno"].values: st.error("ID no encontrado en Q1.")
                else:
                    puntos = 0
                    if f_rev >= 7 and "Sí" in sobrecarga: puntos += 2
                    if "100%" in adherencia or "80-90%" in adherencia: puntos += 1
                    
                    estado_calc = "AVANCE" if puntos >= 2 else "RETROCESO"
                    
                    payload_rev = {
                        "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Tipo_Registro": "REVISION", "ID_Alumno": id_ing,
                        "Peso_Revision": str(peso_rev), "Cintura_Revision": str(cint_rev),
                        "Energia": str(e_rev), "Calidad_Sueno": str(s_rev), "Progreso_Fuerza": str(f_rev), "Hambre": str(h_rev),
                        "Adherencia Real al Sistema": adherencia, "Sobrecarga Progresiva": sobrecarga, "Tolerancia Metabólica": tolerancia,
                        "Foto_Frente_Q2": "Recibida", "Foto_Perfil_Q2": "Recibida", "Foto_Espalda_Q2": "Recibida",
                        "Estado_Calculado": estado_calc
                    }

                    with st.spinner("Procesando deltas y evaluando plan..."):
                        try:
                            resp = requests.post(CONFIG["webhook_url"], json=payload_rev, timeout=10)
                            if resp.status_code == 200:
                                st.cache_data.clear()
                                st.success(f"Dictamen Clínico Generado: **{estado_calc}**.")
                                st.image(obtener_avatar_url(estado_calc, "Registro Exitoso"), width=200)
                            else: st.error("Error conectando con la base.")
                        except Exception as e: st.error(f"Error: {e}")
