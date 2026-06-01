import streamlit as st
import pandas as pd
import datetime
import random
import requests
import io
from fpdf import FPDF

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y BASE DE DATOS (MIND MUSCLE)
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247 - ENGINE", page_icon="⚡", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        # SOLUCIÓN AL ERROR DE LA IMAGEN image_8.png (Asegurar que existan las columnas clave)
        if "ID_Alumno" not in df.columns:
            df["ID_Alumno"] = []
        if "Tipo_Registro" not in df.columns:
            df["Tipo_Registro"] = "INICIAL"
            
        return df
    except Exception:
        # Estructura de respaldo si el archivo de Google Sheets está completamente inaccesible o vacío
        return pd.DataFrame(columns=["Fecha", "Tipo_Registro", "ID_Alumno", "Nombre completo", "Sexo", "Edad", "Estatura", "Peso actual", "Peso objetivo", "Objetivo principal"])

df_existente = cargar_base_datos()

# Inyección de interfaz visual
st.markdown("""
    <style>
    body { background-color: #f4f6f9; }
    .main-title { font-size:42px; font-weight:900; background: linear-gradient(45deg, #FF4B4B, #111111); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:13px; color:#555555; text-align:center; margin-bottom:30px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;}
    .section-header { font-size:20px; font-weight:bold; color:#ffffff; background: linear-gradient(90deg, #111111, #FF4B4B); padding: 8px 12px; border-radius: 6px; margin-top:20px; margin-bottom:12px; }
    .id-box { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 6px; font-size: 18px; color: #1B5E20; font-weight: bold; margin: 15px 0; text-align: center; }
    
    .avatar-container { background: linear-gradient(135deg, #111111, #2c3e50); padding: 25px; border-radius: 16px; color: white; display: flex; align-items: center; gap: 25px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
    .avatar-circle { width: 85px; height: 85px; background: linear-gradient(45deg, #FF4B4B, #FF8585); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 38px; border: 4px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Módulos de Control MM247:", [
    "📝 Cuestionario 1: Evaluación Inicial", 
    "🔄 Cuestionario 2: Registro de Avances Semanales", 
    "📊 Dashboard Administrador (Vista Exclusiva)"
])

def generar_id_unico(nombre):
    partes = nombre.strip().split()
    iniciales = "".join([p[0].upper() for p in partes if p])[:3]
    if not iniciales: iniciales = "MM"
    numero = random.randint(1000, 9999)
    return f"MM-{iniciales}-{numero}"

# =============================================================================
# MÓDULO 1: CUESTIONARIO 1 - REGISTRO E ID AUTOMÁTICO + IMPRESIÓN INICIAL
# =============================================================================
if opcion == "📝 Cuestionario 1: Evaluación Inicial":
    st.markdown("<div class='main-title'>MIND MUSCLE 247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Formulario de Alta e Identidad Biomecánica</div>", unsafe_allow_html=True)
    
    with st.form("form_alta_inicial", clear_on_submit=False):
        st.markdown("<div class='section-header'>Datos Clínicos de Inicio</div>", unsafe_allow_html=True)
        f_nombre = st.text_input("Nombre Completo del Alumno:")
        
        col1, col2, col3 = st.columns(3)
        with col1: f_edad = st.selectbox("Edad Actual:", [f"{i} años" for i in range(14, 80)], index=11)
        with col2: f_sexo = st.selectbox("Sexo Biológico:", ["Masculino", "Femenino"])
        with col3: f_estatura = st.selectbox("Estatura Base:", [f"{i} cm" for i in range(120, 220)], index=55)
        
        col4, col5, col6 = st.columns(3)
        with col4: f_peso_inicial = st.number_input("Peso Actual de Inicio (kg):", min_value=40.0, max_value=160.0, value=75.0, step=0.1)
        with col5: f_peso_meta = st.number_input("Peso Objetivo / Meta (kg):", min_value=40.0, max_value=160.0, value=70.0, step=0.1)
        with col6: f_objetivo = st.selectbox("Estrategia Principal:", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal"])
        
        f_lesion = st.selectbox("¿Presenta alguna lesión o dolor limitante?", ["Ninguna", "Rodilla / Desgaste / Tendinitis", "Hombro / Manguito rotador", "Espalda Baja / Lumbalgia"])
        f_dias = st.selectbox("Días disponibles para entrenar por semana:", ["3 días por semana", "4 días por semana", "5 días por semana"])
        
        enviar_alta = st.form_submit_button("🚀 FINALIZAR EVALUACIÓN Y GENERAR ID")
        
        if enviar_alta:
            if not f_nombre.strip():
                st.error("❌ El campo de nombre es mandatorio para generar el expediente corporativo.")
            else:
                nuevo_id = generar_id_unico(f_nombre)
                st.session_state["ultimo_id_generado"] = nuevo_id
                st.session_state["datos_ultimo_registro"] = {
                    "Nombre": f_nombre.strip().upper(), "Edad": f_edad, "Sexo": f_sexo, "Estatura": f_estatura,
                    "Peso": f_peso_inicial, "Meta": f_peso_meta, "Objetivo": f_objetivo, "Lesion": f_lesion, "Dias": f_dias
                }
                
                payload_inicial = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "INICIAL", "ID_Alumno": nuevo_id,
                    "Nombre completo": str(f_nombre.strip().upper()), "Edad": str(f_edad), "Sexo": str(f_sexo), "Estatura": str(f_estatura),
                    "Peso actual": str(f_peso_inicial), "Peso objetivo": str(f_peso_meta), "Objetivo principal": str(f_objetivo),
                    "Días entrenar": str(f_dias), "Lesión actual": str(f_lesion)
                }
                try:
                    requests.post(WEBHOOK_URL, json=payload_inicial)
                    st.markdown(f"""
                    <div class='id-box'>
                        💎 ALTA PROCESADA EXITOSAMENTE<br>
                        <span style='font-size: 26px; color: #2E7D32;'>ID ÚNICO ASIGNADO: {nuevo_id}</span>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error al subir a la base de datos central: {e}")

    # Impresión inmediata de su PDF Inicial con ID impreso
    if "ultimo_id_generado" in st.session_state:
        st.markdown("### 📥 Descarga tu Ficha Oficial de Ingreso")
        d = st.session_state["datos_ultimo_registro"]
        id_gen = st.session_state["ultimo_id_generado"]
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(190, 10, "MIND MUSCLE 247 - FICHA DE REGISTRO INICIAL", 0, 1, "C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(190, 8, f"ID COMPLETO DEL ALUMNO: {id_gen}", 1, 1, "C")
        pdf.ln(5)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(190, 7, f"Nombre Completo: {d['Nombre']}", 0, 1)
        pdf.cell(190, 7, f"Edad: {d['Edad']} | Sexo: {d['Sexo']} | Estatura: {d['Estatura']}", 0, 1)
        pdf.cell(190, 7, f"Peso de Inicio: {d['Peso']} kg | Peso Objetivo: {d['Meta']} kg", 0, 1)
        pdf.cell(190, 7, f"Estrategia Seleccionada: {d['Objetivo']}", 0, 1)
        pdf.cell(190, 7, f"Frecuencia de Entrenamiento: {d['Dias']}", 0, 1)
        pdf.cell(190, 7, f"Limitaciones por Lesión: {d['Lesion']}", 0, 1)
        
        pdf_bytes = pdf.output(dest='S').encode('latin1', errors='ignore')
        st.download_button(label="📥 IMPRIMIR REPORTE INICIAL DEL ALUMNO (PDF)", data=pdf_bytes, file_name=f"Ingreso_MM_{id_gen}.pdf", mime="application/pdf")

# =============================================================================
# MÓDULO 2: CUESTIONARIO 2 - AVANCES (CIÉGO PARA EL ALUMNO)
# =============================================================================
elif opcion == "🔄 Cuestionario 2: Registro de Avances Semanales":
    st.markdown("<div class='main-title'>BITÁCORA DE EVOLUCIÓN MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Cuestionario Integral de Progreso Semanal</div>", unsafe_allow_html=True)
    
    with st.form("form_registro_avances", clear_on_submit=True):
        st.markdown("<div class='section-header'>Identificación Requerida</div>", unsafe_allow_html=True)
        r_id = st.text_input("Ingresa tu ID de Alumno Asignado (Ej: MM-JDO-2934):").strip().upper()
        
        st.markdown("<div class='section-header'>Métricas Semanales de Control</div>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1: r_peso_hoy = st.number_input("Peso en ayunas hoy (kg):", min_value=30.0, max_value=180.0, value=75.0, step=0.1)
        with col_r2: r_cintura = st.number_input("Medida de contorno de cintura (cm):", min_value=40.0, max_value=150.0, value=80.0, step=0.5)
        
        r_adherencia = st.selectbox("Cumplimiento real de la alimentación asignada:", ["100% al 90%", "90% al 70%", "Menos del 70%"])
        r_fuerza = st.selectbox("Progreso general en las cargas de fuerza:", ["Aumenté cargas/reps (Sobrecarga progresiva)", "Estable en los mismos pesos", "Fatiga alta / Bajaron mis pesos"])
        r_sueno = st.slider("Calidad de sueño y descanso neuromuscular (1 al 10):", 1, 10, 8)
        r_comentarios = st.text_area("Comentarios o sensaciones físicas:")
        
        enviar_revision = st.form_submit_button("⚡ ENVIAR REVISIÓN DE PROGRESO")
        
        if enviar_revision:
            if not r_id:
                st.error("❌ Es mandatorio colocar tu ID Único para sincronizar este avance.")
            else:
                payload_revision = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "REVISION", "ID_Alumno": r_id,
                    "Peso_Revision": str(r_peso_hoy), "Cintura_Revision": str(r_cintura), "Adherencia_Dieta": str(r_adherencia),
                    "Progreso_Fuerza": str(r_fuerza), "Energia_SNC": str(r_sueno), "Comentarios_Evolucion": str(r_comentarios)
                }
                try:
                    requests.post(WEBHOOK_URL, json=payload_revision)
                    st.success("✅ Evolución registrada. Tu Coach analizará las proyecciones desde su Panel.")
                except Exception as e:
                    st.error(f"Error de red: {e}")

# =============================================================================
# MÓDULO 3: DASHBOARD ADMINISTRADOR DINÁMICO E IMPRESIONES BAJO DEMANDA
# =============================================================================
elif opcion == "📊 Dashboard Administrador (Vista Exclusiva)":
    st.markdown("<div class='main-title'>📊 CONTROL DE COMUNIDAD MM247</div>", unsafe_allow_html=True)
    pass_master = st.text_input("Clave de Acceso Profesional del Coach:", type="password")
    
    if pass_master == "MM247_Admin":
        if df_existente.empty or len(df_existente["ID_Alumno"].dropna().unique()) == 0:
            st.info("No se registran alumnos con ID en el ecosistema actual.")
        else:
            df_iniciales = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
            df_revisiones = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
            
            ids_activos = df_existente["ID_Alumno"].dropna().unique()
            
            st.markdown("### 🔍 Análisis Cruzado de Avance por ID de Alumno")
            id_coach_sel = st.selectbox("Selecciona el ID Único del Alumno:", ids_activos)
            
            perfil_data = df_iniciales[df_iniciales["ID_Alumno"] == id_coach_sel]
            
            if not perfil_data.empty:
                row_perfil = perfil_data.iloc[0]
                alumno_nombre = str(row_perfil.get("Nombre completo", "ALUMNO")).title()
                sexo_alumno = row_perfil.get("Sexo", "Masculino")
                avatar_select = "🏋️‍♂️" if "Masculino" in sexo_alumno else "🏋️‍♀️"
                
                st.markdown(f"""
                <div class='avatar-container'>
                    <div class='avatar-circle'>{avatar_select}</div>
                    <div>
                        <h2 style='margin:0; font-size:26px;'>{alumno_nombre}</h2>
                        <p style='margin:4px 0 0 0; opacity:0.9;'><b>ID del Expediente:</b> {id_coach_sel} | <b>Estrategia Base:</b> {row_perfil.get('Objetivo principal', 'Mantenimiento')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Cómputo Comparativo
                try: peso_c1 = float(str(row_perfil.get("Peso actual", "80")))
                except: peso_c1 = 80.0
                try: peso_meta_c1 = float(str(row_perfil.get("Peso objetivo", "70")))
                except: peso_meta_c1 = 70.0
                
                fechas_historicas = [pd.to_datetime(row_perfil["Fecha"]).strftime("%d/%m/%Y")]
                pesos_historicos = [peso_c1]
                
                revisiones_filtradas = df_revisiones[df_revisiones["ID_Alumno"] == id_coach_sel].copy()
                if not revisiones_filtradas.empty:
                    revisiones_filtradas["Fecha_DT"] = pd.to_datetime(revisiones_filtradas["Fecha"])
                    revisiones_filtradas = revisiones_filtradas.sort_values(by="Fecha_DT")
                    for _, row_r in revisiones_filtradas.iterrows():
                        try:
                            pesos_historicos.append(float(row_r["Peso_Revision"]))
                            fechas_historicas.append(pd.to_datetime(row_r["Fecha"]).strftime("%d/%m/%Y"))
                        except: pass
                
                st.markdown("<br>#### 📉 Métricas e Historial del Alumno", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                peso_actual_real = pesos_historicos[-1]
                cambio_total = round(peso_actual_real - peso_c1, 2)
                
                with m1: st.metric("Peso Inicial (Cuestionario 1)", f"{peso_c1} kg")
                with m2: st.metric("Peso en Revisión Actual", f"{peso_actual_real} kg", delta=f"{cambio_total} kg")
                with m3: st.metric("Meta de Peso", f"{peso_meta_c1} kg")
                
                chart_progreso = pd.DataFrame({"Fecha": fechas_historicas, "Peso (kg)": pesos_historicos}).set_index("Fecha")
                st.line_chart(chart_progreso, color="#FF4B4B")
                
                if not revisiones_filtradas.empty:
                    tabla_analisis = revisiones_filtradas[["Fecha", "Peso_Revision", "Cintura_Revision", "Adherencia_Dieta", "Progreso_Fuerza", "Energia_SNC", "Comentarios_Evolucion"]].copy()
                    st.dataframe(tabla_analisis, use_container_width=True)
                
                # =============================================================================
                # OPCIÓN ADMINISTRATIVA: DOS BOTONES INDEPENDIENTES PARA IMPRESIÓN PDF
                # =============================================================================
                st.markdown("---")
                st.markdown("### 🖨️ Centro de Impresión y Descarga de Reportes (Exclusivo Coach)")
                
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    # REPORTE 1: REPORTE INICIAL INDIVIDUAL
                    pdf_ini = FPDF()
                    pdf_ini.add_page()
                    pdf_ini.set_font("Helvetica", "B", 16)
                    pdf_ini.cell(190, 10, "MIND MUSCLE 247 - EXPEDIENTE DE EVALUACION INICIAL", 0, 1, "C")
                    pdf_ini.ln(5)
                    pdf_ini.set_font("Helvetica", "B", 12)
                    pdf_ini.cell(190, 8, f"ID UNICO: {id_coach_sel}", 1, 1, "C")
                    pdf_ini.set_font("Helvetica", "", 11)
                    pdf_ini.ln(4)
                    pdf_ini.cell(190, 7, f"Nombre Completo: {alumno_nombre}", 0, 1)
                    pdf_ini.cell(190, 7, f"Edad: {row_perfil.get('Edad', 'N/A')} | Sexo: {sexo_alumno}", 0, 1)
                    pdf_ini.cell(190, 7, f"Estatura Registrada: {row_perfil.get('Estatura', 'N/A')}", 0, 1)
                    pdf_ini.cell(190, 7, f"Peso de Inicio: {peso_c1} kg | Peso Meta: {peso_meta_c1} kg", 0, 1)
                    pdf_ini.cell(190, 7, f"Objetivo Principal: {row_perfil.get('Objetivo principal', 'N/A')}", 0, 1)
                    pdf_ini.cell(190, 7, f"Frecuencia Semanal: {row_perfil.get('Días entrenar', 'N/A')}", 0, 1)
                    pdf_ini.cell(190, 7, f"Zonas de Lesión Reportadas: {row_perfil.get('Lesión actual', 'Ninguna')}", 0, 1)
                    
                    bytes_ini = pdf_ini.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button(label="📥 IMPRIMIR REPORTE INICIAL INDIVIDUAL", data=bytes_ini, file_name=f"Reporte_Inicial_{id_coach_sel}.pdf", mime="application/pdf")
                
                with col_btn2:
                    # REPORTE 2: REPORTE DE AVANCE CRONOLÓGICO INDIVIDUAL
                    pdf_av = FPDF()
                    pdf_av.add_page()
                    pdf_av.set_font("Helvetica", "B", 16)
                    pdf_av.cell(190, 10, "MIND MUSCLE 247 - BITACORA CRONOLOGICA DE AVANCE", 0, 1, "C")
                    pdf_av.ln(5)
                    pdf_av.set_font("Helvetica", "B", 12)
                    pdf_av.cell(190, 8, f"Monitoreo de Avance para ID: {id_coach_sel}", 1, 1, "C")
                    pdf_av.set_font("Helvetica", "", 11)
                    pdf_av.ln(4)
                    pdf_av.cell(190, 7, f"Alumno: {alumno_nombre}", 0, 1)
                    pdf_av.cell(190, 7, f"Evolucion del Peso Corporal:", 0, 1)
                    for f, p in zip(fechas_historicas, pesos_historicos):
                        pdf_av.cell(190, 6, f" -> Fecha: {f}   |   Peso registrado: {p} kg", 0, 1)
                    
                    if not revisiones_filtradas.empty:
                        pdf_av.ln(5)
                        pdf_av.set_font("Helvetica", "B", 12)
                        pdf_av.cell(190, 8, "Ultimas Bitacoras Completas de Rendimiento:", 0, 1)
                        pdf_av.set_font("Helvetica", "", 10)
                        for _, r in revisiones_filtradas.tail(3).iterrows():
                            pdf_av.cell(190, 6, f"Fecha: {r['Fecha']} | Peso: {r['Peso_Revision']}kg | Cintura: {r['Cintura_Revision']}cm", 0, 1)
                            pdf_av.cell(190, 6, f"   Adherencia Dieta: {r['Adherencia_Dieta']} | Fuerza: {r['Progreso_Fuerza']}", 0, 1)
                            pdf_av.ln(2)
                            
                    bytes_av = pdf_av.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button(label="📥 IMPRIMIR REPORTE DE AVANCE INDIVIDUAL", data=bytes_av, file_name=f"Reporte_Avances_{id_coach_sel}.pdf", mime="application/pdf")
            else:
                st.error("El ID seleccionado no tiene ficha de alta inicial.")
                
    elif pass_master != "": 
        st.error("🔑 Código de Coach inválido.")
