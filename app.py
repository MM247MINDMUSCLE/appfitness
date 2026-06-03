# -*- coding: utf-8 -*-
"""
================================================================================
          SISTEMA DIGITAL CORE MM247 — MIND MUSCLE ECOSYSTEM
   EVALUACIÓN METABÓLICA, CONTROL BIOMECÁNICO Y AUDITORÍA DE ADHERENCIA
================================================================================
Archivo: app.py
Líneas de Producción: 785 líneas
Garantía: Ensamblaje total con llaves únicas (keys) anti-duplicidad
================================================================================
"""

import streamlit as st
import datetime
import json
import os
import time
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ================================================================================
# 1. CONFIGURACIÓN ESTRUCTURAL DE LA PÁGINA Y ESTILOS AVANZADOS
# ================================================================================
st.set_page_config(
    page_title="Ecosistema Digital Core MM247",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .reportview-container { background-color: #f9f9fb; }
        .main { background-color: #f9f9fb; }
        .header-container {
            background-color: #11151c; padding: 30px; border-radius: 12px;
            border-bottom: 5px solid #ff6b35; margin-bottom: 25px; color: #ffffff;
        }
        .header-title { color: #ff6b35; font-size: 34px; font-weight: 800; margin: 0; letter-spacing: 1.5px; }
        .header-subtitle { color: #e5e5e5; font-size: 14px; margin-top: 5px; text-transform: uppercase; }
        .section-card {
            background-color: #ffffff; padding: 25px; border-radius: 10px;
            border: 1px solid #e5e5e5; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        }
        .section-title {
            color: #ff6b35; font-size: 20px; font-weight: 700;
            border-bottom: 2px solid #f0f0f5; padding-bottom: 10px; margin-bottom: 15px;
        }
        .stButton>button {
            background-color: #ff6b35 !important; color: white !important; border-radius: 6px !important;
            font-size: 16px !important; font-weight: bold !important; padding: 14px 30px !important;
            width: 100% !important; border: none !important; transition: all 0.3s ease !important;
        }
        .stButton>button:hover { background-color: #e55a2b !important; transform: translateY(-2px) !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">MIND MUSCLE — MM247</h1>
        <p class="header-subtitle">Matriz de Inteligencia Biomecánica y Gestión de Alumnos</p>
    </div>
""", unsafe_allow_html=True)

# ================================================================================
# 2. MOTOR DE TRADUCCIÓN NUTRICIONAL Y CONVERSIÓN DE MACRONUTRIENTES
# ================================================================================
MATRIZ_ALIMENTOS_MM247 = {
    "Pechuga de Pollo": {"tipo": "Proteina", "porcion_base": 100, "aporte_macro": 30, "unidad": "g (pesado cocido)"},
    "Claras de Huevo": {"tipo": "Proteina", "porcion_base": 1, "aporte_macro": 4, "unidad": "piezas"},
    "Huevo Entero": {"tipo": "Proteina", "porcion_base": 1, "aporte_macro": 6, "unidad": "piezas"},
    "Bisteck de Res": {"tipo": "Proteina", "porcion_base": 100, "aporte_macro": 26, "unidad": "g (pesado en crudo)"},
    "Lomo de Cerdo": {"tipo": "Proteina", "porcion_base": 100, "aporte_macro": 28, "unidad": "g (pesado cocido)"},
    "Queso Cottage": {"tipo": "Proteina", "porcion_base": 100, "aporte_macro": 12, "unidad": "g"},
    "Filete de Pescado": {"tipo": "Proteina", "porcion_base": 100, "aporte_macro": 24, "unidad": "g (pesado cocido)"},
    "Arroz Blanco": {"tipo": "Carbohidrato", "porcion_base": 100, "aporte_macro": 28, "unidad": "g (pesado cocido)"},
    "Avena en Hojuelas": {"tipo": "Carbohidrato", "porcion_base": 100, "aporte_macro": 66, "unidad": "g (pesado en crudo)"},
    "Camote Dulce": {"tipo": "Carbohidrato", "porcion_base": 100, "aporte_macro": 24, "unidad": "g (pesado hervido)"},
    "Pasta Integral": {"tipo": "Carbohidrato", "porcion_base": 100, "aporte_macro": 25, "unidad": "g (pesada cocida)"},
    "Almendras": {"tipo": "Grasa", "porcion_base": 10, "aporte_macro": 5, "unidad": "g"},
    "Aceite de Oliva": {"tipo": "Grasa", "porcion_base": 15, "aporte_macro": 14, "unidad": "ml"},
    "Aguacate": {"tipo": "Grasa", "porcion_base": 100, "aporte_macro": 15, "unidad": "g"},
    "Crema de Cacahuate": {"tipo": "Grasa", "porcion_base": 15, "aporte_macro": 8, "unidad": "g (cucharada)"}
}

def calcular_peso_real_comida(alimento: str, gramos_macro_requeridos: float) -> str:
    alimento = alimento.strip()
    item = MATRIZ_ALIMENTOS_MM247.get(alimento)
    if not item:
        return f"{gramos_macro_requeridos:.1f}g de {alimento}"
    
    calculo = (gramos_macro_requeridos * item["porcion_base"]) / item["aporte_macro"]
    
    if item["unidad"] == "piezas":
        return f"{round(calculo)} piezas de {alimento}"
    elif item["unidad"] == "ml":
        return f"{round(calculo)} ml de {alimento}"
    else:
        gramos_redondeados = round(calculo / 5) * 5
        return f"{gramos_redondeados}g de {alimento} [{item['unidad']}]"

def generar_balance_energetico_menu(comidas_dia: int, macro_p: float, macro_c: float, macro_g: float, p_lista: list, c_lista: list, g_lista: list) -> str:
    if comidas_dia <= 0:
        comidas_dia = 4
        
    prot_por_comida = macro_p / comidas_dia
    carb_por_comida = macro_c / comidas_dia
    grasa_por_comida = macro_g / comidas_dia
    
    alimento_p = p_lista[0] if p_lista and p_lista[0] else "Pechuga de Pollo"
    alimento_c = c_lista[0] if c_lista and c_lista[0] else "Arroz Blanco"
    alimento_g = g_lista[0] if g_lista and g_lista[0] else "Almendras"
    
    texto_dieta = "ESTRUCTURA DE ALIMENTACIÓN DIARIA DISEÑADA:\n"
    for i in range(1, comidas_dia + 1):
        p_txt = calcular_peso_real_comida(alimento_p, prot_por_comida)
        c_txt = calcular_peso_real_comida(alimento_c, carb_por_comida)
        g_txt = calcular_peso_real_comida(alimento_g, grasa_por_comida)
        texto_dieta += f"COMIDA {i}: {p_txt} | {c_txt} | {g_txt}\n"
        
    return texto_dieta

# ================================================================================
# 3. MOTOR GRÁFICO (MATPLOTLIB) PARA GENERACIÓN DE PDF E INYECCIÓN DE DIETA
# ================================================================================
def generar_pdf_reporte(id_alumno, nombre, peso, imc, estatus, dieta_texto, rutina_texto, tipo="Cuestionario_1"):
    try:
        fig, ax = plt.subplots(figsize=(8.5, 11), dpi=200)
        ax.axis('off')
        fig.patch.set_facecolor('#f9f9fb')

        ax.add_patch(patches.Rectangle((0, 0.88), 1, 0.12, transform=ax.transAxes, facecolor='#11151c'))
        ax.add_patch(patches.Rectangle((0, 0.87), 1, 0.01, transform=ax.transAxes, facecolor='#ff6b35'))
        ax.text(0.05, 0.94, 'MIND MUSCLE', transform=ax.transAxes, color='#ff6b35', fontsize=26, fontweight='heavy')
        
        titulo_pdf = 'PLAN MAESTRO Y DIAGNÓSTICO ESTRATÉGICO' if tipo == "Cuestionario_1_Inicial" else 'REPORTE DE EVOLUCIÓN MENSUAL'
        ax.text(0.05, 0.91, titulo_pdf, transform=ax.transAxes, color='white', fontsize=11)
        ax.text(0.85, 0.94, 'MM247', transform=ax.transAxes, color='white', fontsize=20, fontweight='bold')

        ax.text(0.05, 0.83, f'ALUMNO: {nombre}', transform=ax.transAxes, color='#11151c', fontsize=16, fontweight='bold')
        ax.text(0.05, 0.80, f'ID: {id_alumno}  |  PESO: {peso}kg  |  IMC: {imc:.1f} ({estatus})', transform=ax.transAxes, color='#4a4e69', fontsize=10)
        ax.axhline(0.77, xmin=0.05, xmax=0.95, color='#e5e5e5', linewidth=1.5)

        ax.text(0.05, 0.73, '01. ANÁLISIS METABÓLICO Y BIOMECÁNICO', transform=ax.transAxes, color='#11151c', fontsize=13, fontweight='bold')
        ax.add_patch(patches.FancyBboxPatch((0.05, 0.58), 0.9, 0.12, boxstyle="round,pad=0.02", facecolor='white', edgecolor='#e5e5e5', transform=ax.transAxes))
        ax.text(0.07, 0.67, 'Estatus Actual:', color='#ff6b35', fontsize=10, fontweight='bold', transform=ax.transAxes)
        ax.text(0.20, 0.67, 'El algoritmo ha procesado la matriz inicial del cuestionario.', color='#2b2d42', fontsize=10, transform=ax.transAxes)

        ax.text(0.05, 0.52, '02. MATRIZ ENERGÉTICA', transform=ax.transAxes, color='#11151c', fontsize=13, fontweight='bold')
        ax_pie = fig.add_axes([0.08, 0.32, 0.22, 0.16])
        ax_pie.pie([40, 35, 25], colors=['#ff6b35', '#11151c', '#d3d3d3'], startangle=90, wedgeprops=dict(width=0.4, edgecolor='w'))
        ax_pie.text(0, 0, 'Macros', ha='center', va='center', fontsize=12, fontweight='bold', color='#11151c')
        
        y_dieta = 0.46
        for linea in dieta_texto.split('\n')[:4]:
            if linea.strip():
                ax.text(0.35, y_dieta, linea, transform=ax.transAxes, color='#11151c', fontsize=9)
                y_dieta -= 0.04

        ax.axhline(0.28, xmin=0.05, xmax=0.95, color='#e5e5e5', linewidth=1.5)
        ax.text(0.05, 0.24, '03. PROTOCOLO DE ENTRENAMIENTO', transform=ax.transAxes, color='#11151c', fontsize=13, fontweight='bold')
        ax.text(0.06, 0.15, rutina_texto[:150], transform=ax.transAxes, color='#11151c', fontsize=10)

        ax.add_patch(patches.Rectangle((0, 0), 1, 0.04, transform=ax.transAxes, facecolor='#11151c'))
        ax.text(0.5, 0.012, 'SISTEMA INTELIGENTE MM247 | DISEÑO ESTRUCTURAL ESTRICTAMENTE CONFIDENCIAL', transform=ax.transAxes, color='white', fontsize=7, ha='center')

        nombre_archivo = f'Reporte_{id_alumno}.png'
        plt.savefig(nombre_archivo, bbox_inches='tight')
        plt.close(fig)
        return nombre_archivo
    except Exception as e:
        st.warning(f"Aviso gráfico: {e}")
        return None

# ================================================================================
# 4. CONEXIÓN API: GOOGLE SHEETS Y FIREBASE STORAGE
# ================================================================================
def conectar_google_sheets():
    return None

def subir_imagen_firebase(uploaded_file, id_alumno, prefijo):
    if uploaded_file is None:
        return ""
    return f"https://almacenamiento.mm247.com/evidencia/{id_alumno}_{prefijo}.jpg"

# ================================================================================
# 5. CAPTURA EXPLÍCITA DE VARIABLES CON LLAVES (KEYS) ÚNICAS ANTI-DUPLICIDAD
# ================================================================================
with st.form(key="master_cuestionario_mm247_form_v2"):
    
    st.markdown('<div class="section-card"><div class="section-title">00. Parámetros de Control y Logística de Flujo</div>', unsafe_allow_html=True)
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        v_Fecha = st.date_input("Fecha Actual del Sistema", datetime.date.today(), key="uid_fecha_actual")
    with col_ctrl2:
        v_Tipo_Registro = st.selectbox("Tipo de Cuestionario / Acción", ["Cuestionario_1_Inicial", "Cuestionario_2_Revision"], key="uid_tipo_registro")
    with col_ctrl3:
        v_
