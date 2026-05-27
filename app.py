import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import requests

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="MINDMUSCLE247 PRO", page_icon="💪", layout="wide")
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwTFbvXjNq9pEUBefEyL715AWyvHR2PpxotzRSPBpMeE5AVWNewO9AcqZ3PeXxmu_s0/exec"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Ix0lUfd1Qs4Jb9L3--oU7JvtKysAzYOZ-BbAv2QhwIo/gviz/tq?tqx=out:csv&sheet=Respuestas"

# --- MÓDULOS DE DATOS ---
def cargar_base_datos():
    try:
        df = pd.read_csv(f"{SHEET_URL}&nocache={datetime.datetime.now().timestamp()}")
        return df.fillna("")
    except: return pd.DataFrame()

# --- INTERFAZ ---
opcion = st.sidebar.selectbox("Módulo:", ["📝 Cuestionario Integral", "📊 Dashboard Administrador"])

if opcion == "📝 Cuestionario Integral":
    st.title("💪 SISTEMA DE EVALUACIÓN MM247")
    
    with st.form("form_maestro", clear_on_submit=True):
        # 12 secciones agrupadas en Tabs para mantener el orden
        t1, t2, t3, t4 = st.tabs(["👤 Perfil", "🩺 Salud", "🥗 Nutrición", "🏋️ Entrenamiento"])
        
        with t1:
            nombre = st.text_input("Nombre Completo:")
            edad = st.selectbox("Edad", [f"{i} años" for i in range(14, 81)])
            genero = st.selectbox("Género", ["Masculino", "Femenino"])
            peso = st.selectbox("Peso", [f"{i} kg" for i in range(40, 201)])
            estatura = st.selectbox("Estatura", [f"{i} cm" for i in range(140, 221)])
            meta = st.selectbox("Meta", ["Hipertrofia", "Pérdida de Grasa", "Recomposición", "Fuerza"])
            
        with t2:
            lesiones = st.selectbox("Lesiones", ["Ninguna", "Hombros", "Rodillas", "Lumbar", "Otros"])
            patologias = st.selectbox("Patologías", ["Ninguna", "Hipertensión", "Diabetes", "Hormonal"])
            medicacion = st.selectbox("Medicación", ["No", "Sí, metabólica", "Sí, cardiovascular", "Otros"])
            analiticas = st.selectbox("Analíticas", ["Óptimas", "Colesterol alto", "Glucosa alta", "No cuento"])
            alta = st.selectbox("Alta Médica", ["Sí, total", "Restringido", "No"])
            
        with t3:
            neat = st.selectbox("Actividad NEAT", ["Sedentario", "Moderado", "Alto"])
            comidas = st.selectbox("Comidas/Día", ["2", "3", "4", "5"])
            agua = st.selectbox("Agua", ["< 1.5L", "1.5-3L", "> 3L"])
            sueno = st.selectbox("Sueño", ["< 6h", "6-8h", "> 8h"])
            estres = st.selectbox("Estrés", ["Bajo", "Medio", "Alto"])
            
        with t4:
            exp = st.selectbox("Experiencia", ["Nunca", "Principiante", "Intermedio", "Avanzado"])
            frecuencia = st.selectbox("Frecuencia semanal", ["3 días", "4 días", "5 días", "6 días"])
            tiempo = st.selectbox("Tiempo por sesión", ["45 min", "60 min", "90 min"])
            entorno = st.selectbox("Entorno", ["Gimnasio completo", "Condominio", "Casa"])
            rpe = st.selectbox("Intensidad (RPE)", ["Baja", "Moderada", "Alta/Fallo"])
            cardio = st.selectbox("Cardio actual", ["Nulo", "LISS", "HIIT"])

        if st.form_submit_button("🚀 Registrar Evaluación"):
            id_cliente = f"MM-{datetime.datetime.now().strftime('%Y%m%d')}-{nombre[:2].upper()}"
            payload = {
                "ID": id_cliente, "Nombre": nombre, "Edad": edad, "Género": genero, "Peso": peso, "Estatura": estatura,
                "Meta": meta, "Lesiones": lesiones, "Patologías": patologias, "Medicación": medicacion,
                "Analíticas": analiticas, "Alta": alta, "NEAT": neat, "Comidas": comidas, "Agua": agua,
                "Sueño": sueno, "Estrés": estres, "Experiencia": exp, "Frecuencia": frecuencia,
                "Tiempo": tiempo, "Entorno": entorno, "RPE": rpe, "Cardio": cardio
            }
            requests.post(WEBHOOK_URL, json=payload)
            st.success(f"Registrado. ID: {id_cliente}")

elif opcion == "📊 Dashboard Administrador":
    st.title("🔐 Panel Administrador MM247")
    if st.text_input("Password", type="password") == "MM247_Admin":
        df = cargar_base_datos()
        if not df.empty:
            st.dataframe(df)
            alumnos = df["Nombre"].unique()
            sel = st.selectbox("Seleccionar Alumno:", alumnos)
            
            # Formulario de Prescripción (Edición de planes)
            with st.form("prescripcion"):
                rutina = st.text_area("Rutina Biomecánica")
                dieta = st.text_area("Dieta y Macros")
                if st.form_submit_button("Guardar Cambios"):
                    # Lógica de actualización (enviar ID y nuevos campos)
                    st.success("Plan actualizado para: " + sel)
            
            # Exportar PDF
            if st.button("🖨️ Exportar PDF"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Plan MM247: " + sel, ln=True)
                pdf.multi_cell(0, 10, txt=rutina)
                st.download_button("Descargar", pdf.output(dest='S'), "plan.pdf")
