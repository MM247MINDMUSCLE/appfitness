# -*- coding: utf-8 -*-
"""
MM247 — MIND MUSCLE ECOSYSTEM v8.0
Correcciones definitivas:
- Dashboard solo para admin
- Avatar con Pillow (sin internet)
- Fotos persistidas en disco /tmp
- Porciones exactas en nutrición
- PDF con fotos y avatar
"""
import streamlit as st
import pandas as pd
import datetime, requests, uuid, os, base64, io, hashlib, math
from PIL import Image, ImageDraw, ImageFont

# ReportLab para PDF
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors as rl_colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# =============================================================================
# CONFIG
# =============================================================================
CONFIG = {
    "webhook_url": "https://script.google.com/macros/s/AKfycbx5vDCKmqpe-vsZ2fan0ZQoesLjajIHHHXHOZLtG7-w6-ts3uUl1WkZVHnPnn0F3Cbn/exec",
    "sheet_url":   "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas",
    "admin_pass":  "MM247_Admin",
    "foto_dir":    "/tmp/mm247_fotos",
    "factores": {
        "Sedentario": 1.20, "Poco activo": 1.375,
        "Moderadamente activo": 1.55, "Muy activo": 1.725,
    },
    "rutinas": {
        "Inducción (1 Mes)": {
            "sin_lesion": [
                ("Sentadilla Goblet","3","12-15","60s"),
                ("Flexiones Asistidas","3","8-12","60s"),
                ("Remo con Mancuernas","3","10-12","60s"),
                ("Puente de Glúteo","3","15-20","45s"),
                ("Plancha Abdominal","3","30-45s","45s"),
            ],
            "con_lesion": [
                ("Prensa de Piernas","3","15-20","60s"),
                ("Press Pecho Máquina","3","12-15","60s"),
                ("Jalón Agarre Neutro","3","12-15","60s"),
                ("Extensión Cuádriceps","3","15-20","45s"),
                ("Crunch Suelo","3","15-20","45s"),
            ]
        },
        "Empuje": {
            "sin_lesion": [
                ("Press Banca con Barra","4","6-8","90s"),
                ("Press Inclinado Mancuernas","3","10-12","60s"),
                ("Aperturas Polea Alta","3","15-20","45s"),
                ("Press Militar Barra","3","8-10","90s"),
                ("Elevaciones Laterales","4","12-15","45s"),
            ],
            "con_lesion": [
                ("Press Máquina Neutro","4","10-12","90s"),
                ("Aperturas Polea Media","3","12-15","60s"),
                ("Press Hombro Máquina","3","12-15","60s"),
                ("Elevaciones Cable","4","15-20","45s"),
            ],
        },
        "Tracción": {
            "sin_lesion": [
                ("Dominadas / Jalón","4","6-10","90s"),
                ("Remo con Barra","4","8-10","90s"),
                ("Remo Polea Baja","3","12-15","60s"),
                ("Curl Bíceps Barra","3","10-12","60s"),
            ],
            "con_lesion": [
                ("Jalón Agarre Neutro","4","10-12","90s"),
                ("Remo en Máquina","3","12-15","60s"),
                ("Polea Alta Neutro","3","15-20","45s"),
                ("Curl Martillo","3","12-15","60s"),
            ],
        },
        "Pierna": {
            "sin_lesion": [
                ("Sentadilla con Barra","4","6-8","120s"),
                ("Prensa de Pierna","3","10-12","90s"),
                ("Extensión Cuádriceps","3","15-20","60s"),
                ("Curl Femoral","3","12-15","60s"),
                ("Pantorrillas de Pie","4","15-20","45s"),
            ],
            "con_lesion": [
                ("Prensa Rango Parcial","4","12-15","90s"),
                ("Extensión Cuád. Ligero","3","15-20","60s"),
                ("Hip Thrust con Barra","4","10-12","90s"),
                ("Curl Femoral Tumbado","3","15-20","60s"),
            ],
        },
    },
    # Porciones en gramos por 100 kcal de cada macronutriente
    "porciones_ref": {
        "Pechuga de Pollo":     {"prot": 31, "carbs": 0,  "grasa": 3.6, "kcal_per_100g": 165},
        "Bisteck":              {"prot": 26, "carbs": 0,  "grasa": 8,   "kcal_per_100g": 180},
        "Atún":                 {"prot": 30, "carbs": 0,  "grasa": 1,   "kcal_per_100g": 132},
        "Huevos":               {"prot": 13, "carbs": 1,  "grasa": 11,  "kcal_per_100g": 155},
        "Salmón":               {"prot": 25, "carbs": 0,  "grasa": 13,  "kcal_per_100g": 208},
        "Arroz":                {"prot": 2.7,"carbs": 28, "grasa": 0.3, "kcal_per_100g": 130},
        "Avena":                {"prot": 17, "carbs": 66, "grasa": 7,   "kcal_per_100g": 389},
        "Papa":                 {"prot": 2,  "carbs": 17, "grasa": 0.1, "kcal_per_100g": 77},
        "Tortilla":             {"prot": 6,  "carbs": 49, "grasa": 5,   "kcal_per_100g": 218},
        "Camote":               {"prot": 1.6,"carbs": 20, "grasa": 0.1, "kcal_per_100g": 86},
        "Aguacate":             {"prot": 2,  "carbs": 9,  "grasa": 15,  "kcal_per_100g": 160},
        "Almendras":            {"prot": 21, "carbs": 22, "grasa": 50,  "kcal_per_100g": 579},
        "Crema de Cacahuete":   {"prot": 25, "carbs": 20, "grasa": 50,  "kcal_per_100g": 588},
        "Aceite de Oliva":      {"prot": 0,  "carbs": 0,  "grasa": 100, "kcal_per_100g": 884},
        "Brócoli":              {"prot": 2.8,"carbs": 7,  "grasa": 0.4, "kcal_per_100g": 34},
        "Espinacas":            {"prot": 2.9,"carbs": 3.6,"grasa": 0.4, "kcal_per_100g": 23},
        "Lechuga":              {"prot": 1.4,"carbs": 2.9,"grasa": 0.2, "kcal_per_100g": 17},
        "Pepino":               {"prot": 0.7,"carbs": 3.6,"grasa": 0.1, "kcal_per_100g": 16},
        "Calabacín":            {"prot": 1.2,"carbs": 3.1,"grasa": 0.3, "kcal_per_100g": 17},
    },
}

os.makedirs(CONFIG["foto_dir"], exist_ok=True)


# =============================================================================
# PAGE CONFIG & CSS
# =============================================================================
st.set_page_config(page_title="MM247", page_icon="🟩", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');
@keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
@keyframes pulse  { 0%{box-shadow:0 0 0 0 rgba(80,200,120,.45)} 70%{box-shadow:0 0 0 14px rgba(80,200,120,0)} 100%{box-shadow:0 0 0 0 rgba(80,200,120,0)} }

.stApp { background:#F0F4F1; font-family:'Inter',sans-serif; color:#1A2B1F; }

[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#0D1F14 0%,#132B1A 100%) !important;
  border-right:1px solid #50C87830;
}
[data-testid="stSidebar"] * { color:#E8F5EC !important; }
[data-testid="stSidebar"] .stTextInput input {
  background:#1A3322 !important; border:1px solid #50C87870 !important;
  color:#E8F5EC !important; border-radius:8px;
}

.hero-block {
  background:linear-gradient(135deg,#0D1F14 0%,#1A3D24 60%,#0F2417 100%);
  border-radius:20px; padding:36px 48px; margin-bottom:24px;
  border:1px solid #50C87830; animation:fadeUp .7s ease-out; position:relative; overflow:hidden;
}
.hero-block::before {
  content:'247'; position:absolute; right:-10px; top:-20px;
  font-size:150px; font-weight:900; color:#50C87806;
  font-family:'Space Grotesk',sans-serif; line-height:1;
}
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:48px; font-weight:900; color:#fff; margin:0; letter-spacing:3px; }
.hero-title span { color:#50C878; }
.hero-sub   { font-size:11px; color:#8FC99E; letter-spacing:4px; text-transform:uppercase; margin-top:6px; }

.sec-head {
  font-family:'Space Grotesk',sans-serif; font-size:12px; font-weight:700;
  letter-spacing:2.5px; text-transform:uppercase; color:#50C878;
  border-left:3px solid #50C878; padding-left:12px; margin:28px 0 14px;
}
.panel-card {
  background:#fff; border-radius:16px; padding:24px;
  box-shadow:0 2px 16px rgba(0,0,0,.05); border:1px solid #E8F0EA;
  animation:fadeUp .5s ease-out; margin-bottom:18px;
}
.metric-card {
  background:#fff; border-radius:14px; padding:20px 16px;
  border-top:3px solid #50C878; box-shadow:0 2px 12px rgba(0,0,0,.05);
  transition:transform .2s; margin-bottom:14px;
}
.metric-card:hover { transform:translateY(-3px); }
.metric-label { font-size:10px; font-weight:700; color:#7D9A84; letter-spacing:1.5px; text-transform:uppercase; }
.metric-val   { font-size:28px; font-weight:900; color:#0D1F14; font-family:'Space Grotesk',sans-serif; margin:4px 0; }
.delta-pos { color:#22C55E; font-size:12px; font-weight:700; }
.delta-neg { color:#EF4444; font-size:12px; font-weight:700; }

.id-box {
  background:linear-gradient(135deg,#50C878,#2E8B57); border-radius:16px;
  padding:28px; text-align:center; animation:pulse 2s infinite;
  box-shadow:0 8px 32px rgba(80,200,120,.4);
}
.id-box-num   { font-family:'Space Grotesk',sans-serif; font-size:52px; font-weight:900; color:#fff; letter-spacing:6px; }
.id-box-label { font-size:11px; color:rgba(255,255,255,.8); letter-spacing:3px; text-transform:uppercase; }

.confirm-box {
  background:linear-gradient(135deg,#F0FDF4,#ECFDF5); border:2px solid #86EFAC;
  border-radius:16px; padding:32px; text-align:center;
}

.badge-avance    { background:#DCFCE7;color:#166534;border:1px solid #86EFAC;padding:5px 14px;border-radius:20px;font-weight:700;font-size:12px;display:inline-block; }
.badge-retroceso { background:#FEE2E2;color:#991B1B;border:1px solid #FCA5A5;padding:5px 14px;border-radius:20px;font-weight:700;font-size:12px;display:inline-block; }
.badge-lento     { background:#FEF9C3;color:#854D0E;border:1px solid #FDE047;padding:5px 14px;border-radius:20px;font-weight:700;font-size:12px;display:inline-block; }

.accion-ok   { background:#F0FDF4;border-left:4px solid #22C55E;border-radius:0 8px 8px 0;padding:12px 16px;margin:6px 0;font-size:13px;color:#166534; }
.accion-warn { background:#FFFBEB;border-left:4px solid #F59E0B;border-radius:0 8px 8px 0;padding:12px 16px;margin:6px 0;font-size:13px;color:#78350F; }
.accion-alert{ background:#FFF1F2;border-left:4px solid #EF4444;border-radius:0 8px 8px 0;padding:12px 16px;margin:6px 0;font-size:13px;color:#7F1D1D; }

.macro-pill {
  display:inline-flex;flex-direction:column;align-items:center;
  background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:12px;
  padding:14px 18px;min-width:88px;
}
.macro-pill-val { font-size:22px;font-weight:900;color:#166534;font-family:'Space Grotesk',sans-serif; }
.macro-pill-lbl { font-size:10px;color:#4ADE80;letter-spacing:1px;text-transform:uppercase;font-weight:700; }

div[data-testid="stForm"] {
  background:#fff !important;border-radius:16px !important;
  border:1px solid #E8F0EA !important;padding:24px !important;
  box-shadow:0 2px 16px rgba(0,0,0,.04) !important;
}
label[data-testid="stWidgetLabel"] p { color:#1A2B1F !important; font-weight:600 !important; }

div.stButton > button, div[data-testid="stForm"] button {
  background:linear-gradient(90deg,#50C878,#2E8B57) !important;
  color:#fff !important;border:none !important;border-radius:10px !important;
  font-weight:700 !important;height:48px;width:100%;
  font-family:'Space Grotesk',sans-serif !important;
  letter-spacing:1px;text-transform:uppercase;transition:all .25s;
}
div.stButton > button:hover { transform:translateY(-2px) !important; filter:brightness(1.08) !important; }

.rutina-header {
  background:linear-gradient(90deg,#0D1F14,#1A3D24); color:#50C878;
  font-weight:700;font-size:11px;letter-spacing:1.5px;text-transform:uppercase;
  padding:10px 14px;border-radius:8px 8px 0 0;
}
.rutina-row {
  display:grid;grid-template-columns:3fr 1fr 1fr 1fr;
  padding:9px 14px;border-bottom:1px solid #F0F4F1;
  font-size:13px;transition:background .2s;
}
.rutina-row:hover { background:#F0FDF4; }

.chart-wrap { background:#fff;border-radius:14px;padding:22px;box-shadow:0 2px 12px rgba(0,0,0,.05);border:1px solid #E8F0EA;margin-bottom:14px; }

.porcion-card {
  background:#fff;border-radius:12px;padding:16px;
  border-left:4px solid #50C878;margin-bottom:10px;
  box-shadow:0 2px 8px rgba(0,0,0,.04);
}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DATOS
# =============================================================================
@st.cache_data(ttl=60)
def cargar_db() -> pd.DataFrame:
    try:
        url = f"{CONFIG['sheet_url']}&nc={datetime.datetime.now().timestamp()}"
        df  = pd.read_csv(url)
        df  = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df  = df.fillna("")
        if "ID_Alumno"    not in df.columns: df["ID_Alumno"]    = ""
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = "INICIAL"
        return df
    except Exception:
        return pd.DataFrame()


def gen_id(df: pd.DataFrame) -> str:
    ids = df["ID_Alumno"].dropna().astype(str) if not df.empty else []
    nums = [int(i[3:]) for i in ids if i.startswith("247") and i[3:].isdigit()]
    return f"247{(max(nums)+1 if nums else 1):03d}"


def normalizar(row: pd.Series) -> dict:
    def g(k, d=""):
        v = row.get(k, d)
        return str(v).strip() if pd.notna(v) and str(v).strip() not in ("","nan") else d
    return {
        "Nombre completo":    g("Nombre completo","Atleta"),
        "Edad":               g("Edad","25"),
        "Sexo":               g("Sexo","Masculino"),
        "Estatura":           g("Estatura","175"),
        "Peso actual":        g("Peso actual","80"),
        "Cintura inicial":    g("Cintura inicial","85"),
        "Peso objetivo":      g("Peso objetivo","75"),
        "Nivel de actividad": g("Nivel de actividad","Moderadamente activo"),
        "Objetivo principal": g("Objetivo principal","Recomposición corporal"),
        "Tiempo entrenando":  g("Tiempo entrenando","Menos de 6 meses"),
        "Lesión actual":      g("Lesión actual","Ninguna"),
        "Prohibido ejercicio":g("Prohibido ejercicio","No"),
        "Mala postura":       g("Mala postura","No"),
        "Días entrenar":      g("Días entrenar","4 días por semana"),
        "Menu_Proteinas":     g("Menu_Proteinas","Pechuga de Pollo"),
        "Menu_Carbohidratos": g("Menu_Carbohidratos","Arroz"),
        "Menu_Grasas":        g("Menu_Grasas","Aguacate"),
        "Menu_Verduras":      g("Menu_Verduras","Brócoli"),
        "P_Energia_Q1":       g("P_Energia_Q1","5"),
        "P_Sueno_Q1":         g("P_Sueno_Q1","5"),
        "P_Fuerza_Q1":        g("P_Fuerza_Q1","5"),
        "P_Hambre_Q1":        g("P_Hambre_Q1","5"),
        "Historial_Est":      g("Historial de Estancamiento","No estoy estancado"),
        "Recuperacion_Base":  g("Capacidad de Recuperación Base","Normal"),
        "Biofeedback_Dig":    g("Biofeedback Digestivo","Sin molestias"),
        "Estres_Ext":         g("Carga de Estrés Externo","5"),
    }


def pf(v, d=0.0):
    try: return float(str(v).replace("kg","").replace("cm","").replace("años","").strip().split()[0])
    except: return d


def calcular_metabolismo(n: dict) -> dict:
    peso=pf(n["Peso actual"],80); cintura=pf(n["Cintura inicial"],85)
    est=pf(n["Estatura"],175);    edad=pf(n["Edad"],25)
    gen=n["Sexo"];                act=n["Nivel de actividad"]
    meta=n["Objetivo principal"]

    imc = peso/((est/100)**2) if est>0 else 0
    ica = cintura/est if est>0 else 0
    origen = ("Obesidad / Riesgo Metabólico" if ica>=0.53 else
              "Sobrepeso Músculo-Graso"       if ica>=0.50 else
              "Perfil Atlético / Magro"        if ica<0.43  else "Condición Normal")

    tmb = (66.473+13.751*peso+5.0033*est-6.755*edad if "Masculino" in gen
           else 655.095+9.5634*peso+1.8496*est-4.6756*edad)
    factor = CONFIG["factores"].get(act,1.55)
    tdee   = tmb*factor

    if any(k in meta for k in ("Perder","grasa","Bajar")):
        cals,bal = tdee-400,"Déficit Calórico (-400 kcal)"
    elif any(k in meta for k in ("Ganar","muscular","Volumen")):
        cals,bal = tdee+300,"Superávit Calórico (+300 kcal)"
    else:
        cals,bal = tdee,"Normocalórico (mantenimiento)"

    prot  = round(peso*2.0,1)
    grasa = round(peso*1.0,1)
    carbs = round(max((cals-(prot*4)-(grasa*9))/4,50),1)

    return {"imc":round(imc,1),"ica":round(ica,2),"origen":origen,
            "tmb":round(tmb,0),"tdee":round(tdee,0),"cals":round(cals,0),
            "prot":prot,"grasa":grasa,"carbs":carbs,"balance":bal,
            "factor":factor,"edad":edad,"genero":gen,
            "peso":peso,"cintura":cintura,"estatura":est}


def calcular_porciones(norm: dict, mot: dict) -> dict:
    """Calcula gramos exactos de cada alimento por comida."""
    ref = CONFIG["porciones_ref"]
    prot_c  = mot["prot"]  / 4
    carbs_c = mot["carbs"] / 4
    grasa_c = mot["grasa"] / 4

    def gramos_para_macro(alimento, macro_g, macro_key):
        if alimento not in ref: return 0
        r = ref[alimento]
        if r[macro_key] <= 0: return 0
        return round((macro_g / r[macro_key]) * 100)

    prot_alim  = norm["Menu_Proteinas"].split(",")[0].strip()
    carb_alim  = norm["Menu_Carbohidratos"].split(",")[0].strip()
    grasa_alim = norm["Menu_Grasas"].split(",")[0].strip()
    verd_alim  = norm["Menu_Verduras"].split(",")[0].strip()

    return {
        "prot_alim":  prot_alim,
        "carb_alim":  carb_alim,
        "grasa_alim": grasa_alim,
        "verd_alim":  verd_alim,
        "prot_g":     gramos_para_macro(prot_alim,  prot_c,  "prot"),
        "carbs_g":    gramos_para_macro(carb_alim,  carbs_c, "carbs"),
        "grasa_g":    gramos_para_macro(grasa_alim, grasa_c, "grasa"),
        "verd_g":     150,   # verduras siempre 150g libres
        "prot_kcal":  round(prot_c*4),
        "carbs_kcal": round(carbs_c*4),
        "grasa_kcal": round(grasa_c*9),
        "total_kcal": round(mot["cals"]/4),
    }


def calcular_pasos_diarios(norm: dict, mot: dict) -> dict:
    """
    Calcula pasos diarios recomendados según objetivo, peso, IMC y nivel de actividad.
    Basado en gasto calórico estimado por pasos (~0.04-0.05 kcal/paso según peso).
    """
    objetivo = str(norm.get("Objetivo principal",""))
    actividad= str(norm.get("Nivel de actividad",""))
    peso     = mot["peso"]
    imc      = mot["imc"]

    # Base según nivel de actividad declarado
    base_map = {
        "Sedentario": 6000,
        "Poco activo": 7500,
        "Moderadamente activo": 9000,
        "Muy activo": 11000,
    }
    base = base_map.get(actividad, 8000)

    # Ajuste por objetivo
    if "grasa" in objetivo or "Perder" in objetivo:
        ajuste = 2000   # más pasos para déficit
    elif "muscular" in objetivo or "Ganar" in objetivo:
        ajuste = -500    # menos prioridad cardio, preservar energía para fuerza
    else:
        ajuste = 500     # recomposición: pasos moderados extra

    # Ajuste por IMC (sobrepeso necesita más pasos de bajo impacto)
    if imc >= 30:
        ajuste += 1500
    elif imc >= 25:
        ajuste += 800

    pasos_meta = max(5000, base + ajuste)
    pasos_meta = round(pasos_meta / 500) * 500  # redondear a 500

    # Calorías estimadas quemadas por los pasos
    kcal_por_paso = 0.0005 * peso  # aproximación
    kcal_pasos = round(pasos_meta * kcal_por_paso)

    # Distancia aproximada (paso promedio 0.75m)
    km_aprox = round((pasos_meta * 0.75) / 1000, 1)

    return {
        "pasos_meta": pasos_meta,
        "kcal_pasos": kcal_pasos,
        "km_aprox": km_aprox,
    }


# =============================================================================
# FOTOS — PERSISTENCIA EN DISCO
# =============================================================================
def ruta_foto(id_al: str, tipo: str, etapa: str) -> str:
    """Retorna ruta en disco para una foto. tipo=frente/perfil/espalda, etapa=q1/q2"""
    return os.path.join(CONFIG["foto_dir"], f"{id_al}_{etapa}_{tipo}.jpg")


def guardar_foto_disco(id_al: str, tipo: str, etapa: str, file_obj) -> bool:
    """Guarda foto en disco. Retorna True si OK."""
    try:
        file_obj.seek(0)
        img = Image.open(file_obj).convert("RGB")
        img.thumbnail((800, 1200), Image.LANCZOS)
        img.save(ruta_foto(id_al, tipo, etapa), "JPEG", quality=85)
        return True
    except Exception as e:
        return False


def cargar_foto_disco(id_al: str, tipo: str, etapa: str):
    """Carga foto desde disco. Retorna bytes o None."""
    ruta = ruta_foto(id_al, tipo, etapa)
    if os.path.exists(ruta):
        with open(ruta, "rb") as f:
            return f.read()
    return None


def mostrar_foto(col, id_al: str, tipo: str, etapa: str, label: str):
    """Muestra foto desde disco o placeholder."""
    datos = cargar_foto_disco(id_al, tipo, etapa)
    if datos:
        col.image(datos, caption=f"📸 {label}", use_container_width=True)
    else:
        col.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D1F14,#1A3D24);
                    border:2px dashed #50C87840;border-radius:12px;
                    min-height:180px;display:flex;flex-direction:column;
                    align-items:center;justify-content:center;padding:20px;">
          <div style="font-size:30px;">📷</div>
          <div style="font-size:9px;color:#50C87860;letter-spacing:1px;
                      text-transform:uppercase;text-align:center;margin-top:8px;">
            {label}<br>Sin foto
          </div>
        </div>""", unsafe_allow_html=True)


# =============================================================================
# AVATAR — PILLOW LOCAL (SIN INTERNET)
# =============================================================================
def detectar_persona_en_foto(foto_bytes: bytes):
    """
    Detecta la posición real de la cabeza en la foto analizando tonos de piel
    en bandas horizontales — 100% Pillow, SIN dependencias externas (sin cv2).
    Estima las proporciones corporales reales a partir de esa posición.
    Retorna dict con coordenadas reales o None si no detecta nada confiable.
    """
    from PIL import Image

    img = Image.open(io.BytesIO(foto_bytes)).convert("RGB")
    W, H = img.size

    # Reducir para análisis rápido (no afecta las coordenadas finales, se reescalan)
    analysis_w = 200
    scale = analysis_w / W
    analysis_h = max(1, int(H * scale))
    small = img.resize((analysis_w, analysis_h))
    pixels = small.load()

    def es_piel(r, g, b):
        # Regla de detección de tono de piel humana (rango amplio, varias etnias)
        return (r > 95 and g > 40 and b > 20 and
                r > g and r > b and
                (max(r, g, b) - min(r, g, b)) > 15 and
                abs(int(r) - int(g)) > 10)

    band_h = max(1, analysis_h // 60)
    bandas = []
    for y0 in range(0, analysis_h, band_h):
        count, total = 0, 0
        sum_x_piel = 0
        for y in range(y0, min(y0 + band_h, analysis_h)):
            for x in range(0, analysis_w, 2):
                r, g, b = pixels[x, y]
                total += 1
                if es_piel(r, g, b):
                    count += 1
                    sum_x_piel += x
        ratio = count / total if total else 0
        cx_banda = (sum_x_piel / count) if count > 0 else None
        bandas.append((y0, ratio, cx_banda))

    # Buscar primera banda con concentración significativa de piel (inicio de cabeza)
    umbral = 0.12
    idx_inicio = None
    for i, (y0, ratio, cxb) in enumerate(bandas):
        if ratio > umbral:
            idx_inicio = i
            break

    if idx_inicio is None:
        return None

    cabeza_y0 = bandas[idx_inicio][0]

    # Encontrar fin de zona de piel concentrada (fin de cabeza) y centro X promedio
    cabeza_y1 = cabeza_y0 + band_h
    cx_samples = []
    for i in range(idx_inicio, len(bandas)):
        y0, ratio, cxb = bandas[i]
        if ratio > umbral * 0.55:
            cabeza_y1 = y0 + band_h
            if cxb is not None:
                cx_samples.append(cxb)
        else:
            break

    if not cx_samples:
        return None

    cx_analysis = sum(cx_samples) / len(cx_samples)

    # Reescalar a coordenadas reales de la imagen original
    head_top = int(cabeza_y0 / scale)
    head_bot = int(cabeza_y1 / scale)
    cx_real  = int(cx_analysis / scale)
    head_h   = max(head_bot - head_top, int(H * 0.04))  # mínimo razonable

    # ── Proporciones corporales humanas estándar a partir de la cabeza real ──
    neck_y    = head_bot + int(head_h * 0.15)
    sho_y     = neck_y + int(head_h * 0.25)
    chest_y   = sho_y + int(head_h * 0.4)
    waist_y   = sho_y + int(head_h * 2.2)
    hip_y     = waist_y + int(head_h * 0.3)
    knee_y    = hip_y + int(head_h * 2.0)
    foot_y    = knee_y + int(head_h * 1.9)

    waist_y = min(waist_y, H - 1)
    hip_y   = min(hip_y, H - 1)
    knee_y  = min(knee_y, H - 1)
    foot_y  = min(foot_y, H - 1)

    # face_w estimado proporcional a head_h (proporción típica ancho/alto de rostro)
    face_w = int(head_h * 0.78)

    return {
        "W": W, "H": H,
        "cx": cx_real,
        "head_top": head_top, "head_bot": head_bot,
        "neck_y": neck_y, "sho_y": sho_y, "chest_y": chest_y,
        "waist_y": waist_y, "hip_y": hip_y, "knee_y": knee_y, "foot_y": foot_y,
        "head_h": head_h, "face_w": face_w,
        "detectado": True,
    }


def analizar_foto_con_senalizaciones(foto_bytes: bytes, norm: dict, mot: dict, estado: str = "Q1") -> bytes:
    """
    Detecta la posición real de la persona en la foto y dibuja un ANÁLISIS
    CLÍNICO COMPLETO con marcadores numerados conectados a una leyenda lateral,
    usando TODOS los datos relevantes del cliente: objetivo, lesión, postura,
    IMC/ICA, biofeedback digestivo, estancamiento, recuperación y estrés.
    Cada punto numerado en el cuerpo corresponde a una entrada en la leyenda.
    """
    from PIL import Image, ImageDraw, ImageFont

    img_orig = Image.open(io.BytesIO(foto_bytes)).convert("RGBA")
    W0, H0 = img_orig.size

    # ── Lienzo ampliado: foto + banda lateral derecha para la leyenda ────────
    leyenda_w = int(W0 * 0.62)
    W, H = W0 + leyenda_w, H0
    canvas = Image.new("RGBA", (W, H), (10, 22, 14, 255))
    canvas.paste(img_orig, (0, 0))
    d = ImageDraw.Draw(canvas)

    pos = detectar_persona_en_foto(foto_bytes)

    objetivo   = str(norm.get("Objetivo principal", ""))
    lesion     = str(norm.get("Lesión actual", "Ninguna"))
    postura    = str(norm.get("Mala postura", "No"))
    biofeed    = str(norm.get("Biofeedback_Dig", "Sin molestias"))
    estanc     = str(norm.get("Historial_Est", "No estoy estancado"))
    recup      = str(norm.get("Recuperacion_Base", "Normal"))
    estres     = pf(norm.get("Estres_Ext", "5"), 5.0)
    imc        = mot.get("imc", 22.0)
    ica        = mot.get("ica", 0.48)
    fuerza_q1  = pf(norm.get("P_Fuerza_Q1", "5"), 5.0)

    if estado == "AVANCE":
        ring_col = (34, 197, 94, 255); estado_txt = "AVANCE"
    elif estado == "RETROCESO":
        ring_col = (239, 68, 68, 255); estado_txt = "RETROCESO"
    elif estado == "LENTO":
        ring_col = (245, 158, 11, 255); estado_txt = "LENTO"
    else:
        ring_col = (80, 200, 120, 255); estado_txt = "LÍNEA BASE"

    def font(sz, bold=True):
        path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else \
               "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        try:
            return ImageFont.truetype(path, sz)
        except Exception:
            return ImageFont.load_default()

    fnt_title = font(max(16, int(W0*0.05)))
    fnt_item_n= font(max(13, int(W0*0.034)))
    fnt_item_t= font(max(11, int(W0*0.028)))
    fnt_marker= font(max(14, int(W0*0.032)))

    # ── Badge de estado arriba de la foto ─────────────────────────────────
    badge_w = int(W0 * 0.55)
    badge_h = int(fnt_title.size * 1.7)
    bx_top  = int(H0 * 0.015)
    d.rounded_rectangle(
        [(W0//2 - badge_w//2, bx_top), (W0//2 + badge_w//2, bx_top + badge_h)],
        radius=badge_h//2, fill=ring_col
    )
    bbox = d.textbbox((0,0), estado_txt, font=fnt_title)
    d.text((W0//2 - (bbox[2]-bbox[0])//2, bx_top + badge_h//2 - fnt_title.size//2),
           estado_txt, fill=(255,255,255,255), font=fnt_title)

    # ── Panel de leyenda lateral (fondo) ──────────────────────────────────
    pad = int(W0 * 0.04)
    d.rectangle([(W0, 0), (W, H)], fill=(13, 31, 20, 255))
    ly = int(H0 * 0.04)
    d.text((W0+pad, ly), "ANÁLISIS CLÍNICO", fill=(80,200,120,255), font=fnt_title)
    ly += int(fnt_title.size * 1.6)
    d.line([(W0+pad, ly), (W-pad, ly)], fill=(80,200,120,80), width=2)
    ly += int(H0 * 0.025)

    items = []   # cada item: (numero, color, titulo, detalle, punto_xy_en_foto_o_None)

    # Helper para registrar puntos sobre el cuerpo detectado
    def punto(cx_pt, cy_pt, color, numero):
        r = max(10, int(W0 * 0.028))
        d.ellipse([(cx_pt-r, cy_pt-r),(cx_pt+r, cy_pt+r)], fill=color+(235,), outline=(255,255,255,255), width=2)
        bb = d.textbbox((0,0), str(numero), font=fnt_marker)
        d.text((cx_pt-(bb[2]-bb[0])//2, cy_pt-fnt_marker.size//2), str(numero), fill=(255,255,255,255), font=fnt_marker)

    contador = 1

    if pos is not None:
        cx = pos["cx"]

        # 1. Zona de enfoque muscular principal según objetivo
        if "grasa" in objetivo or "Perder" in objetivo:
            py = pos["waist_y"]
            punto(cx, py, (255,107,53), contador)
            items.append((contador, (255,107,53), "Zona abdominal/cintura",
                          "Prioridad: déficit calórico + cardio HIIT enfocado en grasa visceral."))
            contador += 1
        elif "muscular" in objetivo or "Ganar" in objetivo:
            py = pos["chest_y"]
            punto(cx, py, (59,130,246), contador)
            items.append((contador, (59,130,246), "Pecho / Tren superior",
                          "Prioridad: hipertrofia con sobrecarga progresiva semanal."))
            contador += 1
            py2 = pos["sho_y"]
            punto(cx - int(pos["face_w"]*1.4), py2, (139,92,246), contador)
            items.append((contador, (139,92,246), "Hombros / Deltoides",
                          "Trabajo complementario para simetría y estabilidad articular."))
            contador += 1
        else:
            py = pos["chest_y"]
            punto(cx, py, (59,130,246), contador)
            items.append((contador, (59,130,246), "Recomposición — Torso",
                          "Balance entre pérdida de grasa y ganancia muscular simultánea."))
            contador += 1

        # 2. Marcador de lesión (si existe) — el más crítico visualmente
        if "Rodilla" in lesion and pos["knee_y"] < H0:
            for side in [-1, 1]:
                punto(cx + side*int(pos["face_w"]*0.9), pos["knee_y"], (239,68,68), contador)
            items.append((contador, (239,68,68), "LESIÓN: Rodilla",
                          "Evitar impacto axial. Rutina adaptada sin sentadilla profunda."))
            contador += 1
        elif "Hombro" in lesion:
            for side in [-1, 1]:
                punto(cx + side*int(pos["face_w"]*1.3), pos["sho_y"], (239,68,68), contador)
            items.append((contador, (239,68,68), "LESIÓN: Hombro",
                          "Evitar press por encima de cabeza con carga máxima."))
            contador += 1
        elif "Espalda" in lesion:
            punto(cx, pos["waist_y"] - int(pos["head_h"]*0.3), (239,68,68), contador)
            items.append((contador, (239,68,68), "LESIÓN: Espalda baja",
                          "Activación de core obligatoria antes de cargas axiales."))
            contador += 1
        elif "Cervical" in lesion:
            punto(cx, pos["neck_y"], (239,68,68), contador)
            items.append((contador, (239,68,68), "LESIÓN: Cervical",
                          "Evitar encogimientos pesados y press militar tras nuca."))
            contador += 1

        # 3. Postura (si reportada)
        if postura != "No":
            punto(cx, pos["sho_y"] + int(pos["head_h"]*0.5), (245,158,11), contador)
            items.append((contador, (245,158,11), f"Postura: {postura.replace('Sí — ','').capitalize()}",
                          "Incluir ejercicios correctivos posturales en cada sesión."))
            contador += 1

    else:
        items.append((0, (150,150,150), "Detección no disponible",
                      "Sube una foto de frente con buena iluminación para ubicar zonas exactas."))

    # 4. Composición corporal (siempre, no depende de detección)
    origen_imc = ("Bajo peso" if imc<18.5 else "Normal" if imc<25 else "Sobrepeso" if imc<30 else "Obesidad")
    items.append((contador, (16,185,129), f"IMC {imc} — {origen_imc}",
                  f"ICA: {ica} · Indicador de distribución de grasa central."))
    contador += 1

    # 5. Biofeedback digestivo
    if "pesadez" in biofeed.lower() or "Gases" in biofeed:
        items.append((contador, (236,72,153), "Biofeedback digestivo alterado",
                      "Rotar fuentes de carbohidrato. Posible sensibilidad alimentaria."))
        contador += 1

    # 6. Estancamiento previo
    if "Más de 6" in estanc or "1 a 3" in estanc:
        items.append((contador, (168,85,247), f"Estancamiento previo: {estanc}",
                      "Requiere variación de estímulo y posible recalculo calórico."))
        contador += 1

    # 7. Recuperación / estrés
    if "adolorido" in recup.lower():
        items.append((contador, (244,114,182), "Recuperación muscular lenta",
                      "Aumentar descanso entre sesiones del mismo grupo muscular."))
        contador += 1
    if estres >= 7:
        items.append((contador, (250,204,21), f"Estrés externo alto ({int(estres)}/10)",
                      "Factor limitante para recuperación. Priorizar higiene de sueño."))
        contador += 1

    # ── Dibujar leyenda lateral con todos los items ───────────────────────
    for num, color, titulo, detalle in items:
        if ly > H - int(H0*0.06):
            break  # evitar desbordar el lienzo
        # Círculo numerado
        r_leg = max(11, int(W0*0.026))
        d.ellipse([(W0+pad, ly), (W0+pad+r_leg*2, ly+r_leg*2)], fill=color+(255,))
        bb = d.textbbox((0,0), str(num), font=fnt_item_n)
        d.text((W0+pad+r_leg-(bb[2]-bb[0])//2, ly+r_leg-fnt_item_n.size//2), str(num),
               fill=(255,255,255,255), font=fnt_item_n)
        # Título
        tx = W0 + pad + r_leg*2 + int(pad*0.6)
        d.text((tx, ly), titulo, fill=(255,255,255,255), font=fnt_item_n)
        ly += int(fnt_item_n.size * 1.3)
        # Detalle (wrap simple por longitud)
        max_chars = max(20, int((leyenda_w - (tx - W0)) / (fnt_item_t.size*0.52)))
        palabras = detalle.split()
        linea = ""
        for palabra in palabras:
            test = (linea + " " + palabra).strip()
            if len(test) > max_chars:
                d.text((tx, ly), linea, fill=(180,200,185,255), font=fnt_item_t)
                ly += int(fnt_item_t.size * 1.35)
                linea = palabra
            else:
                linea = test
        if linea:
            d.text((tx, ly), linea, fill=(180,200,185,255), font=fnt_item_t)
            ly += int(fnt_item_t.size * 1.35)
        ly += int(H0 * 0.02)

    result = canvas.convert("RGB")
    buf = io.BytesIO()
    result.save(buf, "JPEG", quality=90)
    buf.seek(0)
    return buf.getvalue()


def mostrar_analisis_visual(id_al: str, norm: dict, mot: dict, etapa: str = "q1", estado: str = "Q1", ancho_px: int = 280):
    """
    Muestra la foto de frente del cliente junto con un panel de análisis
    clínico lateral con marcadores numerados. La imagen combinada (foto +
    leyenda) se muestra a ancho completo del contenedor para que el texto
    de la leyenda sea legible.
    """
    foto_frente = cargar_foto_disco(id_al, "frente", etapa)
    if foto_frente:
        try:
            procesada = analizar_foto_con_senalizaciones(foto_frente, norm, mot, estado)
            pos_check = detectar_persona_en_foto(foto_frente)

            st.image(procesada, use_container_width=True)

            if pos_check is None:
                st.info("ℹ️ No se detectó automáticamente a la persona en la foto. Se muestra el análisis clínico general sin marcadores corporales. Para mejor detección, usa una foto de frente con buena iluminación y rostro visible.")
        except Exception as e:
            st.warning(f"No se pudo procesar el análisis visual: {e}")
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0D1F14,#1A3D24);
                    border:2px dashed #50C87850;border-radius:16px;
                    padding:32px;text-align:center;margin:14px 0;">
          <div style="font-size:34px;">📸</div>
          <div style="font-size:13px;color:#8FC99E;margin-top:8px;font-weight:600;">
            Sube tu foto de frente para ver el análisis visual
          </div>
          <div style="font-size:10px;color:#50C87880;margin-top:4px;">
            Las señalizaciones se generan detectando tu posición real en la fotografía
          </div>
        </div>""", unsafe_allow_html=True)


# =============================================================================
# PDF CON REPORTLAB (FOTOS + AVATAR)
# =============================================================================
def _limpiar(t): return str(t).encode("latin-1","replace").decode("latin-1")

def generar_pdf(norm, mot, por, revs_df, id_al, rutas_fotos_q1=None, rutas_fotos_q2=None):
    buf  = io.BytesIO()
    W, H = letter

    def color_mm(r,g,b): return rl_colors.Color(r/255,g/255,b/255)
    VERDE   = color_mm(80,200,120)
    OSCURO  = color_mm(13,31,20)
    BLANCO  = rl_colors.white
    GRIS    = color_mm(240,244,241)

    c = rl_canvas.Canvas(buf, pagesize=letter)

    def header_page(titulo):
        # Barra verde superior
        c.setFillColor(VERDE)
        c.rect(0, H-50, W, 50, fill=1, stroke=0)
        # Logo
        c.setFillColor(OSCURO)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(28, H-36, "MM247")
        # Título
        c.setFillColor(BLANCO)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(W/2, H-36, _limpiar(titulo))
        # ID
        c.setFont("Helvetica", 9)
        c.drawRightString(W-28, H-36, f"ID: {id_al}")
        # Fecha
        c.setFont("Helvetica", 8)
        c.setFillColor(color_mm(100,120,100))
        c.drawString(28, H-60, f"Generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}")
        return H - 80  # y de inicio de contenido

    def dato_fila(y, label, valor, c_left=60, col_w=220):
        c.setFillColor(GRIS)
        c.rect(c_left, y-4, col_w, 18, fill=1, stroke=0)
        c.setFillColor(OSCURO)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(c_left+4, y+2, _limpiar(label))
        c.setFont("Helvetica", 9)
        c.drawString(c_left+col_w+8, y+2, _limpiar(str(valor)))
        return y - 22

    # ── HOJA 1: PERFIL CLÍNICO ────────────────────────────────────────────────
    c.showPage() if False else None
    y = header_page("HOJA 1 — PERFIL CLÍNICO Y LÍNEA BASE")

    # Análisis visual sobre foto real (lado derecho)
    try:
        foto_frente = cargar_foto_disco(id_al, "frente", "q1")
        if foto_frente:
            av_bytes = analizar_foto_con_senalizaciones(foto_frente, norm, mot, "Q1")
            av_img   = Image.open(io.BytesIO(av_bytes))
            av_img.thumbnail((160, 240))
            av_path  = f"/tmp/mm247_fotos/an_{id_al}_q1.jpg"
            av_img.save(av_path)
            c.drawImage(av_path, W-180, y-220, width=150, height=220, preserveAspectRatio=True)
    except Exception:
        pass

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(VERDE)
    c.drawString(60, y, "DATOS GENERALES")
    y -= 24

    y = dato_fila(y, "Nombre", norm["Nombre completo"])
    y = dato_fila(y, "Edad / Sexo", f"{int(mot['edad'])} años / {mot['genero']}")
    y = dato_fila(y, "Estatura / Peso", f"{mot['estatura']} cm / {mot['peso']} kg")
    y = dato_fila(y, "IMC / ICA", f"{mot['imc']} / {mot['ica']}")
    y = dato_fila(y, "Origen físico", mot['origen'])
    y = dato_fila(y, "Objetivo", norm["Objetivo principal"])
    y = dato_fila(y, "Lesión", norm["Lesión actual"])
    y = dato_fila(y, "Restricción axial", norm["Prohibido ejercicio"])
    y = dato_fila(y, "Estancamiento previo", norm["Historial_Est"])
    y = dato_fila(y, "Recuperación muscular", norm["Recuperacion_Base"])
    y = dato_fila(y, "Biofeedback digestivo", norm["Biofeedback_Dig"])
    y -= 16

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(VERDE)
    c.drawString(60, y, "MÉTRICAS METABÓLICAS")
    y -= 24
    y = dato_fila(y, "TMB (Harris-Benedict)", f"{mot['tmb']} kcal/día")
    y = dato_fila(y, f"TDEE (factor {mot['factor']})", f"{mot['tdee']} kcal/día")
    y = dato_fila(y, "Balance calórico", mot["balance"])
    y = dato_fila(y, "Calorías prescritas/día", f"{mot['cals']} kcal")

    # ── HOJA 2: NUTRICIÓN CON PORCIONES ──────────────────────────────────────
    c.showPage()
    y = header_page("HOJA 2 — PROTOCOLO NUTRICIONAL Y PORCIONES")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(VERDE)
    c.drawString(60, y, "MACRONUTRIENTES DIARIOS")
    y -= 30

    # Tabla macros
    macro_data = [
        ["PROTEÍNA", "CARBOHIDRATOS", "GRASAS", "CALORÍAS TOTALES"],
        [f"{mot['prot']}g", f"{mot['carbs']}g", f"{mot['grasa']}g", f"{mot['cals']} kcal"],
    ]
    col_ws = [120, 120, 100, 120]
    x_start = 60
    for ri, row in enumerate(macro_data):
        x = x_start
        for ci, cell in enumerate(row):
            bg = (80,200,120) if ri==0 else (240,253,244)
            c.setFillColorRGB(*[v/255 for v in bg])
            c.rect(x, y-18, col_ws[ci], 22, fill=1, stroke=1)
            c.setFillColor(BLANCO if ri==0 else OSCURO)
            fn = "Helvetica-Bold" if ri==0 else "Helvetica-Bold"
            c.setFont(fn, ri==0 and 8 or 11)
            c.drawCentredString(x+col_ws[ci]//2, y-10, _limpiar(cell))
            x += col_ws[ci]
        y -= 24

    # Pasos diarios recomendados
    y -= 16
    pasos = calcular_pasos_diarios(norm, mot)
    c.setFillColorRGB(0.94, 0.99, 0.95)
    c.rect(60, y-44, 460, 50, fill=1, stroke=1)
    c.setFillColor(VERDE)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(70, y-14, "🚶 META DIARIA DE PASOS")
    c.setFillColor(OSCURO)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(70, y-34, f"{pasos['pasos_meta']:,} pasos/día")
    c.setFont("Helvetica", 9)
    c.setFillColor(color_mm(100,120,100))
    c.drawString(260, y-20, f"≈ {pasos['km_aprox']} km")
    c.drawString(260, y-34, f"≈ {pasos['kcal_pasos']} kcal extra")
    y -= 60

    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(VERDE)
    c.drawString(60, y, "DISTRIBUCIÓN EN 4 COMIDAS (PORCIONES EXACTAS)")
    y -= 24

    comidas = ["COMIDA 1 — DESAYUNO","COMIDA 2 — ALMUERZO","COMIDA 3 — MERIENDA","COMIDA 4 — CENA"]
    for comida in comidas:
        if y < 120:
            c.showPage()
            y = header_page("HOJA 2 (CONT.) — PORCIONES")
        # Encabezado comida
        c.setFillColor(OSCURO)
        c.rect(60, y-16, 480, 20, fill=1, stroke=0)
        c.setFillColor(VERDE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(66, y-10, _limpiar(comida))
        y -= 22

        # Kcal totales
        c.setFillColor(GRIS)
        c.rect(60, y-14, 480, 18, fill=1, stroke=0)
        c.setFillColor(color_mm(22,163,74))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(66, y-8, f"{por['total_kcal']} kcal  |  "
                              f"{por['prot_kcal']} kcal prot  |  "
                              f"{por['carbs_kcal']} kcal carbs  |  "
                              f"{por['grasa_kcal']} kcal grasa")
        y -= 20

        # Porciones por alimento
        items = [
            ("🥩", "PROTEÍNA",      por['prot_alim'],  f"{por['prot_g']}g",  (59,130,246)),
            ("🍚", "CARBOHIDRATOS", por['carb_alim'],  f"{por['carbs_g']}g", (245,158,11)),
            ("🥑", "GRASA",         por['grasa_alim'], f"{por['grasa_g']}g", (16,185,129)),
            ("🥦", "VERDURA LIBRE", por['verd_alim'],  "150g",               (34,197,94)),
        ]
        for emoji, macro_lbl, alim, gramos, col_rgb in items:
            c.setFillColorRGB(*[v/255 for v in col_rgb], alpha=0.12)
            c.rect(60, y-12, 480, 16, fill=1, stroke=0)
            c.setFillColorRGB(*[v/255 for v in col_rgb])
            c.rect(60, y-12, 4, 16, fill=1, stroke=0)
            c.setFillColor(OSCURO)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(70, y-6, f"{macro_lbl}:")
            c.setFont("Helvetica", 8)
            c.drawString(140, y-6, _limpiar(alim))
            c.setFont("Helvetica-Bold", 9)
            c.setFillColorRGB(*[v/255 for v in col_rgb])
            c.drawRightString(530, y-6, _limpiar(gramos))
            y -= 18
        y -= 8

    # ── HOJA 3: ENTRENAMIENTO ────────────────────────────────────────────────
    c.showPage()
    y = header_page("HOJA 3 — PROGRAMACIÓN NEUROMUSCULAR")

    con_lesion = (norm.get("Lesión actual","Ninguna").lower() != "ninguna" or
                  norm.get("Prohibido ejercicio","No").lower() != "no")
    t_ent      = norm.get("Tiempo entrenando","")
    aplica_ind = "Nunca" in t_ent or "Menos de 6" in t_ent
    modo       = "con_lesion" if con_lesion else "sin_lesion"
    num_dias   = int(str(norm.get("Días entrenar","4")).strip()[0]) if str(norm.get("Días entrenar","4")).strip()[0].isdigit() else 4

    if aplica_ind:
        bloques = ["Inducción (1 Mes)"] * num_dias
        nombres = [f"DÍA {i+1} — FULL BODY INDUCCIÓN" for i in range(num_dias)]
    else:
        bloques = ["Empuje","Tracción","Pierna","Empuje","Tracción"][:num_dias]
        nombres = [f"DÍA {i+1} — {b.upper()}" for i,b in enumerate(bloques)]

    for i, bloque in enumerate(bloques):
        if bloque not in CONFIG["rutinas"]: continue
        ejercicios = CONFIG["rutinas"][bloque][modo]
        if y < 140:
            c.showPage()
            y = header_page("HOJA 3 (CONT.) — ENTRENAMIENTO")

        c.setFillColor(OSCURO)
        c.rect(60, y-16, 480, 20, fill=1, stroke=0)
        c.setFillColor(VERDE)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(66, y-10, _limpiar(nombres[i]))
        y -= 24

        # Cabecera tabla
        cols_w = [250, 60, 80, 90]
        cols_x = [60, 310, 370, 450]
        hdrs   = ["EJERCICIO","SERIES","REPS","DESCANSO"]
        c.setFillColor(GRIS)
        c.rect(60, y-14, 480, 18, fill=1, stroke=0)
        for ci,(hdr,cx2) in enumerate(zip(hdrs,cols_x)):
            c.setFillColor(color_mm(100,120,100))
            c.setFont("Helvetica-Bold", 7)
            c.drawString(cx2+2, y-8, hdr)
        y -= 20

        for j,(ej,ser,rep,desc) in enumerate(ejercicios):
            if j%2==0:
                c.setFillColor(rl_colors.Color(0.96,0.99,0.96))
                c.rect(60, y-12, 480, 16, fill=1, stroke=0)
            c.setFillColor(OSCURO)
            c.setFont("Helvetica", 8)
            c.drawString(62, y-6, _limpiar(ej))
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(340, y-6, ser)
            c.drawCentredString(410, y-6, rep)
            c.setFont("Helvetica", 8)
            c.drawCentredString(490, y-6, desc)
            y -= 16
        y -= 10

    # ── HOJA 4: FOTOGRAFÍAS Q1 ────────────────────────────────────────────────
    c.showPage()
    y = header_page("HOJA 4 — EVIDENCIA FOTOGRÁFICA Q1")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(VERDE)
    c.drawString(60, y, "FOTOGRAFÍAS INICIALES (LÍNEA BASE)")
    y -= 24

    foto_tipos  = ["frente","perfil","espalda"]
    foto_labels = ["FRENTE","PERFIL","ESPALDA"]
    foto_x      = [40, 210, 380]
    foto_w      = 155
    foto_h      = 220

    for i, (tipo, lbl, fx) in enumerate(zip(foto_tipos, foto_labels, foto_x)):
        datos = cargar_foto_disco(id_al, tipo, "q1")
        c.setFillColor(OSCURO)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(fx + foto_w//2, y, lbl)
        if datos:
            try:
                tmp = f"/tmp/mm247_fotos/pdf_{id_al}_q1_{tipo}.jpg"
                with open(tmp,"wb") as f: f.write(datos)
                c.drawImage(tmp, fx, y-foto_h-10, width=foto_w, height=foto_h,
                            preserveAspectRatio=True)
            except Exception:
                c.setFillColor(GRIS)
                c.rect(fx, y-foto_h-10, foto_w, foto_h, fill=1, stroke=1)
                c.setFillColor(color_mm(100,120,100))
                c.drawCentredString(fx+foto_w//2, y-foto_h//2-10, "Sin foto")
        else:
            c.setFillColor(GRIS)
            c.rect(fx, y-foto_h-10, foto_w, foto_h, fill=1, stroke=1)
            c.setFillColor(color_mm(100,120,100))
            c.drawCentredString(fx+foto_w//2, y-foto_h//2-10, "Sin foto")

    y -= (foto_h + 30)

    # Análisis visual sobre foto real en PDF
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(VERDE)
    c.drawString(60, y, "ANÁLISIS VISUAL (ZONAS DE ENFOQUE Y SEÑALIZACIONES)")
    y -= 16
    try:
        foto_frente_an = cargar_foto_disco(id_al, "frente", "q1")
        if foto_frente_an:
            av_bytes = analizar_foto_con_senalizaciones(foto_frente_an, norm, mot, "Q1")
            av_path  = f"/tmp/mm247_fotos/an_pdf_{id_al}_q1.jpg"
            with open(av_path,"wb") as f: f.write(av_bytes)
            c.drawImage(av_path, W//2-80, y-240, width=160, height=240, preserveAspectRatio=True)
        else:
            c.setFillColor(color_mm(150,150,150))
            c.setFont("Helvetica", 9)
            c.drawCentredString(W//2, y-100, "Sin foto de frente disponible para análisis")
    except Exception:
        pass

    # ── HOJA 5: AUDITORÍA Q2 (si existe) ────────────────────────────────────
    if not revs_df.empty:
        c.showPage()
        y = header_page("HOJA 5 — AUDITORÍA CLÍNICA Q2")
        ult        = revs_df.iloc[-1]
        peso_q2    = pf(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
        cintura_q2 = pf(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])
        estado     = str(ult.get("Estado_Calculado","AVANCE")).upper()
        dif_p      = round(peso_q2 - mot["peso"],1)
        dif_c      = round(cintura_q2 - mot["cintura"],1)

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(VERDE)
        c.drawString(60, y, "CRUCE BIOMÉTRICO Q1 vs Q2")
        y -= 28

        for lbl2, v1, v2, dif in [
            ("Peso Corporal",f"{mot['peso']} kg",f"{peso_q2} kg",f"{dif_p:+.1f} kg"),
            ("Cintura",      f"{mot['cintura']} cm",f"{cintura_q2} cm",f"{dif_c:+.1f} cm"),
        ]:
            col_v = rl_colors.Color(0.13,0.77,0.37) if float(dif.split()[0])<=0 else rl_colors.Color(0.94,0.27,0.27)
            c.setFillColor(GRIS); c.rect(60,y-14,140,18,fill=1,stroke=0)
            c.setFillColor(OSCURO); c.setFont("Helvetica-Bold",9)
            c.drawString(64,y-8,lbl2)
            c.setFillColor(rl_colors.Color(0.96,0.99,0.96)); c.rect(200,y-14,100,18,fill=1,stroke=0)
            c.setFillColor(OSCURO); c.setFont("Helvetica",9); c.drawCentredString(250,y-8,v1)
            c.setFillColor(rl_colors.Color(0.96,0.99,0.96)); c.rect(305,y-14,100,18,fill=1,stroke=0)
            c.drawCentredString(355,y-8,v2)
            c.setFillColor(col_v); c.rect(410,y-14,100,18,fill=1,stroke=0)
            c.setFont("Helvetica-Bold",10); c.setFillColor(BLANCO); c.drawCentredString(460,y-8,dif)
            y -= 22

        y -= 16
        # Fotos Q2
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(VERDE)
        c.drawString(60, y, "EVIDENCIA FOTOGRÁFICA Q2")
        y -= 22

        for tipo, lbl, fx in zip(foto_tipos, foto_labels, foto_x):
            datos = cargar_foto_disco(id_al, tipo, "q2")
            c.setFillColor(OSCURO); c.setFont("Helvetica-Bold",8)
            c.drawCentredString(fx+foto_w//2, y, lbl+" Q2")
            if datos:
                try:
                    tmp = f"/tmp/mm247_fotos/pdf_{id_al}_q2_{tipo}.jpg"
                    with open(tmp,"wb") as f: f.write(datos)
                    c.drawImage(tmp, fx, y-foto_h-8, width=foto_w, height=foto_h,
                                preserveAspectRatio=True)
                except Exception:
                    c.setFillColor(GRIS); c.rect(fx,y-foto_h-8,foto_w,foto_h,fill=1,stroke=1)
                    c.setFillColor(color_mm(100,120,100)); c.drawCentredString(fx+foto_w//2,y-foto_h//2-8,"Sin foto")
            else:
                c.setFillColor(GRIS); c.rect(fx,y-foto_h-8,foto_w,foto_h,fill=1,stroke=1)
                c.setFillColor(color_mm(100,120,100)); c.drawCentredString(fx+foto_w//2,y-foto_h//2-8,"Sin foto")

        y -= (foto_h + 30)

        # Análisis visual Q2 sobre foto real
        c.setFont("Helvetica-Bold",10); c.setFillColor(VERDE)
        c.drawString(60, y, f"ANÁLISIS VISUAL Q2 — DICTAMEN: {estado}")
        y -= 16
        try:
            foto_frente_q2 = cargar_foto_disco(id_al, "frente", "q2")
            if foto_frente_q2:
                av2_bytes = analizar_foto_con_senalizaciones(foto_frente_q2, norm, mot, estado)
                av2_path  = f"/tmp/mm247_fotos/an_pdf_{id_al}_q2.jpg"
                with open(av2_path,"wb") as f: f.write(av2_bytes)
                c.drawImage(av2_path, W//2-80, y-220, width=160, height=220, preserveAspectRatio=True)
            else:
                c.setFillColor(color_mm(150,150,150))
                c.setFont("Helvetica", 9)
                c.drawCentredString(W//2, y-100, "Sin foto de frente Q2 disponible")
        except Exception:
            pass

    c.save()
    return buf.getvalue()


# =============================================================================
# HELPERS UI
# =============================================================================
def render_hero(titulo, subtitulo, id_al=""):
    id_html = f"<div style='font-size:11px;color:#8FC99E;margin-top:8px;'>ID: {id_al}</div>" if id_al else ""
    st.markdown(f"""
    <div class="hero-block">
      <div class="hero-title">MM<span>247</span></div>
      <div class="hero-sub">{subtitulo}</div>
      <div style="font-size:14px;color:#C8E6D0;margin-top:10px;font-weight:600;">{titulo}</div>
      {id_html}
    </div>""", unsafe_allow_html=True)

def metric_card(label, val, delta="", delta_pos=True):
    dhtml = ""
    if delta:
        cls = "delta-pos" if delta_pos else "delta-neg"
        dhtml = f"<div class='{cls}'>{delta}</div>"
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-val">{val}</div>
      {dhtml}
    </div>""", unsafe_allow_html=True)

def accion_item(tipo, texto):
    css = {"ok":"accion-ok","warn":"accion-warn","alert":"accion-alert"}.get(tipo,"accion-ok")
    st.markdown(f"<div class='{css}'>→ {texto}</div>", unsafe_allow_html=True)

def guardar_y_navegar(datos, destino):
    st.session_state.db.update(datos)
    st.session_state.step = destino
    st.rerun()

def generar_plan(norm, ult, estado):
    plan = []
    adh = str(ult.get("Adherencia Real al Sistema",""))
    sob = str(ult.get("Sobrecarga Progresiva",""))
    tol = str(ult.get("Tolerancia Metabólica",""))
    if "50%" in adh or "Abandoné" in adh:
        plan.append(("alert","ADHERENCIA CRÍTICA: Simplificar el plan. Revisar picos de ansiedad alimentaria."))
    if estado=="RETROCESO" and "No" in sob:
        plan.append(("alert","DELOAD URGENTE: Reducir volumen 30% por 1 semana para disipar fatiga acumulada."))
    if "pesadez" in tol.lower() or "Inflamación" in tol.lower():
        plan.append(("warn","BIOFEEDBACK: Rotar carbohidratos. Eliminar gluten y lácteos 2 semanas."))
    if estado=="AVANCE" and "Sí" in sob:
        plan.append(("ok","LUZ VERDE: Aumentar cargas en compuestos +5%. Mantener balance calórico."))
    if not plan:
        plan.append(("ok","MANTENIMIENTO: Parámetros estables. Continuar sin modificaciones agresivas."))
    return plan


# =============================================================================
# DASHBOARD Q1 — SOLO ADMIN
# =============================================================================
def dashboard_q1(norm, mot, por, id_al):
    nombre = norm.get("Nombre completo","Atleta")
    pasos  = calcular_pasos_diarios(norm, mot)
    render_hero("EXPEDIENTE ACTIVO — LÍNEA BASE", "MI REGISTRO MM247", id_al)

    # Análisis visual sobre foto real — ANCHO COMPLETO para legibilidad
    st.markdown("<div class='sec-head'>ANÁLISIS VISUAL — FOTO CON SEÑALIZACIONES</div>", unsafe_allow_html=True)
    mostrar_analisis_visual(id_al, norm, mot, etapa="q1", estado="Q1")

    col_av, col_info = st.columns([1, 2])
    with col_av:
        lesion = norm.get("Lesión actual","Ninguna")
        imc = mot["imc"]
        comp = ("🔹 Delgado/a" if imc<18.5 else "🟢 Normal" if imc<25 else "🟡 Sobrepeso" if imc<30 else "🔴 Obesidad")
        st.markdown(f"""
        <div style="font-size:11px;color:#7D9A84;text-align:center;line-height:2;margin-top:6px;">
          {'👩' if 'Femen' in norm.get('Sexo','') else '👨'} {norm.get('Sexo','')} · {comp}<br>
          {'🚨 '+lesion if lesion!='Ninguna' else '✅ Sin lesiones'}<br>
          📏 {mot['estatura']} cm · ⚖️ {mot['peso']} kg
        </div>""", unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div style="padding:10px 0;">
          <div style="font-size:28px;font-weight:900;color:#0D1F14;font-family:'Space Grotesk',sans-serif;">{nombre}</div>
          <div style="font-size:12px;color:#50C878;letter-spacing:2px;text-transform:uppercase;margin-top:4px;">
            {mot['genero']} · {int(mot['edad'])} años · IMC {mot['imc']} · {mot['origen']}
          </div>
          <div style="margin-top:8px;"><span class="badge-avance">✅ EXPEDIENTE ACTIVO</span></div>
          <div style="font-size:13px;color:#6B7280;margin-top:8px;">
            Objetivo: <strong style='color:#166534;'>{norm.get('Objetivo principal','')}</strong>
          </div>
        </div>""", unsafe_allow_html=True)

        # Zonas de enfoque
        objetivo = norm.get("Objetivo principal","")
        estres   = pf(norm.get("Estres_Ext","5"),5)
        zonas = []
        if "grasa" in objetivo or "Perder" in objetivo:
            zonas.append(("🔥","Quema de grasa","Déficit calórico · Cardio HIIT recomendado"))
        if "muscular" in objetivo or "Ganar" in objetivo:
            zonas.append(("💪","Hipertrofia","Superávit · Progresión de cargas"))
        if "Recomposición" in objetivo:
            zonas.append(("⚖️","Recomposición","Balance calórico · Alta proteína"))
        if norm.get("Lesión actual","Ninguna") != "Ninguna":
            zonas.append(("⚠️",f"Lesión: {norm['Lesión actual']}","Protocolo adaptado activo"))
        if estres >= 7:
            zonas.append(("🧠","Estrés elevado","Priorizar sueño · Reducir volumen"))
        if "pesadez" in norm.get("Biofeedback_Dig","").lower():
            zonas.append(("🫀","Biofeedback digestivo","Rotar carbohidratos"))
        if "Nunca" in norm.get("Tiempo entrenando","") or "Menos de 6" in norm.get("Tiempo entrenando",""):
            zonas.append(("🌱","Principiante","Inducción activa · Técnica primero"))

        st.markdown("<div style='margin-top:12px;font-size:11px;color:#7D9A84;letter-spacing:1.5px;font-weight:700;'>ÁREAS DE ENFOQUE</div>", unsafe_allow_html=True)
        for ico, tit, desc in zonas[:5]:
            st.markdown(f"""
            <div style="display:flex;gap:10px;padding:7px 10px;background:#F0FDF4;
                        border-left:3px solid #50C878;border-radius:0 8px 8px 0;margin:4px 0;">
              <span style="font-size:16px;">{ico}</span>
              <div>
                <div style="font-size:12px;font-weight:700;color:#166534;">{tit}</div>
                <div style="font-size:10px;color:#6B7280;">{desc}</div>
              </div>
            </div>""", unsafe_allow_html=True)

    # Métricas biométricas
    st.markdown("<div class='sec-head'>MÉTRICAS BIOMÉTRICAS</div>", unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    with m1: metric_card("Peso Base",    f"{mot['peso']} kg")
    with m2: metric_card("Cintura",      f"{mot['cintura']} cm")
    with m3: metric_card("IMC",          str(mot['imc']))
    with m4: metric_card("ICA",          str(mot['ica']))

    # Metabolismo
    st.markdown(f"""
    <div class="panel-card" style="border-left:4px solid #50C878;">
      <div style="font-size:11px;color:#7D9A84;font-weight:700;letter-spacing:1.5px;">ORIGEN FÍSICO CALCULADO</div>
      <div style="font-size:20px;font-weight:900;color:#0D1F14;margin-top:4px;">{mot['origen']}</div>
      <div style="font-size:12px;color:#6B7280;margin-top:4px;">
        TMB: <strong>{mot['tmb']} kcal</strong> · TDEE: <strong>{mot['tdee']} kcal</strong> ·
        Prescrito: <strong style='color:#166534;'>{mot['cals']} kcal ({mot['balance']})</strong>
      </div>
    </div>""", unsafe_allow_html=True)

    # Macronutrientes + Porciones
    st.markdown("<div class='sec-head'>PROTOCOLO NUTRICIONAL — PORCIONES POR COMIDA</div>", unsafe_allow_html=True)
    mn1,mn2,mn3,mn4 = st.columns(4)
    with mn1:
        st.markdown(f"""<div class="macro-pill">
          <div class="macro-pill-val">{mot['prot']}g</div>
          <div class="macro-pill-lbl">Proteína/día</div>
        </div>""", unsafe_allow_html=True)
    with mn2:
        st.markdown(f"""<div class="macro-pill">
          <div class="macro-pill-val">{mot['carbs']}g</div>
          <div class="macro-pill-lbl">Carbs/día</div>
        </div>""", unsafe_allow_html=True)
    with mn3:
        st.markdown(f"""<div class="macro-pill">
          <div class="macro-pill-val">{mot['grasa']}g</div>
          <div class="macro-pill-lbl">Grasa/día</div>
        </div>""", unsafe_allow_html=True)
    with mn4:
        st.markdown(f"""<div class="macro-pill">
          <div class="macro-pill-val">{mot['cals']}</div>
          <div class="macro-pill-lbl">kcal/día</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    for i, comida in enumerate(["🌅 COMIDA 1 — DESAYUNO","☀️ COMIDA 2 — ALMUERZO","🌤️ COMIDA 3 — MERIENDA","🌙 COMIDA 4 — CENA"]):
        st.markdown(f"""
        <div class="porcion-card">
          <div style="font-size:12px;font-weight:700;color:#166534;margin-bottom:8px;">{comida} — {por['total_kcal']} kcal</div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;font-size:12px;">
            <div><span style="color:#3B82F6;font-weight:700;">🥩 {por['prot_alim']}</span><br>
                 <span style="font-size:16px;font-weight:900;color:#1E40AF;">{por['prot_g']}g</span></div>
            <div><span style="color:#F59E0B;font-weight:700;">🍚 {por['carb_alim']}</span><br>
                 <span style="font-size:16px;font-weight:900;color:#D97706;">{por['carbs_g']}g</span></div>
            <div><span style="color:#10B981;font-weight:700;">🥑 {por['grasa_alim']}</span><br>
                 <span style="font-size:16px;font-weight:900;color:#059669;">{por['grasa_g']}g</span></div>
            <div><span style="color:#22C55E;font-weight:700;">🥦 {por['verd_alim']}</span><br>
                 <span style="font-size:16px;font-weight:900;color:#16A34A;">150g</span></div>
          </div>
        </div>""", unsafe_allow_html=True)

    # Pasos diarios recomendados
    st.markdown("<div class='sec-head'>ACTIVIDAD DIARIA — PASOS RECOMENDADOS</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="panel-card" style="border-left:4px solid #50C878;text-align:center;">
      <div style="font-size:11px;color:#7D9A84;font-weight:700;letter-spacing:1.5px;">META DIARIA DE PASOS</div>
      <div style="font-size:42px;font-weight:900;color:#166534;font-family:'Space Grotesk',sans-serif;margin:8px 0;">
        🚶 {pasos['pasos_meta']:,}
      </div>
      <div style="font-size:13px;color:#6B7280;">
        Equivalente a <strong>{pasos['km_aprox']} km</strong> ·
        Quema aprox. <strong>{pasos['kcal_pasos']} kcal</strong> adicionales/día
      </div>
      <div style="font-size:11px;color:#9CA3AF;margin-top:8px;">
        Calculado según nivel de actividad, objetivo ({norm.get('Objetivo principal','')}) e IMC actual
      </div>
    </div>""", unsafe_allow_html=True)

    # Rutina
    st.markdown("<div class='sec-head'>PROGRAMACIÓN NEUROMUSCULAR</div>", unsafe_allow_html=True)
    con_lesion = (norm.get("Lesión actual","Ninguna").lower()!="ninguna" or
                  norm.get("Prohibido ejercicio","No").lower()!="no")
    t_ent      = norm.get("Tiempo entrenando","")
    aplica_ind = "Nunca" in t_ent or "Menos de 6" in t_ent
    modo       = "con_lesion" if con_lesion else "sin_lesion"
    nd         = int(str(norm.get("Días entrenar","4")).strip()[0]) if str(norm.get("Días entrenar","4")).strip()[0].isdigit() else 4

    if aplica_ind:
        bloques = ["Inducción (1 Mes)"]*nd
        nombres = [f"DÍA {i+1} — FULL BODY" for i in range(nd)]
    else:
        bloques = ["Empuje","Tracción","Pierna","Empuje","Tracción"][:nd]
        nombres = [f"DÍA {i+1} — {b.upper()}" for i,b in enumerate(bloques)]

    tabs = st.tabs(nombres)
    for tab, bloque, nom in zip(tabs, bloques, nombres):
        with tab:
            if bloque in CONFIG["rutinas"]:
                ejs = CONFIG["rutinas"][bloque][modo]
                st.markdown(f"<div class='rutina-header'>{nom}</div>", unsafe_allow_html=True)
                for ej,ser,rep,desc in ejs:
                    st.markdown(f"""<div class='rutina-row'>
                      <div>{ej}</div>
                      <div style='text-align:center;font-weight:700;color:#166534;'>{ser}</div>
                      <div style='text-align:center;color:#50C878;font-weight:700;'>{rep}</div>
                      <div style='text-align:center;color:#9CA3AF;'>{desc}</div>
                    </div>""", unsafe_allow_html=True)

    # Parámetros espejo
    st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO — LÍNEA BASE</div>", unsafe_allow_html=True)
    pe1,pe2,pe3,pe4 = st.columns(4)
    with pe1: metric_card("Energía",       f"{norm.get('P_Energia_Q1','5')}/10")
    with pe2: metric_card("Calidad Sueño", f"{norm.get('P_Sueno_Q1','5')}/10")
    with pe3: metric_card("Fuerza",        f"{norm.get('P_Fuerza_Q1','5')}/10")
    with pe4: metric_card("Hambre",        f"{norm.get('P_Hambre_Q1','5')}/10")

    # Fotos Q1
    st.markdown("<div class='sec-head'>EVIDENCIA VISUAL (FOTOGRAFÍAS Q1)</div>", unsafe_allow_html=True)
    fc1,fc2,fc3 = st.columns(3)
    mostrar_foto(fc1, id_al, "frente",  "q1", "Frente Q1")
    mostrar_foto(fc2, id_al, "perfil",  "q1", "Perfil Q1")
    mostrar_foto(fc3, id_al, "espalda", "q1", "Espalda Q1")

    # Alertas biomecánicas
    st.markdown("<div class='sec-head'>ALERTAS BIOMECÁNICAS</div>", unsafe_allow_html=True)
    alertas = [
        f"Lesión: {norm['Lesión actual']}",
        f"Restricción axial: {norm['Prohibido ejercicio']}",
        f"Estancamiento previo: {norm['Historial_Est']}",
        f"Recuperación: {norm['Recuperacion_Base']}",
        f"Biofeedback: {norm['Biofeedback_Dig']}",
    ]
    for a in alertas:
        col = "#EF4444" if any(k in a for k in ["Rodilla","Hombro","Espalda","Sí","pesadez"]) else "#50C878"
        st.markdown(f"<div style='padding:7px 12px;border-left:3px solid {col};margin:3px 0;font-size:13px;background:#fff;border-radius:0 6px 6px 0;'>{a}</div>", unsafe_allow_html=True)


# =============================================================================
# DASHBOARD Q2 — SOLO ADMIN
# =============================================================================
def dashboard_q2(norm, mot, revs_df, id_al):
    nombre = norm.get("Nombre completo","Atleta")
    if revs_df.empty:
        st.info("⚠️ Sin auditoría Q2 registrada para este atleta.")
        return

    ult        = revs_df.iloc[-1]
    estado     = str(ult.get("Estado_Calculado","AVANCE")).upper()
    peso_q2    = pf(ult.get("Peso_Revision", mot["peso"]), mot["peso"])
    cintura_q2 = pf(ult.get("Cintura_Revision", mot["cintura"]), mot["cintura"])
    dif_p      = round(peso_q2 - mot["peso"], 1)
    dif_c      = round(cintura_q2 - mot["cintura"], 1)

    render_hero("AUDITORÍA COMPARATIVA Q1 vs Q2", "MI AVANCE MM247", id_al)

    # Foto de frente Q2 con señalizaciones — ANCHO COMPLETO
    st.markdown("<div class='sec-head'>ANÁLISIS VISUAL Q2 — FOTO CON SEÑALIZACIONES</div>", unsafe_allow_html=True)
    mostrar_analisis_visual(id_al, norm, mot, etapa="q2", estado=estado)

    col_av, col_info = st.columns([1, 2])
    with col_av:
        col_p = "#22C55E" if dif_p<=0 else "#EF4444"
        col_c = "#22C55E" if dif_c<=0 else "#EF4444"
        st.markdown(f"""
        <div style="text-align:center;font-size:12px;margin-top:8px;line-height:2;">
          <span style="color:{col_p};font-weight:700;">Peso {dif_p:+.1f} kg</span><br>
          <span style="color:{col_c};font-weight:700;">Cintura {dif_c:+.1f} cm</span><br>
          <span style="color:#7D9A84;">Fuerza: {ult.get('Progreso_Fuerza','5')}/10</span>
        </div>""", unsafe_allow_html=True)

    with col_info:
        badge = {"AVANCE":"<span class='badge-avance'>🚀 EN AVANCE</span>",
                 "RETROCESO":"<span class='badge-retroceso'>⚠️ RETROCESO</span>",
                 "LENTO":"<span class='badge-lento'>⏳ LENTO</span>"}.get(estado,"")
        st.markdown(f"""
        <div style="padding:10px 0;">
          <div style="font-size:26px;font-weight:900;color:#0D1F14;">{nombre}</div>
          <div style="margin:8px 0;">{badge}</div>
          <div style="font-size:12px;color:#6B7280;">
            Adherencia: <strong>{ult.get('Adherencia Real al Sistema','--')}</strong><br>
            Sobrecarga: <strong>{ult.get('Sobrecarga Progresiva','--')}</strong><br>
            Tolerancia: <strong>{ult.get('Tolerancia Metabólica','--')}</strong>
          </div>
        </div>""", unsafe_allow_html=True)

        # Análisis dinámico
        adh = str(ult.get("Adherencia Real al Sistema",""))
        sob = str(ult.get("Sobrecarga Progresiva",""))
        tol = str(ult.get("Tolerancia Metabólica",""))
        fza = pf(ult.get("Progreso_Fuerza","5"),5)
        ene = pf(ult.get("Energia","5"),5)

        analisis = []
        if "100%" in adh or "80-90%" in adh:
            analisis.append(("ok","Adherencia alta — protocolo seguido correctamente."))
        elif "50%" in adh:
            analisis.append(("warn","Adherencia media — simplificar plan, revisar obstáculos."))
        else:
            analisis.append(("alert","Adherencia crítica — reencuadre motivacional urgente."))
        if "Sí, subí" in sob:
            analisis.append(("ok","Sobrecarga progresiva confirmada — autorizado +5% en cargas."))
        elif "mantuve" in sob:
            analisis.append(("warn","Sin progresión — revisar periodización y descanso."))
        else:
            analisis.append(("alert","Pérdida de fuerza — posible sobreentrenamiento o déficit excesivo."))
        if "pesadez" in tol.lower() or "Inflamación" in tol.lower():
            analisis.append(("warn","Intolerancia digestiva — rotar carbohidratos."))
        if ene <= 4:
            analisis.append(("warn","Energía baja — revisar distribución calórica pre-entreno."))
        if fza >= 8 and estado == "AVANCE":
            analisis.append(("ok","Alto rendimiento — candidato para protocolo avanzado."))

        st.markdown("<div style='margin-top:10px;font-size:11px;color:#7D9A84;font-weight:700;letter-spacing:1.5px;'>ANÁLISIS CLÍNICO</div>", unsafe_allow_html=True)
        for tipo, texto in analisis:
            accion_item(tipo, texto)

    # Deltas biométricos
    st.markdown("<div class='sec-head'>CRUCE BIOMÉTRICO Q1 → Q2</div>", unsafe_allow_html=True)
    dc1,dc2,dc3,dc4 = st.columns(4)
    with dc1: metric_card("Peso Q1",     f"{mot['peso']} kg")
    with dc2: metric_card("Peso Q2",     f"{peso_q2} kg",    f"{dif_p:+.1f} kg", dif_p<=0)
    with dc3: metric_card("Cintura Q1",  f"{mot['cintura']} cm")
    with dc4: metric_card("Cintura Q2",  f"{cintura_q2} cm", f"{dif_c:+.1f} cm", dif_c<=0)

    # Gráficas
    st.markdown("<div class='sec-head'>VISUALIZACIÓN COMPARATIVA</div>", unsafe_allow_html=True)
    gc1,gc2 = st.columns(2)
    with gc1:
        st.markdown("<div class='chart-wrap'><div style='font-size:11px;color:#7D9A84;font-weight:700;margin-bottom:10px;'>EVOLUCIÓN PESO (kg)</div>", unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"Peso(kg)":[mot["peso"],peso_q2]}, index=["Q1 Base","Q2 Actual"]), color="#50C878", height=200)
        st.markdown("</div>", unsafe_allow_html=True)
    with gc2:
        st.markdown("<div class='chart-wrap'><div style='font-size:11px;color:#7D9A84;font-weight:700;margin-bottom:10px;'>EVOLUCIÓN CINTURA (cm)</div>", unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"Cintura(cm)":[mot["cintura"],cintura_q2]}, index=["Q1 Base","Q2 Actual"]), color="#3CB371", height=200)
        st.markdown("</div>", unsafe_allow_html=True)

    # Parámetros espejo Q1 vs Q2
    st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO Q1 vs Q2</div>", unsafe_allow_html=True)
    df_radar = pd.DataFrame({
        "Q1": [pf(norm.get("P_Energia_Q1","5"),5), pf(norm.get("P_Sueno_Q1","5"),5),
               pf(norm.get("P_Fuerza_Q1","5"),5),  pf(norm.get("P_Hambre_Q1","5"),5)],
        "Q2": [pf(ult.get("Energia","5"),5), pf(ult.get("Calidad_Sueno","5"),5),
               pf(ult.get("Progreso_Fuerza","5"),5), pf(ult.get("Hambre","5"),5)],
    }, index=["Energía","Sueño","Fuerza","Hambre"])
    st.markdown("<div class='chart-wrap'>", unsafe_allow_html=True)
    st.bar_chart(df_radar, height=220, color=["#50C878","#0D1F14"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Fotos comparativas
    st.markdown("<div class='sec-head'>EVIDENCIA VISUAL COMPARATIVA (Q1 vs Q2)</div>", unsafe_allow_html=True)

    # Encabezados
    eh = st.columns(6)
    for col, lbl, color in [
        (eh[0],"FRENTE Q1","#50C878"),(eh[1],"PERFIL Q1","#50C878"),(eh[2],"ESPALDA Q1","#50C878"),
        (eh[3],"FRENTE Q2","#4ADE80"),(eh[4],"PERFIL Q2","#4ADE80"),(eh[5],"ESPALDA Q2","#4ADE80"),
    ]:
        col.markdown(f"<div style='text-align:center;font-size:9px;font-weight:700;color:{color};padding:4px 0;'>{lbl}</div>", unsafe_allow_html=True)

    fc = st.columns(6)
    mostrar_foto(fc[0], id_al, "frente",  "q1", "Frente Q1")
    mostrar_foto(fc[1], id_al, "perfil",  "q1", "Perfil Q1")
    mostrar_foto(fc[2], id_al, "espalda", "q1", "Espalda Q1")
    mostrar_foto(fc[3], id_al, "frente",  "q2", "Frente Q2")
    mostrar_foto(fc[4], id_al, "perfil",  "q2", "Perfil Q2")
    mostrar_foto(fc[5], id_al, "espalda", "q2", "Espalda Q2")

    # Plan de acción
    st.markdown("<div class='sec-head'>PLAN DE ACCIÓN CLÍNICO</div>", unsafe_allow_html=True)
    plan = generar_plan(norm, ult, estado)
    for tipo, texto in plan:
        accion_item(tipo, texto)

    # Dictamen final
    cols_dict = {"AVANCE":"linear-gradient(135deg,#50C878,#2E8B57)",
                 "RETROCESO":"linear-gradient(135deg,#EF4444,#B91C1C)",
                 "LENTO":"linear-gradient(135deg,#F59E0B,#D97706)"}
    textos_dict = {
        "AVANCE":    "Sistema positivo. Mantener protocolo e incrementar intensidad.",
        "RETROCESO": "Indicadores de retroceso. Aplicar deload y revisar nutrición.",
        "LENTO":     "Progreso por debajo del esperado. Auditar adherencia y sueño.",
    }
    st.markdown(f"""
    <div style="background:{cols_dict.get(estado,cols_dict['AVANCE'])};border-radius:16px;
                padding:28px;text-align:center;color:#fff;margin-top:12px;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:34px;font-weight:900;letter-spacing:4px;">{estado}</div>
      <div style="font-size:13px;margin-top:8px;opacity:.9;max-width:500px;margin-left:auto;margin-right:auto;">
        {textos_dict.get(estado,'')}
      </div>
    </div>""", unsafe_allow_html=True)


# =============================================================================
# FORMULARIO Q1 — CLIENTE (SOLO VE CONFIRMACIÓN + ID)
# =============================================================================
def formulario_q1(df_existente):
    render_hero("NUEVO EXPEDIENTE — REGISTRO INICIAL", "MI REGISTRO MM247")

    if "step" not in st.session_state: st.session_state.step = 1
    if "db"   not in st.session_state: st.session_state.db   = {}

    total = 6
    st.progress(st.session_state.step / total)
    st.markdown(f"<div style='text-align:center;font-size:11px;color:#7D9A84;letter-spacing:2px;margin-bottom:16px;'>PASO {st.session_state.step} DE {total}</div>", unsafe_allow_html=True)

    # ── PASO 1: Datos fisiológicos ────────────────────────────────────────────
    if st.session_state.step == 1:
        with st.form("f_p1"):
            st.markdown("<div class='sec-head'>DATOS FISIOLÓGICOS BASE</div>", unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                v_nom  = st.text_input("Nombre completo:", value=st.session_state.db.get("Nombre completo",""))
                v_edad = st.selectbox("Edad:", [f"{i} años" for i in range(14,81)], index=11)
                v_sexo = st.selectbox("Sexo:", ["Masculino","Femenino"])
                v_est  = st.selectbox("Estatura:", [f"{i} cm" for i in range(120,221)], index=55)
                v_act  = st.selectbox("Nivel de actividad:", list(CONFIG["factores"].keys()), index=2)
            with c2:
                v_peso  = st.selectbox("Peso actual:", [f"{i} kg" for i in range(40,161)], index=40)
                v_cint  = st.selectbox("Cintura actual:", [f"{i} cm" for i in range(50,150)], index=35)
                v_meta  = st.selectbox("Peso objetivo:", [f"{i} kg" for i in range(40,161)], index=35)
                v_mail  = st.text_input("Correo electrónico:", value=st.session_state.db.get("Correo electrónico",""))
            if st.form_submit_button("Siguiente ➡️"):
                if not v_nom.strip():
                    st.error("El nombre es requerido.")
                else:
                    guardar_y_navegar({
                        "Nombre completo":v_nom,"Edad":v_edad,"Sexo":v_sexo,
                        "Estatura":v_est,"Peso actual":v_peso,"Cintura inicial":v_cint,
                        "Peso objetivo":v_meta,"Correo electrónico":v_mail,
                        "Nivel de actividad":v_act
                    }, 2)

    # ── PASO 2: Fotografías Q1 (guardado en disco) ────────────────────────────
    elif st.session_state.step == 2:
        st.markdown("<div class='sec-head'>EVIDENCIA VISUAL — FOTOGRAFÍAS Q1</div>", unsafe_allow_html=True)
        st.info("📸 Sube tus 3 fotos y presiona **GUARDAR FOTOS** antes de continuar.")

        # Necesitamos el ID temporal para guardar las fotos
        # Usamos nombre como semilla temporal
        nombre_temp = st.session_state.db.get("Nombre completo","tmp")
        id_temp     = "TMP_" + hashlib.md5(nombre_temp.encode()).hexdigest()[:6].upper()

        f1,f2,f3 = st.columns(3)
        up_fr = f1.file_uploader("📷 Frente",  type=["jpg","jpeg","png"], key="up_fr_q1")
        up_pf = f2.file_uploader("📷 Perfil",  type=["jpg","jpeg","png"], key="up_pf_q1")
        up_es = f3.file_uploader("📷 Espalda", type=["jpg","jpeg","png"], key="up_es_q1")

        if st.button("💾 GUARDAR FOTOS", key="btn_guardar_fotos", use_container_width=True):
            guardadas = 0
            if up_fr:
                if guardar_foto_disco(id_temp, "frente", "q1", up_fr): guardadas += 1
            if up_pf:
                if guardar_foto_disco(id_temp, "perfil", "q1", up_pf): guardadas += 1
            if up_es:
                if guardar_foto_disco(id_temp, "espalda","q1", up_es): guardadas += 1
            st.session_state.db["id_temp_fotos"] = id_temp
            st.session_state.db["fotos_guardadas_q1"] = guardadas
            st.rerun()

        # Preview desde disco (persiste)
        id_temp_prev = st.session_state.db.get("id_temp_fotos", id_temp)
        n_fotos = 0
        pv1,pv2,pv3 = st.columns(3)
        for col, tipo, lbl in [(pv1,"frente","Frente"),(pv2,"perfil","Perfil"),(pv3,"espalda","Espalda")]:
            datos = cargar_foto_disco(id_temp_prev, tipo, "q1")
            if datos:
                n_fotos += 1
                col.image(datos, caption=f"✅ {lbl} guardada", use_container_width=True)
            else:
                col.markdown(f"""
                <div style="background:#0D1F14;border:2px dashed #50C87840;border-radius:10px;
                            min-height:130px;display:flex;align-items:center;justify-content:center;
                            flex-direction:column;gap:6px;">
                  <div style="font-size:26px;">📷</div>
                  <div style="font-size:9px;color:#50C87860;text-align:center;">{lbl.upper()}<br>SIN FOTO</div>
                </div>""", unsafe_allow_html=True)

        if n_fotos == 3:
            st.success("✅ Las 3 fotos guardadas correctamente.")
        elif n_fotos > 0:
            st.info(f"📷 {n_fotos}/3 fotos guardadas.")
        else:
            st.warning("Sube tus fotos y presiona GUARDAR FOTOS.")

        b1,b2 = st.columns(2)
        if b1.button("⬅️ Atrás", key="back_p2"): guardar_y_navegar({}, 1)
        if b2.button("Siguiente ➡️", key="next_p2"):
            guardar_y_navegar({"fotos_q1": "Cargadas" if n_fotos==3 else "Pendientes"}, 3)

    # ── PASO 3: Antecedentes ──────────────────────────────────────────────────
    elif st.session_state.step == 3:
        with st.form("f_p3"):
            st.markdown("<div class='sec-head'>ANTECEDENTES Y ESTANCAMIENTO</div>", unsafe_allow_html=True)
            v_tent = st.selectbox("Tiempo entrenando:", ["Nunca","Menos de 6 meses","De 6 meses a 1 año","1 a 3 años","Más de 3 años"])
            v_dias = st.selectbox("Días disponibles/semana:", ["3 días por semana","4 días por semana","5 días por semana"])
            v_est  = st.selectbox("Historial de estancamiento:", ["No estoy estancado","Menos de 1 mes","1 a 3 meses","Más de 6 meses"])
            b1,b2 = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"): guardar_y_navegar({"Tiempo entrenando":v_tent,"Días entrenar":v_dias,"Historial de Estancamiento":v_est}, 2)
            if b2.form_submit_button("Siguiente ➡️"): guardar_y_navegar({"Tiempo entrenando":v_tent,"Días entrenar":v_dias,"Historial de Estancamiento":v_est}, 4)

    # ── PASO 4: Perfil clínico ────────────────────────────────────────────────
    elif st.session_state.step == 4:
        with st.form("f_p4"):
            st.markdown("<div class='sec-head'>PERFIL CLÍNICO Y BIOFEEDBACK</div>", unsafe_allow_html=True)
            v_les   = st.selectbox("Lesión actual:", ["Ninguna","Rodilla","Hombro","Espalda Baja","Cervicales"])
            v_proh  = st.selectbox("Prohibición carga axial:", ["No","Sí, sobre columna","Sí, flexiones profundas"])
            v_rec   = st.selectbox("Capacidad de recuperación (DOMS):", ["Recuperación rápida","Normal","Llego muy adolorido a la siguiente sesión"])
            v_dig   = st.selectbox("Biofeedback digestivo:", ["Sin molestias","Inflamación ocasional","Gases y pesadez frecuente"])
            v_est2  = st.slider("Carga de estrés externo (1-10):", 1, 10, 5)
            v_pos   = st.selectbox("Problemas de postura:", ["No","Sí — cifosis","Sí — lordosis","Sí — escoliosis"])
            b1,b2   = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"Lesión actual":v_les,"Prohibido ejercicio":v_proh,"Capacidad de Recuperación Base":v_rec,"Biofeedback Digestivo":v_dig,"Carga de Estrés Externo":str(v_est2),"Mala postura":v_pos}, 3)
            if b2.form_submit_button("Siguiente ➡️"):
                guardar_y_navegar({"Lesión actual":v_les,"Prohibido ejercicio":v_proh,"Capacidad de Recuperación Base":v_rec,"Biofeedback Digestivo":v_dig,"Carga de Estrés Externo":str(v_est2),"Mala postura":v_pos}, 5)

    # ── PASO 5: Nutrición ─────────────────────────────────────────────────────
    elif st.session_state.step == 5:
        with st.form("f_p5"):
            st.markdown("<div class='sec-head'>NUTRICIÓN Y METAS</div>", unsafe_allow_html=True)
            v_obj   = st.selectbox("Objetivo principal:", ["Perder grasa","Ganar masa muscular","Recomposición corporal"])
            v_prots = st.multiselect("Proteínas preferidas:", list(CONFIG["porciones_ref"].keys())[:5], default=["Pechuga de Pollo"])
            v_carbs = st.multiselect("Carbohidratos:", ["Arroz","Avena","Papa","Tortilla","Camote"], default=["Arroz"])
            v_gras  = st.multiselect("Grasas saludables:", ["Aguacate","Almendras","Crema de Cacahuete","Aceite de Oliva"], default=["Aguacate"])
            v_verd  = st.multiselect("Verduras:", ["Brócoli","Espinacas","Lechuga","Pepino","Calabacín"], default=["Brócoli"])
            b1,b2   = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"Objetivo principal":v_obj,"Menu_Proteinas":", ".join(v_prots),"Menu_Carbohidratos":", ".join(v_carbs),"Menu_Grasas":", ".join(v_gras),"Menu_Verduras":", ".join(v_verd)}, 4)
            if b2.form_submit_button("Siguiente ➡️"):
                guardar_y_navegar({"Objetivo principal":v_obj,"Menu_Proteinas":", ".join(v_prots),"Menu_Carbohidratos":", ".join(v_carbs),"Menu_Grasas":", ".join(v_gras),"Menu_Verduras":", ".join(v_verd)}, 6)

    # ── PASO 6: Parámetros espejo + ENVÍO ─────────────────────────────────────
    elif st.session_state.step == 6:
        with st.form("f_p6"):
            st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO — LÍNEA BASE</div>", unsafe_allow_html=True)
            v_ener = st.slider("Energía promedio (1-10):", 1, 10, 5)
            v_suen = st.slider("Calidad de sueño (1-10):", 1, 10, 5)
            v_fuer = st.slider("Fuerza actual (1-10):", 1, 10, 5)
            v_hamb = st.slider("Hambre/ansiedad (1-10):", 1, 10, 5)
            b1,b2  = st.columns(2)
            if b1.form_submit_button("⬅️ Atrás"):
                guardar_y_navegar({"P_Energia_Q1":v_ener,"P_Sueno_Q1":v_suen,"P_Fuerza_Q1":v_fuer,"P_Hambre_Q1":v_hamb}, 5)
            if b2.form_submit_button("🚀 ACTIVAR MI EXPEDIENTE MM247"):
                d = st.session_state.db
                d.update({"P_Energia_Q1":v_ener,"P_Sueno_Q1":v_suen,"P_Fuerza_Q1":v_fuer,"P_Hambre_Q1":v_hamb})

                id_nuevo = gen_id(df_existente)

                # Renombrar fotos temporales al ID real
                id_temp = d.get("id_temp_fotos","")
                if id_temp:
                    for tipo in ["frente","perfil","espalda"]:
                        src = ruta_foto(id_temp, tipo, "q1")
                        dst = ruta_foto(id_nuevo, tipo, "q1")
                        if os.path.exists(src):
                            os.rename(src, dst)

                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "INICIAL", "ID_Alumno": id_nuevo,
                    "Nombre completo": str(d.get("Nombre completo","")),
                    "Edad": str(d.get("Edad","")), "Sexo": str(d.get("Sexo","")),
                    "Estatura": str(d.get("Estatura","")), "Peso actual": str(d.get("Peso actual","")),
                    "Cintura inicial": str(d.get("Cintura inicial","")),
                    "Peso objetivo": str(d.get("Peso objetivo","")),
                    "Correo electrónico": str(d.get("Correo electrónico","")),
                    "Nivel de actividad": str(d.get("Nivel de actividad","")),
                    "Tiempo entrenando": str(d.get("Tiempo entrenando","")),
                    "Días entrenar": str(d.get("Días entrenar","")),
                    "Lesión actual": str(d.get("Lesión actual","")),
                    "Prohibido ejercicio": str(d.get("Prohibido ejercicio","")),
                    "Mala postura": str(d.get("Mala postura","")),
                    "Menu_Proteinas": str(d.get("Menu_Proteinas","")),
                    "Menu_Carbohidratos": str(d.get("Menu_Carbohidratos","")),
                    "Menu_Grasas": str(d.get("Menu_Grasas","")),
                    "Menu_Verduras": str(d.get("Menu_Verduras","")),
                    "Objetivo principal": str(d.get("Objetivo principal","")),
                    "P_Energia_Q1": str(v_ener), "P_Sueno_Q1": str(v_suen),
                    "P_Fuerza_Q1": str(v_fuer), "P_Hambre_Q1": str(v_hamb),
                    "Historial de Estancamiento": str(d.get("Historial de Estancamiento","")),
                    "Capacidad de Recuperación Base": str(d.get("Capacidad de Recuperación Base","")),
                    "Biofeedback Digestivo": str(d.get("Biofeedback Digestivo","")),
                    "Carga de Estrés Externo": str(d.get("Carga de Estrés Externo","")),
                    "Foto_Frente_Q1": "Guardada" if cargar_foto_disco(id_nuevo,"frente","q1") else "Pendiente",
                    "Foto_Perfil_Q1": "Guardada" if cargar_foto_disco(id_nuevo,"perfil","q1") else "Pendiente",
                    "Foto_Espalda_Q1":"Guardada" if cargar_foto_disco(id_nuevo,"espalda","q1") else "Pendiente",
                }

                with st.spinner("Compilando tu ecosistema MM247..."):
                    try:
                        resp = requests.post(CONFIG["webhook_url"], json=payload, timeout=10)
                        if resp.status_code == 200:
                            st.cache_data.clear()
                            # CLIENTE SOLO VE CONFIRMACIÓN + ID
                            st.markdown(f"""
                            <div class="id-box">
                              <div class="id-box-label">TU ID DE ATLETA MM247</div>
                              <div class="id-box-num">{id_nuevo}</div>
                              <div style="font-size:12px;margin-top:10px;opacity:.85;">
                                Guarda este código — lo necesitarás para registrar tu avance
                              </div>
                            </div>""", unsafe_allow_html=True)
                            st.balloons()
                            st.markdown("""
                            <div class="confirm-box" style="margin-top:24px;">
                              <div style="font-size:32px;">🎉</div>
                              <div style="font-size:20px;font-weight:900;color:#166534;margin-top:8px;">¡Expediente Activado!</div>
                              <div style="font-size:14px;color:#4B7A5A;margin-top:8px;">
                                Tu registro ha sido recibido exitosamente.<br>
                                Tu entrenador revisará tu expediente y te contactará pronto.<br><br>
                                <strong>Próximo paso:</strong> Cuando tu entrenador te lo indique,<br>
                                regresa aquí con tu ID para registrar tu avance en <em>Mi Avance MM247</em>.
                              </div>
                            </div>""", unsafe_allow_html=True)
                            st.session_state.step = 1
                            st.session_state.db   = {}
                        else:
                            st.error("Error al conectar con la base de datos. Intenta de nuevo.")
                    except Exception as e:
                        st.error(f"Error de conexión: {e}")


# =============================================================================
# FORMULARIO Q2 — CLIENTE (SOLO VE CONFIRMACIÓN)
# =============================================================================
def formulario_q2(df_existente):
    render_hero("AUDITORÍA DE AVANCE — REGISTRO", "MI AVANCE MM247")

    st.markdown("""
    <div class="panel-card" style="border-left:4px solid #50C878;margin-bottom:20px;">
      <div style="font-size:13px;color:#4B5563;line-height:1.7;">
        Ingresa tu <strong style='color:#166534;'>ID de Atleta</strong> y completa tu auditoría.<br>
        Tu entrenador recibirá el reporte y te dará retroalimentación personalizada.
      </div>
    </div>""", unsafe_allow_html=True)

    # ID fuera del form para usarlo en guardar fotos
    id_ing = st.text_input("🔑 ID de Atleta (Ej: 247001):",
                            placeholder="Ingresa tu ID MM247",
                            key="q2_id_inp").strip().upper()

    # Fotos Q2 con guardado en disco
    st.markdown("<div class='sec-head'>FOTOGRAFÍAS ACTUALES (Q2)</div>", unsafe_allow_html=True)
    st.info("📸 Sube tus 3 fotos actuales y presiona **GUARDAR FOTOS Q2**.")

    fq1,fq2,fq3 = st.columns(3)
    up_fr2 = fq1.file_uploader("📷 Frente Actual",  type=["png","jpg","jpeg"], key="up_fr_q2")
    up_pf2 = fq2.file_uploader("📷 Perfil Actual",  type=["png","jpg","jpeg"], key="up_pf_q2")
    up_es2 = fq3.file_uploader("📷 Espalda Actual", type=["png","jpg","jpeg"], key="up_es_q2")

    if st.button("💾 GUARDAR FOTOS Q2", key="btn_guardar_fotos_q2", use_container_width=True):
        if not id_ing:
            st.error("Ingresa tu ID primero.")
        else:
            guardadas = 0
            if up_fr2:
                if guardar_foto_disco(id_ing, "frente", "q2", up_fr2): guardadas += 1
            if up_pf2:
                if guardar_foto_disco(id_ing, "perfil", "q2", up_pf2): guardadas += 1
            if up_es2:
                if guardar_foto_disco(id_ing, "espalda","q2", up_es2): guardadas += 1
            st.session_state["fotos_q2_guardadas"] = guardadas
            st.session_state["id_q2_fotos"] = id_ing
            st.rerun()

    # Preview desde disco
    id_prev = st.session_state.get("id_q2_fotos", id_ing)
    n_fotos_q2 = 0
    pv1,pv2,pv3 = st.columns(3)
    for col, tipo, lbl in [(pv1,"frente","Frente Q2"),(pv2,"perfil","Perfil Q2"),(pv3,"espalda","Espalda Q2")]:
        datos = cargar_foto_disco(id_prev, tipo, "q2") if id_prev else None
        if datos:
            n_fotos_q2 += 1
            col.image(datos, caption=f"✅ {lbl}", use_container_width=True)
        else:
            col.markdown(f"""
            <div style="background:#0D1F14;border:2px dashed #50C87840;border-radius:10px;
                        min-height:120px;display:flex;align-items:center;justify-content:center;
                        flex-direction:column;gap:6px;">
              <div style="font-size:24px;">📷</div>
              <div style="font-size:9px;color:#50C87860;text-align:center;">{lbl}<br>SIN FOTO</div>
            </div>""", unsafe_allow_html=True)

    if n_fotos_q2 == 3:
        st.success("✅ Las 3 fotos Q2 guardadas.")
    elif n_fotos_q2 > 0:
        st.info(f"📷 {n_fotos_q2}/3 fotos guardadas.")

    # Formulario de datos
    with st.form("f_aud", clear_on_submit=False):
        st.markdown("<div class='sec-head'>MÉTRICAS ACTUALES</div>", unsafe_allow_html=True)
        m1,m2    = st.columns(2)
        peso_rev = m1.number_input("Peso Actual (kg):", min_value=30.0, value=70.0, step=0.1)
        cint_rev = m2.number_input("Cintura Actual (cm):", min_value=40.0, value=80.0, step=0.5)

        st.markdown("<div class='sec-head'>ADHERENCIA Y DESEMPEÑO</div>", unsafe_allow_html=True)
        adherencia = st.selectbox("Adherencia real al sistema:", [
            "100% Perfecto","80-90% Con fallos mínimos","Cerca del 50%","Menos del 50% / Abandoné"])
        sobrecarga = st.selectbox("Sobrecarga progresiva:", [
            "Sí, subí peso/reps","Me mantuve igual","No, perdí fuerza"])
        tolerancia = st.selectbox("Tolerancia metabólica:", [
            "Digestión rápida y normal","Ligera pesadez","Mucha pesadez / Inflamación constante"])

        st.markdown("<div class='sec-head'>PARÁMETROS ESPEJO ACTUALES (1-10)</div>", unsafe_allow_html=True)
        cp1,cp2 = st.columns(2)
        e_rev = cp1.slider("Energía:",         1, 10, 5)
        s_rev = cp2.slider("Calidad Sueño:",   1, 10, 5)
        f_rev = cp1.slider("Fuerza:",          1, 10, 5)
        h_rev = cp2.slider("Hambre/Ansiedad:", 1, 10, 5)

        if st.form_submit_button("🚀 ENVIAR MI AUDITORÍA"):
            if not id_ing:
                st.error("El ID es obligatorio.")
            elif df_existente.empty or id_ing not in df_existente["ID_Alumno"].values:
                st.error(f"❌ ID '{id_ing}' no encontrado. Verifica tu ID.")
            else:
                puntos = 0
                if f_rev >= 7 and "Sí" in sobrecarga: puntos += 2
                if "100%" in adherencia or "80-90%" in adherencia: puntos += 1
                estado_calc = "AVANCE" if puntos >= 2 else "RETROCESO"

                payload_rev = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "REVISION", "ID_Alumno": id_ing,
                    "Peso_Revision": str(peso_rev), "Cintura_Revision": str(cint_rev),
                    "Energia": str(e_rev), "Calidad_Sueno": str(s_rev),
                    "Progreso_Fuerza": str(f_rev), "Hambre": str(h_rev),
                    "Adherencia Real al Sistema": adherencia,
                    "Sobrecarga Progresiva": sobrecarga,
                    "Tolerancia Metabólica": tolerancia,
                    "Foto_Frente_Q2":  "Guardada" if cargar_foto_disco(id_ing,"frente","q2")  else "Pendiente",
                    "Foto_Perfil_Q2":  "Guardada" if cargar_foto_disco(id_ing,"perfil","q2")  else "Pendiente",
                    "Foto_Espalda_Q2": "Guardada" if cargar_foto_disco(id_ing,"espalda","q2") else "Pendiente",
                    "Estado_Calculado": estado_calc,
                }

                with st.spinner("Procesando tu auditoría..."):
                    try:
                        resp = requests.post(CONFIG["webhook_url"], json=payload_rev, timeout=10)
                        if resp.status_code == 200:
                            st.cache_data.clear()
                            # CLIENTE SOLO VE CONFIRMACIÓN
                            st.markdown(f"""
                            <div class="confirm-box">
                              <div style="font-size:40px;">✅</div>
                              <div style="font-size:22px;font-weight:900;color:#166534;margin-top:10px;">
                                ¡Auditoría Registrada!
                              </div>
                              <div style="font-size:14px;color:#4B7A5A;margin-top:10px;line-height:1.8;">
                                Tu información ha sido enviada exitosamente.<br>
                                Tu entrenador analizará tus resultados y te dará retroalimentación.<br><br>
                                <strong>ID registrado:</strong> {id_ing}
                              </div>
                            </div>""", unsafe_allow_html=True)
                        else:
                            st.error("Error al conectar. Intenta de nuevo.")
                    except Exception as e:
                        st.error(f"Error: {e}")


# =============================================================================
# DASHBOARD ADMINISTRADOR
# =============================================================================
def dashboard_admin(df_existente):
    render_hero("PANEL DE CONTROL MAESTRO", "CONTROL CLÍNICO AVANZADO")

    if df_existente.empty:
        st.warning("Base de datos vacía.")
        return

    df_c1 = df_existente[df_existente["Tipo_Registro"]=="INICIAL"].copy()
    df_c2 = df_existente[df_existente["Tipo_Registro"]=="REVISION"].copy()
    ids   = df_c1["ID_Alumno"].replace("",pd.NA).dropna().unique()

    # KPIs
    st.markdown("<div class='sec-head'>KPIs GLOBALES</div>", unsafe_allow_html=True)
    k1,k2,k3,k4 = st.columns(4)
    con_q2    = len(df_c2["ID_Alumno"].unique())
    en_avance = len(df_c2[df_c2.get("Estado_Calculado","") == "AVANCE"]["ID_Alumno"].unique()) if "Estado_Calculado" in df_c2.columns else 0

    with k1: metric_card("Total Atletas",   str(len(ids)))
    with k2: metric_card("Con Auditoría Q2",str(con_q2))
    with k3: metric_card("En Avance",       str(en_avance), delta_pos=True)
    with k4: metric_card("Sin Q2 aún",      str(len(ids)-con_q2))

    # Lista + detalle
    col_list, col_det = st.columns([1,2])

    with col_list:
        st.markdown("<div class='sec-head'>ATLETAS ACTIVOS</div>", unsafe_allow_html=True)
        for id_al in ids:
            fila    = df_c1[df_c1["ID_Alumno"]==id_al].iloc[0]
            nombre  = str(fila.get("Nombre completo","Atleta"))[:18]
            tiene_q2= id_al in df_c2["ID_Alumno"].values
            icono   = "🟢" if tiene_q2 else "🔵"
            if st.button(f"{icono} {id_al} — {nombre}", key=f"btn_{id_al}", use_container_width=True):
                st.session_state.alumno_sel = id_al

    with col_det:
        if "alumno_sel" not in st.session_state: return

        id_sel  = st.session_state.alumno_sel
        d_brutos= df_c1[df_c1["ID_Alumno"]==id_sel].iloc[0]
        d_norm  = normalizar(d_brutos)
        m_calc  = calcular_metabolismo(d_norm)
        por     = calcular_porciones(d_norm, m_calc)
        r_df    = df_c2[df_c2["ID_Alumno"]==id_sel]

        st.markdown(f"<div class='sec-head'>EXPEDIENTE: {id_sel}</div>", unsafe_allow_html=True)

        estado_act = "SIN AUDITORÍA"
        if not r_df.empty:
            estado_act = str(r_df.iloc[-1].get("Estado_Calculado","AVANCE")).upper()

        # Info de identificación primero
        etapa_admin = "q2" if not r_df.empty else "q1"
        estado_render = estado_act if estado_act != "SIN AUDITORÍA" else "Q1"
        badge_map = {
            "AVANCE":        "<span class='badge-avance'>🚀 EN AVANCE</span>",
            "RETROCESO":     "<span class='badge-retroceso'>⚠️ RETROCESO</span>",
            "LENTO":         "<span class='badge-lento'>⏳ LENTO</span>",
            "SIN AUDITORÍA": "<span class='badge-lento'>📋 SIN Q2</span>",
        }
        sexo_ic = "👩" if "Femen" in m_calc.get("genero","") else "👨"
        st.markdown(f"""
        <div style="padding:8px 0;">
          <div style="font-size:20px;font-weight:900;color:#0D1F14;">{d_norm.get('Nombre completo','')}</div>
          <div style="margin:6px 0;">{badge_map.get(estado_act, badge_map['SIN AUDITORÍA'])}</div>
          <div style="font-size:12px;color:#6B7280;">
            {sexo_ic} {m_calc['genero']} · {int(m_calc['edad'])} años · {m_calc['peso']} kg · {m_calc['estatura']} cm<br>
            IMC: {m_calc['imc']} · {m_calc['origen']}
          </div>
        </div>""", unsafe_allow_html=True)

        # Análisis visual sobre foto real — ANCHO COMPLETO
        st.markdown("<div class='sec-head'>ANÁLISIS VISUAL CON SEÑALIZACIONES</div>", unsafe_allow_html=True)
        mostrar_analisis_visual(id_sel, d_norm, m_calc, etapa=etapa_admin, estado=estado_render, ancho_px=240)

        # Deltas
        peso_act   = pf(r_df.iloc[-1].get("Peso_Revision",m_calc["peso"]) if not r_df.empty else m_calc["peso"], m_calc["peso"])
        cint_act   = pf(r_df.iloc[-1].get("Cintura_Revision",m_calc["cintura"]) if not r_df.empty else m_calc["cintura"], m_calc["cintura"])
        dif_p2     = round(peso_act - m_calc["peso"],1)
        dif_c2     = round(cint_act - m_calc["cintura"],1)

        ma,mb,mc = st.columns(3)
        with ma: metric_card("Peso", f"{peso_act} kg", f"{dif_p2:+.1f} kg", dif_p2<=0)
        with mb: metric_card("Cintura", f"{cint_act} cm", f"{dif_c2:+.1f} cm", dif_c2<=0)
        with mc: metric_card("TDEE Prescrito", f"{m_calc['cals']} kcal")

        # Tabs Q1 / Q2
        tab_q1, tab_q2 = st.tabs(["📋 Dashboard Q1 — Línea Base", "📊 Dashboard Q2 — Auditoría"])
        with tab_q1:
            dashboard_q1(d_norm, m_calc, por, id_sel)
        with tab_q2:
            dashboard_q2(d_norm, m_calc, r_df, id_sel)

        # PDF
        st.markdown("<div class='sec-head'>EXPORTAR EXPEDIENTE</div>", unsafe_allow_html=True)
        try:
            pdf_bytes = generar_pdf(d_norm, m_calc, por, r_df, id_sel)
            st.download_button(
                "🖨️ DESCARGAR EXPEDIENTE COMPLETO (PDF)",
                data=pdf_bytes,
                file_name=f"MM247_Expediente_{id_sel}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as err:
            st.error(f"Error generando PDF: {err}")


# =============================================================================
# SIDEBAR Y ENRUTADOR PRINCIPAL
# =============================================================================
df_existente = cargar_db()

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
      <div style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:900;
                  letter-spacing:4px;background:linear-gradient(135deg,#50C878,#B8F0CB);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;">MM247</div>
      <div style="font-size:9px;letter-spacing:3px;color:#50C87880;text-transform:uppercase;
                  margin-top:4px;">MIND · MUSCLE · ECOSYSTEM</div>
    </div>
    <hr style="border:none;border-top:1px solid #50C87825;margin:12px 0;">
    """, unsafe_allow_html=True)

    admin_pass = st.text_input("⚙️ Acceso Maestro", type="password", key="admin_pw")

    st.markdown("""
    <hr style="border:none;border-top:1px solid #50C87825;margin:12px 0;">
    <div style="font-size:10px;color:#50C87870;letter-spacing:2px;text-transform:uppercase;padding:4px 0;">
      ÁREA DE CLIENTES
    </div>""", unsafe_allow_html=True)

    if "vista" not in st.session_state:
        st.session_state.vista = "registro"

    if st.button("📝  Mi Registro MM247", key="btn_reg", use_container_width=True):
        st.session_state.vista = "registro"
        st.session_state.step  = 1
        st.session_state.db    = {}
        st.rerun()

    if st.button("📈  Mi Avance MM247", key="btn_av", use_container_width=True):
        st.session_state.vista = "avance"
        st.rerun()

    st.markdown("""
    <hr style="border:none;border-top:1px solid #50C87825;margin:12px 0;">
    <div style="background:#0D1F14;border:1px solid #50C87830;border-radius:8px;
                padding:10px 12px;margin-top:8px;">
      <div style="font-size:9px;letter-spacing:2px;color:#50C87870;">Sistema</div>
      <div style="font-size:10px;color:#4B7A5A;margin-top:3px;">v8.0 · MM247 Ecosystem</div>
    </div>""", unsafe_allow_html=True)

# ── ENRUTADOR ────────────────────────────────────────────────────────────────
if admin_pass == CONFIG["admin_pass"]:
    dashboard_admin(df_existente)

elif admin_pass and admin_pass != CONFIG["admin_pass"]:
    st.error("🔑 Clave maestra incorrecta.")

else:
    vista = st.session_state.get("vista","registro")
    if vista == "registro":
        formulario_q1(df_existente)
    elif vista == "avance":
        formulario_q2(df_existente)


