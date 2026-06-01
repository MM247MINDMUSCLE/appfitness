import streamlit as st
import pandas as pd
import datetime
import random
import requests
from fpdf import FPDF

# =============================================================================
# 1. CONFIGURACIÓN BASE Y CONEXIÓN
# =============================================================================
st.set_page_config(page_title="MINDMUSCLE247", page_icon="⚡", layout="wide")

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

def cargar_base_datos():
    try:
        url_fresca = f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}"
        df = pd.read_csv(url_fresca)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        
        # Evita el error KeyError en el Dashboard si la hoja está limpia
        if "ID_Alumno" not in df.columns: df["ID_Alumno"] = []
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = []
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Estilos limpios
st.markdown("""
    <style>
    .main-title { font-size:36px; font-weight:900; color: #111; text-align:center; }
    .section-header { font-size:18px; font-weight:bold; color:#fff; background: #111; padding: 8px 12px; border-radius: 4px; margin-top:20px; margin-bottom:12px; }
    .id-box { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 4px; font-size: 18px; color: #1B5E20; text-align: center; margin: 15px 0;}
    .avatar-circle { width: 70px; height: 70px; background: #111; color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Selecciona el Módulo:", [
    "📝 Cuestionario 1: Evaluación Inicial", 
    "🔄 Cuestionario 2: Revisión de Avance", 
    "📊 Panel Admin (Dashboard)"
])

def generar_id(nombre):
    iniciales = "".join([p[0].upper() for p in nombre.strip().split() if p])[:3]
    if not iniciales: iniciales = "MM"
    return f"MM-{iniciales}-{random.randint(1000, 9999)}"

# =============================================================================
# MÓDULO 1: CUESTIONARIO 1 (EVALUACIÓN ORIGINAL + GENERACIÓN DE ID)
# =============================================================================
if opcion == "📝 Cuestionario 1: Evaluación Inicial":
    st.markdown("<div class='main-title'>CUESTIONARIO 1: ALTA DE ALUMNO</div>", unsafe_allow_html=True)
    
    with st.form("form_c1"):
        st.markdown("<div class='section-header'>Datos Personales y Físicos</div>", unsafe_allow_html=True)
        nombre = st.text_input("Nombre Completo:")
        
        c1, c2, c3 = st.columns(3)
        with c1: edad = st.number_input("Edad:", min_value=12, max_value=90, value=25)
        with c2: sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
        with c3: estatura = st.number_input("Estatura (cm):", min_value=100, max_value=230, value=170)
        
        c4, c5, c6 = st.columns(3)
        with c4: peso_actual = st.number_input("Peso Actual (kg):", min_value=30.0, value=75.0, step=0.1)
        with c5: peso_meta = st.number_input("Peso Meta (kg):", min_value=30.0, value=70.0, step=0.1)
        with c6: objetivo = st.selectbox("Objetivo:", ["Perder grasa", "Ganar masa muscular", "Recomposición"])
        
        lesion = st.selectbox("Lesiones:", ["Ninguna", "Rodilla", "Hombro", "Espalda"])
        dias = st.selectbox("Días de entrenamiento:", ["3 días", "4 días", "5 días"])
        
        submit_c1 = st.form_submit_button("Guardar Evaluación y Generar ID")

    if submit_c1 and nombre:
        # Lógica exacta solicitada: 2g Proteína, 1g Grasa
        prot = round(peso_actual * 2.0, 1)
        grasa = round(peso_actual * 1.0, 1)
        
        nuevo_id = generar_id(nombre)
        st.session_state["ultimo_id"] = nuevo_id
        st.session_state["datos_c1"] = {"nombre": nombre, "peso": peso_actual, "meta": peso_meta, "prot": prot, "grasa": grasa}
        
        payload_c1 = {
            "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "INICIAL", "ID_Alumno": nuevo_id,
            "Nombre completo": nombre, "Edad": edad, "Sexo": sexo, "Estatura": estatura,
            "Peso actual": peso_actual, "Peso objetivo": peso_meta, "Objetivo principal": objetivo,
            "Días entrenar": dias, "Lesión actual": lesion, "Proteina_g": prot, "Grasa_g": grasa
        }
        
        try:
            requests.post(WEBHOOK_URL, json=payload_c1)
            st.markdown(f"<div class='id-box'>✅ Registro exitoso. Tu ID de Alumno es: <b>{nuevo_id}</b></div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al guardar: {e}")

    # Opción de imprimir el Cuestionario 1 inmediatamente
    if "ultimo_id" in st.session_state:
        id_gen = st.session_state["ultimo_id"]
        d = st.session_state["datos_c1"]
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(190, 10, "REPORTE INICIAL MM247", 0, 1, "C")
        pdf.set_font("Helvetica", "", 12)
        pdf.cell(190, 10, f"ID de Alumno: {id_gen}", 0, 1)
        pdf.cell(190, 10, f"Nombre: {d['nombre']}", 0, 1)
        pdf.cell(190, 10, f"Peso Inicial: {d['peso']} kg | Meta: {d['meta']} kg", 0, 1)
        pdf.cell(190, 10, f"Macros Asignados -> Proteina: {d['prot']}g | Grasa: {d['grasa']}g", 0, 1)
        
        pdf_b = pdf.output(dest='S').encode('latin1', errors='ignore')
        st.download_button("📥 Descargar Reporte Inicial (PDF)", data=pdf_b, file_name=f"Inicial_{id_gen}.pdf", mime="application/pdf")

# =============================================================================
# MÓDULO 2: CUESTIONARIO 2 (REVISIÓN CON ID, RESULTADOS OCULTOS AL CLIENTE)
# =============================================================================
elif opcion == "🔄 Cuestionario 2: Revisión de Avance":
    st.markdown("<div class='main-title'>CUESTIONARIO 2: REVISIÓN</div>", unsafe_allow_html=True)
    
    with st.form("form_c2", clear_on_submit=True):
        st.markdown("<div class='section-header'>Ingresa tu ID para registrar tu avance</div>", unsafe_allow_html=True)
        id_ingresado = st.text_input("ID de Alumno (Ej: MM-JDO-1234):").strip().upper()
        
        col1, col2 = st.columns(2)
        with col1: peso_rev = st.number_input("Peso actual (kg):", min_value=30.0, value=75.0, step=0.1)
        with col2: cintura = st.number_input("Cintura (cm):", min_value=40.0, value=80.0, step=0.5)
        
        adherencia = st.selectbox("Adherencia a la dieta:", ["100% - 90%", "89% - 70%", "Menos de 70%"])
        fuerza = st.selectbox("Progresión de fuerza:", ["Subí pesos/reps", "Mantuve pesos", "Bajé pesos"])
        sueno = st.slider("Calidad de sueño (1-10):", 1, 10, 8)
        comentarios = st.text_area("Comentarios o dudas adicionales:")
        
        submit_c2 = st.form_submit_button("Enviar Revisión")
        
        if submit_c2:
            if not id_ingresado:
                st.error("Debes ingresar tu ID.")
            else:
                payload_c2 = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "REVISION", "ID_Alumno": id_ingresado,
                    "Peso_Revision": str(peso_rev), "Cintura_Revision": str(cintura), "Adherencia_Dieta": adherencia,
                    "Progreso_Fuerza": fuerza, "Energia_SNC": str(sueno), "Comentarios_Evolucion": comentarios
                }
                try:
                    requests.post(WEBHOOK_URL, json=payload_c2)
                    # El cliente NO ve resultados, solo confirmación.
                    st.success("✅ Tus datos de revisión fueron enviados al Coach exitosamente.")
                except Exception as e:
                    st.error("Error al enviar.")

# =============================================================================
# MÓDULO 3: PANEL ADMIN (CRUCE DE DATOS EXACTO E IMPRESIONES)
# =============================================================================
elif opcion == "📊 Panel Admin (Dashboard)":
    st.markdown("<div class='main-title'>DASHBOARD ADMINISTRADOR</div>", unsafe_allow_html=True)
    passw = st.text_input("Clave Admin:", type="password")
    
    if passw == "MM247_Admin":
        if df_existente.empty or "ID_Alumno" not in df_existente.columns:
            st.info("No hay datos registrados aún.")
        else:
            df_c1 = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
            df_c2 = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
            
            ids_disponibles = df_existente["ID_Alumno"].replace("", pd.NA).dropna().unique()
            id_sel = st.selectbox("Selecciona ID de Alumno:", ids_disponibles)
            
            perfil = df_c1[df_c1["ID_Alumno"] == id_sel]
            
            if not perfil.empty:
                row = perfil.iloc[0]
                nombre = str(row.get("Nombre completo", "ALUMNO"))
                peso_base = float(row.get("Peso actual", 0))
                
                # Render Avatar Dinámico
                st.markdown(f"""
                <div style='display:flex; align-items:center; gap:20px; background:#fff; padding:15px; border-radius:8px; border: 1px solid #ddd;'>
                    <div class='avatar-circle'>{"🏋️" if row.get("Sexo") == "Masculino" else "🧘"}</div>
                    <div>
                        <h2 style='margin:0;'>{nombre.title()}</h2>
                        <p style='margin:0;'><b>ID:</b> {id_sel} | <b>Objetivo:</b> {row.get('Objetivo principal')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Cruce exacto por fecha
                fechas = [pd.to_datetime(row["Fecha"]).strftime("%Y-%m-%d")]
                pesos = [peso_base]
                
                avances_alumno = df_c2[df_c2["ID_Alumno"] == id_sel].copy()
                if not avances_alumno.empty:
                    avances_alumno["Fecha_DT"] = pd.to_datetime(avances_alumno["Fecha"])
                    avances_alumno = avances_alumno.sort_values(by="Fecha_DT")
                    for _, rev in avances_alumno.iterrows():
                        try:
                            pesos.append(float(rev["Peso_Revision"]))
                            fechas.append(pd.to_datetime(rev["Fecha"]).strftime("%Y-%m-%d"))
                        except: pass
                
                st.markdown("### Comparativo de Avance")
                chart_df = pd.DataFrame({"Fecha": fechas, "Peso": pesos}).set_index("Fecha")
                st.line_chart(chart_df)
                
                st.markdown("### Respuestas Exactas del Cuestionario 2")
                if not avances_alumno.empty:
                    tabla = avances_alumno[["Fecha", "Peso_Revision", "Cintura_Revision", "Adherencia_Dieta", "Progreso_Fuerza", "Comentarios_Evolucion"]]
                    st.dataframe(tabla, use_container_width=True)
                else:
                    st.write("Aún no hay revisiones de este alumno.")
                
                # Botones de Impresión
                st.markdown("---")
                col_btn1, col_btn2 = st.columns(2)
                
                with col_btn1:
                    pdf_i = FPDF()
                    pdf_i.add_page()
                    pdf_i.set_font("Helvetica", "B", 14)
                    pdf_i.cell(190, 10, f"REPORTE CUESTIONARIO 1 - {id_sel}", 0, 1)
                    pdf_i.set_font("Helvetica", "", 12)
                    pdf_i.cell(190, 8, f"Nombre: {nombre}", 0, 1)
                    pdf_i.cell(190, 8, f"Peso Inicial: {peso_base} kg | Meta: {row.get('Peso objetivo')} kg", 0, 1)
                    b1 = pdf_i.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button("🖨️ Imprimir Cuestionario 1", data=b1, file_name=f"C1_{id_sel}.pdf", mime="application/pdf")
                    
                with col_btn2:
                    pdf_a = FPDF()
                    pdf_a.add_page()
                    pdf_a.set_font("Helvetica", "B", 14)
                    pdf_a.cell(190, 10, f"REPORTE CUESTIONARIO 2 (AVANCES) - {id_sel}", 0, 1)
                    pdf_a.set_font("Helvetica", "", 12)
                    for f, p in zip(fechas, pesos):
                        pdf_a.cell(190, 8, f"Fecha: {f} -> Peso: {p} kg", 0, 1)
                    b2 = pdf_a.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button("🖨️ Imprimir Avances (C2)", data=b2, file_name=f"C2_{id_sel}.pdf", mime="application/pdf")
            else:
                st.warning("No se encontró el Cuestionario 1 para este ID.")
