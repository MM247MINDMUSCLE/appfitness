import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF
import datetime

# 1. CONFIGURACIÓN DE PÁGINA (BRANDING MM247)
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# 2. CONEXIÓN DIRECTA Y SEGURA A TU GOOGLE SHEET
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Leemos la pestaña principal de datos. ttl=0 evita que guarde respuestas viejas en caché
    df_existente = conn.read(worksheet="Respuestas", ttl=0)
except Exception as e:
    st.error("Error de conexión con Google Sheets. Revisa los Secrets en Streamlit Cloud.")
    df_existente = pd.DataFrame()

# Estilos visuales limpios y profesionales
st.markdown("""
    <style>
    .main-title { font-size:40px; font-weight:bold; color:#111111; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:18px; color:#666666; text-align:center; margin-bottom:30px; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 4px; }
    .stButton>button:hover { background-color: #444444; color: white; }
    </style>
    """, unsafe_allow_html=True)

# Menú lateral para navegar en la App
opcion = st.sidebar.selectbox("Sección de la App:", ["📝 Cuestionario de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# MÓDULO 1: CUESTIONARIO DE EVALUACIÓN (CAMPOS 100% OBLIGATORIOS Y OPCIÓN MÚLTIPLE)
# =============================================================================
if opcion == "📝 Cuestionario de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación Inicial Obligatoria para Resultados Reales y Medibles</div>", unsafe_allow_html=True)
    
    st.info("📌 Para garantizar la máxima exactitud en tu propuesta y balance energético, todos los campos son obligatorios.")
    
    with st.form("cuestionario_mm247", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo del Alumno:")
            edad = st.number_input("Edad Actual:", min_value=12, max_value=90, step=1, value=20)
            genero = st.selectbox("Género Biológico:", ["Seleccione...", "Masculino", "Femenino"])
            condicion_inicial = st.selectbox("Condición Física Inicial Actual:", [
                "Seleccione...",
                "Sedentario (Sin actividad física regular)",
                "Principiante (Actividad ligera o adaptándose)",
                "Intermedio (Entrenamiento constante en gimnasio)",
                "Avanzado (Dominio de cargas y alta intensidad)"
            ])
            
        with col2:
            meta_cliente = st.selectbox("Objetivo Principal de Entrenamiento (Meta):", [
                "Seleccione...",
                "Hipertrofia Muscular Eficiente",
                "Pérdida de Grasa / Definición Estética",
                "Acondicionamiento Físico General Progresivo",
                "Recomposición Corporal (Grasa y Músculo simultáneo)"
            ])
            lesiones = st.selectbox("Historial de Lesiones o Patologías Clínicas:", [
                "Seleccione...",
                "Ninguna (Completamente Sano)",
                "Lesión Articular / Limitación Biomecánica",
                "Molestia Lumbar / Columna",
                "Condición Cardiovascular / Metabolismo controlado"
            ])
            frecuencia = st.selectbox("Disponibilidad Semanal para Entrenar en Gym:", [
                "Seleccione...", "3 Días", "4 Días", "5 Días", "6 Días"
            ])
            experiencia = st.selectbox("Tiempo de Experiencia previa en Gimnasio:", [
                "Seleccione...", "Ninguna", "Menos de 1 año", "1 a 3 años", "Más de 3 años"
            ])
            
        enviar_datos = st.form_submit_button("🚀 Enviar mi Evaluación Inicial")
        
        if enviar_datos:
            # Control estricto de campos vacíos en el Frontend
            if (not nombre.strip() or genero == "Seleccione..." or condicion_inicial == "Seleccione..." or 
                meta_cliente == "Seleccione..." or lesiones == "Seleccione..." or 
                frecuencia == "Seleccione..." or experiencia == "Seleccione..."):
                st.error("❌ Error de envío: Todos los campos del cuestionario son obligatorios para diseñar tu plan.")
            else:
                # Estructura idéntica y limpia para evitar rechazos en el Google Sheet
                nueva_fila = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre.strip(),
                    "Edad": int(edad),
                    "Género": genero,
                    "Condición Inicial": condicion_inicial,
                    "Meta": meta_cliente,
                    "Lesiones/Patologías": lesiones,
                    "Frecuencia Semanal": frecuencia,
                    "Experiencia": experiencia,
                    "Propuesta General": "",      # Columnas destinadas a los ajustes posteriores del Coach
                    "Balance Energético": "",
                    "Rutina Biomecánica": ""
                }])
                
                try:
                    # Combinación matemática perfecta de filas
                    df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
                    conn.update(worksheet="Respuestas", data=df_final)
                    st.success("✅ ¡Evaluación procesada correctamente! Tu información ya está con tu Coach de MINDMUSCLE247.")
                    st.balloons()
                except Exception as err:
                    st.error(f"Error crítico en el motor de base de datos: {err}. Por favor notifica al Coach.")

# =============================================================================
# MÓDULO 2: DASHBOARD ADMINISTRADOR (CON CONTRASEÑA, OBSERVACIONES Y PDF)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel Administrador MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Gestión de Alumnos, Prescripción y Descarga de Fichas Oficiales</div>", unsafe_allow_html=True)
    
    password = st.text_input("Introduzca la clave de acceso de Administrador:", type="password")
    
    # Cambia esta clave por la de tu preferencia personal
    if password == "MM247_Admin":
        st.success("Acceso seguro autorizado.")
        
        if df_existente.empty or len(df_existente) == 0:
            st.warning("Aún no existen registros de alumnos completados en la base de datos.")
        else:
            st.subheader("📋 Base de Datos de Respuestas Recibidas")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🛠️ Evaluación de Alumno y Planificación Técnica")
            
            # Selector dinámico de alumnos únicos en la base de datos
            lista_alumnos = df_existente["Nombre"].unique()
            alumno_sel = st.selectbox("Seleccione el alumno a evaluar en esta sesión:", lista_alumnos)
            
            # Ubicación exacta del alumno seleccionado
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            # Formulario técnico del Administrador para rellenar observaciones
            with st.form("planificacion_coach"):
                st.markdown("### 🥗 1. Propuesta General e Inicios en la Pirámide Nutricional")
                propuesta = st.text_area("Establecer propuesta general de mejora según metas:", 
                                         value=str(datos_alumno.get("Propuesta General", "")))
                
                st.markdown("### 🧮 2. Balance Energético Inicial y Ajuste Saludable Progresivo")
                balance = st.text_area("Cálculo calórico, macronutrientes y pauta alimenticia diaria:", 
                                       value=str(datos_alumno.get("Balance Energético", "")))
                
                st.markdown("### 🏋️ 3. Plan de Entrenamiento Semanal (Biomecánica y Fundamentos de Hipertrofia)")
                rutina = st.text_area("Dosificación de ejercicios semanales basados en mecánica del movimiento y acondicionamiento:", 
                                      value=str(datos_alumno.get("Rutina Biomecánica", "")))
                
                guardar_cambios = st.form_submit_button("💾 Guardar y Actualizar Ficha de Alumno")
                
                if guardar_cambios:
                    try:
                        df_existente.at[idx_alumno, "Propuesta General"] = propuesta
                        df_existente.at[idx_alumno, "Balance Energético"] = balance
                        df_existente.at[idx_alumno, "Rutina Biomecánica"] = rutina
                        
                        conn.update(worksheet="Respuestas", data=df_existente)
                        st.success(f"Datos grabados y sincronizados correctamente en la nube para {alumno_sel}.")
                        st.rerun()
                    except Exception as e_save:
                        st.error(f"Fallo de sincronización: {e_save}")
            
            # GENERACIÓN DEL DOCUMENTO EXPORTABLE EN PDF
            st.markdown("---")
            st.subheader("📄 Exportación de Ficha PDF Oficial")
            
            if st.button("🖨️ Estructurar y Compilar Ficha PDF"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Encabezado Corporativo Minimalista
                    pdf.set_font("Arial", "B", 18)
                    pdf.cell(0, 10, "MINDMUSCLE247", ln=True, align="C")
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "FICHA TÉCNICA PERSONALIZADA DE EVOLUCIÓN", ln=True, align="C")
                    pdf.set_font("Arial", "I", 9)
                    pdf.cell(0, 6, f"Generado el: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True, align="C")
                    pdf.line(10, 36, 200, 36)
                    pdf.ln(12)
                    
                    # Sección 1: Ficha Clínica del Alumno
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, f"1. CONDICIONES INICIALES DEL CLIENTE: {datos_alumno['Nombre']}", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 6, f"Edad: {datos_alumno['Edad']} años | Género: {datos_alumno['Género']} | Frecuencia: {datos_alumno['Frecuencia Semanal']}", ln=True)
                    pdf.cell(0, 6, f"Condición de Partida: {datos_alumno['Condición Inicial']}", ln=True)
                    pdf.cell(0, 6, f"Meta Establecida: {datos_alumno['Meta']}", ln=True)
                    pdf.cell(0, 6, f"Lesiones o Limitaciones Registradas: {datos_alumno['Lesiones/Patologías']}", ln=True)
                    pdf.ln(6)
                    
                    # Sección 2: Propuesta General
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "2. PROPUESTA GENERAL DE MEJORA PROGRESIVA Y SALUDABLE", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Propuesta General"]))
                    pdf.ln(6)
                    
                    # Sección 3: Balance Energético
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "3. BALANCE ENERGÉTICO INICIAL Y AJUSTE DE PIRÁMIDE NUTRICIONAL", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Balance Energético"]))
                    pdf.ln(6)
                    
                    # Sección 4: Rutina de Entrenamiento
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, "4. PLANIFICACIÓN SEMANAL DE GYM (FUNDAMENTOS BIOMECÁNICOS Y HIPERTROFIA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 5, str(df_existente.loc[idx_alumno, "Rutina Biomecánica"]))
                    
                    # Renderizado seguro en memoria y descarga limpia
                    pdf_data = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Guardar Ficha PDF del Alumno",
                        data=pdf_data,
                        file_name=f"Ficha_MM247_{alumno_sel.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as err_pdf:
                    st.error(f"Error técnico durante la compilación del PDF: {err_pdf}")
                    
    elif password != "":
        st.error("🔑 Contraseña incorrecta. Acceso restringido al sistema MINDMUSCLE247.")
