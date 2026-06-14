# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA CLÍNICA
   VERSIÓN 6.0 — IDs SECUENCIALES, SIDEBAR NAVIGATION, DUAL DASHBOARD
================================================================================
"""

import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests
import tempfile
import os

# =============================================================================
# 0. CONFIGURACIÓN CENTRAL
# =============================================================================
CONFIG = {
    "page_title": "MM247",
    "page_icon": "🟩",
    "webhook_url": "https://script.google.com/macros/s/AKfycbx5vDCKmqpe-vsZ2fan0ZQoesLjajIHHHXHOZLtG7-w6-ts3uUl1WkZVHnPnn0F3Cbn/exec",
    "sheet_url": "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas",
    "admin_password": "MM247_Admin",
    "total_misiones_q1": 6,
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
st.set_page_config(
    page_title=CONFIG["page_title"],
    page_icon=CONFIG["page_icon"],
    layout="wide"
)

# =============================================================================
# 2. ESTILOS CSS GLOBALES
# =============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

/* ── ANIMACIONES ── */
@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulseGreen {
  0%   { box-shadow: 0 0 0 0 rgba(80,200,120,.45); }
  70%  { box-shadow: 0 0 0 14px rgba(80,200,120,0); }
  100% { box-shadow: 0 0 0 0 rgba(80,200,120,0); }
}
@keyframes shimmer {
  0%   { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
@keyframes countUp {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}
@keyframes borderPulse {
  0%,100% { border-color: #50C878; }
  50%      { border-color: #3CB371; }
}

/* ── BASE ── */
.stApp { background: #F0F4F1; font-family: 'Inter', sans-serif; color: #1A2B1F; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0D1F14 0%, #132B1A 100%) !important;
  border-right: 1px solid #50C87830;
}
[data-testid="stSidebar"] * { color: #E8F5EC !important; }
[data-testid="stSidebar"] .stTextInput input {
  background: #1A3322 !important;
  border: 1px solid #50C87870 !important;
  color: #E8F5EC !important;
  border-radius: 8px;
}

/* Botones sidebar */
.sidebar-nav-btn {
  display: block; width: 100%; padding: 14px 18px; margin: 6px 0;
  background: linear-gradient(135deg, #1A3D24 0%, #0F2417 100%);
  border: 1px solid #50C87840; border-radius: 10px;
  color: #B8F0CB !important; font-family: 'Space Grotesk', sans-serif;
  font-weight: 600; font-size: 13px; letter-spacing: 0.5px;
  cursor: pointer; transition: all .25s ease; text-align: left;
  text-decoration: none;
}
.sidebar-nav-btn:hover {
  background: linear-gradient(135deg, #50C878 0%, #3CB371 100%);
  color: #fff !important; border-color: #50C878;
  transform: translateX(4px); box-shadow: 0 4px 16px rgba(80,200,120,.35);
}
.sidebar-nav-btn.active {
  background: linear-gradient(135deg, #50C878 0%, #2E8B57 100%);
  color: #fff !important; border-color: #50C878;
  animation: pulseGreen 2.5s infinite;
}
.sidebar-logo {
  text-align: center; padding: 20px 0 10px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px; font-weight: 900; letter-spacing: 4px;
  background: linear-gradient(135deg, #50C878, #B8F0CB);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sidebar-tagline {
  text-align: center; font-size: 9px; letter-spacing: 3px;
  color: #50C87880 !important; text-transform: uppercase; margin-bottom: 20px;
}
.sidebar-divider {
  border: none; border-top: 1px solid #50C87825; margin: 16px 0;
}

/* ── HERO / TÍTULO ── */
.hero-block {
  background: linear-gradient(135deg, #0D1F14 0%, #1A3D24 60%, #0F2417 100%);
  border-radius: 20px; padding: 40px 50px; margin-bottom: 28px;
  position: relative; overflow: hidden;
  animation: fadeSlideUp .7s ease-out;
  border: 1px solid #50C87830;
}
.hero-block::before {
  content: '247'; position: absolute; right: -20px; top: -20px;
  font-size: 160px; font-weight: 900; color: #50C87808;
  font-family: 'Space Grotesk', sans-serif; line-height: 1;
}
.hero-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 52px; font-weight: 900; color: #fff; margin: 0;
  letter-spacing: 3px;
}
.hero-title span { color: #50C878; }
.hero-sub {
  font-size: 12px; color: #8FC99E; letter-spacing: 4px;
  text-transform: uppercase; margin-top: 6px;
}

/* ── METRIC CARDS ── */
.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin: 20px 0; }
.metric-card {
  background: #fff; border-radius: 14px; padding: 22px 18px;
  border-top: 3px solid #50C878;
  box-shadow: 0 2px 12px rgba(0,0,0,.06);
  animation: countUp .5s ease-out both;
  transition: transform .2s, box-shadow .2s;
}
.metric-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(80,200,120,.15); }
.metric-label { font-size: 10px; font-weight: 700; color: #7D9A84; letter-spacing: 1.5px; text-transform: uppercase; }
.metric-val   { font-size: 30px; font-weight: 900; color: #0D1F14; font-family: 'Space Grotesk', sans-serif; margin: 4px 0; }
.metric-delta { font-size: 12px; font-weight: 600; }
.delta-pos { color: #22C55E; }
.delta-neg { color: #EF4444; }
.delta-neu { color: #94A3B8; }

/* ── SECTION HEADERS ── */
.sec-head {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: #50C878;
  border-left: 3px solid #50C878; padding-left: 12px;
  margin: 28px 0 14px;
}

/* ── PANEL CARDS ── */
.panel-card {
  background: #fff; border-radius: 16px; padding: 28px;
  box-shadow: 0 2px 16px rgba(0,0,0,.05);
  border: 1px solid #E8F0EA;
  animation: fadeSlideUp .5s ease-out;
  margin-bottom: 20px;
}

/* ── ID BOX ── */
.id-box {
  background: linear-gradient(135deg, #50C878 0%, #2E8B57 100%);
  border-radius: 16px; padding: 30px; text-align: center;
  animation: pulseGreen 2s infinite;
  box-shadow: 0 8px 32px rgba(80,200,120,.4);
}
.id-box-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 48px; font-weight: 900; color: #fff; letter-spacing: 6px;
}
.id-box-label { font-size: 11px; color: rgba(255,255,255,.8); letter-spacing: 3px; text-transform: uppercase; }

/* ── AVATAR RING ── */
.avatar-container {
  display: flex; justify-content: center; margin: 10px 0;
}
.avatar-ring {
  width: 120px; height: 120px; border-radius: 50%;
  border: 4px solid #50C878;
  animation: borderPulse 2s infinite;
  overflow: hidden; display: flex; align-items: center; justify-content: center;
  box-shadow: 0 0 24px rgba(80,200,120,.3);
}
.avatar-ring img { width: 100%; height: 100%; object-fit: cover; }

/* ── STATUS BADGES ── */
.badge-avance   { background:#DCFCE7; color:#166534; border:1px solid #86EFAC; padding:6px 16px; border-radius:20px; font-weight:700; font-size:12px; display:inline-block; }
.badge-retroceso{ background:#FEE2E2; color:#991B1B; border:1px solid #FCA5A5; padding:6px 16px; border-radius:20px; font-weight:700; font-size:12px; display:inline-block; }
.badge-lento    { background:#FEF9C3; color:#854D0E; border:1px solid #FDE047; padding:6px 16px; border-radius:20px; font-weight:700; font-size:12px; display:inline-block; }

/* ── PLAN DE ACCION ── */
.accion-item {
  background: linear-gradient(135deg, #F0FDF4, #ECFDF5);
  border-left: 4px solid #22C55E;
  border-radius: 0 10px 10px 0;
  padding: 14px 18px; margin: 8px 0;
  font-size: 13px; color: #166534;
  animation: fadeSlideUp .4s ease-out;
}
.accion-item.warning {
  background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
  border-left-color: #F59E0B; color: #78350F;
}
.accion-item.alert {
  background: linear-gradient(135deg, #FFF1F2, #FFE4E6);
  border-left-color: #EF4444; color: #7F1D1D;
}

/* ── PROGRESS STEPS ── */
.step-bar {
  display: flex; justify-content: space-between;
  padding: 0; list-style: none; margin: 0 0 24px;
}
.step-dot {
  width: 32px; height: 32px; border-radius: 50%;
  background: #E5E7EB; display: flex; align-items: center;
  justify-content: center; font-size: 12px; font-weight: 700; color: #9CA3AF;
  border: 2px solid #E5E7EB; transition: all .3s;
}
.step-dot.done  { background: #50C878; color: #fff; border-color: #50C878; }
.step-dot.active{ background: #fff; color: #50C878; border-color: #50C878; box-shadow: 0 0 0 4px rgba(80,200,120,.2); }

/* ── RUTINA TABLE ── */
.rutina-header {
  background: linear-gradient(90deg, #0D1F14, #1A3D24);
  color: #50C878; font-weight: 700; font-size: 11px;
  letter-spacing: 1.5px; text-transform: uppercase;
  padding: 10px 14px; border-radius: 8px 8px 0 0;
}
.rutina-row {
  display: grid; grid-template-columns: 3fr 1fr 1fr 1fr;
  padding: 10px 14px; border-bottom: 1px solid #F0F4F1;
  font-size: 13px; transition: background .2s;
}
.rutina-row:hover { background: #F0FDF4; }

/* ── CHART CONTAINERS ── */
.chart-wrap {
  background: #fff; border-radius: 14px; padding: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,.05);
  border: 1px solid #E8F0EA; margin-bottom: 16px;
}

/* ── FORMS ── */
div[data-testid="stForm"] {
  background: #fff !important; border-radius: 16px !important;
  border: 1px solid #E8F0EA !important; padding: 28px !important;
  box-shadow: 0 2px 16px rgba(0,0,0,.04) !important;
}
label[data-testid="stWidgetLabel"] p { color: #1A2B1F !important; font-weight: 600 !important; }

/* ── BUTTONS ── */
div.stButton > button, div[data-testid="stForm"] button {
  background: linear-gradient(90deg, #50C878, #2E8B57) !important;
  color: #fff !important; border: none !important; border-radius: 10px !important;
  font-weight: 700 !important; height: 48px; width: 100%;
  font-family: 'Space Grotesk', sans-serif !important;
  letter-spacing: 1px; text-transform: uppercase; transition: all .25s;
}
div.stButton > button:hover, div[data-testid="stForm"] button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 20px rgba(80,200,120,.4) !important;
  filter: brightness(1.08) !important;
}

/* ── PHOTO FRAMES ── */
.photo-frame {
  border: 2px solid #50C87840; border-radius: 12px; overflow: hidden;
  aspect-ratio: 2/3; background: #0D1F14;
  display: flex; align-items: center; justify-content: center;
  color: #50C87860; font-size: 12px; letter-spacing: 1px;
  text-transform: uppercase; font-weight: 600;
}

/* ── NUTRITION ROW ── */
.macro-pill {
  display: inline-flex; flex-direction: column; align-items: center;
  background: #F0FDF4; border: 1.5px solid #86EFAC;
  border-radius: 12px; padding: 14px 20px; min-width: 90px;
}
.macro-pill-val  { font-size: 22px; font-weight: 900; color: #166534; font-family: 'Space Grotesk', sans-serif; }
.macro-pill-lbl  { font-size: 10px; color: #4ADE80; letter-spacing: 1px; text-transform: uppercase; font-weight: 700; }

/* ── SHIMMER LOADING ── */
.shimmer {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 400px 100%; animation: shimmer 1.5s infinite;
  border-radius: 8px; height: 20px;
}
</style>
""", unsafe_allow_html=True)

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


def generar_id_secuencial(df: pd.DataFrame) -> str:
    """Genera el próximo ID en formato 247XXX."""
    if df.empty:
        return "247001"
    ids_existentes = df["ID_Alumno"].dropna().astype(str)
    numeros = []
    for id_val in ids_existentes:
        if id_val.startswith("247") and id_val[3:].isdigit():
            numeros.append(int(id_val[3:]))
    if not numeros:
        return "247001"
    siguiente = max(numeros) + 1
    return f"247{siguiente:03d}"


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
# 4. MOTOR METABÓLICO
# =============================================================================
def _parse_float(valor, defecto: float) -> float:
    try:
        return float(str(valor).replace("kg","").replace("cm","").replace("años","").strip().split()[0])
    except Exception:
        return defecto


def calcular_metabolismo(datos: dict) -> dict:
    peso     = _parse_float(datos.get("Peso actual", "80"), 80.0)
    cintura  = _parse_float(datos.get("Cintura inicial", "85"), 85.0)
    estatura = _parse_float(datos.get("Estatura", "175"), 175.0)
    edad     = _parse_float(datos.get("Edad", "25"), 25.0)
    genero   = str(datos.get("Sexo", "Masculino"))
    actividad= str(datos.get("Nivel de actividad", "Moderadamente activo"))
    meta     = str(datos.get("Objetivo principal", "Recomposición corporal"))

    imc = peso / ((estatura / 100) ** 2) if estatura > 0 else 0.0
    ica = cintura / estatura if estatura > 0 else 0.0

    origen_fisico = "Condición Normal"
    if ica >= 0.53:  origen_fisico = "Obesidad / Riesgo Metabólico"
    elif ica >= 0.50: origen_fisico = "Sobrepeso Músculo-Graso"
    elif ica < 0.43:  origen_fisico = "Perfil Atlético / Magro"

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

    prot  = round(peso * 2.0, 1)
    grasa = round(peso * 1.0, 1)
    carbs = round(max((cals - (prot * 4) - (grasa * 9)) / 4, 50.0), 1)

    return {
        "imc": round(imc, 1), "ica": round(ica, 2), "origen": origen_fisico,
        "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals, 0),
        "prot": prot, "grasa": grasa, "carbs": carbs, "balance_str": balance_str,
        "factor": factor, "edad": edad, "genero": genero,
        "peso": peso, "cintura": cintura, "estatura": estatura,
    }

# =============================================================================
# 5. PLAN DE ACCIÓN CLÍNICO
# =============================================================================
def generar_plan_accion(norm: dict, ult_rev: pd.Series, estado: str) -> list:
    plan = []
    adherencia  = str(ult_rev.get("Adherencia Real al Sistema", "100%"))
    sobrecarga  = str(ult_rev.get("Sobrecarga Progresiva", "Sí, en la mayoría"))
    tolerancia  = str(ult_rev.get("Tolerancia Metabólica", "Digestión rápida y normal"))

    if "menos del 50%" in adherencia.lower() or "50%" in adherencia:
        plan.append(("alert", "ADHERENCIA CRÍTICA: Reducir la complejidad del menú actual. Priorizar alimentos de fácil preparación y revisar picos de ansiedad."))
    if estado == "RETROCESO" and "No" in sobrecarga:
        plan.append(("warning", "AJUSTE NEUROMUSCULAR: Descarga programada (Deload) de 1 semana. Reducir volumen 30% para disipar fatiga sistémica."))
    if "pesadez" in tolerancia.lower() or "inflamación" in tolerancia.lower():
        plan.append(("warning", "BIOFEEDBACK: Ajuste en fuentes de carbohidratos. Rotar arroz/papa por avena/vegetales fibrosos."))
    if estado == "AVANCE" and "Sí" in sobrecarga:
        plan.append(("success", "LUZ VERDE (INTENSIDAD): Mantener balance calórico intacto. Autorizado para aumentar cargas en ejercicios compuestos +5%."))
    if not plan:
        plan.append(("success", "MANTENIMIENTO ÓPTIMO: Parámetros estables. Continuar protocolo actual sin modificaciones agresivas."))
    return plan

# =============================================================================
# 6. AVATAR
# =============================================================================
# 6. MOTOR DE AVATAR INTELIGENTE
# =============================================================================
def obtener_avatar_url(estatus: str, nombre: str = "Atleta") -> str:
    """Avatar básico de fallback."""
    nom = str(nombre).replace(" ", "+")
    bg = {"AVANCE": "50C878", "RETROCESO": "EF4444"}.get(estatus, "F59E0B")
    return f"https://ui-avatars.com/api/?name={nom}&background={bg}&color=fff&size=256&font-size=0.4&bold=true&rounded=true"


def construir_avatar_q1(norm: dict, mot: dict) -> str:
    """
    Avatar SVG fitness profesional Q1 con anatomía, zonas musculares
    señalizadas dinámicamente y diferenciación hombre/mujer completa.
    """
    sexo     = str(norm.get("Sexo", "Masculino"))
    imc      = mot.get("imc", 22.0)
    estatura = mot.get("estatura", 175.0)
    objetivo = str(norm.get("Objetivo principal", ""))
    lesion   = str(norm.get("Lesión actual", "Ninguna"))
    nivel    = str(norm.get("Tiempo entrenando", "Menos de 6 meses"))
    nombre   = str(norm.get("Nombre completo", "Atleta"))

    es_mujer = "Femen" in sexo or "femen" in sexo
    skin  = "#F4C49E" if not es_mujer else "#F2B08A"
    hair  = "#3B2314" if not es_mujer else "#7B3F00"
    acc   = "#50C878"
    cx, W, H = 110, 220, 420

    # ── Complexión según IMC ────────────────────────────────────────────────
    if imc < 18.5:
        sw, cw, lw = 44, 52, 16   # delgado
        grasa_op = 0.0
    elif imc < 25:
        sw, cw, lw = 54, 62, 20   # normal-atlético
        grasa_op = 0.05
    elif imc < 30:
        sw, cw, lw = 66, 74, 24   # sobrepeso
        grasa_op = 0.18
    else:
        sw, cw, lw = 78, 86, 28   # obesidad
        grasa_op = 0.32

    # Hombros más anchos si objetivo muscular
    if any(k in objetivo for k in ("Ganar","muscular","Volumen")):
        sw = min(sw + 10, 88)

    # Escala por estatura
    sc = 0.90 if estatura < 162 else (1.08 if estatura > 178 else 1.0)

    # Posiciones anatómicas
    cy_h  = int(52 * sc)          # centro cabeza
    cr    = int(24 * sc)          # radio cabeza
    neck_y= cy_h + cr
    sho_y = neck_y + int(10*sc)   # hombros
    torso_y = sho_y
    torso_h = int(72 * sc)
    waist_y = torso_y + torso_h
    hip_y   = waist_y + int(8*sc)
    knee_y  = hip_y + int(60*sc)
    foot_y  = knee_y + int(58*sc)

    sw2, cw2 = sw//2, cw//2       # half-widths

    # ── Zonas musculares a entrenar según objetivo ──────────────────────────
    zonas_color = []
    if "grasa" in objetivo or "Perder" in objetivo:
        # Cardio → cintura y todo el cuerpo
        zonas_color = [
            ("abdomen",  cx-14, waist_y-18, 28, 20, "#FF6B35", "ABDOMEN"),
            ("cardio",   cx-sw2+2, torso_y+10, sw-4, 16, "#FF6B35", "CARDIO"),
        ]
    elif "muscular" in objetivo or "Ganar" in objetivo:
        zonas_color = [
            ("pecho",    cx-sw2+4, torso_y+6,  sw-8, 22, "#3B82F6", "PECHO"),
            ("espalda",  cx-sw2+4, torso_y+30, sw-8, 18, "#8B5CF6", "ESPALDA"),
            ("biceps_i", cx-sw2-lw-2, torso_y+10, lw, 20, "#3B82F6", "BIC"),
            ("biceps_d", cx+sw2+2,    torso_y+10, lw, 20, "#3B82F6", "BIC"),
            ("cuad_i",   cx-cw2+2, hip_y+4, cw2-4, 30, "#10B981", "CUAD"),
            ("cuad_d",   cx+2,     hip_y+4, cw2-4, 30, "#10B981", "CUAD"),
        ]
    else:  # recomposición
        zonas_color = [
            ("pecho",    cx-sw2+4, torso_y+6,  sw-8, 18, "#3B82F6", "PECHO"),
            ("abdomen",  cx-14, waist_y-16, 28, 18, "#FF6B35", "ABS"),
            ("gluteo",   cx-cw2+2, hip_y+2, cw-4, 18, "#EC4899", "GLUT"),
        ]

    # ── Señal de lesión ─────────────────────────────────────────────────────
    lesion_markers = ""
    if "Rodilla" in lesion:
        for lx in [cx-cw2+4, cx+4]:
            lesion_markers += f'''
            <circle cx="{lx+lw//2}" cy="{knee_y}" r="9" fill="#EF4444" opacity="0.9">
              <animate attributeName="r" values="7;12;7" dur="1s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.9;0.4;0.9" dur="1s" repeatCount="indefinite"/>
            </circle>
            <text x="{lx+lw//2}" y="{knee_y+4}" font-size="8" fill="#fff" text-anchor="middle" font-weight="bold">!</text>'''
    elif "Hombro" in lesion:
        for lx in [cx-sw2-4, cx+sw2+4]:
            lesion_markers += f'''
            <circle cx="{lx}" cy="{sho_y+6}" r="9" fill="#EF4444" opacity="0.9">
              <animate attributeName="r" values="7;12;7" dur="1s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.9;0.4;0.9" dur="1s" repeatCount="indefinite"/>
            </circle>
            <text x="{lx}" y="{sho_y+10}" font-size="8" fill="#fff" text-anchor="middle" font-weight="bold">!</text>'''
    elif "Espalda" in lesion:
        lesion_markers += f'''
        <ellipse cx="{cx}" cy="{torso_y+torso_h//2}" rx="18" ry="12" fill="#EF4444" opacity="0.7">
          <animate attributeName="ry" values="10;16;10" dur="1.2s" repeatCount="indefinite"/>
          <animate attributeName="opacity" values="0.7;0.3;0.7" dur="1.2s" repeatCount="indefinite"/>
        </ellipse>
        <text x="{cx}" y="{torso_y+torso_h//2+4}" font-size="9" fill="#fff" text-anchor="middle" font-weight="bold">ESC</text>'''
    elif "Cervical" in lesion:
        lesion_markers += f'''
        <circle cx="{cx}" cy="{neck_y+5}" r="9" fill="#EF4444" opacity="0.9">
          <animate attributeName="r" values="7;12;7" dur="1s" repeatCount="indefinite"/>
        </circle>
        <text x="{cx}" y="{neck_y+9}" font-size="7" fill="#fff" text-anchor="middle" font-weight="bold">CRV</text>'''

    # ── Nivel badge ─────────────────────────────────────────────────────────
    if "Más de 3" in nivel:    nivel_txt, nivel_col = "PRO", "#FFD700"
    elif "1 a 3" in nivel:     nivel_txt, nivel_col = "INT", "#C0C0C0"
    elif "6 meses" in nivel:   nivel_txt, nivel_col = "MED", "#CD7F32"
    else:                       nivel_txt, nivel_col = "INI", "#50C878"

    # ── Capas de grasa corporal ─────────────────────────────────────────────
    grasa_layer = ""
    if grasa_op > 0:
        grasa_layer = f'''
        <ellipse cx="{cx}" cy="{waist_y-10}" rx="{cw2+8}" ry="14" fill="#FFA07A" opacity="{grasa_op:.2f}"/>
        <ellipse cx="{cx}" cy="{hip_y+10}" rx="{cw2+10}" ry="12" fill="#FFA07A" opacity="{grasa_op:.2f}"/>'''

    # ── Cabello por género ──────────────────────────────────────────────────
    if es_mujer:
        cabello = f'''
        <ellipse cx="{cx}" cy="{cy_h-cr+6}" rx="{cr+8}" ry="{cr//2+4}" fill="{hair}"/>
        <path d="M {cx-cr-6} {cy_h-4} Q {cx-cr-14} {cy_h+cr+10} {cx-cr-4} {cy_h+cr+20}" stroke="{hair}" stroke-width="10" fill="none" stroke-linecap="round"/>
        <path d="M {cx+cr+6} {cy_h-4} Q {cx+cr+14} {cy_h+cr+10} {cx+cr+4} {cy_h+cr+20}" stroke="{hair}" stroke-width="10" fill="none" stroke-linecap="round"/>'''
    else:
        cabello = f'<ellipse cx="{cx}" cy="{cy_h-cr+7}" rx="{cr+2}" ry="{cr//2+3}" fill="{hair}"/>'

    # ── Cuerpo fitness con anatomía ─────────────────────────────────────────
    if es_mujer:
        # Figura femenina: hombros estrechos, cintura marcada, caderas
        cuerpo = f'''
        <!-- Cuello -->
        <rect x="{cx-7}" y="{neck_y}" width="14" height="{int(10*sc)}" rx="4" fill="{skin}"/>
        <!-- Hombros trapecio -->
        <ellipse cx="{cx}" cy="{sho_y+4}" rx="{sw//2}" ry="10" fill="{skin}"/>
        <!-- Torso superior (pecho/espalda) -->
        <path d="M {cx-sw2} {sho_y+6} C {cx-sw2-4} {torso_y+torso_h//3} {cx-cw2-2} {waist_y-12} {cx-cw2} {waist_y}
                 L {cx+cw2} {waist_y} C {cx+cw2+2} {waist_y-12} {cx+sw2+4} {torso_y+torso_h//3} {cx+sw2} {sho_y+6} Z"
              fill="{skin}"/>
        <!-- Sujetador deportivo -->
        <path d="M {cx-sw2+4} {sho_y+8} C {cx-sw2} {sho_y+28} {cx-10} {sho_y+32} {cx} {sho_y+32}
                 C {cx+10} {sho_y+32} {cx+sw2} {sho_y+28} {cx+sw2-4} {sho_y+8} Z"
              fill="#7C3D8A" opacity="0.9"/>
        <line x1="{cx-sw2+6}" y1="{sho_y+8}" x2="{cx-4}" y2="{sho_y+2}" stroke="#9D50BB" stroke-width="3" stroke-linecap="round"/>
        <line x1="{cx+sw2-6}" y1="{sho_y+8}" x2="{cx+4}" y2="{sho_y+2}" stroke="#9D50BB" stroke-width="3" stroke-linecap="round"/>
        <!-- Caderas -->
        <ellipse cx="{cx}" cy="{hip_y+6}" rx="{cw2+6}" ry="10" fill="{skin}"/>
        <!-- Leggings piernas -->
        <path d="M {cx-cw2} {hip_y} L {cx-4} {hip_y+10} L {cx-lw//2-2} {knee_y} L {cx-lw//2-6} {foot_y}
                 L {cx-lw//2+lw//2} {foot_y} L {cx-lw//2+lw//2+2} {knee_y} L {cx-2} {hip_y+10} Z"
              fill="#6D28D9"/>
        <path d="M {cx+cw2} {hip_y} L {cx+4} {hip_y+10} L {cx+lw//2+2} {knee_y} L {cx+lw//2+6} {foot_y}
                 L {cx+lw//2-lw//2} {foot_y} L {cx+lw//2-lw//2-2} {knee_y} L {cx+2} {hip_y+10} Z"
              fill="#6D28D9"/>
        <!-- Línea quad -->
        <line x1="{cx-cw2//2}" y1="{hip_y+12}" x2="{cx-cw2//2+2}" y2="{knee_y-6}" stroke="#8B5CF6" stroke-width="1.5" opacity="0.5"/>
        <line x1="{cx+cw2//2}" y1="{hip_y+12}" x2="{cx+cw2//2-2}" y2="{knee_y-6}" stroke="#8B5CF6" stroke-width="1.5" opacity="0.5"/>
        '''
    else:
        # Figura masculina: hombros anchos, torso en V, cuádriceps marcados
        cuerpo = f'''
        <!-- Cuello -->
        <rect x="{cx-8}" y="{neck_y}" width="16" height="{int(10*sc)}" rx="4" fill="{skin}"/>
        <!-- Trapecios / deltoides -->
        <ellipse cx="{cx-sw2}" cy="{sho_y+6}" rx="14" ry="10" fill="{skin}"/>
        <ellipse cx="{cx+sw2}" cy="{sho_y+6}" rx="14" ry="10" fill="{skin}"/>
        <!-- Torso en V (pecho → cintura) -->
        <path d="M {cx-sw2} {sho_y+4} L {cx-cw2} {waist_y} L {cx+cw2} {waist_y} L {cx+sw2} {sho_y+4} Z"
              fill="{skin}"/>
        <!-- División pectoral -->
        <line x1="{cx}" y1="{torso_y+4}" x2="{cx}" y2="{torso_y+torso_h//3+4}" stroke="rgba(0,0,0,0.12)" stroke-width="2"/>
        <!-- Pectorales forma -->
        <ellipse cx="{cx-sw2//2}" cy="{torso_y+torso_h//4}" rx="{sw//4+2}" ry="{int(14*sc)}" fill="rgba(0,0,0,0.04)"/>
        <ellipse cx="{cx+sw2//2}" cy="{torso_y+torso_h//4}" rx="{sw//4+2}" ry="{int(14*sc)}" fill="rgba(0,0,0,0.04)"/>
        <!-- Abdomen 6-pack -->
        <rect x="{cx-10}" y="{torso_y+torso_h//2}" width="20" height="{torso_h//3}" rx="4" fill="rgba(0,0,0,0.06)"/>
        <line x1="{cx}" y1="{torso_y+torso_h//2}" x2="{cx}" y2="{waist_y-4}" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
        <line x1="{cx-10}" y1="{torso_y+torso_h//2+10}" x2="{cx+10}" y2="{torso_y+torso_h//2+10}" stroke="rgba(0,0,0,0.08)" stroke-width="1"/>
        <line x1="{cx-10}" y1="{torso_y+torso_h//2+20}" x2="{cx+10}" y2="{torso_y+torso_h//2+20}" stroke="rgba(0,0,0,0.08)" stroke-width="1"/>
        <!-- Shorts deportivos -->
        <path d="M {cx-cw2} {waist_y} L {cx-lw-2} {knee_y-16} L {cx-2} {knee_y-10} L {cx} {waist_y+10} Z" fill="#1A3D24"/>
        <path d="M {cx+cw2} {waist_y} L {cx+lw+2} {knee_y-16} L {cx+2} {knee_y-10} L {cx} {waist_y+10} Z" fill="#1A3D24"/>
        <!-- Cuádriceps -->
        <path d="M {cx-lw-2} {knee_y-16} L {cx-lw-4} {knee_y} L {cx-2} {knee_y+4} L {cx-2} {knee_y-10} Z" fill="{skin}"/>
        <path d="M {cx+lw+2} {knee_y-16} L {cx+lw+4} {knee_y} L {cx+2} {knee_y+4} L {cx+2} {knee_y-10} Z" fill="{skin}"/>
        <!-- Línea quad sep -->
        <line x1="{cx-lw//2-1}" y1="{knee_y-14}" x2="{cx-lw//2+1}" y2="{knee_y-2}" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
        <line x1="{cx+lw//2+1}" y1="{knee_y-14}" x2="{cx+lw//2-1}" y2="{knee_y-2}" stroke="rgba(0,0,0,0.10)" stroke-width="1.5"/>
        <!-- Gemelos / espinillas -->
        <path d="M {cx-lw-4} {knee_y} C {cx-lw-6} {knee_y+20} {cx-lw//2-4} {foot_y-10} {cx-lw//2} {foot_y}
                 L {cx-2} {foot_y} C {cx-2} {foot_y-10} {cx-2} {knee_y+4} {cx-2} {knee_y+4} Z" fill="{skin}"/>
        <path d="M {cx+lw+4} {knee_y} C {cx+lw+6} {knee_y+20} {cx+lw//2+4} {foot_y-10} {cx+lw//2} {foot_y}
                 L {cx+2} {foot_y} C {cx+2} {foot_y-10} {cx+2} {knee_y+4} {cx+2} {knee_y+4} Z" fill="{skin}"/>
        <!-- Gemelo línea -->
        <line x1="{cx-lw//2-2}" y1="{knee_y+8}" x2="{cx-lw//2}" y2="{knee_y+28}" stroke="rgba(0,0,0,0.09)" stroke-width="1.5"/>
        <line x1="{cx+lw//2+2}" y1="{knee_y+8}" x2="{cx+lw//2}" y2="{knee_y+28}" stroke="rgba(0,0,0,0.09)" stroke-width="1.5"/>
        '''

    # ── Brazos fitness ───────────────────────────────────────────────────────
    if es_mujer:
        brazos = f'''
        <path d="M {cx-sw2} {sho_y+4} C {cx-sw2-lw-8} {sho_y+20} {cx-sw2-lw-6} {waist_y-14} {cx-sw2-lw+4} {waist_y}"
              stroke="{skin}" stroke-width="{lw}" fill="none" stroke-linecap="round"/>
        <path d="M {cx+sw2} {sho_y+4} C {cx+sw2+lw+8} {sho_y+20} {cx+sw2+lw+6} {waist_y-14} {cx+sw2+lw-4} {waist_y}"
              stroke="{skin}" stroke-width="{lw}" fill="none" stroke-linecap="round"/>'''
    else:
        brazos = f'''
        <!-- Brazo izq con bícep -->
        <path d="M {cx-sw2} {sho_y+4} C {cx-sw2-lw-10} {sho_y+18} {cx-sw2-lw-12} {waist_y-20} {cx-sw2-lw+2} {waist_y+2}"
              stroke="{skin}" stroke-width="{lw+2}" fill="none" stroke-linecap="round"/>
        <ellipse cx="{cx-sw2-lw-6}" cy="{torso_y+torso_h//3+8}" rx="{lw//2+3}" ry="{int(14*sc)}" fill="{skin}" opacity="0.5"/>
        <!-- Brazo der con bícep -->
        <path d="M {cx+sw2} {sho_y+4} C {cx+sw2+lw+10} {sho_y+18} {cx+sw2+lw+12} {waist_y-20} {cx+sw2+lw-2} {waist_y+2}"
              stroke="{skin}" stroke-width="{lw+2}" fill="none" stroke-linecap="round"/>
        <ellipse cx="{cx+sw2+lw+6}" cy="{torso_y+torso_h//3+8}" rx="{lw//2+3}" ry="{int(14*sc)}" fill="{skin}" opacity="0.5"/>'''

    # ── Zapatillas deportivas ────────────────────────────────────────────────
    shoe_color = "#50C878" if not es_mujer else "#9D50BB"
    zapatillas = f'''
    <ellipse cx="{cx-lw//2-2}" cy="{foot_y+6}" rx="{lw//2+8}" ry="7" fill="#1A1A2E"/>
    <ellipse cx="{cx+lw//2+2}" cy="{foot_y+6}" rx="{lw//2+8}" ry="7" fill="#1A1A2E"/>
    <ellipse cx="{cx-lw//2+2}" cy="{foot_y+4}" rx="{lw//2+4}" ry="4" fill="{shoe_color}" opacity="0.6"/>
    <ellipse cx="{cx+lw//2-2}" cy="{foot_y+4}" rx="{lw//2+4}" ry="4" fill="{shoe_color}" opacity="0.6"/>'''

    # ── Overlays de zonas musculares con animación ──────────────────────────
    zonas_svg = ""
    for zid, zx, zy, zw, zh, zcol, zlbl in zonas_color:
        zonas_svg += f'''
        <rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="4" fill="{zcol}" opacity="0.0">
          <animate attributeName="opacity" values="0;0.35;0" dur="2s" begin="{hash(zid)%10*0.2:.1f}s" repeatCount="indefinite"/>
        </rect>
        <rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" rx="4" fill="none" stroke="{zcol}" stroke-width="1.5" opacity="0.6">
          <animate attributeName="opacity" values="0.3;0.9;0.3" dur="2s" begin="{hash(zid)%10*0.2:.1f}s" repeatCount="indefinite"/>
        </rect>
        <text x="{zx+zw//2}" y="{zy+zh//2+3}" font-size="7" fill="{zcol}" text-anchor="middle" font-weight="bold" font-family="monospace">{zlbl}</text>'''

    # ── Leyenda lateral zonas ────────────────────────────────────────────────
    leyenda_svg = ""
    colores_unicos = list({z[5]: z[6] for z in zonas_color}.items())
    for i, (col, lbl) in enumerate(colores_unicos[:3]):
        ly = H - 70 + i*18
        leyenda_svg += f'''
        <rect x="8" y="{ly}" width="8" height="8" rx="2" fill="{col}"/>
        <text x="20" y="{ly+7}" font-size="8" fill="{col}" font-family="monospace">{lbl}</text>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <radialGradient id="bg1q" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#1E3A28"/>
      <stop offset="100%" stop-color="#0A1A0F"/>
    </radialGradient>
    <filter id="softshadow">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Fondo -->
  <rect width="{W}" height="{H}" fill="url(#bg1q)" rx="18"/>

  <!-- Grid decorativo de fondo -->
  <g opacity="0.04" stroke="{acc}" stroke-width="0.5">
    {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0,W,20))}
    {"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0,H,20))}
  </g>

  <!-- Anillo pulsante cabeza -->
  <circle cx="{cx}" cy="{cy_h}" r="{cr+14}" fill="none" stroke="{acc}" stroke-width="1.5" opacity="0.3">
    <animate attributeName="r" values="{cr+10};{cr+20};{cr+10}" dur="2.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.3;0.05;0.3" dur="2.5s" repeatCount="indefinite"/>
  </circle>

  <!-- Sombra pies -->
  <ellipse cx="{cx}" cy="{foot_y+14}" rx="36" ry="9" fill="#000" opacity="0.3" filter="url(#softshadow)"/>

  <!-- Cabello -->
  {cabello}

  <!-- Cara -->
  <circle cx="{cx}" cy="{cy_h}" r="{cr}" fill="{skin}"/>
  <!-- Ojos -->
  <ellipse cx="{cx-8}" cy="{cy_h-4}" rx="4" ry="4.5" fill="#2C1810"/>
  <ellipse cx="{cx+8}" cy="{cy_h-4}" rx="4" ry="4.5" fill="#2C1810"/>
  <circle cx="{cx-7}" cy="{cy_h-5}" r="1.5" fill="#fff"/>
  <circle cx="{cx+9}" cy="{cy_h-5}" r="1.5" fill="#fff"/>
  <!-- Cejas -->
  <path d="M {cx-12} {cy_h-11} Q {cx-8} {cy_h-14} {cx-4} {cy_h-11}" stroke="#3B2314" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M {cx+12} {cy_h-11} Q {cx+8} {cy_h-14} {cx+4} {cy_h-11}" stroke="#3B2314" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- Nariz -->
  <path d="M {cx-3} {cy_h+2} Q {cx} {cy_h+8} {cx+3} {cy_h+2}" stroke="{skin}" stroke-width="2" fill="none" opacity="0.6"/>
  <!-- Sonrisa -->
  <path d="M {cx-7} {cy_h+9} Q {cx} {cy_h+15} {cx+7} {cy_h+9}" stroke="#8B4513" stroke-width="2" fill="none" stroke-linecap="round"/>

  <!-- Cuerpo -->
  {cuerpo}

  <!-- Grasa corporal overlay -->
  {grasa_layer}

  <!-- Brazos -->
  {brazos}

  <!-- Zapatillas -->
  {zapatillas}

  <!-- Zonas musculares señalizadas -->
  {zonas_svg}

  <!-- Indicadores de lesión -->
  {lesion_markers}

  <!-- Badge nivel superior derecha -->
  <rect x="{W-42}" y="10" width="34" height="18" rx="9" fill="{nivel_col}" opacity="0.9"/>
  <text x="{W-25}" y="23" font-size="9" fill="#000" text-anchor="middle" font-weight="bold" font-family="monospace">{nivel_txt}</text>

  <!-- Leyenda zonas -->
  {leyenda_svg}

  <!-- Nombre abajo -->
  <text x="{cx}" y="{H-8}" font-size="10" fill="{acc}" text-anchor="middle" font-family="monospace" letter-spacing="2">{nombre[:14].upper()}</text>
</svg>'''
    return svg


def construir_avatar_q2(norm: dict, mot: dict, ult_rev: dict, estado: str) -> str:
    """
    Avatar fitness Q2 que refleja avance/retroceso con anatomía dinámica,
    zonas musculares, expresión facial y partículas de energía.
    """
    sexo     = str(norm.get("Sexo", "Masculino"))
    imc      = mot.get("imc", 22.0)
    nombre   = str(norm.get("Nombre completo", "Atleta"))
    objetivo = str(norm.get("Objetivo principal", ""))
    es_mujer = "Femen" in sexo or "femen" in sexo

    peso_q2    = _parse_float(ult_rev.get("Peso_Revision", mot["peso"]), mot["peso"])
    cintura_q2 = _parse_float(ult_rev.get("Cintura_Revision", mot["cintura"]), mot["cintura"])
    fuerza_q2  = _parse_float(ult_rev.get("Progreso_Fuerza", "5"), 5.0)
    energia_q2 = _parse_float(ult_rev.get("Energia", "5"), 5.0)

    dif_peso    = peso_q2 - mot["peso"]
    dif_cintura = cintura_q2 - mot["cintura"]

    skin  = "#F4C49E" if not es_mujer else "#F2B08A"
    hair  = "#3B2314" if not es_mujer else "#7B3F00"
    cx, W, H = 110, 220, 440

    # ── Paleta y postura según estado ──────────────────────────────────────
    if estado == "AVANCE":
        ring_col = "#22C55E"; acc = "#4ADE80"; outfit = "#166534"
        postura  = -6        # erguido
        boca_svg = f'<path d="M {{cx-9}} {{cy_h+10}} Q {{cx}} {{cy_h+17}} {{cx+9}} {{cy_h+10}}" stroke="#666" stroke-width="2" fill="none" stroke-linecap="round"/>'
    elif estado == "RETROCESO":
        ring_col = "#EF4444"; acc = "#F87171"; outfit = "#7F1D1D"
        postura  = 10        # ligeramente encorvado
        boca_svg = f'<path d="M {{cx-9}} {{cy_h+14}} Q {{cx}} {{cy_h+8}} {{cx+9}} {{cy_h+14}}" stroke="#666" stroke-width="2" fill="none" stroke-linecap="round"/>'
    else:
        ring_col = "#F59E0B"; acc = "#FCD34D"; outfit = "#78350F"
        postura  = 2
        boca_svg = f'<line x1="{{cx-8}}" y1="{{cy_h+12}}" x2="{{cx+8}}" y2="{{cy_h+12}}" stroke="#666" stroke-width="2" stroke-linecap="round"/>'

    # IMC Q2 actualizado
    imc_q2 = peso_q2 / ((mot["estatura"]/100)**2) if mot["estatura"] > 0 else imc
    sc = 0.90 if mot["estatura"] < 162 else (1.08 if mot["estatura"] > 178 else 1.0)

    if imc_q2 < 18.5:   sw, cw, lw = 44, 52, 16
    elif imc_q2 < 25:   sw, cw, lw = 54, 62, 20
    elif imc_q2 < 30:   sw, cw, lw = 66, 74, 24
    else:                sw, cw, lw = 78, 86, 28

    if any(k in objetivo for k in ("Ganar","muscular","Volumen")):
        sw = min(sw+10, 88)

    cy_h  = int(54*sc) + postura
    cr    = int(24*sc)
    neck_y= cy_h + cr
    sho_y = neck_y + int(10*sc)
    torso_y = sho_y
    torso_h = int(72*sc)
    waist_y = torso_y + torso_h
    hip_y   = waist_y + int(8*sc)
    knee_y  = hip_y + int(60*sc)
    foot_y  = knee_y + int(58*sc)
    sw2, cw2 = sw//2, cw//2

    # Boca con posiciones reales
    if estado == "AVANCE":
        boca = f'<path d="M {cx-9} {cy_h+10} Q {cx} {cy_h+17} {cx+9} {cy_h+10}" stroke="#666" stroke-width="2" fill="none" stroke-linecap="round"/>'
    elif estado == "RETROCESO":
        boca = f'<path d="M {cx-9} {cy_h+14} Q {cx} {cy_h+8} {cx+9} {cy_h+14}" stroke="#666" stroke-width="2" fill="none" stroke-linecap="round"/>'
    else:
        boca = f'<line x1="{cx-8}" y1="{cy_h+12}" x2="{cx+8}" y2="{cy_h+12}" stroke="#666" stroke-width="2" stroke-linecap="round"/>'

    # Cabello
    if es_mujer:
        cabello = f'''
        <ellipse cx="{cx}" cy="{cy_h-cr+6}" rx="{cr+8}" ry="{cr//2+4}" fill="{hair}"/>
        <path d="M {cx-cr-6} {cy_h-4} Q {cx-cr-14} {cy_h+cr+10} {cx-cr-4} {cy_h+cr+20}" stroke="{hair}" stroke-width="10" fill="none" stroke-linecap="round"/>
        <path d="M {cx+cr+6} {cy_h-4} Q {cx+cr+14} {cy_h+cr+10} {cx+cr+4} {cy_h+cr+20}" stroke="{hair}" stroke-width="10" fill="none" stroke-linecap="round"/>'''
    else:
        cabello = f'<ellipse cx="{cx}" cy="{cy_h-cr+7}" rx="{cr+2}" ry="{cr//2+3}" fill="{hair}"/>'

    # Cuerpo fitness Q2 (mismo que Q1 pero con outfit de estado)
    if es_mujer:
        cuerpo = f'''
        <rect x="{cx-7}" y="{neck_y}" width="14" height="{int(10*sc)}" rx="4" fill="{skin}"/>
        <ellipse cx="{cx}" cy="{sho_y+4}" rx="{sw2}" ry="10" fill="{skin}"/>
        <path d="M {cx-sw2} {sho_y+6} C {cx-sw2-4} {torso_y+torso_h//3} {cx-cw2-2} {waist_y-12} {cx-cw2} {waist_y}
                 L {cx+cw2} {waist_y} C {cx+cw2+2} {waist_y-12} {cx+sw2+4} {torso_y+torso_h//3} {cx+sw2} {sho_y+6} Z" fill="{skin}"/>
        <path d="M {cx-sw2+4} {sho_y+8} C {cx-sw2} {sho_y+28} {cx-10} {sho_y+32} {cx} {sho_y+32}
                 C {cx+10} {sho_y+32} {cx+sw2} {sho_y+28} {cx+sw2-4} {sho_y+8} Z" fill="{outfit}" opacity="0.9"/>
        <ellipse cx="{cx}" cy="{hip_y+6}" rx="{cw2+6}" ry="10" fill="{skin}"/>
        <path d="M {cx-cw2} {hip_y} L {cx-4} {hip_y+10} L {cx-lw//2-2} {knee_y} L {cx-lw//2-6} {foot_y}
                 L {cx-lw//2+lw//2} {foot_y} L {cx-lw//2+lw//2+2} {knee_y} L {cx-2} {hip_y+10} Z" fill="{outfit}"/>
        <path d="M {cx+cw2} {hip_y} L {cx+4} {hip_y+10} L {cx+lw//2+2} {knee_y} L {cx+lw//2+6} {foot_y}
                 L {cx+lw//2-lw//2} {foot_y} L {cx+lw//2-lw//2-2} {knee_y} L {cx+2} {hip_y+10} Z" fill="{outfit}"/>
        <path d="M {cx-sw2} {sho_y+4} C {cx-sw2-lw-8} {sho_y+20} {cx-sw2-lw-6} {waist_y-14} {cx-sw2-lw+4} {waist_y}"
              stroke="{skin}" stroke-width="{lw}" fill="none" stroke-linecap="round"/>
        <path d="M {cx+sw2} {sho_y+4} C {cx+sw2+lw+8} {sho_y+20} {cx+sw2+lw+6} {waist_y-14} {cx+sw2+lw-4} {waist_y}"
              stroke="{skin}" stroke-width="{lw}" fill="none" stroke-linecap="round"/>'''
    else:
        cuerpo = f'''
        <rect x="{cx-8}" y="{neck_y}" width="16" height="{int(10*sc)}" rx="4" fill="{skin}"/>
        <ellipse cx="{cx-sw2}" cy="{sho_y+6}" rx="14" ry="10" fill="{skin}"/>
        <ellipse cx="{cx+sw2}" cy="{sho_y+6}" rx="14" ry="10" fill="{skin}"/>
        <path d="M {cx-sw2} {sho_y+4} L {cx-cw2} {waist_y} L {cx+cw2} {waist_y} L {cx+sw2} {sho_y+4} Z" fill="{skin}"/>
        <path d="M {cx-sw2+2} {sho_y+6} L {cx-cw2+2} {waist_y-2} L {cx+cw2-2} {waist_y-2} L {cx+sw2-2} {sho_y+6} Z" fill="{outfit}" opacity="0.85"/>
        <line x1="{cx}" y1="{torso_y+4}" x2="{cx}" y2="{torso_y+torso_h//3+4}" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
        <path d="M {cx-cw2} {waist_y} L {cx-lw-2} {knee_y-16} L {cx-2} {knee_y-10} L {cx} {waist_y+10} Z" fill="#111827"/>
        <path d="M {cx+cw2} {waist_y} L {cx+lw+2} {knee_y-16} L {cx+2} {knee_y-10} L {cx} {waist_y+10} Z" fill="#111827"/>
        <path d="M {cx-lw-2} {knee_y-16} L {cx-lw-4} {knee_y} L {cx-2} {knee_y+4} L {cx-2} {knee_y-10} Z" fill="{skin}"/>
        <path d="M {cx+lw+2} {knee_y-16} L {cx+lw+4} {knee_y} L {cx+2} {knee_y+4} L {cx+2} {knee_y-10} Z" fill="{skin}"/>
        <path d="M {cx-lw-4} {knee_y} C {cx-lw-6} {knee_y+20} {cx-lw//2-4} {foot_y-10} {cx-lw//2} {foot_y}
                 L {cx-2} {foot_y} C {cx-2} {foot_y-10} {cx-2} {knee_y+4} {cx-2} {knee_y+4} Z" fill="{skin}"/>
        <path d="M {cx+lw+4} {knee_y} C {cx+lw+6} {knee_y+20} {cx+lw//2+4} {foot_y-10} {cx+lw//2} {foot_y}
                 L {cx+2} {foot_y} C {cx+2} {foot_y-10} {cx+2} {knee_y+4} {cx+2} {knee_y+4} Z" fill="{skin}"/>
        <path d="M {cx-sw2} {sho_y+4} C {cx-sw2-lw-10} {sho_y+18} {cx-sw2-lw-12} {waist_y-20} {cx-sw2-lw+2} {waist_y+2}"
              stroke="{skin}" stroke-width="{lw+2}" fill="none" stroke-linecap="round"/>
        <path d="M {cx+sw2} {sho_y+4} C {cx+sw2+lw+10} {sho_y+18} {cx+sw2+lw+12} {waist_y-20} {cx+sw2+lw-2} {waist_y+2}"
              stroke="{skin}" stroke-width="{lw+2}" fill="none" stroke-linecap="round"/>'''

    # Zapatillas
    shoe_color = acc
    zapatillas = f'''
    <ellipse cx="{cx-lw//2-2}" cy="{foot_y+6}" rx="{lw//2+8}" ry="7" fill="#1A1A2E"/>
    <ellipse cx="{cx+lw//2+2}" cy="{foot_y+6}" rx="{lw//2+8}" ry="7" fill="#1A1A2E"/>
    <ellipse cx="{cx-lw//2+2}" cy="{foot_y+4}" rx="{lw//2+4}" ry="4" fill="{shoe_color}" opacity="0.6"/>
    <ellipse cx="{cx+lw//2-2}" cy="{foot_y+4}" rx="{lw//2+4}" ry="4" fill="{shoe_color}" opacity="0.6"/>'''

    # Partículas de energía (avance) o niebla (retroceso)
    particulas = ""
    if estado == "AVANCE":
        pts = [(cx-20,sho_y-10,0.0),(cx+20,sho_y-15,0.4),(cx,sho_y-20,0.8),(cx-10,torso_y,1.2),(cx+15,torso_y-5,0.6)]
        for px,py,dl in pts:
            particulas += f'''<circle cx="{px}" cy="{py}" r="4" fill="{acc}" opacity="0">
              <animate attributeName="cy" values="{py};{py-30};{py}" dur="2s" begin="{dl}s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0;0.85;0" dur="2s" begin="{dl}s" repeatCount="indefinite"/>
              <animate attributeName="r" values="3;6;3" dur="2s" begin="{dl}s" repeatCount="indefinite"/>
            </circle>'''
    elif estado == "RETROCESO":
        for i in range(3):
            particulas += f'''<circle cx="{cx-20+i*20}" cy="{torso_y+20}" r="12" fill="#EF4444" opacity="0">
              <animate attributeName="opacity" values="0;0.08;0" dur="3s" begin="{i*0.8}s" repeatCount="indefinite"/>
              <animate attributeName="r" values="10;20;10" dur="3s" begin="{i*0.8}s" repeatCount="indefinite"/>
            </circle>'''

    # Barra de fuerza lateral
    barra_max = 80
    barra_h = int((fuerza_q2 / 10) * barra_max)
    barra_x = W - 28

    # Barra de energía lateral izquierda
    energia_h = int((energia_q2 / 10) * barra_max)

    # Delta peso visual sobre figura
    color_delta = "#22C55E" if dif_peso <= 0 else "#EF4444"
    icono_delta = "▼" if dif_peso < 0 else ("▲" if dif_peso > 0 else "━")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <radialGradient id="bg2q" cx="50%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#1C2E20"/>
      <stop offset="100%" stop-color="#080F0A"/>
    </radialGradient>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg2q)" rx="18"/>

  <!-- Grid -->
  <g opacity="0.03" stroke="{acc}" stroke-width="0.5">
    {"".join(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0,W,20))}
    {"".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0,H,20))}
  </g>

  <!-- Anillo de estado -->
  <circle cx="{cx}" cy="{cy_h}" r="{cr+14}" fill="none" stroke="{ring_col}" stroke-width="2" opacity="0.4">
    <animate attributeName="r" values="{cr+10};{cr+22};{cr+10}" dur="1.8s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.4;0.05;0.4" dur="1.8s" repeatCount="indefinite"/>
  </circle>

  <!-- Partículas -->
  {particulas}

  <!-- Sombra -->
  <ellipse cx="{cx}" cy="{foot_y+14}" rx="36" ry="9" fill="#000" opacity="0.35"/>

  <!-- Cabello -->
  {cabello}

  <!-- Cara -->
  <circle cx="{cx}" cy="{cy_h}" r="{cr}" fill="{skin}"/>
  <ellipse cx="{cx-8}" cy="{cy_h-4}" rx="4" ry="4.5" fill="#2C1810"/>
  <ellipse cx="{cx+8}" cy="{cy_h-4}" rx="4" ry="4.5" fill="#2C1810"/>
  <circle cx="{cx-7}" cy="{cy_h-5}" r="1.5" fill="#fff"/>
  <circle cx="{cx+9}" cy="{cy_h-5}" r="1.5" fill="#fff"/>
  <path d="{f'M {cx-12} {cy_h-11} Q {cx-8} {cy_h-14} {cx-4} {cy_h-11}'}" stroke="#3B2314" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="{f'M {cx+12} {cy_h-11} Q {cx+8} {cy_h-14} {cx+4} {cy_h-11}'}" stroke="#3B2314" stroke-width="2" fill="none" stroke-linecap="round"/>
  {boca}

  <!-- Cuerpo -->
  {cuerpo}

  <!-- Zapatillas -->
  {zapatillas}

  <!-- Barra FUERZA derecha -->
  <rect x="{barra_x}" y="{cy_h}" width="10" height="{barra_max}" rx="5" fill="#1A3D24"/>
  <rect x="{barra_x}" y="{cy_h + barra_max - barra_h}" width="10" height="{barra_h}" rx="5" fill="{acc}">
    <animate attributeName="height" from="0" to="{barra_h}" dur="1.2s" fill="freeze"/>
    <animate attributeName="y" from="{cy_h+barra_max}" to="{cy_h+barra_max-barra_h}" dur="1.2s" fill="freeze"/>
  </rect>
  <text x="{barra_x+5}" y="{cy_h-5}" font-size="7" fill="{acc}" text-anchor="middle" font-family="monospace">FZA</text>
  <text x="{barra_x+5}" y="{cy_h+barra_max+12}" font-size="8" fill="{acc}" text-anchor="middle" font-weight="bold">{int(fuerza_q2)}</text>

  <!-- Barra ENERGÍA izquierda -->
  <rect x="8" y="{cy_h}" width="10" height="{barra_max}" rx="5" fill="#1A3D24"/>
  <rect x="8" y="{cy_h + barra_max - energia_h}" width="10" height="{energia_h}" rx="5" fill="#FBBF24">
    <animate attributeName="height" from="0" to="{energia_h}" dur="1.4s" fill="freeze"/>
    <animate attributeName="y" from="{cy_h+barra_max}" to="{cy_h+barra_max-energia_h}" dur="1.4s" fill="freeze"/>
  </rect>
  <text x="13" y="{cy_h-5}" font-size="7" fill="#FBBF24" text-anchor="middle" font-family="monospace">ENE</text>
  <text x="13" y="{cy_h+barra_max+12}" font-size="8" fill="#FBBF24" text-anchor="middle" font-weight="bold">{int(energia_q2)}</text>

  <!-- Badge estado -->
  <rect x="{cx-30}" y="10" width="60" height="20" rx="10" fill="{ring_col}" opacity="0.9"/>
  <text x="{cx}" y="24" font-size="10" fill="#fff" text-anchor="middle" font-weight="bold" font-family="monospace">{estado}</text>

  <!-- Delta peso cintura -->
  <text x="{cx}" y="{H-40}" font-size="11" fill="{color_delta}" text-anchor="middle" font-weight="bold" font-family="monospace">
    {icono_delta} PESO {dif_peso:+.1f}kg
  </text>
  <text x="{cx}" y="{H-24}" font-size="10" fill="{('#22C55E' if dif_cintura<=0 else '#EF4444')}" text-anchor="middle" font-family="monospace">
    CIN {dif_cintura:+.1f}cm
  </text>

  <!-- Nombre -->
  <text x="{cx}" y="{H-8}" font-size="9" fill="{acc}" text-anchor="middle" font-family="monospace" letter-spacing="2">{nombre[:14].upper()}</text>
</svg>'''
    return svg


def render_avatar_svg(svg_str: str, height: int = 280):
    """Renderiza SVG inline en Streamlit."""
    import base64
    b64 = base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    st.markdown(
        f'<div style="display:flex;justify-content:center;margin:10px 0;">'
        f'<img src="data:image/svg+xml;base64,{b64}" height="{height}" style="filter:drop-shadow(0 8px 24px rgba(80,200,120,0.3));"/>'
        f'</div>',
        unsafe_allow_html=True
    )

# =============================================================================
# 7. PDF GENERATOR
# =============================================================================
def _limpiar(texto: str) -> str:
    return str(texto).encode("latin-1", "replace").decode("latin-1")


def _tiene_lesion(norm: dict) -> bool:
    return (norm.get("Lesión actual", "Ninguna").lower() != "ninguna" or
            norm.get("Prohibido ejercicio", "No").lower() != "no")


def generar_pdf_mm247(norm: dict, mot: dict, revs_df: pd.DataFrame, id_al: str) -> bytes:
    pdf = FPDF("P", "mm", "Letter")
    pdf.set_auto_page_break(auto=True, margin=15)
    con_lesion = _tiene_lesion(norm)
    t_ent = norm.get("Tiempo entrenando", "Menos de 6 meses")
    aplica_induccion = "Nunca" in t_ent or "Menos de 6 meses" in t_ent
    num_dias = int(str(norm.get("Días entrenar","4")).strip()[0]) if str(norm.get("Días entrenar","4")).strip()[0].isdigit() else 4

    def header(titulo: str):
        pdf.add_page()
        pdf.set_fill_color(80, 200, 120)
        pdf.rect(0, 0, 216, 30, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 24)
        pdf.set_xy(10, 8); pdf.cell(100, 10, "MM247", 0, 0, "L")
        pdf.set_font("Arial", "B", 12)
        pdf.set_xy(160, 12); pdf.cell(45, 10, "CONFIDENCIAL", 0, 0, "R")
        pdf.set_text_color(240, 255, 240)
        pdf.set_font("Arial", "", 10)
        pdf.set_xy(10, 18); pdf.cell(100, 10, f"ID: {id_al}", 0, 0, "L")
        pdf.set_text_color(44, 62, 80)
        pdf.set_font("Arial", "B", 14)
        pdf.set_xy(10, 35); pdf.cell(196, 10, _limpiar(titulo), 0, 1, "C")
        pdf.set_draw_color(229, 231, 235); pdf.set_line_width(0.5)
        pdf.line(10, 45, 206, 45); pdf.ln(10)

    def fila_dato(label: str, valor: str, col_w: int = 98):
        pdf.set_font("Arial","B",10); pdf.cell(col_w,7,_limpiar(label),1,0,"L")
        pdf.set_font("Arial","",10);  pdf.cell(col_w,7,_limpiar(valor),1,1,"L")

    # HOJA 1
    header("HOJA 1: PERFIL CLÍNICO Y LÍNEA BASE")
    pdf.set_font("Arial","B",12); pdf.cell(0,10,_limpiar("1. DATOS GENERALES"),0,1)
    fila_dato("Cliente", norm["Nombre completo"])
    fila_dato("Edad / Sexo", f"{int(mot['edad'])} años / {mot['genero']}")
    fila_dato("Estatura / Peso Base", f"{mot['estatura']} cm / {mot['peso']} kg")
    fila_dato("Punto de Partida", f"{mot['origen']} (ICA: {mot['ica']})")
    fila_dato("Objetivo principal", norm.get("Objetivo principal","--"))
    pdf.ln(8)
    pdf.set_font("Arial","B",12); pdf.set_text_color(239,68,68)
    pdf.cell(0,10,_limpiar("2. ALERTAS BIOMECÁNICAS"),0,1)
    pdf.set_fill_color(254,242,242); pdf.set_draw_color(239,68,68)
    pdf.rect(10,pdf.get_y(),196,38,"FD")
    pdf.set_xy(15,pdf.get_y()+4)
    pdf.set_text_color(51,51,51); pdf.set_font("Arial","",10)
    for linea in [f"Lesión Base: {norm['Lesión actual']}",f"Restricción Axial: {norm['Prohibido ejercicio']}",
                  f"Estancamiento Previo: {norm['Historial_Est']}",f"Recuperación Base: {norm['Recuperacion_Base']}",
                  f"Biofeedback Digestivo: {norm['Biofeedback_Dig']}"]:
        pdf.set_x(15); pdf.cell(0,6,_limpiar(f"• {linea}"),0,1)

    # HOJA 2 - Rutinas
    header("HOJA 2: PROGRAMACIÓN NEUROMUSCULAR")
    modo = "con_lesion" if con_lesion else "sin_lesion"
    if aplica_induccion:
        bloques = ["Inducción (1 Mes)"] * num_dias
        nombres_bloque = [f"DÍA {i+1} — FULL BODY ACONDICIONAMIENTO" for i in range(num_dias)]
    else:
        bloques = ["Empuje","Tracción","Pierna","Empuje","Tracción"][:num_dias]
        nombres_bloque = [f"DÍA {i+1} — {b.upper()}" for i,b in enumerate(bloques)]

    for i, bloque in enumerate(bloques):
        if bloque in CONFIG["rutinas"]:
            ejercicios = CONFIG["rutinas"][bloque][modo]
            pdf.set_fill_color(80,200,120); pdf.set_text_color(255,255,255); pdf.set_font("Arial","B",10)
            pdf.cell(196,8,_limpiar(nombres_bloque[i]),0,1,"L",fill=True)
            pdf.set_fill_color(243,244,246); pdf.set_text_color(51,51,51)
            for txt,w in [("EJERCICIO",90),("SERIES",26),("REPS",40),("DESCANSO",40)]:
                pdf.cell(w,7,_limpiar(txt),1,0,"C",fill=True)
            pdf.ln(); pdf.set_font("Arial","",10)
            for ej,series,reps,desc in ejercicios:
                pdf.cell(90,7,_limpiar(ej),1,0,"L")
                pdf.cell(26,7,_limpiar(series),1,0,"C")
                pdf.cell(40,7,_limpiar(reps),1,0,"C")
                pdf.cell(40,7,_limpiar(desc),1,1,"C")
            pdf.ln(6)

    # HOJA 3 - Nutrición
    header("HOJA 3: PROTOCOLO NUTRICIONAL")
    pdf.set_font("Arial","B",12); pdf.cell(0,10,_limpiar("1. MÉTRICAS METABÓLICAS"),0,1)
    fila_dato("TMB (Harris-Benedict)", f"{mot['tmb']} kcal/día")
    fila_dato(f"TDEE (factor {mot['factor']})", f"{mot['tdee']} kcal/día")
    fila_dato("Balance objetivo", mot["balance_str"])
    fila_dato("Calorías diarias prescritas", f"{mot['cals']} kcal")
    pdf.ln(8)
    pdf.set_font("Arial","B",12); pdf.cell(0,10,_limpiar("2. MACRONUTRIENTES DIARIOS"),0,1)
    pdf.set_fill_color(80,200,120); pdf.set_text_color(255,255,255)
    for h,w in [("PROTEÍNA",49),("CARBOHIDRATOS",49),("GRASAS",49),("CALORÍAS",49)]:
        pdf.cell(w,8,_limpiar(h),1,0,"C",fill=True)
    pdf.ln(); pdf.set_text_color(51,51,51); pdf.set_font("Arial","B",13)
    for val,w in [(f"{mot['prot']}g",49),(f"{mot['carbs']}g",49),(f"{mot['grasa']}g",49),(f"{mot['cals']} kcal",49)]:
        pdf.cell(w,10,_limpiar(val),1,0,"C")
    pdf.ln(12)
    pdf.set_font("Arial","B",12); pdf.cell(0,10,_limpiar("3. DISTRIBUCIÓN EN 4 TOMAS"),0,1)
    p_c,c_c,g_c,k_c = round(mot["prot"]/4,1),round(mot["carbs"]/4,1),round(mot["grasa"]/4,1),round(mot["cals"]/4,0)
    for comida in ["COMIDA 1","COMIDA 2","COMIDA 3","COMIDA 4"]:
        pdf.set_fill_color(243,244,246); pdf.set_font("Arial","B",11)
        pdf.cell(196,8,_limpiar(comida),0,1,"L",fill=True)
        pdf.set_font("Arial","",10)
        pdf.cell(0,6,_limpiar(f"  {k_c} kcal  |  {p_c}g Prot  |  {c_c}g Carbs  |  {g_c}g Grasa"),0,1)
        pdf.cell(0,6,_limpiar(f"  Proteína: {norm['Menu_Proteinas']} | Carbs: {norm['Menu_Carbohidratos']}"),0,1)
        pdf.cell(0,6,_limpiar(f"  Grasas: {norm['Menu_Grasas']} | Verduras: {norm['Menu_Verduras']}"),0,1)
        pdf.ln(3)

    # HOJA 4 - Auditoría clínica
    if len(revs_df) > 0:
        header("HOJA 4: AUDITORÍA CLÍNICA, DELTAS Y PLAN DE ACCIÓN")
        ult = revs_df.iloc[-1]
        peso_actual    = _parse_float(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
        cintura_actual = _parse_float(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])
        estado = str(ult.get("Estado_Calculado","AVANCE")).upper()

        pdf.set_font("Arial","B",12); pdf.cell(0,10,_limpiar("1. CRUCE BIOMÉTRICO (Q1 vs Q2)"),0,1)
        pdf.set_fill_color(80,200,120); pdf.set_text_color(255,255,255)
        for h,w in [("MÉTRICA",60),("Q1 (BASE)",45),("Q2 (ACTUAL)",45),("DELTA NETO",46)]:
            pdf.cell(w,8,_limpiar(h),1,0,"C",fill=True)
        pdf.ln(); pdf.set_text_color(51,51,51); pdf.set_font("Arial","",11)
        dif_peso = round(peso_actual - mot["peso"], 1)
        pdf.cell(60,8,"Peso Corporal",1,0,"C")
        pdf.cell(45,8,f"{mot['peso']} kg",1,0,"C")
        pdf.cell(45,8,f"{peso_actual} kg",1,0,"C")
        pdf.set_text_color(34,197,94) if dif_peso<=0 else pdf.set_text_color(239,68,68)
        pdf.cell(46,8,f"{dif_peso:+.1f} kg",1,1,"C")
        pdf.set_text_color(51,51,51)
        dif_cintura = round(cintura_actual - mot["cintura"], 1)
        pdf.cell(60,8,"Cintura",1,0,"C")
        pdf.cell(45,8,f"{mot['cintura']} cm",1,0,"C")
        pdf.cell(45,8,f"{cintura_actual} cm",1,0,"C")
        pdf.set_text_color(34,197,94) if dif_cintura<=0 else pdf.set_text_color(239,68,68)
        pdf.cell(46,8,f"{dif_cintura:+.1f} cm",1,1,"C")
        pdf.ln(8)
        pdf.set_text_color(51,51,51); pdf.set_font("Arial","B",12)
        pdf.cell(0,10,_limpiar("2. PLAN DE ACCIÓN CLÍNICO"),0,1)
        plan_accion = generar_plan_accion(norm, ult, estado)
        pdf.set_font("Arial","",10)
        for tipo, accion in plan_accion:
            pdf.set_x(15); pdf.multi_cell(180,6,_limpiar(f"-> {accion}"),0,"L")

    return pdf.output(dest="S").encode("latin-1","ignore")

# =============================================================================
# 8. HELPERS DE NAVEGACIÓN
# =============================================================================
def guardar_y_navegar(datos: dict, destino: int):
    st.session_state.db.update(datos)
    st.session_state.step = destino
    st.rerun()

# =============================================================================
# 9. COMPONENTES DE DASHBOARD
# =============================================================================
def render_hero(titulo: str, subtitulo: str, id_al: str = ""):
    id_txt = f"<div style='font-size:11px;color:#8FC99E;letter-spacing:2px;margin-top:8px;'>ID: {id_al}</div>" if id_al else ""
    st.markdown(f"""
    <div class="hero-block">
      <div class="hero-title">MM<span>247</span></div>
      <div class="hero-sub">{subtitulo}</div>
      <div style="font-size:15px;color:#C8E6D0;margin-top:12px;font-weight:600;">{titulo}</div>
      {id_txt}
    </div>
    """, unsafe_allow_html=True)


def render_metric_card(label: str, valor: str, delta: str = "", delta_tipo: str = "neu"):
    delta_html = f"<div class='metric-delta delta-{delta_tipo}'>{delta}</div>" if delta else ""
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-val">{valor}</div>
      {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_accion(tipo: str, texto: str):
    st.markdown(f"<div class='accion-item {'' if tipo=='success' else tipo}'>{texto}</div>", unsafe_allow_html=True)


def render_rutina_table(ejercicios: list, titulo: str):
    st.markdown(f"<div class='rutina-header'>{titulo}</div>", unsafe_allow_html=True)
    for ej, series, reps, desc in ejercicios:
        st.markdown(f"""
        <div class='rutina-row'>
          <div>{ej}</div>
          <div style='text-align:center;font-weight:700;color:#166534;'>{series}</div>
          <div style='text-align:center;color:#50C878;font-weight:700;'>{reps}</div>
          <div style='text-align:center;color:#9CA3AF;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# 10. DASHBOARD Q1 — MI REGISTRO MM247
# =============================================================================
def mostrar_dashboard_q1(norm: dict, mot: dict, id_al: str):
    nombre = norm.get("Nombre completo","Atleta")
    render_hero("EXPEDIENTE ACTIVO — LÍNEA BASE", "MI REGISTRO MM247", id_al)

    # ── Avatar inteligente Q1 + perfil ────────────────────────────────────────
    ca, cb = st.columns([1, 3])
    with ca:
        svg_q1 = construir_avatar_q1(norm, mot)
        render_avatar_svg(svg_q1, height=260)

        # Leyenda de indicadores del avatar
        lesion = norm.get("Lesión actual","Ninguna")
        imc    = mot.get("imc", 22)
        if imc < 18.5:   complexion_lbl = "🔹 Complexión: Delgado"
        elif imc < 25:   complexion_lbl = "🟢 Complexión: Normal"
        elif imc < 30:   complexion_lbl = "🟡 Complexión: Sobrepeso"
        else:            complexion_lbl = "🔴 Complexión: Obesidad"
        st.markdown(f"""
        <div style='font-size:10px;color:#7D9A84;text-align:center;line-height:1.8;margin-top:4px;'>
          {'👩' if 'Femen' in norm.get('Sexo','') else '👨'} {norm.get('Sexo','')}<br>
          {complexion_lbl}<br>
          {'🚨 Lesión: ' + lesion if lesion != 'Ninguna' else '✅ Sin lesiones activas'}<br>
          📏 {mot['estatura']} cm
        </div>
        """, unsafe_allow_html=True)

    with cb:
        # Análisis de zonas de enfoque basado en datos reales
        objetivo  = norm.get("Objetivo principal","")
        estres    = _parse_float(norm.get("Estres_Ext","5"), 5.0)
        recup     = norm.get("Recuperacion_Base","Normal")
        biofeed   = norm.get("Biofeedback_Dig","Sin molestias")
        nivel     = norm.get("Tiempo entrenando","")
        postura   = norm.get("Mala postura","No")

        zonas = []
        if "Perder" in objetivo or "grasa" in objetivo:
            zonas.append(("🔥","Quema de grasa","Déficit calórico activo · Cardio HIIT recomendado"))
        if "Ganar" in objetivo or "muscular" in objetivo:
            zonas.append(("💪","Hipertrofia muscular","Superávit calórico · Progresión de cargas clave"))
        if "Recomposición" in objetivo:
            zonas.append(("⚖️","Recomposición corporal","Balance calórico · Prioridad proteica alta"))
        if lesion != "Ninguna":
            zonas.append(("⚠️",f"Lesión: {lesion}","Protocolo adaptado · Evitar carga axial"))
        if estres >= 7:
            zonas.append(("🧠","Estrés elevado","Priorizar sueño · Reducir volumen de entrenamiento"))
        if "pesadez" in biofeed.lower() or "Gases" in biofeed:
            zonas.append(("🫀","Biofeedback digestivo","Ajuste de fuentes de carbohidratos recomendado"))
        if "Nunca" in nivel or "Menos de 6" in nivel:
            zonas.append(("🌱","Principiante","Inducción activa · Técnica antes que carga"))
        if postura != "No":
            zonas.append(("🦴",f"Corrección postural: {postura}","Ejercicios correctivos incluidos en rutina"))
        if not zonas:
            zonas.append(("✅","Perfil equilibrado","Continuar protocolo estándar de progresión"))

        st.markdown(f"""
        <div style="padding:12px 0 4px;">
          <div style="font-size:26px;font-weight:900;color:#0D1F14;font-family:'Space Grotesk',sans-serif;">{nombre}</div>
          <div style="font-size:12px;color:#50C878;letter-spacing:2px;text-transform:uppercase;margin-top:4px;">
            {mot['genero']} · {int(mot['edad'])} años · {mot['estatura']} cm · IMC {mot['imc']}
          </div>
          <div style="margin-top:8px;"><span class="badge-avance">✅ EXPEDIENTE ACTIVO</span></div>
          <div style="font-size:13px;color:#6B7280;margin-top:6px;">
            Objetivo: <strong style='color:#166534;'>{objetivo}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:12px;'><div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;margin-bottom:8px;'>ÁREAS DE ENFOQUE DETECTADAS</div>", unsafe_allow_html=True)
        for icono, titulo_zona, desc_zona in zonas:
            st.markdown(f"""
            <div style='display:flex;align-items:flex-start;gap:10px;padding:8px 12px;
                        background:#F0FDF4;border-left:3px solid #50C878;border-radius:0 8px 8px 0;
                        margin-bottom:6px;'>
              <span style='font-size:18px;'>{icono}</span>
              <div>
                <div style='font-size:12px;font-weight:700;color:#166534;'>{titulo_zona}</div>
                <div style='font-size:11px;color:#6B7280;margin-top:2px;'>{desc_zona}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Métricas biométricas
    st.markdown("<div class='sec-head'>MÉTRICAS BIOMÉTRICAS BASE</div>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1: render_metric_card("Peso Base", f"{mot['peso']} kg")
    with m2: render_metric_card("Cintura", f"{mot['cintura']} cm")
    with m3: render_metric_card("IMC", str(mot['imc']))
    with m4: render_metric_card("ICA", str(mot['ica']))

    # Origen físico
    st.markdown(f"""
    <div class="panel-card" style="border-left:4px solid #50C878;">
      <div style="font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;">ORIGEN FÍSICO CALCULADO</div>
      <div style="font-size:20px;font-weight:900;color:#0D1F14;margin-top:6px;">{mot['origen']}</div>
      <div style="font-size:12px;color:#6B7280;margin-top:4px;">
        TMB: <strong>{mot['tmb']} kcal</strong> ·
        TDEE: <strong>{mot['tdee']} kcal</strong> ·
        Prescrito: <strong style='color:#166534;'>{mot['cals']} kcal ({mot['balance_str']})</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Macronutrientes
    st.markdown("<div class='sec-head'>PROTOCOLO NUTRICIONAL DIARIO</div>", unsafe_allow_html=True)
    mn1, mn2, mn3, mn4 = st.columns(4)
    with mn1:
        st.markdown(f"""<div class='macro-pill'>
          <div class='macro-pill-val'>{mot['prot']}g</div>
          <div class='macro-pill-lbl'>Proteína</div>
        </div>""", unsafe_allow_html=True)
    with mn2:
        st.markdown(f"""<div class='macro-pill'>
          <div class='macro-pill-val'>{mot['carbs']}g</div>
          <div class='macro-pill-lbl'>Carbohidratos</div>
        </div>""", unsafe_allow_html=True)
    with mn3:
        st.markdown(f"""<div class='macro-pill'>
          <div class='macro-pill-val'>{mot['grasa']}g</div>
          <div class='macro-pill-lbl'>Grasas</div>
        </div>""", unsafe_allow_html=True)
    with mn4:
        st.markdown(f"""<div class='macro-pill'>
          <div class='macro-pill-val'>{mot['cals']}</div>
          <div class='macro-pill-lbl'>kcal/día</div>
        </div>""", unsafe_allow_html=True)

    # Alimentos preferidos
    st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:4px 0;">
      <div>
        <div style="font-size:10px;color:#7D9A84;letter-spacing:1px;font-weight:700;">PROTEÍNAS</div>
        <div style="font-size:13px;color:#0D1F14;font-weight:600;margin-top:4px;">{norm['Menu_Proteinas']}</div>
      </div>
      <div>
        <div style="font-size:10px;color:#7D9A84;letter-spacing:1px;font-weight:700;">CARBOHIDRATOS</div>
        <div style="font-size:13px;color:#0D1F14;font-weight:600;margin-top:4px;">{norm['Menu_Carbohidratos']}</div>
      </div>
      <div>
        <div style="font-size:10px;color:#7D9A84;letter-spacing:1px;font-weight:700;">GRASAS</div>
        <div style="font-size:13px;color:#0D1F14;font-weight:600;margin-top:4px;">{norm['Menu_Grasas']}</div>
      </div>
      <div>
        <div style="font-size:10px;color:#7D9A84;letter-spacing:1px;font-weight:700;">VERDURAS</div>
        <div style="font-size:13px;color:#0D1F14;font-weight:600;margin-top:4px;">{norm['Menu_Verduras']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Programación de entrenamiento
    st.markdown("<div class='sec-head'>PROGRAMACIÓN NEUROMUSCULAR</div>", unsafe_allow_html=True)
    con_lesion = _tiene_lesion(norm)
    t_ent = norm.get("Tiempo entrenando","Menos de 6 meses")
    aplica_induccion = "Nunca" in t_ent or "Menos de 6 meses" in t_ent
    modo = "con_lesion" if con_lesion else "sin_lesion"
    num_dias = int(str(norm.get("Días entrenar","4")).strip()[0]) if str(norm.get("Días entrenar","4")).strip()[0].isdigit() else 4

    if aplica_induccion:
        st.info("⚡ **Protocolo Inducción (1 Mes)** — Acondicionamiento articular y corrección técnica.")
        bloques = ["Inducción (1 Mes)"] * num_dias
        nombres_bloque = [f"DÍA {i+1} — FULL BODY" for i in range(num_dias)]
    else:
        bloques = ["Empuje","Tracción","Pierna","Empuje","Tracción"][:num_dias]
        nombres_bloque = [f"DÍA {i+1} — {b.upper()}" for i, b in enumerate(bloques)]

    tabs_dias = st.tabs(nombres_bloque)
    for i, (tab, bloque) in enumerate(zip(tabs_dias, bloques)):
        with tab:
            if bloque in CONFIG["rutinas"]:
                ejercicios = CONFIG["rutinas"][bloque][modo]
                render_rutina_table(ejercicios, nombres_bloque[i])

    # Parámetros espejo Q1
    st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO — LÍNEA BASE</div>", unsafe_allow_html=True)
    pe1, pe2, pe3, pe4 = st.columns(4)
    items_espejo = [
        (pe1, "Energía", norm.get("P_Energia_Q1","5"), "/10"),
        (pe2, "Calidad Sueño", norm.get("P_Sueno_Q1","5"), "/10"),
        (pe3, "Fuerza", norm.get("P_Fuerza_Q1","5"), "/10"),
        (pe4, "Hambre/Ansiedad", norm.get("P_Hambre_Q1","5"), "/10"),
    ]
    for col, lbl, val, suf in items_espejo:
        with col:
            render_metric_card(lbl, f"{val}{suf}")

    # Fotografías Q1
    st.markdown("<div class='sec-head'>EVIDENCIA VISUAL (FOTOGRAFÍAS Q1)</div>", unsafe_allow_html=True)
    pf1, pf2, pf3 = st.columns(3)

    def mostrar_foto(col, b64_key, label, norm_data=None):
        import base64 as b64lib
        # Intentar desde session_state primero
        b64_data = st.session_state.db.get(b64_key, "") if hasattr(st, 'session_state') else ""
        # Si no hay en session, intentar desde norm (base de datos)
        if not b64_data and norm_data:
            b64_data = str(norm_data.get(b64_key, ""))

        if b64_data and len(b64_data) > 100:
            try:
                img_bytes = b64lib.b64decode(b64_data)
                col.image(img_bytes, caption=f"📸 {label}", use_container_width=True)
            except Exception:
                _foto_placeholder(col, label)
        else:
            _foto_placeholder(col, label)

    def _foto_placeholder(col, label):
        col.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D1F14,#1A3D24);
                    border:2px dashed #50C87840;border-radius:12px;
                    aspect-ratio:2/3;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;padding:20px;
                    min-height:180px;">
          <div style="font-size:32px;margin-bottom:8px;">📷</div>
          <div style="font-size:10px;color:#50C87880;letter-spacing:1px;
                      text-transform:uppercase;text-align:center;">{label}<br>Sin foto</div>
        </div>
        """, unsafe_allow_html=True)

    mostrar_foto(pf1, "foto_frente_b64",  "Frente",  norm)
    mostrar_foto(pf2, "foto_perfil_b64",  "Perfil",  norm)
    mostrar_foto(pf3, "foto_espalda_b64", "Espalda", norm)

    # Alertas clínicas
    st.markdown("<div class='sec-head'>ALERTAS BIOMECÁNICAS</div>", unsafe_allow_html=True)
    alertas = [
        f"Lesión declarada: {norm['Lesión actual']}",
        f"Restricción axial: {norm['Prohibido ejercicio']}",
        f"Estancamiento previo: {norm['Historial_Est']}",
        f"Recuperación muscular: {norm['Recuperacion_Base']}",
        f"Biofeedback digestivo: {norm['Biofeedback_Dig']}",
    ]
    for a in alertas:
        color = "#EF4444" if any(k in a for k in ["Rodilla","Hombro","Espalda","Sí","pesadez","Inflamación"]) else "#50C878"
        st.markdown(f"<div style='padding:8px 14px;border-left:3px solid {color};margin:4px 0;font-size:13px;background:#fff;border-radius:0 6px 6px 0;'>{a}</div>", unsafe_allow_html=True)


# =============================================================================
# 11. DASHBOARD Q2 — MI AVANCE MM247 (AUDITORÍA COMPARATIVA)
# =============================================================================
def mostrar_dashboard_q2(norm: dict, mot: dict, revs_df: pd.DataFrame, id_al: str):
    nombre = norm.get("Nombre completo","Atleta")

    if revs_df.empty:
        st.warning("⚠️ Aún no hay revisiones registradas para este ID. Completa tu auditoría Q2.")
        return

    ult = revs_df.iloc[-1]
    estado = str(ult.get("Estado_Calculado","AVANCE")).upper()
    peso_act    = _parse_float(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
    cintura_act = _parse_float(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])

    render_hero("AUDITORÍA COMPARATIVA — Q1 vs Q2", "MI AVANCE MM247", id_al)

    # ── Avatar inteligente Q2 + análisis dinámico ─────────────────────────────
    ca, cb = st.columns([1, 3])
    with ca:
        svg_q2 = construir_avatar_q2(norm, mot, dict(ult), estado)
        render_avatar_svg(svg_q2, height=280)

        # Leyenda dinámica Q2
        dif_p_prev = round(peso_act - mot["peso"], 1)
        dif_c_prev = round(cintura_act - mot["cintura"], 1)
        color_p = "#22C55E" if dif_p_prev <= 0 else "#EF4444"
        color_c = "#22C55E" if dif_c_prev <= 0 else "#EF4444"
        ring_color_leg = {"AVANCE":"#22C55E","RETROCESO":"#EF4444"}.get(estado,"#F59E0B")
        st.markdown(f"""
        <div style='font-size:10px;text-align:center;line-height:2;margin-top:4px;'>
          <span style='color:{ring_color_leg};font-weight:700;'>{estado}</span><br>
          <span style='color:{color_p};'>Peso {dif_p_prev:+.1f} kg</span><br>
          <span style='color:{color_c};'>Cintura {dif_c_prev:+.1f} cm</span><br>
          <span style='color:#7D9A84;'>Fuerza: {ult.get("Progreso_Fuerza","5")}/10</span>
        </div>
        """, unsafe_allow_html=True)

    with cb:
        badge_map = {
            "AVANCE":    "<span class='badge-avance'>🚀 EN AVANCE</span>",
            "RETROCESO": "<span class='badge-retroceso'>⚠️ RETROCESO DETECTADO</span>",
            "LENTO":     "<span class='badge-lento'>⏳ PROGRESO LENTO</span>",
        }

        # Análisis dinámico basado en datos Q2
        adherencia  = str(ult.get("Adherencia Real al Sistema",""))
        sobrecarga  = str(ult.get("Sobrecarga Progresiva",""))
        tolerancia  = str(ult.get("Tolerancia Metabólica",""))
        fuerza_q2v  = _parse_float(ult.get("Progreso_Fuerza","5"), 5.0)
        energia_q2  = _parse_float(ult.get("Energia","5"), 5.0)
        sueno_q2    = _parse_float(ult.get("Calidad_Sueno","5"), 5.0)

        analisis = []
        if "100%" in adherencia or "80-90%" in adherencia:
            analisis.append(("✅","Adherencia alta","El cliente sigue el protocolo correctamente. Mantener estructura."))
        elif "50%" in adherencia:
            analisis.append(("⚠️","Adherencia media","Revisar obstáculos prácticos. Simplificar plan nutricional."))
        else:
            analisis.append(("🚨","Adherencia crítica","Protocolo abandonado parcialmente. Reencuadre motivacional urgente."))

        if "Sí, subí" in sobrecarga:
            analisis.append(("💪","Sobrecarga progresiva ✓","Adaptación neuromuscular confirmada. Autorizado aumentar +5%."))
        elif "mantuve" in sobrecarga:
            analisis.append(("⏸️","Sin progresión de cargas","Estancamiento potencial. Revisar periodización."))
        else:
            analisis.append(("📉","Pérdida de fuerza","Posible sobreentrenamiento o déficit calórico excesivo."))

        if "pesadez" in tolerancia.lower() or "Inflamación" in tolerancia:
            analisis.append(("🫀","Intolerancia digestiva","Rotar carbohidratos. Evitar gluten y lácteos 2 semanas."))
        else:
            analisis.append(("✅","Tolerancia metabólica OK","Sin ajustes digestivos requeridos."))

        if energia_q2 <= 4:
            analisis.append(("⚡","Energía baja","Revisar calidad de sueño y distribución calórica pre-entreno."))
        if sueno_q2 <= 4:
            analisis.append(("😴","Sueño deficiente","Factor limitante clave. Higiene de sueño como prioridad."))
        if fuerza_q2v >= 8 and estado == "AVANCE":
            analisis.append(("🏆","Alto rendimiento","Perfil de alto desempeño. Candidato para protocolo avanzado."))

        st.markdown(f"""
        <div style="padding:12px 0 4px;">
          <div style="font-size:26px;font-weight:900;color:#0D1F14;">{nombre}</div>
          <div style="margin:8px 0;">{badge_map.get(estado, badge_map['LENTO'])}</div>
          <div style="font-size:12px;color:#6B7280;">
            Adherencia: <strong>{adherencia}</strong> · Sobrecarga: <strong>{sobrecarga}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:10px;'><div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;margin-bottom:8px;'>ANÁLISIS CLÍNICO DINÁMICO</div>", unsafe_allow_html=True)
        for icono, titulo_an, desc_an in analisis:
            color_borde = "#22C55E" if icono in ("✅","💪","🏆") else ("#EF4444" if icono in ("🚨","📉") else "#F59E0B")
            st.markdown(f"""
            <div style='display:flex;align-items:flex-start;gap:10px;padding:7px 12px;
                        background:#fff;border-left:3px solid {color_borde};border-radius:0 8px 8px 0;
                        margin-bottom:5px;box-shadow:0 1px 4px rgba(0,0,0,.04);'>
              <span style='font-size:16px;'>{icono}</span>
              <div>
                <div style='font-size:12px;font-weight:700;color:#0D1F14;'>{titulo_an}</div>
                <div style='font-size:11px;color:#6B7280;margin-top:1px;'>{desc_an}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Deltas biométricos
    st.markdown("<div class='sec-head'>CRUCE BIOMÉTRICO — DELTAS Q1 → Q2</div>", unsafe_allow_html=True)
    dif_peso    = round(peso_act - mot["peso"], 1)
    dif_cintura = round(cintura_act - mot["cintura"], 1)

    dc1, dc2, dc3, dc4 = st.columns(4)
    with dc1:
        render_metric_card("Peso Q1 (Base)", f"{mot['peso']} kg")
    with dc2:
        render_metric_card("Peso Q2 (Actual)", f"{peso_act} kg",
                           f"{dif_peso:+.1f} kg", "pos" if dif_peso <= 0 else "neg")
    with dc3:
        render_metric_card("Cintura Q1 (Base)", f"{mot['cintura']} cm")
    with dc4:
        render_metric_card("Cintura Q2 (Actual)", f"{cintura_act} cm",
                           f"{dif_cintura:+.1f} cm", "pos" if dif_cintura <= 0 else "neg")

    # Gráficas comparativas
    st.markdown("<div class='sec-head'>VISUALIZACIÓN COMPARATIVA</div>", unsafe_allow_html=True)
    gc1, gc2 = st.columns(2)

    with gc1:
        st.markdown("<div class='chart-wrap'><div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;margin-bottom:12px;'>EVOLUCIÓN DE PESO (kg)</div>", unsafe_allow_html=True)
        df_peso = pd.DataFrame({
            "Período": ["Q1 — Base", "Q2 — Actual"],
            "Peso (kg)": [mot["peso"], peso_act]
        })
        st.bar_chart(df_peso.set_index("Período"), color="#50C878", height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    with gc2:
        st.markdown("<div class='chart-wrap'><div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;margin-bottom:12px;'>EVOLUCIÓN DE CINTURA (cm)</div>", unsafe_allow_html=True)
        df_cin = pd.DataFrame({
            "Período": ["Q1 — Base", "Q2 — Actual"],
            "Cintura (cm)": [mot["cintura"], cintura_act]
        })
        st.bar_chart(df_cin.set_index("Período"), color="#3CB371", height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    # Parámetros espejo comparados
    st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO — COMPARATIVA Q1 vs Q2</div>", unsafe_allow_html=True)
    items = [
        ("Energía",         norm.get("P_Energia_Q1","5"), ult.get("Energia","5")),
        ("Calidad Sueño",   norm.get("P_Sueno_Q1","5"),   ult.get("Calidad_Sueno","5")),
        ("Fuerza",          norm.get("P_Fuerza_Q1","5"),  ult.get("Progreso_Fuerza","5")),
        ("Hambre/Ansiedad", norm.get("P_Hambre_Q1","5"),  ult.get("Hambre","5")),
    ]
    radar_data = {}
    for lbl, v1_str, v2_str in items:
        v1 = _parse_float(v1_str, 5.0)
        v2 = _parse_float(v2_str, 5.0)
        radar_data[lbl] = {"Q1": v1, "Q2": v2}

    df_radar = pd.DataFrame(radar_data).T
    st.markdown("<div class='chart-wrap'>", unsafe_allow_html=True)
    st.bar_chart(df_radar, height=250, color=["#50C878","#0D1F14"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Fotografías comparativas Q1 vs Q2
    st.markdown("<div class='sec-head'>EVIDENCIA VISUAL COMPARATIVA (Q1 vs Q2)</div>", unsafe_allow_html=True)
    import base64 as b64lib

    def _decode_foto(b64_str):
        """Decodifica base64 a bytes. Retorna None si no hay datos válidos."""
        if not b64_str or len(str(b64_str)) < 100:
            return None
        try:
            return b64lib.b64decode(str(b64_str))
        except Exception:
            return None

    def _col_foto(col, img_bytes, caption, tag_color="#50C878"):
        if img_bytes:
            col.image(img_bytes, caption=caption, use_container_width=True)
        else:
            col.markdown(f"""
            <div style="background:linear-gradient(135deg,#0D1F14,#1A3D24);
                        border:2px dashed {tag_color}40;border-radius:10px;
                        min-height:160px;display:flex;flex-direction:column;
                        align-items:center;justify-content:center;padding:16px;">
              <div style="font-size:28px;">📷</div>
              <div style="font-size:9px;color:{tag_color}60;letter-spacing:1px;
                          text-transform:uppercase;text-align:center;margin-top:6px;">{caption}</div>
            </div>
            """, unsafe_allow_html=True)

    # Fotos Q1 desde session_state o norm
    f_q1_frente  = _decode_foto(st.session_state.db.get("foto_frente_b64",""))
    f_q1_perfil  = _decode_foto(st.session_state.db.get("foto_perfil_b64",""))
    f_q1_espalda = _decode_foto(st.session_state.db.get("foto_espalda_b64",""))

    # Fotos Q2 desde session_state (recién subidas)
    f_q2_frente  = _decode_foto(st.session_state.get("foto_frente_q2_b64",""))
    f_q2_perfil  = _decode_foto(st.session_state.get("foto_perfil_q2_b64",""))
    f_q2_espalda = _decode_foto(st.session_state.get("foto_espalda_q2_b64",""))

    # Encabezado de columnas
    lbl1, lbl2, lbl3, lbl4, lbl5, lbl6 = st.columns(6)
    for col, txt, color in [
        (lbl1,"FRENTE Q1","#50C878"),(lbl2,"PERFIL Q1","#50C878"),(lbl3,"ESPALDA Q1","#50C878"),
        (lbl4,"FRENTE Q2","#4ADE80"),(lbl5,"PERFIL Q2","#4ADE80"),(lbl6,"ESPALDA Q2","#4ADE80"),
    ]:
        col.markdown(f"<div style='text-align:center;font-size:9px;font-weight:700;color:{color};letter-spacing:1px;padding:4px 0;'>{txt}</div>", unsafe_allow_html=True)

    fc1, fc2, fc3, fc4, fc5, fc6 = st.columns(6)
    _col_foto(fc1, f_q1_frente,  "Frente Q1",  "#50C878")
    _col_foto(fc2, f_q1_perfil,  "Perfil Q1",  "#50C878")
    _col_foto(fc3, f_q1_espalda, "Espalda Q1", "#50C878")
    _col_foto(fc4, f_q2_frente,  "Frente Q2",  "#4ADE80")
    _col_foto(fc5, f_q2_perfil,  "Perfil Q2",  "#4ADE80")
    _col_foto(fc6, f_q2_espalda, "Espalda Q2", "#4ADE80")

    # Análisis adherencia y metabólico
    st.markdown("<div class='sec-head'>ANÁLISIS CLÍNICO DETALLADO</div>", unsafe_allow_html=True)
    aa1, aa2 = st.columns(2)
    with aa1:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;'>ADHERENCIA Y DESEMPEÑO</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='margin-top:12px;'>
          <div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F0F4F1;'>
            <span style='font-size:13px;color:#4B5563;'>Adherencia al sistema</span>
            <strong style='color:#166534;'>{ult.get('Adherencia Real al Sistema','--')}</strong>
          </div>
          <div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F0F4F1;'>
            <span style='font-size:13px;color:#4B5563;'>Sobrecarga progresiva</span>
            <strong style='color:#166534;'>{ult.get('Sobrecarga Progresiva','--')}</strong>
          </div>
          <div style='display:flex;justify-content:space-between;padding:8px 0;'>
            <span style='font-size:13px;color:#4B5563;'>Tolerancia metabólica</span>
            <strong style='color:#166534;'>{ult.get('Tolerancia Metabólica','--')}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with aa2:
        st.markdown("<div class='panel-card'>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;'>RESUMEN DE CAMBIOS</div>", unsafe_allow_html=True)
        color_peso    = "#22C55E" if dif_peso <= 0 else "#EF4444"
        color_cintura = "#22C55E" if dif_cintura <= 0 else "#EF4444"
        icono_peso    = "📉" if dif_peso < 0 else ("📈" if dif_peso > 0 else "➡️")
        icono_cintura = "📉" if dif_cintura < 0 else ("📈" if dif_cintura > 0 else "➡️")
        st.markdown(f"""
        <div style='margin-top:12px;'>
          <div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F0F4F1;'>
            <span style='font-size:13px;color:#4B5563;'>{icono_peso} Variación de peso</span>
            <strong style='color:{color_peso};'>{dif_peso:+.1f} kg</strong>
          </div>
          <div style='display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #F0F4F1;'>
            <span style='font-size:13px;color:#4B5563;'>{icono_cintura} Variación de cintura</span>
            <strong style='color:{color_cintura};'>{dif_cintura:+.1f} cm</strong>
          </div>
          <div style='display:flex;justify-content:space-between;padding:8px 0;'>
            <span style='font-size:13px;color:#4B5563;'>🎯 Objetivo en curso</span>
            <strong style='color:#166534;'>{norm.get('Objetivo principal','--')}</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Plan de acción
    st.markdown("<div class='sec-head'>PLAN DE ACCIÓN CLÍNICO AUTOMATIZADO</div>", unsafe_allow_html=True)
    plan = generar_plan_accion(norm, ult, estado)
    for tipo, texto in plan:
        render_accion(tipo, f"→ {texto}")

    # Dictamen final
    st.markdown("<div class='sec-head'>DICTAMEN FINAL</div>", unsafe_allow_html=True)
    color_dict = {"AVANCE":"linear-gradient(135deg,#50C878,#2E8B57)","RETROCESO":"linear-gradient(135deg,#EF4444,#B91C1C)","LENTO":"linear-gradient(135deg,#F59E0B,#D97706)"}
    texto_dict = {
        "AVANCE":    "El sistema reporta sobrecarga progresiva positiva y adherencia adecuada. Mantener protocolo e incrementar intensidad gradualmente.",
        "RETROCESO": "Se detectan indicadores de retroceso. Revisar adherencia, aplicar deload y ajustar variables nutricionales según plan de acción.",
        "LENTO":     "Progreso por debajo del esperado. Auditar fuentes de estrés externo, calidad de sueño y consistencia del protocolo.",
    }
    st.markdown(f"""
    <div style="background:{color_dict.get(estado, color_dict['AVANCE'])};border-radius:16px;padding:28px;text-align:center;color:#fff;margin-top:8px;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:900;letter-spacing:4px;">{estado}</div>
      <div style="font-size:13px;margin-top:8px;opacity:.9;max-width:600px;margin-left:auto;margin-right:auto;">{texto_dict.get(estado,'')}</div>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# 12. FORMULARIOS DE REGISTRO (Q1 — MULTI PASO)
# =============================================================================
def mostrar_formulario_q1(df_existente: pd.DataFrame):
    render_hero("NUEVO EXPEDIENTE — REGISTRO INICIAL", "MI REGISTRO MM247")

    if "step" not in st.session_state: st.session_state.step = 1
    if "db"   not in st.session_state: st.session_state.db   = {}

    total = 6
    st.progress(st.session_state.step / total)
    st.markdown(f"<div style='text-align:center;font-size:12px;color:#7D9A84;letter-spacing:2px;margin-bottom:20px;'>PASO {st.session_state.step} DE {total}</div>", unsafe_allow_html=True)

    # ── PASO 1: Datos Fisiológicos ────────────────────────────────────────────
    if st.session_state.step == 1:
        with st.form("f_p1"):
            st.markdown("<div class='sec-head'>DATOS FISIOLÓGICOS BASE</div>", unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                v_nom  = st.text_input("Nombre completo:", value=st.session_state.db.get("Nombre completo",""))
                v_edad = st.selectbox("Edad:", [f"{i} años" for i in range(14,81)], index=11)
                v_sexo = st.selectbox("Sexo:", ["Masculino","Femenino"])
                v_est  = st.selectbox("Estatura:", [f"{i} cm" for i in range(120,221)], index=55)
            with c2:
                v_peso  = st.selectbox("Peso actual:", [f"{i} kg" for i in range(40,161)], index=40)
                v_cint  = st.selectbox("Cintura actual:", [f"{i} cm" for i in range(50,150)], index=35)
                v_meta_p= st.selectbox("Peso objetivo:", [f"{i} kg" for i in range(40,161)], index=35)
                v_mail  = st.text_input("Correo electrónico:", value=st.session_state.db.get("Correo electrónico",""))
                v_act   = st.selectbox("Nivel de actividad:", list(CONFIG["factores_actividad"].keys()), index=2)

            if st.form_submit_button("Siguiente ➡️"):
                if not v_nom.strip():
                    st.error("El nombre es requerido.")
                else:
                    guardar_y_navegar({
                        "Nombre completo":v_nom,"Edad":v_edad,"Sexo":v_sexo,
                        "Estatura":v_est,"Peso actual":v_peso,"Cintura inicial":v_cint,
                        "Peso objetivo":v_meta_p,"Correo electrónico":v_mail,
                        "Nivel de actividad":v_act
                    }, 2)

    # ── PASO 2: Fotografías Q1 ────────────────────────────────────────────────
    elif st.session_state.step == 2:
        import base64
        st.markdown("<div class='sec-head'>EVIDENCIA VISUAL — FOTOGRAFÍAS Q1</div>", unsafe_allow_html=True)
        st.info("📸 Sube tus fotos iniciales. Se cruzarán con tus resultados en Mi Avance MM247.")

        # Los file_uploader FUERA del form para poder leerlos antes del submit
        f1, f2, f3 = st.columns(3)
        f_frente  = f1.file_uploader("📷 Frente (Obligatorio)", type=["jpg","jpeg","png"], key="up_frente_q1")
        f_perfil  = f2.file_uploader("📷 Perfil (Obligatorio)",  type=["jpg","jpeg","png"], key="up_perfil_q1")
        f_espalda = f3.file_uploader("📷 Espalda (Obligatorio)", type=["jpg","jpeg","png"], key="up_espalda_q1")

        # Preview en tiempo real
        if f_frente:  f1.image(f_frente,  caption="✅ Frente cargada",  use_container_width=True)
        if f_perfil:  f2.image(f_perfil,  caption="✅ Perfil cargado",  use_container_width=True)
        if f_espalda: f3.image(f_espalda, caption="✅ Espalda cargada", use_container_width=True)

        b1, b2 = st.columns(2)
        if b1.button("⬅️ Atrás", key="back_p2"): guardar_y_navegar({}, 1)
        if b2.button("Siguiente ➡️", key="next_p2"):
            # Convertir a base64 y guardar en session_state
            def to_b64(f):
                if f is None: return ""
                return base64.b64encode(f.read()).decode("utf-8")

            st.session_state.db["foto_frente_b64"]  = to_b64(f_frente)
            st.session_state.db["foto_perfil_b64"]  = to_b64(f_perfil)
            st.session_state.db["foto_espalda_b64"] = to_b64(f_espalda)
            st.session_state.db["fotos_q1"] = "Cargadas" if (f_frente and f_perfil and f_espalda) else "Pendientes"
            guardar_y_navegar({}, 3)

    # ── PASO 3: Antecedentes ──────────────────────────────────────────────────
    elif st.session_state.step == 3:
        with st.form("f_p3"):
            st.markdown("<div class='sec-head'>ANTECEDENTES Y ESTANCAMIENTO</div>", unsafe_allow_html=True)
            v_t_ent = st.selectbox("Tiempo entrenando:", ["Nunca","Menos de 6 meses","De 6 meses a 1 año","1 a 3 años","Más de 3 años"])
            v_dias  = st.selectbox("Días disponibles/semana:", ["3 días por semana","4 días por semana","5 días por semana"])
            v_est   = st.selectbox("Historial de estancamiento:", ["No estoy estancado","Menos de 1 mes","1 a 3 meses","Más de 6 meses"])
            b1, b2 = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Tiempo entrenando":v_t_ent,"Días entrenar":v_dias,"Historial de Estancamiento":v_est}, 2)
            if b2.form_submit_button("Siguiente ➡️"): guardar_y_navegar({"Tiempo entrenando":v_t_ent,"Días entrenar":v_dias,"Historial de Estancamiento":v_est}, 4)

    # ── PASO 4: Perfil Clínico ────────────────────────────────────────────────
    elif st.session_state.step == 4:
        with st.form("f_p4"):
            st.markdown("<div class='sec-head'>PERFIL CLÍNICO Y BIOFEEDBACK</div>", unsafe_allow_html=True)
            v_lesion = st.selectbox("Lesión actual:", ["Ninguna","Rodilla","Hombro","Espalda Baja","Cervicales"])
            v_proh   = st.selectbox("Prohibición carga axial:", ["No","Sí, sobre columna","Sí, flexiones profundas"])
            v_recup  = st.selectbox("Capacidad de recuperación (DOMS):", ["Recuperación rápida","Normal","Llego muy adolorido a la siguiente sesión"])
            v_dig    = st.selectbox("Biofeedback digestivo:", ["Sin molestias","Inflamación ocasional","Gases y pesadez frecuente"])
            v_estres = st.slider("Carga de estrés externo (1=Mínimo, 10=Extremo):", 1, 10, 5)
            v_postura= st.selectbox("Problemas de postura:", ["No","Sí — cifosis","Sí — lordosis","Sí — escoliosis"])
            b1, b2 = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"Lesión actual":v_lesion,"Prohibido ejercicio":v_proh,"Capacidad de Recuperación Base":v_recup,"Biofeedback Digestivo":v_dig,"Carga de Estrés Externo":str(v_estres),"Mala postura":v_postura}, 3)
            if b2.form_submit_button("Siguiente ➡️"):
                guardar_y_navegar({"Lesión actual":v_lesion,"Prohibido ejercicio":v_proh,"Capacidad de Recuperación Base":v_recup,"Biofeedback Digestivo":v_dig,"Carga de Estrés Externo":str(v_estres),"Mala postura":v_postura}, 5)

    # ── PASO 5: Nutrición y Metas ─────────────────────────────────────────────
    elif st.session_state.step == 5:
        with st.form("f_p5"):
            st.markdown("<div class='sec-head'>NUTRICIÓN Y METAS</div>", unsafe_allow_html=True)
            v_obj    = st.selectbox("Objetivo principal:", ["Perder grasa","Ganar masa muscular","Recomposición corporal"])
            v_prots  = st.multiselect("Proteínas preferidas:", ["Pechuga de Pollo","Bisteck","Atún","Huevos","Salmón"], default=["Pechuga de Pollo"])
            v_carbs  = st.multiselect("Carbohidratos:", ["Arroz","Avena","Papa","Tortilla","Camote"], default=["Arroz"])
            v_grasas = st.multiselect("Grasas saludables:", ["Aguacate","Almendras","Crema de Cacahuete","Aceite de Oliva"], default=["Aguacate"])
            v_verds  = st.multiselect("Verduras:", ["Brócoli","Espinacas","Lechuga","Pepino","Calabacín"], default=["Brócoli"])
            b1, b2 = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"Objetivo principal":v_obj,"Menu_Proteinas":", ".join(v_prots),"Menu_Carbohidratos":", ".join(v_carbs),"Menu_Grasas":", ".join(v_grasas),"Menu_Verduras":", ".join(v_verds)}, 4)
            if b2.form_submit_button("Siguiente ➡️"):
                guardar_y_navegar({"Objetivo principal":v_obj,"Menu_Proteinas":", ".join(v_prots),"Menu_Carbohidratos":", ".join(v_carbs),"Menu_Grasas":", ".join(v_grasas),"Menu_Verduras":", ".join(v_verds)}, 6)

    # ── PASO 6: Parámetros Espejo + ENVÍO ─────────────────────────────────────
    elif st.session_state.step == 6:
        with st.form("f_p6"):
            st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO — LÍNEA BASE</div>", unsafe_allow_html=True)
            v_ener = st.slider("Energía promedio en el día (1-10):", 1, 10, 5)
            v_suen = st.slider("Calidad de sueño (1-10):", 1, 10, 5)
            v_fuer = st.slider("Fuerza actual (1-10):", 1, 10, 5)
            v_hamb = st.slider("Nivel de hambre/ansiedad (1-10):", 1, 10, 5)

            b1, b2 = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"P_Energia_Q1":v_ener,"P_Sueno_Q1":v_suen,"P_Fuerza_Q1":v_fuer,"P_Hambre_Q1":v_hamb}, 5)

            if b2.form_submit_button("🚀 ACTIVAR MI EXPEDIENTE MM247"):
                d = st.session_state.db
                d.update({"P_Energia_Q1":v_ener,"P_Sueno_Q1":v_suen,"P_Fuerza_Q1":v_fuer,"P_Hambre_Q1":v_hamb})

                id_nuevo = generar_id_secuencial(df_existente)

                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "INICIAL",
                    "ID_Alumno": id_nuevo,
                    "Nombre completo":             str(d.get("Nombre completo","")),
                    "Edad":                        str(d.get("Edad","")),
                    "Sexo":                        str(d.get("Sexo","")),
                    "Estatura":                    str(d.get("Estatura","")),
                    "Peso actual":                 str(d.get("Peso actual","")),
                    "Cintura inicial":             str(d.get("Cintura inicial","")),
                    "Peso objetivo":               str(d.get("Peso objetivo","")),
                    "Correo electrónico":          str(d.get("Correo electrónico","")),
                    "Nivel de actividad":          str(d.get("Nivel de actividad","")),
                    "Tiempo entrenando":           str(d.get("Tiempo entrenando","")),
                    "Días entrenar":               str(d.get("Días entrenar","")),
                    "Lesión actual":               str(d.get("Lesión actual","")),
                    "Prohibido ejercicio":         str(d.get("Prohibido ejercicio","")),
                    "Mala postura":                str(d.get("Mala postura","")),
                    "Menu_Proteinas":              str(d.get("Menu_Proteinas","")),
                    "Menu_Carbohidratos":          str(d.get("Menu_Carbohidratos","")),
                    "Menu_Grasas":                 str(d.get("Menu_Grasas","")),
                    "Menu_Verduras":               str(d.get("Menu_Verduras","")),
                    "Objetivo principal":          str(d.get("Objetivo principal","")),
                    "P_Energia_Q1":                str(v_ener),
                    "P_Sueno_Q1":                  str(v_suen),
                    "P_Fuerza_Q1":                 str(v_fuer),
                    "P_Hambre_Q1":                 str(v_hamb),
                    "Historial de Estancamiento":  str(d.get("Historial de Estancamiento","")),
                    "Capacidad de Recuperación Base": str(d.get("Capacidad de Recuperación Base","")),
                    "Biofeedback Digestivo":       str(d.get("Biofeedback Digestivo","")),
                    "Carga de Estrés Externo":     str(d.get("Carga de Estrés Externo","")),
                    "Foto_Frente_Q1":              "Recibida" if d.get("foto_frente_b64") else "Pendiente",
                    "Foto_Perfil_Q1":              "Recibida" if d.get("foto_perfil_b64") else "Pendiente",
                    "Foto_Espalda_Q1":             "Recibida" if d.get("foto_espalda_b64") else "Pendiente",
                }

                with st.spinner("Compilando tu ecosistema MM247..."):
                    try:
                        resp = requests.post(CONFIG["webhook_url"], json=payload, timeout=10)
                        if resp.status_code == 200:
                            # Mostrar ID generado
                            st.markdown(f"""
                            <div class="id-box">
                              <div class="id-box-label">TU ID DE ATLETA MM247</div>
                              <div class="id-box-num">{id_nuevo}</div>
                              <div style="font-size:12px;margin-top:10px;opacity:.85;">
                                Guarda este código — lo necesitarás para registrar tu avance
                              </div>
                            </div>
                            """, unsafe_allow_html=True)
                            st.balloons()

                            # Mostrar Dashboard Q1 inmediatamente
                            st.markdown("---")
                            st.markdown("<div style='text-align:center;font-size:14px;color:#50C878;font-weight:700;letter-spacing:2px;'>TU EXPEDIENTE ESTÁ LISTO</div>", unsafe_allow_html=True)
                            norm_temp = {k: str(v) for k, v in d.items()}
                            mot_temp  = calcular_metabolismo(norm_temp)
                            mostrar_dashboard_q1(norm_temp, mot_temp, id_nuevo)

                            st.cache_data.clear()
                            st.session_state.step = 1
                            st.session_state.db   = {}
                        else:
                            st.error("Error al conectar con la base de datos. Inténtalo de nuevo.")
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")


# =============================================================================
# 13. FORMULARIO AUDITORÍA Q2
# =============================================================================
def mostrar_formulario_q2(df_existente: pd.DataFrame):
    render_hero("AUDITORÍA DE AVANCE — REGISTRO PERIÓDICO", "MI AVANCE MM247")

    st.markdown("""
    <div class="panel-card" style="border-left:4px solid #50C878;margin-bottom:24px;">
      <div style="font-size:13px;color:#4B5563;line-height:1.6;">
        Ingresa tu <strong style='color:#166534;'>ID de Atleta</strong> generado al registrarte y
        completa tu auditoría de avance. El sistema calculará tus deltas y generará un plan de acción
        personalizado.
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("f_auditoria", clear_on_submit=False):
        id_ing = st.text_input("🔑 ID de Atleta (Ej: 247001):", placeholder="Ingresa tu ID MM247").strip().upper()

        st.markdown("<div class='sec-head'>EVIDENCIA VISUAL — FOTOGRAFÍAS Q2</div>", unsafe_allow_html=True)
        st.info("📸 Sube tus fotos actuales para el cruce comparativo Q1 vs Q2.")
        fq1, fq2, fq3 = st.columns(3)
        f2_frente  = fq1.file_uploader("📷 Frente Actual",  type=["png","jpg","jpeg"], key="up_frente_q2")
        f2_perfil  = fq2.file_uploader("📷 Perfil Actual",  type=["png","jpg","jpeg"], key="up_perfil_q2")
        f2_espalda = fq3.file_uploader("📷 Espalda Actual", type=["png","jpg","jpeg"], key="up_espalda_q2")
        if f2_frente:  fq1.image(f2_frente,  caption="✅ Frente Q2",  use_container_width=True)
        if f2_perfil:  fq2.image(f2_perfil,  caption="✅ Perfil Q2",  use_container_width=True)
        if f2_espalda: fq3.image(f2_espalda, caption="✅ Espalda Q2", use_container_width=True)

        st.markdown("<div class='sec-head'>MÉTRICAS ACTUALES</div>", unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        peso_rev = m1.number_input("Peso Actual (kg):", min_value=30.0, value=70.0, step=0.1)
        cint_rev = m2.number_input("Cintura Actual (cm):", min_value=40.0, value=80.0, step=0.5)

        st.markdown("<div class='sec-head'>ADHERENCIA Y DESEMPEÑO</div>", unsafe_allow_html=True)
        adherencia = st.selectbox("Adherencia real al sistema:", ["100% Perfecto","80-90% Con fallos mínimos","Cerca del 50%","Menos del 50% / Abandoné"])
        sobrecarga = st.selectbox("Sobrecarga progresiva:", ["Sí, subí peso/reps","Me mantuve igual","No, perdí fuerza"])
        tolerancia = st.selectbox("Tolerancia metabólica:", ["Digestión rápida y normal","Ligera pesadez","Mucha pesadez / Inflamación constante"])

        st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO ACTUALES (1-10)</div>", unsafe_allow_html=True)
        cp1, cp2 = st.columns(2)
        e_rev = cp1.slider("Energía:",        1, 10, 5)
        s_rev = cp2.slider("Calidad Sueño:",  1, 10, 5)
        f_rev = cp1.slider("Fuerza:",         1, 10, 5)
        h_rev = cp2.slider("Hambre/Ansiedad:",1, 10, 5)

        if st.form_submit_button("🚀 GENERAR MI AUDITORÍA DE AVANCE"):
            if not id_ing:
                st.error("El ID es obligatorio para cruzar tus datos.")
            elif df_existente.empty or id_ing not in df_existente["ID_Alumno"].values:
                st.error(f"❌ ID '{id_ing}' no encontrado. Verifica tu ID o regístrate en Mi Registro MM247.")
            else:
                # Calcular estado
                puntos = 0
                if f_rev >= 7 and "Sí" in sobrecarga: puntos += 2
                if "100%" in adherencia or "80-90%" in adherencia: puntos += 1
                estado_calc = "AVANCE" if puntos >= 2 else "RETROCESO"

                payload_rev = {
                    "Fecha":          datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro":  "REVISION",
                    "ID_Alumno":      id_ing,
                    "Peso_Revision":  str(peso_rev),
                    "Cintura_Revision": str(cint_rev),
                    "Energia":        str(e_rev),
                    "Calidad_Sueno":  str(s_rev),
                    "Progreso_Fuerza":str(f_rev),
                    "Hambre":         str(h_rev),
                    "Adherencia Real al Sistema": adherencia,
                    "Sobrecarga Progresiva":      sobrecarga,
                    "Tolerancia Metabólica":      tolerancia,
                    "Foto_Frente_Q2":  "Recibida" if f2_frente  else "Pendiente",
                    "Foto_Perfil_Q2":  "Recibida" if f2_perfil  else "Pendiente",
                    "Foto_Espalda_Q2": "Recibida" if f2_espalda else "Pendiente",
                    "Estado_Calculado": estado_calc,
                }

                # Guardar fotos Q2 en session_state para visualización inmediata
                import base64 as b64lib
                def _to_b64(f):
                    if f is None: return ""
                    f.seek(0)
                    return b64lib.b64encode(f.read()).decode("utf-8")
                st.session_state["foto_frente_q2_b64"]  = _to_b64(f2_frente)
                st.session_state["foto_perfil_q2_b64"]  = _to_b64(f2_perfil)
                st.session_state["foto_espalda_q2_b64"] = _to_b64(f2_espalda)

                with st.spinner("Procesando tu auditoría..."):
                    try:
                        resp = requests.post(CONFIG["webhook_url"], json=payload_rev, timeout=10)
                        if resp.status_code == 200:
                            st.cache_data.clear()
                            st.success(f"✅ Auditoría registrada. Dictamen: **{estado_calc}**")

                            # Cargar datos Q1 y mostrar dashboard Q2
                            df_fresh = cargar_base_datos()
                            df_c1    = df_fresh[df_fresh["Tipo_Registro"] == "INICIAL"]
                            df_c2    = df_fresh[df_fresh["Tipo_Registro"] == "REVISION"]
                            d_brutos = df_c1[df_c1["ID_Alumno"] == id_ing].iloc[0]
                            d_norm   = normalizar_datos_alumno(d_brutos)
                            m_calc   = calcular_metabolismo(d_norm)
                            r_df     = df_c2[df_c2["ID_Alumno"] == id_ing]

                            mostrar_dashboard_q2(d_norm, m_calc, r_df, id_ing)
                        else:
                            st.error("Error al conectar con la base de datos.")
                    except Exception as e:
                        st.error(f"Error: {e}")


# =============================================================================
# 14. DASHBOARD ADMINISTRADOR
# =============================================================================
def mostrar_dashboard_admin(df_existente: pd.DataFrame):
    render_hero("PANEL DE CONTROL MAESTRO", "CONTROL CLÍNICO AVANZADO")

    if df_existente.empty:
        st.warning("Base de datos vacía. En espera de registros Q1.")
        return

    df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"].copy()
    df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"].copy()
    ids_unicos = df_c1["ID_Alumno"].replace("",pd.NA).dropna().unique()

    # KPIs globales
    st.markdown("<div class='sec-head'>KPIs GLOBALES DEL SISTEMA</div>", unsafe_allow_html=True)
    k1, k2, k3, k4 = st.columns(4)
    total_atletas   = len(ids_unicos)
    con_auditoria   = len(df_c2["ID_Alumno"].unique())
    en_avance       = len(df_c2[df_c2["Estado_Calculado"].str.upper() == "AVANCE"]["ID_Alumno"].unique()) if not df_c2.empty else 0
    en_retroceso    = len(df_c2[df_c2["Estado_Calculado"].str.upper() == "RETROCESO"]["ID_Alumno"].unique()) if not df_c2.empty else 0

    with k1: render_metric_card("Total Atletas", str(total_atletas))
    with k2: render_metric_card("Con Auditoría Q2", str(con_auditoria))
    with k3: render_metric_card("En Avance", str(en_avance), delta_tipo="pos")
    with k4: render_metric_card("En Retroceso", str(en_retroceso), delta_tipo="neg")

    # Lista + detalle
    col_list, col_det = st.columns([1, 2])

    with col_list:
        st.markdown("<div class='sec-head'>ATLETAS ACTIVOS</div>", unsafe_allow_html=True)
        for id_al in ids_unicos:
            datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
            nombre_corto = str(datos_al.get("Nombre completo","Atleta"))[:16]
            tiene_q2 = id_al in df_c2["ID_Alumno"].values
            icono = "🟢" if tiene_q2 else "🔵"
            if st.button(f"{icono} {id_al} — {nombre_corto}", key=f"btn_{id_al}", use_container_width=True):
                st.session_state.alumno_seleccionado = id_al

    with col_det:
        if "alumno_seleccionado" in st.session_state:
            id_sel   = st.session_state.alumno_seleccionado
            d_brutos = df_c1[df_c1["ID_Alumno"] == id_sel].iloc[0]
            d_norm   = normalizar_datos_alumno(d_brutos)
            m_calc   = calcular_metabolismo(d_norm)
            r_df     = df_c2[df_c2["ID_Alumno"] == id_sel]

            st.markdown(f"<div class='sec-head'>EXPEDIENTE: {id_sel}</div>", unsafe_allow_html=True)

            estado_actual = "SIN AUDITORÍA"
            if not r_df.empty:
                estado_actual = str(r_df.iloc[-1].get("Estado_Calculado","AVANCE")).upper()

            # Avatar inteligente en admin
            ca2, cb2 = st.columns([1, 3])
            with ca2:
                if not r_df.empty:
                    svg_admin = construir_avatar_q2(d_norm, m_calc, dict(r_df.iloc[-1]), estado_actual)
                else:
                    svg_admin = construir_avatar_q1(d_norm, m_calc)
                render_avatar_svg(svg_admin, height=220)
            with cb2:
                badge_map = {
                    "AVANCE":        "<span class='badge-avance'>🚀 EN AVANCE</span>",
                    "RETROCESO":     "<span class='badge-retroceso'>⚠️ RETROCESO</span>",
                    "SIN AUDITORÍA": "<span class='badge-lento'>📋 SIN Q2 AÚN</span>",
                }
                sexo_icon = "👩" if "Femen" in m_calc.get("genero","") else "👨"
                st.markdown(f"""
                <div style="padding:8px 0;">
                  <div style="font-size:20px;font-weight:900;color:#0D1F14;">{d_norm.get('Nombre completo','')}</div>
                  <div style="margin:6px 0;">{badge_map.get(estado_actual, badge_map['SIN AUDITORÍA'])}</div>
                  <div style="font-size:12px;color:#6B7280;">
                    {sexo_icon} {m_calc['genero']} · {int(m_calc['edad'])} años · {m_calc['peso']} kg · {m_calc['estatura']} cm
                  </div>
                  <div style="font-size:11px;color:#7D9A84;margin-top:4px;">
                    IMC: {m_calc['imc']} · {m_calc['origen']}
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # Deltas
            peso_act    = _parse_float(r_df.iloc[-1].get("Peso_Revision", m_calc["peso"]) if not r_df.empty else m_calc["peso"], m_calc["peso"])
            cintura_act = _parse_float(r_df.iloc[-1].get("Cintura_Revision", m_calc["cintura"]) if not r_df.empty else m_calc["cintura"], m_calc["cintura"])
            dif_p = round(peso_act - m_calc["peso"], 1)
            dif_c = round(cintura_act - m_calc["cintura"], 1)

            ma, mb, mc = st.columns(3)
            with ma: render_metric_card("Peso", f"{peso_act} kg", f"{dif_p:+.1f} kg", "pos" if dif_p<=0 else "neg")
            with mb: render_metric_card("Cintura", f"{cintura_act} cm", f"{dif_c:+.1f} cm", "pos" if dif_c<=0 else "neg")
            with mc: render_metric_card("TDEE", str(m_calc["cals"]), "kcal/día", "neu")

            # Tabs de expediente
            tab_q1_admin, tab_q2_admin = st.tabs(["📋 Dashboard Q1", "📊 Dashboard Q2"])
            with tab_q1_admin:
                mostrar_dashboard_q1(d_norm, m_calc, id_sel)
            with tab_q2_admin:
                mostrar_dashboard_q2(d_norm, m_calc, r_df, id_sel)

            # PDF
            try:
                pdf_bytes = generar_pdf_mm247(d_norm, m_calc, r_df, id_sel)
                st.download_button(
                    "🖨️ DESCARGAR EXPEDIENTE PDF COMPLETO",
                    data=pdf_bytes,
                    file_name=f"MM247_Clinica_{id_sel}.pdf",
                    mime="application/pdf"
                )
            except Exception as err:
                st.error(f"Error generando PDF: {err}")


# =============================================================================
# 15. SIDEBAR Y ENRUTADOR PRINCIPAL
# =============================================================================
df_existente = cargar_base_datos()

with st.sidebar:
    st.markdown("<div class='sidebar-logo'>MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-tagline'>MIND · MUSCLE · ECOSYSTEM</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    # ── Acceso Maestro ──────────────────────────────────────────────────────
    admin_pass = st.text_input("⚙️ Acceso Maestro", type="password", key="admin_pass_input")

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;color:#50C87870;letter-spacing:2px;text-transform:uppercase;padding:4px 0;'>ÁREA DE CLIENTES</div>", unsafe_allow_html=True)

    # ── Botones de navegación clientes ─────────────────────────────────────
    if "vista" not in st.session_state:
        st.session_state.vista = "registro"

    btn_reg_active = "active" if st.session_state.vista == "registro" else ""
    btn_av_active  = "active" if st.session_state.vista == "avance"   else ""

    if st.button("📝  Mi Registro MM247", key="btn_nav_registro", use_container_width=True):
        st.session_state.vista = "registro"
        if "step" in st.session_state: st.session_state.step = 1
        if "db"   in st.session_state: st.session_state.db   = {}
        st.rerun()

    if st.button("📈  Mi Avance MM247", key="btn_nav_avance", use_container_width=True):
        st.session_state.vista = "avance"
        st.rerun()

    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#0D1F14;border:1px solid #50C87830;border-radius:8px;padding:10px 12px;margin-top:8px;'>
      <div style='font-size:9px;letter-spacing:2px;color:#50C87870;text-transform:uppercase;'>Sistema</div>
      <div style='font-size:10px;color:#4B7A5A;margin-top:4px;'>v7.0 · Mind Muscle Ecosystem</div>
    </div>
    """, unsafe_allow_html=True)

# ── ENRUTADOR PRINCIPAL ─────────────────────────────────────────────────────
if admin_pass == CONFIG["admin_password"]:
    mostrar_dashboard_admin(df_existente)

elif admin_pass and admin_pass != CONFIG["admin_password"]:
    st.error("🔑 Clave maestra incorrecta.")

else:
    # Vista clientes según selección del sidebar
    vista = st.session_state.get("vista", "registro")

    if vista == "registro":
        mostrar_formulario_q1(df_existente)

    elif vista == "avance":
        mostrar_formulario_q2(df_existente)
