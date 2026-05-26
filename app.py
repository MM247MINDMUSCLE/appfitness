import streamlit as str
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from fpdf import FPDF
import datetime

# Configuración de página con branding
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide")

# Inicializar conexión a la base de datos (Google Sheets)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Reemplaza por el nombre exacto de tu hoja o pestaña principal
    df_existente = conn.read(worksheet="Respuestas", ttl=0)
except Exception as e:
    st.error("Error de conexión con la base de datos. Verifica los Secrets.")
    df_existente = pd.DataFrame()

# --- ESTILOS VISUALES (Elegante / Dark Metallic vibe) ---
st.markdown("""
    <style>
    .main-title { font-size:42px; font-weight:bold; color:#111111; text-align:center; margin-bottom:5px; }
    .subtitle { font-size:18px; color:#555555; text-align:center; margin-bottom:30px; }
    .stButton>button { background-color: #111111; color: white; width: 100%; border-radius: 5px; }
    .stButton>button:hover { background-color: #333333; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- MENÚ DE NAVEGACIÓN ---
opcion = st.sidebar.selectbox("Seleccione una sección:", ["📝 Cuestionario de Evaluación", "📊 Dashboard Administrador"])

# =============================================================================
# 📝 SECCIÓN 1: CUESTIONARIO DE EVALUACIÓN (CAMPOS OBLIGATORIOS Y OPCIÓN MÚLTIPLE)
# =============================================================================
if opcion == "📝 Cuestionario de Evaluación":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Ficha Clínica y Evaluación Inicial de Fitness</div>", unsafe_allow_html=True)
    
    st.info("📌 Todos los campos son obligatorios para garantizar la exactitud de tus resultados.")
    
    with st.form("cuestionario_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nombre = st.text_input("Nombre Completo:")
            edad = st.number_input("Edad:", min_value=14, max_value=90, step=1)
            genero = st.selectbox("Género:", ["Seleccione...", "Masculino", "Femenino", "Otro"])
            condicion_inicial = st.selectbox("Condición Física Inicial Actual:", [
                "Seleccione...",
                "Sedentario (Sin actividad)",
                "Principiante (Actividad ligera 1-2 días)",
                "Intermedio (Entrena regular 3-4 días)",
                "Avanzado (Entrena pesado 5+ días)"
            ])
            
        with col2:
            meta_cliente = st.selectbox("Objetivo Principal (Meta):", [
                "Seleccione...",
                "Hipertrofia (Ganancia de Masa Muscular)",
                "Pérdida de Grasa / Definición",
                "Acondicionamiento Físico General",
                "Recomposición Corporal"
            ])
            patologias = st.selectbox("¿Sufre de alguna lesión o patología clínica?", [
                "Seleccione...",
                "Ninguna - Sano",
                "Lesión articular (Rodillas/Hombros)",
                "Problemas lumbares / Columna",
                "Hipertensión / Problemas cardiovasculares",
                "Diabetes / Resistencia a la insulina"
            ])
            Frecuencia_entrenamiento = st.selectbox("Días disponibles para entrenar a la semana:", [
                "Seleccione...", "3 días", "4 días", "5 días", "6 días"
            ])
            experiencia_gym = st.selectbox("Experiencia previa en gimnasio:", [
                "Seleccione...", "Ninguna", "Menos de 1 año", "1 a 3 años", "Más de 3 años"
            ])
            
        enviar = st.form_submit_submit_button("Enviar mi Cuestionario")
        
        if enviar:
            # Validación estricta en el Frontend para asegurar que ningún campo quede vacío
            if (not nombre or genero == "Seleccione..." or condicion_inicial == "Seleccione..." or 
                meta_cliente == "Seleccione..." or patologias == "Seleccione..." or 
                Frecuencia_entrenamiento == "Seleccione..." or experiencia_gym == "Seleccione..."):
                st.error("❌ No se pudo enviar. Por favor responde todos los campos obligatorios del cuestionario.")
            else:
                # Mapeo exacto de datos para evitar el rechazo de la base de datos
                nueva_respuesta = pd.DataFrame([{
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nombre": nombre.strip(),
                    "Edad": int(edad),
                    "Género": genero,
                    "Condición Inicial": condicion_inicial,
                    "Meta": meta_cliente,
                    "Patologías/Lesiones": patologias,
                    "Frecuencia Semanal": Frecuencia_entrenamiento,
                    "Experiencia": experiencia_gym,
                    "Observaciones Coach": "",  # Campos vacíos iniciales para el Administrador
                    "Plan Dieta": "",
                    "Plan Rutina": ""
                }])
                
                try:
                    # Combinar filas manteniendo estructura idéntica
                    df_actualizado = pd.concat([df_existente, nueva_respuesta], ignore_index=True)
                    conn.update(worksheet="Respuestas", data=df_actualizado)
                    st.success("✅ ¡Cuestionario enviado con éxito! Tu coach revisará tus datos para armar tu plan personalizado.")
                    st.balloons()
                except Exception as error:
                    st.error(f"❌ Error crítico al guardar en la base de datos: {error}. Reporta esto con el administrador.")

# =============================================================================
# 📊 Dashboard Administrador (PROTEGIDO CON CLAVE)
# =============================================================================
elif opcion == "📊 Dashboard Administrador":
    st.markdown("<div class='main-title'>🔐 Panel de Control</div>", unsafe_allow_html=True)
    
    password = st.text_input("Ingrese la clave de administrador:", type="password")
    if password == "MM247_Admin": # Cambia esta clave por la que gustes
        st.success("Acceso concedido.")
        
        if df_existente.empty or len(df_existente) == 0:
            st.warning("No hay registros de alumnos en la base de datos actualmente.")
        else:
            st.subheader("📋 Gestión Integral de Alumnos")
            st.dataframe(df_existente, use_container_width=True)
            
            st.markdown("---")
            st.subheader("🛠️ Ficha de Evaluación Personalizada & Ajustes")
            
            # Selector de Alumno registrado
            lista_alumnos = df_existente["Nombre"].unique()
            alumno_sel = st.selectbox("Seleccione el alumno a evaluar:", lista_alumnos)
            
            # Extraer datos actuales del alumno seleccionado
            idx_alumno = df_existente[df_existente["Nombre"] == alumno_sel].index[0]
            datos_alumno = df_existente.loc[idx_alumno]
            
            # Mostrar Ficha Clínica inicial capturada
            st.markdown(f"**Condición Inicial:** {datos_alumno['Condición Inicial']} | **Meta:** {datos_alumno['Meta']}")
            
            # Formulario de prescripción del Coach (Basado en la Pirámide Nutricional y Biomecánica)
            with st.form("form_ajustes"):
                st.markdown("### 🥗 1. Balance Energético e Historial Nutricional")
                dieta_propuesta = st.text_area("Establecer dieta diaria y distribución de macronutrientes:", 
                                               value=str(datos_alumno.get("Plan Dieta", "")))
                
                st.markdown("### 🏋️ 2. Prescripción del Entrenamiento (Hipertrofia y Biomecánica)")
                rutina_propuesta = st.text_area("Establecer rutina semanal de Gym y ajustes biomecánicos:", 
                                                value=str(datos_alumno.get("Plan Rutina", "")))
                
                st.markdown("### 📝 3. Propuesta General de Mejora y Observaciones")
                obs_propuestas = st.text_area("Observaciones del Coach:", 
                                              value=str(datos_alumno.get("Observaciones Coach", "")))
                
                guardar_ajustes = st.form_submit_button("💾 Guardar Ajustes del Alumno")
                
                if guardar_ajustes:
                    try:
                        df_existente.at[idx_alumno, "Plan Dieta"] = dieta_propuesta
                        df_existente.at[idx_alumno, "Plan Rutina"] = rutina_propuesta
                        df_existente.at[idx_alumno, "Observaciones Coach"] = obs_propuestas
                        
                        conn.update(worksheet="Respuestas", data=df_existente)
                        st.success(f"Ajustes guardados correctamente para {alumno_sel} en la base de datos.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Error al actualizar los datos: {err}")
            
            # --- GENERADOR DE REPORTE PDF ---
            st.markdown("---")
            st.subheader("📄 Exportación de Reporte de Progreso")
            
            if st.button("🖨️ Generar Reporte PDF Oficial"):
                try:
                    pdf = FPDF()
                    pdf.add_page()
                    
                    # Encabezado / Branding
                    pdf.set_font("Arial", "B", 18)
                    pdf.cell(0, 10, "MINDMUSCLE247 - REPORTE DE EVOLUCIÓN", ln=True, align="C")
                    pdf.set_font("Arial", "I", 10)
                    pdf.cell(0, 10, f"Fecha de Emisión: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True, align="C")
                    pdf.line(10, 30, 200, 30)
                    pdf.ln(10)
                    
                    # Ficha Clínica Inicial
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, f"1. FICHA CLÍNICA: {datos_alumno['Nombre']}", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.cell(0, 7, f"Edad: {datos_alumno['Edad']} años  |  Género: {datos_alumno['Género']}", ln=True)
                    pdf.cell(0, 7, f"Condición Física Inicial: {datos_alumno['Condición Inicial']}", ln=True)
                    pdf.cell(0, 7, f"Meta Establecida: {datos_alumno['Meta']}", ln=True)
                    pdf.cell(0, 7, f"Patologías o Limitaciones: {datos_alumno['Patologías/Lesiones']}", ln=True)
                    pdf.ln(5)
                    
                    # Plan Nutricional
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "2. PROPUESTA DE BALANCE ENERGÉTICO Y DIETA", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 6, str(df_existente.loc[idx_alumno, "Plan Dieta"]))
                    pdf.ln(5)
                    
                    # Plan de Entrenamiento
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "3. PLANIFICACIÓN SEMANAL DE ENTRENAMIENTO (BIOMECÁNICA)", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 6, str(df_existente.loc[idx_alumno, "Plan Rutina"]))
                    pdf.ln(5)
                    
                    # Observaciones
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 10, "4. OBSERVACIONES DE SEGUIMIENTO Y MEJORA PROGRESIVA", ln=True)
                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 6, str(df_existente.loc[idx_alumno, "Observaciones Coach"]))
                    
                    # Descarga del PDF terminado
                    pdf_output = pdf.output(dest='S').encode('latin-1', errors='ignore')
                    st.download_button(
                        label="⬇️ Descargar Ficha PDF",
                        data=pdf_output,
                        file_name=f"Reporte_{alumno_sel.replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as pdf_err:
                    st.error(f"Error al construir el archivo PDF: {pdf_err}")
    
    elif password != "":
        st.error("🔑 Clave incorrecta. Acceso denegado a los reportes de MINDMUSCLE247.")
