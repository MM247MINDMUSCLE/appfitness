# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA DE ADHERENCIA
================================================================================
"""

import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests
import random

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y BRANDING (MIND MUSCLE AESTHETIC)
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        if "ID_Alumno" not in df.columns: df["ID_Alumno"] = ""
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = "INICIAL"
        
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

def generar_id_unico(nombre):
    iniciales = "".join([p[0].upper() for p in str(nombre).strip().split() if p])[:3]
    if not iniciales: iniciales = "MM"
    anio = datetime.datetime.now().year
    numero = str(random.randint(1, 9999)).zfill(4)
    return f"MM247-{anio}-{numero}"

# Estilos CSS - Estética Profesional, Oscura y Atlética
st.markdown("""
    <style>
    /* Fondo principal y textos */
    .stApp { background-color: #0E0E0E; color: #FFFFFF; }
    
    /* Títulos de Impacto */
    .main-title { font-size: 50px; font-weight: 900; color: #FFFFFF; text-align: center; letter-spacing: 2px; margin-bottom: 0px; text-transform: uppercase; }
    .subtitle { font-size: 16px; color: #A0A0A0; text-align: center; margin-bottom: 35px; text-transform: uppercase; letter-spacing: 3px; }
    
    /* Separadores de sección */
    .section-header { font-size: 22px; font-weight: 900; color: #FFFFFF; margin-top: 30px; margin-bottom: 15px; border-bottom: 2px solid #D32F2F; padding-bottom: 8px; text-transform: uppercase; }
    
    /* Caja de ID de Éxito */
    .id-box { background: linear-gradient(135deg, #1B5E20 0%, #000000 100%); border-left: 5px solid #4CAF50; padding: 20px; border-radius: 8px; font-size: 18px; color: #FFFFFF; text-align: center; font-weight: bold; margin-top: 20px; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3); }
    
    /* Botones Call to Action */
    div.stButton > button, div[data-testid="stForm"] button { background: linear-gradient(90deg, #D32F2F 0%, #B71C1C 100%); color: white; width: 100%; border-radius: 6px; font-weight: 900; height: 55px; border: none; text-transform: uppercase; letter-spacing: 1px; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(211, 47, 47, 0.4); }
    div.stButton > button:hover, div[data-testid="stForm"] button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(211, 47, 47, 0.6); }
    
    /* Tarjetas/Tabs de Preguntas y legibilidad */
    div[data-testid="stForm"] { background: #181818; padding: 30px; border-radius: 12px; border: 1px solid #333333; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .stTextInput>div>div>input { background-color: #2D2D2D !important; color: white !important; }
    .stSelectbox>div>div { background-color: #2D2D2D !important; color: white !important; }
    .stTextArea>div>div>textarea { background-color: #2D2D2D !important; color: white !important; }
    
    /* Barras de Admin y Progreso */
    .barra-base { height: 12px; border-radius: 6px; width: 100%; background: #333333; margin-top: 5px;}
    .barra-verde { background: #4CAF50; height: 12px; border-radius: 6px; box-shadow: 0 0 10px #4CAF50;}
    .barra-roja { background: #D32F2F; height: 12px; border-radius: 6px; box-shadow: 0 0 10px #D32F2F;}
    .barra-amarilla { background: #FBC02D; height: 12px; border-radius: 6px; box-shadow: 0 0 10px #FBC02D;}
    .barra-gris { background: #757575; height: 12px; border-radius: 6px;}
    .stProgress > div > div > div > div { background-color: #D32F2F; }
    
    /* Estilizar las pestañas */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #222222; border-radius: 4px 4px 0px 0px; padding: 10px 20px; color: #AAAAAA; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #D32F2F; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# =============================================================================
# ACCESO ADMINISTRATIVO DISCRETO
# =============================================================================
with st.sidebar:
    st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
    admin_pass = st.text_input("⚙️ Modo Administrador", type="password", help="Acceso exclusivo panel MM247")

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
    norm['Condición médica'] = buscar_columna(['condición médica', 'patología', 'enfermedad'], 'Ninguna')
    norm['Tiempo entrenando'] = buscar_columna(['tiempo entrenando', 'experiencia'], 'Menos de 6 meses')
    norm['Lesión actual'] = buscar_columna(['lesión', 'lesion', 'lastimado'], 'Ninguna')
    norm['Mala postura'] = buscar_columna(['postura', 'desviación', 'hombros'], 'No')
    norm['Prohibido ejercicio'] = buscar_columna(['prohibido', 'restricción', 'axial'], 'No')
    norm['Días entrenar'] = buscar_columna(['días entrenar', 'semana cuántos', 'dias'], '4 días por semana')
    norm['Tiempo por sesión'] = buscar_columna(['tiempo por sesión', 'disponibilidad'], '60 minutos')
    norm['Compromiso'] = buscar_columna(['compromiso'], 'Alto')
    norm['Menu_Proteinas'] = buscar_columna(['menu_proteinas', 'proteínas', 'proteinas'], 'Pechuga de Pollo')
    norm['Menu_Carbohidratos'] = buscar_columna(['menu_carbohidratos', 'carbs'], 'Arroz Blanco')
    norm['Menu_Grasas'] = buscar_columna(['menu_grasas', 'grasas'], 'Aguacate')
    norm['Menu_Frutas'] = buscar_columna(['menu_frutas', 'frutas'], 'Manzana')
    
    return norm

def calcular_motores_automatizados(datos):
    try: peso = float(str(datos.get('Peso actual', '80')).replace(" kg", "").split()[0])
    except: peso = 80.0
    try: estatura = float(str(datos.get('Estatura', '175')).replace(" cm", "").split()[0])
    except: estatura = 175.0
    try: edad = float(str(datos.get('Edad', '25')).replace(" años", "").split()[0])
    except: edad = 25.0
    genero = str(datos.get('Sexo', 'Masculino'))
    
    imc = peso / ((estatura/100)**2) if estatura > 0 else 0
    
    if "Masculino" in genero: tmb = 66.473 + (13.751 * peso) + (5.0033 * estatura) - (6.755 * edad)
    else: tmb = 655.095 + (9.5634 * peso) + (1.8496 * estatura) - (4.6756 * edad)
        
    factor = 1.55
    tdee = tmb * factor
    meta = str(datos.get('Objetivo principal', 'Recomposición corporal'))
    
    if "Perder" in meta or "Bajar" in meta or "Déficit" in meta or "grasa" in meta:
        cals_obj = tdee - 400
        balance_str = "Déficit Calórico"
    elif "Ganar" in meta or "Subir" in meta or "Volumen" in meta:
        cals_obj = tdee + 300
        balance_str = "Superávit Calórico"
    else:
        cals_obj = tdee
        balance_str = "Normocalórico"
        
    prot = peso * 2.0  
    grasa = peso * 1.0 
    cals_restantes = cals_obj - ((prot * 4) + (grasa * 9))
    carbs = max(cals_restantes / 4, 50.0)
    
    return {
        "imc": round(imc, 1), "tmb": round(tmb, 0), "tdee": round(tdee, 0), "cals": round(cals_obj, 0),
        "prot": round(prot, 1), "grasa": round(grasa, 1), "carbs": round(carbs, 1), "balance_str": balance_str,
        "edad": edad, "genero": genero, "peso": peso, "estatura": estatura
    }

# =============================================================================
# 3. MOTOR DE GENERACIÓN PDF
# =============================================================================
def generar_pdf_mm247(norm, mot, revs_df, id_al):
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def limpiar(t):
        return str(t).encode('latin-1', 'replace').decode('latin-1')

    def draw_header(titulo_hoja):
        pdf.add_page()
        pdf.set_fill_color(17, 17, 17)
        pdf.rect(0, 0, 216, 30, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 24)
        pdf.set_xy(10, 8)
        pdf.cell(100, 10, 'MIND MUSCLE', 0, 0, 'L')
        pdf.set_font('Arial', 'B', 12)
        pdf.set_xy(160, 12)
        pdf.cell(45, 10, 'CONFIDENCIAL', 0, 0, 'R')
        pdf.set_text_color(200, 200, 200)
        pdf.set_font('Arial', '', 10)
        pdf.set_xy(10, 18)
        pdf.cell(100, 10, 'REPORTE MAESTRO - MM247', 0, 0, 'L')
        pdf.set_text_color(17, 17, 17)
        pdf.set_font('Arial', 'B', 14)
        pdf.set_xy(10, 35)
        pdf.cell(196, 10, limpiar(titulo_hoja), 0, 1, 'C')
        pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(0.5)
        pdf.line(10, 45, 206, 45)
        pdf.ln(10)

    draw_header("HOJA 1: PERFIL CLINICO Y DIAGNOSTICO")
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, limpiar("1. DATOS GENERALES Y METRICAS DE INICIO"), 0, 1)
    pdf.set_fill_color(248, 248, 248)
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(10, pdf.get_y(), 196, 25, 'FD')
    pdf.set_font('Arial', '', 11)
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.cell(80, 7, limpiar(f"CLIENTE: {norm['Nombre completo']}"), 0, 0)
    pdf.cell(50, 7, limpiar(f"EDAD: {int(mot['edad'])} anos"), 0, 0)
    pdf.cell(50, 7, limpiar(f"ESTATURA: {mot['estatura']} cm"), 0, 1)
    pdf.set_x(15)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(80, 7, limpiar(f"PESO INICIAL: {mot['peso']} kg"), 0, 0)
    pdf.cell(80, 7, limpiar(f"META: {norm['Objetivo principal']}"), 0, 1)
    pdf.ln(15)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, limpiar("2. DISPONIBILIDAD Y COMPROMISO LOGISTICO"), 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 7, limpiar(f"DIAS A ENTRENAR: {norm['Días entrenar']}"), 0, 1)
    pdf.cell(0, 7, limpiar(f"TIEMPO POR SESION: {norm['Tiempo por sesión']}"), 0, 1)
    pdf.cell(0, 7, limpiar(f"NIVEL DE COMPROMISO: {norm['Compromiso']}"), 0, 1)
    pdf.ln(10)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(204, 0, 0)
    pdf.cell(0, 10, limpiar("3. LIMITACIONES Y ALERTAS BIOMECANICAS"), 0, 1)
    pdf.set_fill_color(255, 240, 240)
    pdf.set_draw_color(204, 0, 0)
    pdf.rect(10, pdf.get_y(), 196, 30, 'FD')
    pdf.set_xy(15, pdf.get_y() + 5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, limpiar("ADVERTENCIA CLINICA ACTIVA:"), 0, 1)
    pdf.set_text_color(17, 17, 17)
    pdf.set_font('Arial', '', 11)
    pdf.set_x(15)
    pdf.cell(0, 6, limpiar(f"- Lesion/Condicion: {norm['Lesión actual']} / {norm['Condición médica']}"), 0, 1)
    pdf.set_x(15)
    pdf.cell(0, 6, limpiar(f"- Restriccion de Movimiento: {norm['Prohibido ejercicio']}"), 0, 1)
    pdf.set_x(15)
    pdf.cell(0, 6, limpiar(f"- Correccion Postural: {norm['Mala postura']}"), 0, 1)

    draw_header("HOJA 2: PROGRAMACION SEMANAL DE ENTRENAMIENTO")
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 7, limpiar(f"ESTRUCTURA BASADA EN: {norm['Días entrenar']}"), 0, 1)
    pdf.ln(5)
    dias = ["DIA 1 (ENFOQUE EMPUJE / PECHO-HOMBRO)", "DIA 2 (ENFOQUE TRACCION / ESPALDA)", "DIA 3 (ENFOQUE PIERNA)", "DIA 4 (ENFOQUE BRAZO / FULL BODY)"]
    for dia in dias:
        pdf.set_fill_color(17, 17, 17)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(196, 8, limpiar(dia), 0, 1, 'L', fill=True)
        pdf.set_fill_color(238, 238, 238)
        pdf.set_text_color(17, 17, 17)
        pdf.cell(96, 7, limpiar("EJERCICIO"), 1, 0, 'C', fill=True)
        pdf.cell(30, 7, limpiar("SERIES"), 1, 0, 'C', fill=True)
        pdf.cell(35, 7, limpiar("REPETICIONES"), 1, 0, 'C', fill=True)
        pdf.cell(35, 7, limpiar("DESCANSO"), 1, 1, 'C', fill=True)
        pdf.set_font('Arial', '', 10)
        ejercicios = [("Press Principal (Ajustado a lesion)", "4", "8 - 10", "90s"), ("Movimiento Secundario Maquina", "3", "10 - 12", "60s"), ("Aislamiento Polea", "4", "15 - 20", "60s")]
        for ej in ejercicios:
            pdf.cell(96, 7, limpiar(ej[0]), 1, 0, 'L')
            pdf.cell(30, 7, limpiar(ej[1]), 1, 0, 'C')
            pdf.cell(35, 7, limpiar(ej[2]), 1, 0, 'C')
            pdf.cell(35, 7, limpiar(ej[3]), 1, 1, 'C')
        pdf.ln(8)

    draw_header("HOJA 3: PROTOCOLO NUTRICIONAL Y PORCIONES EXACTAS")
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, limpiar("1. MACRONUTRIENTES Y OBJETIVO DIARIO EXACTO"), 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, limpiar("(Regla MM247: 2.0g Proteina / 1.0g Grasa por Kg de peso)"), 0, 1)
    pdf.ln(3)
    pdf.set_fill_color(248, 248, 248)
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(10, pdf.get_y(), 196, 20, 'FD')
    pdf.set_xy(10, pdf.get_y() + 5)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(49, 5, limpiar("ENERGIA TOTAL"), 0, 0, 'C')
    pdf.cell(49, 5, limpiar("PROTEINA"), 0, 0, 'C')
    pdf.cell(49, 5, limpiar("CARBOHIDRATOS"), 0, 0, 'C')
    pdf.cell(49, 5, limpiar("GRASAS"), 0, 1, 'C')
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(49, 8, limpiar(f"{mot['cals']} Kcal"), 0, 0, 'C')
    pdf.cell(49, 8, limpiar(f"{mot['prot']} g"), 0, 0, 'C')
    pdf.cell(49, 8, limpiar(f"{mot['carbs']} g"), 0, 0, 'C')
    pdf.cell(49, 8, limpiar(f"{mot['grasa']} g"), 0, 1, 'C')
    pdf.ln(15)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, limpiar("2. ESTRUCTURA DE COMIDAS (4 TOMAS DIARIAS)"), 0, 1)
    p_c, c_c, g_c, cal_c = mot['prot']/4, mot['carbs']/4, mot['grasa']/4, mot['cals']/4
    nombres_comida = ["COMIDA 1 (Desayuno)", "COMIDA 2 (Post-Entrenamiento)", "COMIDA 3 (Comida Fuerte)", "COMIDA 4 (Cena)"]
    for comida in nombres_comida:
        pdf.set_fill_color(238, 238, 238)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(196, 8, limpiar(comida), 0, 1, 'L', fill=True)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, limpiar(f"  {cal_c} Kcal | {p_c}g Prot | {c_c}g Carbs | {g_c}g Grasa"), 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.cell(0, 6, limpiar(f"  - Fuentes Sugeridas: {norm['Menu_Proteinas']} | {norm['Menu_Carbohidratos']}"), 0, 1)
        pdf.cell(0, 6, limpiar(f"  - Complementos: {norm['Menu_Grasas']} | {norm['Menu_Verduras']}"), 0, 1)
        pdf.ln(4)

    if len(revs_df) > 0:
        draw_header("HOJA 4: AUDITORIA DE RESULTADOS Y PLAN DE ACCION")
        ult_rev = revs_df.iloc[-1]
        peso_actual = float(ult_rev.get('Peso_Revision', mot['peso']))
        dif_peso = peso_actual - mot['peso']
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, limpiar("1. COMPARATIVO DE RUBROS MEDIBLES"), 0, 1)
        pdf.set_fill_color(17, 17, 17)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(60, 8, limpiar("METRICA"), 1, 0, 'C', fill=True)
        pdf.cell(45, 8, limpiar("INICIAL"), 1, 0, 'C', fill=True)
        pdf.cell(45, 8, limpiar("ACTUAL"), 1, 0, 'C', fill=True)
        pdf.cell(46, 8, limpiar("DIFERENCIA"), 1, 1, 'C', fill=True)
        pdf.set_text_color(17, 17, 17)
        pdf.set_font('Arial', '', 11)
        pdf.cell(60, 8, limpiar("Peso Corporal"), 1, 0, 'C')
        pdf.cell(45, 8, limpiar(f"{mot['peso']} kg"), 1, 0, 'C')
        pdf.cell(45, 8, limpiar(f"{peso_actual} kg"), 1, 0, 'C')
        pdf.set_text_color(34, 197, 94) if dif_peso <= 0 else pdf.set_text_color(239, 68, 68)
        pdf.cell(46, 8, limpiar(f"{dif_peso:+.1f} kg"), 1, 1, 'C')
        pdf.set_text_color(17, 17, 17)
        pdf.cell(60, 8, limpiar("Nivel de Adherencia"), 1, 0, 'C')
        pdf.cell(45, 8, limpiar("N/A"), 1, 0, 'C')
        pdf.cell(45, 8, limpiar(ult_rev.get('Adherencia_Dieta', '--')[:15]), 1, 0, 'C')
        pdf.cell(46, 8, limpiar("Reportado"), 1, 1, 'C')
        pdf.ln(15)
        estado = ult_rev.get('Estado_Calculado', 'AVANCE')
        color_fill = (34, 197, 94) if "AVANCE" in estado else (234, 179, 8) if "LENTO" in estado else (239, 68, 68)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, limpiar("2. DIAGNOSTICO DEL SISTEMA Y ESTADO"), 0, 1)
        pdf.set_fill_color(*color_fill)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(80, 10, limpiar(f"ESTATUS: {estado}"), 0, 1, 'C', fill=True)
        pdf.ln(10)
        pdf.set_text_color(17, 17, 17)
        pdf.cell(0, 10, limpiar("3. DICTAMEN ESTRATEGICO Y PLAN DE ACCION"), 0, 1)
        pdf.set_fill_color(248, 248, 248)
        pdf.rect(10, pdf.get_y(), 196, 25, 'F')
        pdf.set_font('Arial', '', 11)
        pdf.set_xy(15, pdf.get_y() + 5)
        pdf.multi_cell(186, 6, limpiar(f"El sistema ha dictaminado un estado de {estado}. Se mantendran los registros para continuar con la progresion. Ajustar cargas mecanicas en base a la percepcion de fuerza reportada."))

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# =============================================================================
# ENRUTAMIENTO DE VISTAS (ADMIN vs CLIENTE)
# =============================================================================

if admin_pass == "MM247_Admin":
    # -------------------------------------------------------------------------
    # VISTA ADMINISTRADOR
    # -------------------------------------------------------------------------
    st.markdown("<div class='main-title'>🔐 Panel Maestro MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>CONTROL CENTRAL DE RESULTADOS</div>", unsafe_allow_html=True)
    
    if df_existente.empty or len(df_existente["ID_Alumno"].dropna().unique()) == 0:
        st.warning("Aún no hay alumnos dados de alta en el sistema.")
    else:
        df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
        df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
        
        st.markdown("### 🗂️ Estatus de Atletas Activos")
        
        h1, h2, h3, h4, h5 = st.columns([1.5, 2, 2.5, 2, 1.5])
        with h1: st.markdown("**ID Atleta**")
        with h2: st.markdown("**Nombre**")
        with h3: st.markdown("**Inicio -> Meta**")
        with h4: st.markdown("**Métrica de Avance**")
        with h5: st.markdown("**Acciones**")
        st.markdown("---")
        
        ids_unicos = df_c1["ID_Alumno"].replace("", pd.NA).dropna().unique()
        
        for id_al in ids_unicos:
            datos_al = df_c1[df_c1["ID_Alumno"] == id_al].iloc[0]
            revs_al = df_c2[df_c2["ID_Alumno"] == id_al]
            
            clase_barra = "barra-gris"
            texto_barra = "Esperando Reporte"
            
            if not revs_al.empty:
                estado = str(revs_al.iloc[-1].get("Estado_Calculado", "AVANCE")).upper()
                if "AVANCE" in estado:
                    clase_barra = "barra-verde"
                    texto_barra = "Progresando"
                elif "LENTO" in estado:
                    clase_barra = "barra-amarilla"
                    texto_barra = "Avance Estancado"
                elif "RETROCESO" in estado:
                    clase_barra = "barra-roja"
                    texto_barra = "Retroceso Activo"
            
            c1, c2, c3, c4, c5 = st.columns([1.5, 2, 2.5, 2, 1.5])
            with c1: st.write(f"`{id_al}`")
            with c2: st.write(str(datos_al.get("Nombre completo", "Alumno")).title())
            with c3: st.write(f"{datos_al.get('Peso actual', '--')} -> {datos_al.get('Peso objetivo', '--')}")
            with c4: 
                st.markdown(f"<div style='font-size:12px; font-weight:bold; color:#AAAAAA;'>{texto_barra}</div><div class='barra-base'><div class='{clase_barra}'></div></div>", unsafe_allow_html=True)
            with c5:
                if st.button("Ver Expediente", key=f"btn_{id_al}"):
                    st.session_state.alumno_seleccionado = id_al
        
        st.markdown("---")
        
        if "alumno_seleccionado" in st.session_state:
            id_sel = st.session_state.alumno_seleccionado
            st.markdown(f"### 📋 Expediente Técnico: `{id_sel}`")
            
            d_brutos = df_c1[df_c1["ID_Alumno"] == id_sel].iloc[0]
            d_norm = normalizar_datos_alumno(d_brutos)
            m_calc = calcular_motores_automatizados(d_norm)
            r_df = df_c2[df_c2["ID_Alumno"] == id_sel]
            
            try:
                pdf_bytes = generar_pdf_mm247(d_norm, m_calc, r_df, id_sel)
                st.download_button(
                    label=f"🖨️ Descargar Ficha Técnica PDF",
                    data=pdf_bytes,
                    file_name=f"Ficha_Tecnica_MM247_{id_sel}.pdf",
                    mime="application/pdf"
                )
            except Exception as err:
                st.error(f"Error al compilar el PDF: {err}")

elif admin_pass != "" and admin_pass != "MM247_Admin":
    st.error("🔑 Clave de acceso inválida.")

else:
    # -------------------------------------------------------------------------
    # VISTA CLIENTE (PROGRESIVA Y DINÁMICA)
    # -------------------------------------------------------------------------
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>SISTEMA DE ALTA INTENSIDAD Y DISCIPLINA</div>", unsafe_allow_html=True)
    
    # Inicializar el estado de sesión para guardar datos y controlar los pasos
    if 'step' not in st.session_state: st.session_state.step = 1
    if 'db' not in st.session_state: st.session_state.db = {}

    # Función auxiliar para buscar el índice de un valor guardado en un selectbox
    def g_idx(lista, clave, def_val=0):
        val = st.session_state.db.get(clave)
        return lista.index(val) if val in lista else def_val

    tab_nuevo, tab_revision = st.tabs(["📝 Iniciar Expediente Nuevo", "🔄 Registrar Mi Avance (ID Requerido)"])

    # --- MÓDULO 1: FORMULARIO MAESTRO (SISTEMA DE MISIONES) ---
    with tab_nuevo:
        st.info("🔥 Bienvenido al ecosistema MM247. Completa las misiones para activar el registro.")
        
        # Barra de progreso
        st.progress(st.session_state.step / 6)
        st.markdown(f"<h4 style='text-align:center; color:#A0A0A0;'>MISIÓN {st.session_state.step} DE 6</h4>", unsafe_allow_html=True)
        
        # --- MISIÓN 1 ---
        if st.session_state.step == 1:
            with st.form("form_m1"):
                st.markdown("<div class='section-header'>1. DATOS FISIOLÓGICOS Y DEMOGRÁFICOS</div>", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                
                ops_edad = [f"{i} años" for i in range(14, 81)]
                ops_sexo = ["Masculino", "Femenino"]
                ops_est = [f"{i} cm" for i in range(120, 221)]
                ops_peso = [f"{i} kg" for i in range(40, 161)]
                ops_ocup = ["Sedentaria", "Ligera", "Activa", "Estudiante"]
                ops_hor = ["Turno Matutino", "Turno Vespertino", "Turno Nocturno", "Horario Variable"]
                ops_ciu = ["México", "Estados Unidos", "España", "Latinoamérica / Otro"]
                ops_obj = ["Perder grasa", "Ganar masa muscular", "Recomposición corporal", "Aumentar fuerza", "Mejorar salud general"]
                ops_tiem = ["1-3 meses", "3-6 meses", "6-12 meses", "Más de 1 año"]

                with col1:
                    v_nombre = st.text_input("Nombre completo (Tu identidad en el sistema):", value=st.session_state.db.get('Nombre completo', ''))
                    v_edad = st.selectbox("Edad:", ops_edad, index=g_idx(ops_edad, 'Edad', 11))
                    v_sexo = st.selectbox("Sexo asignado al nacer:", ops_sexo, index=g_idx(ops_sexo, 'Sexo', 0))
                    v_estatura = st.selectbox("Estatura base:", ops_est, index=g_idx(ops_est, 'Estatura', 55))
                    v_peso_actual = st.selectbox("Peso corporal actual:", ops_peso, index=g_idx(ops_peso, 'Peso actual', 40))
                with col2:
                    v_peso_obj = st.selectbox("Peso corporal objetivo:", ops_peso, index=g_idx(ops_peso, 'Peso objetivo', 35))
                    v_ocupacion = st.selectbox("Ocupación de rutina:", ops_ocup, index=g_idx(ops_ocup, 'Ocupación', 0))
                    v_horario = st.selectbox("Horario diario habitual:", ops_hor, index=g_idx(ops_hor, 'Horario laboral', 0))
                    v_ciudad = st.selectbox("Zona geográfica:", ops_ciu, index=g_idx(ops_ciu, 'Ciudad / País', 0))
                    v_contacto = st.text_input("WhatsApp de contacto:", value=st.session_state.db.get('Número de contacto', '55'))
                    v_correo = st.text_input("Correo electrónico:", value=st.session_state.db.get('Correo electrónico', ''))
                    
                st.markdown("<div class='section-header'>2. ENFOQUE PRINCIPAL</div>", unsafe_allow_html=True)
                v_objetivo = st.selectbox("¿Cuál es tu meta prioritaria de transformación?", ops_obj, index=g_idx(ops_obj, 'Objetivo principal', 0))
                v_tiempoloro = st.selectbox("¿En cuánto tiempo proyectas ver los primeros resultados?", ops_tiem, index=g_idx(ops_tiem, 'Tiempo deseado', 0))
                v_compromiso = st.slider("Tu nivel de disciplina real para este proceso (1 al 10):", 1, 10, st.session_state.db.get('Compromiso', 10))
                
                if st.form_submit_button("Siguiente: Misión 2 ➡️"):
                    if not v_nombre.strip():
                        st.error("❌ El campo de Nombre Completo es obligatorio para avanzar.")
                    else:
                        st.session_state.db.update({'Nombre completo': v_nombre, 'Edad': v_edad, 'Sexo': v_sexo, 'Estatura': v_estatura, 'Peso actual': v_peso_actual, 'Peso objetivo': v_peso_obj, 'Ocupación': v_ocupacion, 'Horario laboral': v_horario, 'Ciudad / País': v_ciudad, 'Número de contacto': v_contacto, 'Correo electrónico': v_correo, 'Objetivo principal': v_objetivo, 'Tiempo deseado': v_tiempoloro, 'Compromiso': v_compromiso})
                        st.session_state.step = 2
                        st.rerun()

        # --- MISIÓN 2 ---
        elif st.session_state.step == 2:
            with st.form("form_m2"):
                st.success("La constancia es la clave de la hipertrofia. Cuéntanos tu experiencia.")
                st.markdown("<div class='section-header'>3. ANTECEDENTES DE ENTRENAMIENTO</div>", unsafe_allow_html=True)
                
                ops_t_ent = ["Nunca", "Menos de 6 meses", "De 6 meses a 1 año", "1 a 3 años", "Más de 3 años"]
                ops_d_sem = ["3 días por semana", "4 días por semana", "5 días por semana"]
                ops_t_ses = ["Menos de 45 minutos", "De 45 a 75 minutos", "Más de 75 minutos"]
                ops_s_n = ["Sí", "No"]
                
                v_tiempo_entrenando = st.selectbox("Tiempo entrenando de forma ininterrumpida:", ops_t_ent, index=g_idx(ops_t_ent, 'Tiempo entrenando', 0))
                v_tipo_entreno = st.multiselect("Sistemas deportivos practicados con anterioridad:", ["Gimnasio", "Calistenia", "Crossfit", "Deportes", "Funcional", "Ninguno"], default=st.session_state.db.get('Tipo entreno', ["Gimnasio"]))
                v_dias_semana = st.selectbox("¿Cuántos días a la semana estarás en las trincheras?", ops_d_sem, index=g_idx(ops_d_sem, 'Días entrenar', 1))
                v_tiempo_sesion = st.selectbox("Disponibilidad de tiempo por sesión:", ops_t_ses, index=g_idx(ops_t_ses, 'Tiempo por sesión', 1))
                v_entrena_act = st.selectbox("¿Te encuentras entrenando actualmente?", ops_s_n, index=g_idx(ops_s_n, 'Entrena actualmente', 0))
                v_coach_antes = st.selectbox("¿Has tenido entrenadores personales previos?", ops_s_n, index=g_idx(ops_s_n, 'Coach anterior', 1))
                
                c1, c2 = st.columns(2)
                btn_back = c1.form_submit_button("⬅️ Atrás")
                btn_next = c2.form_submit_button("Siguiente: Misión 3 ➡️")
                
                if btn_back or btn_next:
                    st.session_state.db.update({'Tiempo entrenando': v_tiempo_entrenando, 'Tipo entreno': v_tipo_entreno, 'Días entrenar': v_dias_semana, 'Tiempo por sesión': v_tiempo_sesion, 'Entrena actualmente': v_entrena_act, 'Coach anterior': v_coach_antes})
                    if btn_back: st.session_state.step = 1
                    if btn_next: st.session_state.step = 3
                    st.rerun()

        # --- MISIÓN 3 ---
        elif st.session_state.step == 3:
            with st.form("form_m3"):
                st.error("⚠️ El dolor articular no es negociable. Reporta cualquier lesión para ajustar tu carga mecánica.")
                st.markdown("<div class='section-header'>4. CONDICIÓN CLÍNICA Y LESIONES</div>", unsafe_allow_html=True)
                
                ops_les = ["Ninguna", "Rodilla / Desgaste / Tendinitis", "Hombro / Manguito rotador", "Espalda Baja / Lumbalgia", "Cervicales", "Muñeca / Tobillo"]
                ops_cir = ["No", "Sí, en miembros inferiores", "Sí, en miembros superiores / columna"]
                ops_dol = ["No", "Sí, al hacer presses", "Sí, al hacer sentadillas", "Sí, dolor lumbar constante"]
                ops_med = ["No", "Sí, para presión / glucosa", "Sí, antiinflamatorios"]
                ops_con = ["Ninguna", "Diabetes", "Hipertensión", "Problemas de Tiroides / Hormonales", "Hernia Discal / Umbilical"]
                ops_pro = ["No", "Sí, cargas sobre la columna", "Sí, flexiones profundas"]
                
                v_lesion = st.selectbox("¿Sufres de alguna lesión o dolor recurrente?", ops_les, index=g_idx(ops_les, 'Lesión actual', 0))
                v_cirugias = st.selectbox("¿Cuentas con cirugías o intervenciones médicas?", ops_cir, index=g_idx(ops_cir, 'Cirugías', 0))
                v_dolor_frec = st.selectbox("¿Sientes molestias agudas al ejecutar cargas pesadas?", ops_dol, index=g_idx(ops_dol, 'Dolor frecuente', 0))
                v_medica = st.selectbox("¿Consumes medicamentos de prescripción diaria?", ops_med, index=g_idx(ops_med, 'Medicamentos', 0))
                v_cond_diag = st.selectbox("¿Tienes alguna patología crónica diagnosticada?", ops_con, index=g_idx(ops_con, 'Condición médica', 0))
                v_restriccion = st.selectbox("¿Tienes prohibiciones médicas explícitas?", ["No", "Sí"], index=g_idx(["No", "Sí"], 'Restricciones', 0))
                v_prohibido = st.selectbox("¿Te han prohibido cargas pesadas sobre la columna (carga axial)?:", ops_pro, index=g_idx(ops_pro, 'Prohibido ejercicio', 0))
                
                st.markdown("<div class='section-header'>5. AUTO-EVALUACIÓN BIOMECÁNICA</div>", unsafe_allow_html=True)
                v_molestias_mov = st.multiselect("¿Limitaciones o dolor en movimientos básicos?:", ["Sentadilla", "Press de pecho", "Peso muerto", "Press militar", "Ninguno"], default=st.session_state.db.get('Molestias movimientos', ["Ninguno"]))
                v_movilidad = st.selectbox("¿Cómo evalúas tu flexibilidad general?", ["Mala / Muy rígido", "Regular", "Buena"], index=g_idx(["Mala / Muy rígido", "Regular", "Buena"], 'Movilidad', 1))
                v_lim_mov = st.selectbox("¿Notas acortamientos evidentes de movimiento?", ["No", "Sí, en tobillos/cadera", "Sí, en hombros"], index=g_idx(["No", "Sí, en tobillos/cadera", "Sí, en hombros"], 'Limitaciones movilidad', 0))
                v_sentado = st.selectbox("¿Cuántas horas pasas sentado al día?", ["Sí, más de 6 horas", "Moderado (3 a 6 horas)", "No"], index=g_idx(["Sí, más de 6 horas", "Moderado (3 a 6 horas)", "No"], 'Horas sentado', 1))
                v_postura = st.selectbox("¿Desviaciones posturales conocidas?", ["No", "Sí, hombros adelantados", "Sí, hiperlordosis lumbar"], index=g_idx(["No", "Sí, hombros adelantados", "Sí, hiperlordosis lumbar"], 'Mala postura', 0))
                v_debil = st.selectbox("¿Tu eslabón muscular más débil?:", ["Tren Inferior", "Tren Superior", "Zona Media / Core", "Espalda"], index=g_idx(["Tren Inferior", "Tren Superior", "Zona Media / Core", "Espalda"], 'Parte débil', 0))
                v_desarrollado = st.selectbox("¿Grupo muscular con mejor genética?:", ["Ninguno", "Piernas", "Pectoral / Brazos", "Espalda"], index=g_idx(["Ninguno", "Piernas", "Pectoral / Brazos", "Espalda"], 'Músculo desarrollado', 0))
                v_equilibrio = st.selectbox("¿Problemas de coordinación mecánica?:", ["No", "Sí"], index=g_idx(["No", "Sí"], 'Equilibrio', 0))

                c1, c2 = st.columns(2)
                btn_back = c1.form_submit_button("⬅️ Atrás")
                btn_next = c2.form_submit_button("Siguiente: Misión 4 ➡️")
                
                if btn_back or btn_next:
                    st.session_state.db.update({'Lesión actual': v_lesion, 'Cirugías': v_cirugias, 'Dolor frecuente': v_dolor_frec, 'Medicamentos': v_medica, 'Condición médica': v_cond_diag, 'Restricciones': v_restriccion, 'Prohibido ejercicio': v_prohibido, 'Molestias movimientos': v_molestias_mov, 'Movilidad': v_movilidad, 'Limitaciones movilidad': v_lim_mov, 'Horas sentado': v_sentado, 'Mala postura': v_postura, 'Parte débil': v_debil, 'Músculo desarrollado': v_desarrollado, 'Equilibrio': v_equilibrio})
                    if btn_back: st.session_state.step = 2
                    if btn_next: st.session_state.step = 4
                    st.rerun()

        # --- MISIÓN 4 ---
        elif st.session_state.step == 4:
            with st.form("form_m4"):
                st.warning("El músculo crece fuera del gimnasio. Evalúa tu recuperación.")
                st.markdown("<div class='section-header'>6. MORFOLOGÍA Y ESTRUCTURA</div>", unsafe_allow_html=True)
                
                v_fisico = st.selectbox("¿Con qué somatotipo te identificas?", ["Delgado / Ectomorfo", "Atlético / Mesomorfo", "Robusto / Endomorfo", "Sobrepeso"], index=g_idx(["Delgado / Ectomorfo", "Atlético / Mesomorfo", "Robusto / Endomorfo", "Sobrepeso"], 'Consideración física', 1))
                v_acumula_grasa = st.selectbox("¿Dónde tiendes a acumular tejido graso?:", ["Abdomen / Zona lumbar", "Piernas y Cadera", "Distribución General"], index=g_idx(["Abdomen / Zona lumbar", "Piernas y Cadera", "Distribución General"], 'Acumula grasa', 0))
                v_gana_musculo = st.selectbox("¿Facilidad para construir masa muscular?", ["Muy difícil", "Ritmo Normal", "Fácil"], index=g_idx(["Muy difícil", "Ritmo Normal", "Fácil"], 'Facilidad músculo', 1))
                v_gana_grasa = st.selectbox("¿Velocidad de aumento de grasa en periodos libres?", ["Muy fácil", "Ritmo Normal", "Difícil"], index=g_idx(["Muy fácil", "Ritmo Normal", "Difícil"], 'Facilidad grasa', 1))
                
                st.markdown("<div class='section-header'>7. CALIDAD DE HÁBITOS Y DESCANSO</div>", unsafe_allow_html=True)
                v_horas_sueno = st.selectbox("Promedio de horas de sueño por noche:", ["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"], index=g_idx(["4-5 horas", "6 horas", "7-8 horas", "Más de 8 horas"], 'Horas sueño', 2))
                v_calif_sueno = st.selectbox("Calidad percibida de tu descanso nocturno:", ["Malo", "Regular", "Excelente"], index=g_idx(["Malo", "Regular", "Excelente"], 'Calificación descanso', 1))
                v_estres_diario = st.selectbox("Nivel de estrés mental / laboral cotidiano:", ["Bajo / Controlado", "Medio", "Alto"], index=g_idx(["Bajo / Controlado", "Medio", "Alto"], 'Nivel de estrés', 1))
                v_num_comidas = st.selectbox("¿Cuántas comidas sólidas realizas al día?", ["2 comidas", "3 comidas", "4 comidas", "5 comidas o más"], index=g_idx(["2 comidas", "3 comidas", "4 comidas", "5 comidas o más"], 'Comidas al día', 2))
                v_litros_agua = st.selectbox("Consumo diario estimado de agua:", ["Menos de 1.5 Litros", "Entre 1.5 y 3 Litros", "Más de 3 Litros"], index=g_idx(["Menos de 1.5 Litros", "Entre 1.5 y 3 Litros", "Más de 3 Litros"], 'Agua diaria', 1))
                v_alcohol = st.selectbox("Frecuencia de consumo de alcohol:", ["No / Nunca", "Solo Ocasional", "Frecuente fines de semana"], index=g_idx(["No / Nunca", "Solo Ocasional", "Frecuente fines de semana"], 'Alcohol', 1))
                v_fuma = st.selectbox("¿Consumes tabaco?", ["No", "Sí"], index=g_idx(["No", "Sí"], 'Fuma', 0))
                v_pasos = st.selectbox("Estimación diaria de movimiento (Pasos/NEAT):", ["Menos de 5k", "5k a 10k", "Más de 10k"], index=g_idx(["Menos de 5k", "5k a 10k", "Más de 10k"], 'Pasos día', 1))
                v_nivel_actividad = st.selectbox("Nivel de actividad física fuera del gimnasio:", ["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"], index=g_idx(["Sedentario", "Poco activo", "Moderadamente activo", "Muy activo"], 'Nivel de actividad', 2))

                c1, c2 = st.columns(2)
                btn_back = c1.form_submit_button("⬅️ Atrás")
                btn_next = c2.form_submit_button("Siguiente: Misión 5 ➡️")
                
                if btn_back or btn_next:
                    st.session_state.db.update({'Consideración física': v_fisico, 'Acumula grasa': v_acumula_grasa, 'Facilidad músculo': v_gana_musculo, 'Facilidad grasa': v_gana_grasa, 'Horas sueño': v_horas_sueno, 'Calificación descanso': v_calif_sueno, 'Nivel de estrés': v_estres_diario, 'Comidas al día': v_num_comidas, 'Agua diaria': v_litros_agua, 'Alcohol': v_alcohol, 'Fuma': v_fuma, 'Pasos día': v_pasos, 'Nivel de actividad': v_nivel_actividad})
                    if btn_back: st.session_state.step = 3
                    if btn_next: st.session_state.step = 5
                    st.rerun()

        # --- MISIÓN 5 ---
        elif st.session_state.step == 5:
            with st.form("form_m5"):
                st.info("Selecciona el combustible que formará tu dieta estructurada. Mantente apegado al plan.")
                st.markdown("<div class='section-header'>8. MENÚ DE SELECCIÓN CONTROLADA</div>", unsafe_allow_html=True)
                
                v_menu_prots = st.multiselect("🥩 FUENTES DE PROTEÍNA:", ["Pechuga de Pollo", "Bisteck de Res magro", "Lomo de Cerdo", "Claras de Huevo", "Atún en agua", "Filete de Pescado"], default=st.session_state.db.get('Menu_Proteinas', ["Pechuga de Pollo", "Claras de Huevo"]))
                v_menu_carbs = st.multiselect("🍞 CARBOHIDRATOS COMPLEJOS:", ["Arroz Blanco", "Avena en Hojuelas", "Camote asado", "Papa cocida", "Tortilla de Maíz"], default=st.session_state.db.get('Menu_Carbohidratos', ["Arroz Blanco", "Avena en Hojuelas"]))
                v_menu_grasas = st.multiselect("🥑 GRASAS SALUDABLES:", ["Aguacate", "Almendras naturales", "Crema de Cacahuete"], default=st.session_state.db.get('Menu_Grasas', ["Aguacate"]))
                v_menu_frutas = st.multiselect("🍎 FRUTAS:", ["Plátano", "Manzana", "Fresas / Berries"], default=st.session_state.db.get('Menu_Frutas', ["Plátano", "Manzana"]))
                v_menu_verds = st.multiselect("🥦 VERDURAS:", ["Brócoli", "Espinacas", "Lechuga / Pepino"], default=st.session_state.db.get('Menu_Verduras', ["Brócoli", "Espinacas"]))
                
                st.markdown("<div class='section-header'>9. PERFIL NUTRICIONAL</div>", unsafe_allow_html=True)
                v_obj_nutri = st.selectbox("Preferencia alimenticia actual:", ["Bajar porcentaje de grasa", "Aumento de masa magra"], index=g_idx(["Bajar porcentaje de grasa", "Aumento de masa magra"], 'Objetivo nutricional', 0))
                v_alergias = st.text_input("¿Tienes alergias alimentarias graves?", placeholder="Ej: Cacahuates...", value=st.session_state.db.get('Alergias alimenticias', ''))
                v_intolerancia = st.text_input("¿Padeces intolerancias digestivas?", placeholder="Ej: Lactosa...", value=st.session_state.db.get('Intolerancias', ''))
                v_tipo_alimentacion = st.selectbox("Estructura dietética:", ["Omnívoro", "Vegetariano"], index=g_idx(["Omnívoro", "Vegetariano"], 'Tipo alimentación', 0))
                v_no_gustan = st.text_input("Alimentos que rechazas rotundamente:", placeholder="Ej: Pescado, cebolla...", value=st.session_state.db.get('Alimentos no gustan', ''))
                v_comer_fuera = st.selectbox("¿Sueles comer en restaurantes?", ["Nunca", "1-2 veces por semana"], index=g_idx(["Nunca", "1-2 veces por semana"], 'Comer fuera', 0)) # Added index check just in case
                v_presupuesto = st.selectbox("Presupuesto para tu plan nutricional:", ["Básico / Económico", "Estándar flexible"], index=g_idx(["Básico / Económico", "Estándar flexible"], 'Presupuesto', 1))
                v_horarios_fijos = st.selectbox("¿Necesitas horarios estrictos para comer?", ["Sí", "No"], index=g_idx(["Sí", "No"], 'Horarios fijos', 1))
                v_cocinar = st.selectbox("¿Cocinas tus propios alimentos?", ["Sí", "No"], index=g_idx(["Sí", "No"], 'Cocinar', 0))

                c1, c2 = st.columns(2)
                btn_back = c1.form_submit_button("⬅️ Atrás")
                btn_next = c2.form_submit_button("Siguiente: Misión 6 ➡️")
                
                if btn_back or btn_next:
                    st.session_state.db.update({'Menu_Proteinas': v_menu_prots, 'Menu_Carbohidratos': v_menu_carbs, 'Menu_Grasas': v_menu_grasas, 'Menu_Frutas': v_menu_frutas, 'Menu_Verduras': v_menu_verds, 'Objetivo nutricional': v_obj_nutri, 'Alergias alimenticias': v_alergias, 'Intolerancias': v_intolerancia, 'Tipo alimentación': v_tipo_alimentacion, 'Alimentos no gustan': v_no_gustan})
                    if btn_back: st.session_state.step = 4
                    if btn_next: st.session_state.step = 6
                    st.rerun()

        # --- MISIÓN 6 ---
        elif st.session_state.step == 6:
            with st.form("form_m6"):
                st.markdown("<div class='section-header'>10. DISPONIBILIDAD LOGÍSTICA</div>", unsafe_allow_html=True)
                v_donde_entrena = st.selectbox("¿Dónde entrenarás?", ["Gimnasio comercial completo", "Casa con equipo"], index=g_idx(["Gimnasio comercial completo", "Casa con equipo"], 'Donde entrenará', 0))
                v_equipo = st.multiselect("¿De qué equipamiento dispones?", ["Mancuernas", "Barras y Discos", "Poleas"], default=st.session_state.db.get('Equipo disponible', ["Mancuernas", "Barras y Discos"]))
                v_lim_space = st.selectbox("¿Limitaciones de espacio físico?", ["No", "Sí"], index=g_idx(["No", "Sí"], 'Limitación espacio', 0))
                
                st.markdown("<div class='section-header'>11. METAS DE ENFOQUE Y FILTROS</div>", unsafe_allow_html=True)
                v_partes_mejorar = st.selectbox("Sector muscular prioritario a desarrollar:", ["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda", "Brazos", "Abdomen / Definición"], index=g_idx(["Glúteos / Femorales", "Cuádriceps", "Hombros y Espalda", "Brazos", "Abdomen / Definición"], 'Partes mejorar', 2))
                v_dificultad = st.text_input("¿Cuál ha sido tu mayor obstáculo en el pasado?", value=st.session_state.db.get('Dificultades físicas', ''))
                v_odia_ex = st.text_input("¿Qué ejercicio odias y prefieres evitar?", value=st.session_state.db.get('Ejercicio odia', ''))
                v_disfruta_ex = st.text_input("¿Con qué ejercicio sientes mayor conexión o bombeo?", value=st.session_state.db.get('Ejercicio disfruta', ''))
                v_impide_progresar = st.text_area("¿Qué saboteó tu avance en intentos anteriores?", value=st.session_state.db.get('Impedido progresar', ''))
                
                st.markdown("<div class='section-header'>12. ESCALAS PSICOMÉTRICAS (1 AL 10)</div>", unsafe_allow_html=True)
                v_p_disciplina = st.slider("Tu nivel de Disciplina Actual:", 1, 10, st.session_state.db.get('P_Disciplina', 8))
                v_p_estres = st.slider("Carga de Estrés mental:", 1, 10, st.session_state.db.get('P_Estres', 5))
                v_p_sueno = st.slider("Capacidad de descansar profundo:", 1, 10, st.session_state.db.get('P_Sueno', 8))
                v_p_motivacion = st.slider("Fuego interno / Motivación:", 1, 10, st.session_state.db.get('P_Motivacion', 9))
                v_p_energia = st.slider("Energía vital diaria:", 1, 10, st.session_state.db.get('P_Energia', 7))
                v_p_hambre = st.slider("Ansiedad por comida fuera de dieta:", 1, 10, st.session_state.db.get('P_Hambre', 5))
                v_p_recup = st.slider("Velocidad de recuperación muscular:", 1, 10, st.session_state.db.get('P_Recup', 7))
                v_prioridad = st.selectbox("Prioridad central de tu entrenamiento:", ["Salud", "Estética", "Rendimiento"], index=g_idx(["Salud", "Estética", "Rendimiento"], 'Prioridad', 1))
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                btn_back = c1.form_submit_button("⬅️ Atrás")
                enviar_maestro = c2.form_submit_button("🚀 REGISTRAR EXPEDIENTE")
                
                if btn_back:
                    st.session_state.db.update({'Donde entrenará': v_donde_entrena, 'Equipo disponible': v_equipo, 'Limitación espacio': v_lim_space, 'Partes mejorar': v_partes_mejorar, 'Dificultades físicas': v_dificultad, 'Ejercicio odia': v_odia_ex, 'Ejercicio disfruta': v_disfruta_ex, 'Impedido progresar': v_impide_progresar, 'P_Disciplina': v_p_disciplina, 'P_Estres': v_p_estres, 'P_Sueno': v_p_sueno, 'P_Motivacion': v_p_motivacion, 'P_Energia': v_p_energia, 'P_Hambre': v_p_hambre, 'P_Recup': v_p_recup, 'Prioridad': v_prioridad})
                    st.session_state.step = 5
                    st.rerun()
                    
                if enviar_maestro:
                    # Guardamos la última info
                    st.session_state.db.update({'Donde entrenará': v_donde_entrena, 'Equipo disponible': v_equipo, 'Limitación espacio': v_lim_space, 'Partes mejorar': v_partes_mejorar, 'Dificultades físicas': v_dificultad, 'Ejercicio odia': v_odia_ex, 'Ejercicio disfruta': v_disfruta_ex, 'Impedido progresar': v_impide_progresar, 'P_Disciplina': v_p_disciplina, 'P_Estres': v_p_estres, 'P_Sueno': v_p_sueno, 'P_Motivacion': v_p_motivacion, 'P_Energia': v_p_energia, 'P_Hambre': v_p_hambre, 'P_Recup': v_p_recup, 'Prioridad': v_prioridad})
                    
                    nombre_final = st.session_state.db.get("Nombre completo", "")
                    if not nombre_final.strip():
                        st.error("❌ Ocurrió un error. El nombre está vacío.")
                    else:
                        id_nuevo_alumno = generar_id_unico(nombre_final)
                        d = st.session_state.db
                        
                        payload = {
                            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Tipo_Registro": "INICIAL",
                            "ID_Alumno": id_nuevo_alumno,
                            "Nombre completo": str(d.get("Nombre completo")).title(), "Edad": str(d.get("Edad")), "Sexo": str(d.get("Sexo")), "Estatura": str(d.get("Estatura")), "Peso actual": str(d.get("Peso actual")),
                            "Peso objetivo": str(d.get("Peso objetivo")), "Ocupación": str(d.get("Ocupación")), "Horario laboral": str(d.get("Horario laboral")), "Ciudad / País": str(d.get("Ciudad / País")), "Número de contacto": str(d.get("Número de contacto")), "Correo electrónico": str(d.get("Correo electrónico")),
                            "Objetivo principal": str(d.get("Objetivo principal")), "Tiempo deseado": str(d.get("Tiempo deseado")), "Compromiso": str(d.get("Compromiso")), "Tiempo entrenando": str(d.get("Tiempo entrenando")), "Tipo entreno": ",".join(d.get("Tipo entreno", [])),
                            "Días entrenar": str(d.get("Días entrenar")), "Tiempo por sesión": str(d.get("Tiempo por sesión")), "Entrena actualmente": str(d.get("Entrena actualmente")), "Coach anterior": str(d.get("Coach anterior")), "Lesión actual": str(d.get("Lesión actual")),
                            "Cirugías": str(d.get("Cirugías")), "Dolor frecuente": str(d.get("Dolor frecuente")), "Medicamentos": str(d.get("Medicamentos")), "Condición médica": str(d.get("Condición médica")), "Restricciones": str(d.get("Restricciones")), "Prohibido ejercicio": str(d.get("Prohibido ejercicio")),
                            "Molestias movimientos": ",".join(d.get("Molestias movimientos", [])), "Movilidad": str(d.get("Movilidad")), "Limitaciones movilidad": str(d.get("Limitaciones movilidad")), "Horas sentado": str(d.get("Horas sentado")), "Mala postura": str(d.get("Mala postura")),
                            "Parte débil": str(d.get("Parte débil")), "Músculo desarrollado": str(d.get("Músculo desarrollado")), "Equilibrio": str(d.get("Equilibrio")), "Consideración física": str(d.get("Consideración física")), "Acumula grasa": str(d.get("Acumula grasa")),
                            "Facilidad músculo": str(d.get("Facilidad músculo")), "Facilidad grasa": str(d.get("Facilidad grasa")), "Horas sueño": str(d.get("Horas sueño")), "Calificación descanso": str(d.get("Calificación descanso")), "Nivel de estrés": str(d.get("Nivel de estrés")),
                            "Comidas al día": str(d.get("Comidas al día")), "Agua diaria": str(d.get("Agua diaria")), "Alcohol": str(d.get("Alcohol")), "Fuma": str(d.get("Fuma")), "Pasos día": str(d.get("Pasos día")), "Nivel de actividad": str(d.get("Nivel de actividad")),
                            "Objetivo nutricional": str(d.get("Objetivo nutricional")), "Alergias alimenticias": str(d.get("Alergias alimenticias")), "Intolerancias": str(d.get("Intolerancias")), "Tipo alimentación": str(d.get("Tipo alimentación")), "Alimentos no gustan": str(d.get("Alimentos no gustan")),
                            "Donde entrenará": str(d.get("Donde entrenará")), "Equipo disponible": ",".join(d.get("Equipo disponible", [])), "Limitación espacio": str(d.get("Limitación espacio")), "Partes mejorar": str(d.get("Partes mejorar")), "Dificultades físicas": str(d.get("Dificultades físicas")),
                            "Ejercicio odia": str(d.get("Ejercicio odia")), "Ejercicio disfruta": str(d.get("Ejercicio disfruta")), "Impedido progresar": str(d.get("Impedido progresar")), "P_Disciplina": str(d.get("P_Disciplina")), "P_Estres": str(d.get("P_Estres")),
                            "P_Sueno": str(d.get("P_Sueno")), "P_Motivacion": str(d.get("P_Motivacion")), "P_Energia": str(d.get("P_Energia")), "P_Hambre": str(d.get("P_Hambre")), "P_Recup": str(d.get("P_Recup")), "Prioridad": str(d.get("Prioridad")),
                            "Menu_Proteinas": ",".join(d.get("Menu_Proteinas", [])), "Menu_Carbohidratos": ",".join(d.get("Menu_Carbohidratos", [])), "Menu_Grasas": ",".join(d.get("Menu_Grasas", [])), "Menu_Frutas": ",".join(d.get("Menu_Frutas", [])), "Menu_Verduras": ",".join(d.get("Menu_Verduras", [])),
                            "Propuesta General": "", "Balance Energético": "", "Rutina Biomecánica": ""
                        }
                        
                        with st.spinner("Sincronizando expediente con el servidor principal..."):
                            try:
                                response = requests.post(WEBHOOK_URL, json=payload)
                                if response.status_code == 200 and "success" in response.text:
                                    st.markdown(f"<div class='id-box'>✅ ¡EXPEDIENTE GUARDADO CON ÉXITO!<br><br>TU ID ÚNICO DE ATLETA ES:<br><span style='font-size:36px; color:#4CAF50;'>{id_nuevo_alumno}</span><br><br><small style='color:#DDD; font-weight:normal;'>Guárdalo. Lo usarás para evaluar tu progreso periódicamente en la pestaña de revisión.</small></div>", unsafe_allow_html=True)
                                    st.balloons()
                                    # Reiniciamos el formulario para el siguiente usuario
                                    st.session_state.step = 1
                                    st.session_state.db = {}
                                else: st.error(f"Error en servidor: {response.text}")
                            except Exception as api_err: st.error(f"Fallo de comunicación: {api_err}")

    # --- MÓDULO 2: REVISIÓN DE AVANCE (CLIENTE) ---
    with tab_revision:
        st.info("La constancia se mide en datos. Ingresa tu ID para reportar tu estado actual a tu entrenador.")
        
        with st.form("form_revision_c2", clear_on_submit=True):
            id_ingresado = st.text_input("Tu ID de Atleta (Ej: MM247-2026-0001):").strip().upper()
            st.markdown("<div class='section-header'>1. Evaluación Corporal</div>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1: peso_rev = st.number_input("Peso Actual en Ayunas (kg):", min_value=30.0, value=70.0, step=0.1)
            with col2: cintura_rev = st.number_input("Contorno de Cintura (cm):", min_value=40.0, value=80.0, step=0.5)
            
            st.markdown("<div class='section-header'>2. Métricas de Progreso y Apego</div>", unsafe_allow_html=True)
            adherencia = st.radio("Nivel de cumplimiento de dieta y macros:", ["Cumplimiento Total (Excelente)", "Cumplimiento Parcial (Aceptable)", "Cumplimiento Bajo (Mal apego)"])
            fuerza = st.radio("Nivel de fuerza reportado en entrenamientos:", ["Incrementé los pesos o repeticiones", "Me mantuve estable", "Me sentí más débil / fatigado"])
            sueno_c2 = st.slider("Calidad del sueño esta semana (1-10):", 1, 10, 8)
            comentarios = st.text_area("Reporte de campo: Dudas, dolores, o sensaciones de la semana:")
            
            st.markdown("<br>", unsafe_allow_html=True)
            btn_enviar_c2 = st.form_submit_button("🚀 ENVIAR REPORTE DE CAMPO")
            
            if btn_enviar_c2:
                if not id_ingresado:
                    st.error("❌ El ID de Atleta es obligatorio.")
                elif df_existente.empty or id_ingresado not in df_existente["ID_Alumno"].values:
                    st.error("❌ El ID ingresado no está registrado en el sistema. Verifica mayúsculas y guiones.")
                else:
                    puntos = 0
                    if adherencia == "Cumplimiento Total (Excelente)": puntos += 2
                    elif adherencia == "Cumplimiento Parcial (Aceptable)": puntos += 1
                    
                    if fuerza == "Incrementé los pesos o repeticiones": puntos += 2
                    elif fuerza == "Me mantuve estable": puntos += 1
                    
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
                        "Estado_Calculado": estado_calculado
                    }
                    
                    with st.spinner("Evaluando métricas..."):
                        try:
                            requests.post(WEBHOOK_URL, json=payload_c2)
                            st.success("✅ Evaluación registrada correctamente en el sistema. Mantén el enfoque.")
                        except Exception as e:
                            st.error(f"Error de red al enviar: {e}")
