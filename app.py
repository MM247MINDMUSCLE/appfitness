import streamlit as st
from fpdf import FPDF
import pandas as pd
import datetime
import os

# CONTRASEÑA DEL COACH
PASSWORD_COACH = "MM247"
ARCHIVO_DATOS = "registro_clientes.csv"

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA CON ESTÉTICA PREMIUM DARK (MIND MUSCLE)
# ==============================================================================
st.set_page_config(page_title="MIND MUSCLE - Plataforma de Coaching", page_icon="🏋️‍♂️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0b0d; color: #e1e1e6; }
    h1, h2, h3, h4 { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 800; letter-spacing: -0.5px; }
    h1 { color: #ffffff !important; border-bottom: 2px solid #202024; padding-bottom: 10px; }
    h2 { color: #ffffff !important; margin-top: 20px !important; }
    h3 { color: #ffffff !important; border-left: 4px solid #ffffff; padding-left: 10px; }
    
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stMultiSelect>div>div {
        background-color: #121214 !important; color: #ffffff !important; border: 1px solid #29292e !important; border-radius: 6px !important;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #121214; border: 1px solid #29292e; padding: 10px 16px; border-radius: 6px; color: #a8a8b3; font-weight: 600;
    }
    .stTabs [data-baseweb="tab"]:hover { color: #ffffff; border-color: #48484a; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #ffffff; color: #000000 !important; font-weight: 800; border-color: #ffffff; }

    .stInfo { background-color: #121214 !important; border-left: 4px solid #ffffff !important; color: #e1e1e6 !important; border-top: 0; border-right: 0; border-bottom: 0; }
    
    .stButton>button { 
        background: linear-gradient(135deg, #ffffff 0%, #e1e1e6 100%); color: #000000; font-weight: 800; text-transform: uppercase;
        letter-spacing: 1px; border: none; border-radius: 6px; width: 100%; height: 55px; transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(255,255,255,0.1); margin-top: 20px;
    }
    .stButton>button:hover { background: #cccccc; transform: translateY(-2px); }
    
    .stDownloadButton>button {
        background: linear-gradient(135deg, #202024 0%, #121214 100%) !important; color: #ffffff !important;
        border: 1px solid #323238 !important; font-weight: 700 !important; border-radius: 6px !important; width: 100% !important; height: 52px !important; text-transform: uppercase;
    }
    .stDownloadButton>button:hover { background: #29292e !important; border-color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# Barra lateral
st.sidebar.title("🛡️ Panel de Control Coach")
url_app = st.sidebar.text_input("Enlace de tu App (Streamlit Cloud):", placeholder="Pega aquí la URL de tu app para crear el QR")
if url_app:
    st.sidebar.subheader("📱 Código QR para Clientes")
    qr_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={url_app}"
    st.sidebar.image(qr_api, caption="Hazle captura a este QR y envíaselo a tus clientes")

st.sidebar.markdown("---")
acceso_coach = st.sidebar.text_input("Clave de Acceso (Coach):", type="password")
es_coach = acceso_coach == PASSWORD_COACH

if es_coach:
    st.sidebar.success("🔑 Modo Coach Activado")
else:
    if acceso_coach:
        st.sidebar.error("❌ Contraseña incorrecta")

if es_coach:
    st.title("SISTEMA DE DIAGNÓSTICO MM - VISTA DEL COACH")
else:
    st.title("SISTEMA DE DIAGNÓSTICO INTEGRAL - MIND MUSCLE")
    st.write("Por favor, rellena detalladamente cada una de las pestañas del cuestionario.")

st.markdown("---")

# Pestañas del Cuestionario
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "1. Info General", "2. Experiencia", "3. Historial Médico", 
    "4. Biomecánica", "5. Rendimiento", "6. Estilo de Vida", 
    "7. Logística & Gustos", "8. Evaluación Visual"
])

with tab1:
    st.header("1. Información General y Objetivos")
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre Completo:")
        edad = st.number_input("Edad (años):", min_value=12, max_value=90, value=25)
        genero = st.selectbox("Sexo / Género:", ["Masculino", "Femenino"])
        estatura_cm = st.number_input("Estatura (cm):", min_value=100, max_value=250, value=170)
        peso = st.number_input("Peso Actual (kg):", min_value=30.0, max_value=200.0, value=70.0, step=0.1)
    with col2:
        ocupacion = st.text_input("Ocupación / Trabajo:", value="Empleado de oficina")
        horas_sentado = st.selectbox("¿Cuántas horas pasas sentado al día?", ["0 a 3 horas", "3 a 6 horas", "6 a 9 horas", "Más de 9 horas"])
        actividad_fuera = st.selectbox("Nivel de actividad diaria (NEAT):", ["Muy Bajo", "Moderado", "Alto", "Extremo"])
    obj_principal = st.selectbox("Objetivo Principal:", ["Hipertrofia / ganar masa muscular", "Pérdida de grasa", "Recomposición corporal"])
    prioridad_muscular = st.multiselect("Músculos a priorizar:", ["Pectoral", "Dorsal Ancho", "Deltoides", "Piernas"])

with tab2:
    st.header("2. Experiencia en Entrenamiento")
    tiempo_entrenando = st.selectbox("¿Cuánto tiempo llevas entrenando?", ["Menos de 6 meses", "6 meses a 2 años", "Más de 2 años (Avanzado)"])
    t_intensidad = st.slider("Nivel de Intensidad autopercibido (1 al 10)", 1, 10, 7)

with tab3:
    st.header("3. Historial Médico y Lesiones")
    con_hombro = st.checkbox("Lesiones / Limitaciones de Hombro")
    con_rodilla = st.checkbox("Problemas / Dolores de Rodilla")

with tab4:
    st.header("4. Perfil Biomecánico y Estructura Corporal")
    palanca_piernas = st.selectbox("Miembros inferiores:", ["Proporcionales", "Piernas largas respecto al torso"])
    postura_hombros = st.checkbox("Hombros adelantados / Rotación interna")

with tab5:
    st.header("5. Fuerza Actual")
    w_banca = st.number_input("Press de Banca (kg):", min_value=0.0, value=0.0, step=2.5)
    w_sentadilla = st.number_input("Sentadilla (kg):", min_value=0.0, value=0.0, step=2.5)
    w_deadlift = st.number_input("Peso Muerto (kg):", min_value=0.0, value=0.0, step=2.5)

with tab6:
    st.header("6. Recuperación y Estilo de Vida")
    horas_sueno = st.slider("Horas de sueño diarias:", 4, 12, 7)
    calidad_sueno = st.selectbox("Calidad del sueño:", ["Mala", "Regular", "Buena"])
    estres_laboral = st.slider("Estrés Laboral (1 al 10)", 1, 10, 5)

with tab7:
    st.header("7. Disponibilidad y Preferencias")
    menos_activacion = st.text_input("¿En qué músculos sientes menos activación?")

with tab8:
    st.header("8. Evaluación Visual")
    f_frontal = st.file_uploader("Foto Frontal:", type=["jpg", "png", "jpeg"])

if not es_coach:
    st.markdown("---")
    st.info("👍 **Cuestionario completado.** Avísale a tu coach para que procese tu planificación.")

# ==============================================================================
# MOTOR DE PROCESAMIENTO (EXCLUSIVO COACH)
# ==============================================================================
if es_coach:
    st.markdown("---")
    st.header("⚙️ MOTOR DE PROCESAMIENTO BIOMECÁNICO (EXCLUSIVO COACH)")
    
    if st.button("PROCESAR DIAGNÓSTICO COMPLETO & GUARDAR HISTORIAL"):
        if not nombre:
            st.error("Por favor, introduce el nombre del cliente para ejecutar el reporte.")
        else:
            # Lógica analítica del perfil
            if "Avanzado" in tiempo_entrenando or t_intensidad >= 8:
                perfil_usuario = "Avanzado (Alta demanda de intensidad)"
                RIR_pdf = "RIR 0 (Fallo absoluto controlado)"
            else:
                perfil_usuario = "Intermedio / Adaptación"
                RIR_pdf = "RIR 1"
                
            puntos_recuperacion = 10
            if horas_sueno < 6: puntos_recuperacion -= 3
            if estres_laboral > 7: puntos_recuperacion -= 2
            cap_recuperacion = "Alta" if puntos_recuperacion >= 7 else "Comprometida / Media"
            
            if "Piernas largas" in palanca_piernas:
                dominancia_articular = "Dominancia de Cadera (Femures largos)"
                ej_pierna = "Sentadilla Hack (Estabilizada)"
                ejercicios_evitar = "Sentadilla libre trasera pesada debido a la palanca desventajosa en fémures."
                riesgos_articulares = "Cizallamiento incrementado en vertebras lumbares L4-S1."
            else:
                dominancia_articular = "Dominancia de Rodilla"
                ej_pierna = "Sentadilla Libre Profunda"
                ejercicios_evitar = "Ninguno crítico detectado."
                riesgos_articulares = "Ninguno crítico severo bajo técnica óptima."

            # Almacenamiento en Base de Datos Local
            nueva_fila = {
                "Fecha": datetime.date.today().strftime("%Y-%m-%d"), "Cliente": nombre, "Edad": int(edad),
                "Peso (kg)": float(peso), "Estatura (cm)": int(estatura_cm), "Objetivo": obj_principal,
                "Nivel": perfil_usuario, "Recuperacion": cap_recuperacion, "Banca (kg)": float(w_banca),
                "Sentadilla (kg)": float(w_sentadilla), "Peso Muerto (kg)": float(w_deadlift)
            }
            df_fila = pd.DataFrame([nueva_fila])
            if not os.path.isfile(ARCHIVO_DATOS):
                df_fila.to_csv(ARCHIVO_DATOS, index=False)
            else:
                df_fila.to_csv(ARCHIVO_DATOS, mode='a', header=False, index=False)
                
            st.success(f"✔️ ¡Datos de {nombre} archivados con éxito en el registro!")

            # Clase de PDF estructurada sin errores de desborde horizontal
            class MindMuscleMegaPDF(FPDF):
                def header(self):
                    self.set_fill_color(24, 24, 27)
                    self.rect(0, 0, 210, 38, 'F')
                    self.set_text_color(255, 255, 255)
                    self.set_font('helvetica', 'B', 18)
                    self.set_xy(15, 14)
                    self.cell(80, 8, 'MIND MUSCLE PRO', border=0, align='L')
                    self.set_font('helvetica', 'B', 10)
                    self.set_xy(110, 15)
                    self.cell(85, 6, 'DIAGNOSTICO & PLANIFICACION 3D', border=0, align='R')
                    self.set_xy(15, 45)
                def footer(self):
                    self.set_y(-15)
                    self.set_font('helvetica', 'I', 8)
                    self.set_text_color(128, 128, 128)
                    self.cell(0, 10, f'MIND MUSCLE PLATFORM PRO - Pagina {self.page_no()}', 0, 0, 'C')
                def agregar_seccion(self, titulo):
                    self.set_fill_color(32, 32, 36)
                    self.set_text_color(255, 255, 255)
                    self.set_font('helvetica', 'B', 10)
                    self.cell(180, 7, f"  {titulo}", fill=True, ln=1)
                    self.ln(2)

            pdf = MindMuscleMegaPDF()
            pdf.set_margins(15, 20, 15)
            pdf.set_auto_page_break(auto=True, margin=20)
            
            # HOJA 1: RESUMEN BIOMECÁNICO
            pdf.add_page()
            pdf.set_font('helvetica', 'B', 14)
            pdf.cell(180, 8, f"REPORTE DE INGENIERIA CORPORAL: {nombre.upper()}", ln=1)
            pdf.set_font('helvetica', '', 10)
            pdf.cell(180, 5, f"Edad: {edad} anos | Peso: {peso} kg | Estatura: {estatura_cm} cm", ln=1)
            pdf.cell(180, 5, f"Objetivo: {obj_principal.upper()}", ln=1)
            pdf.ln(5)
            
            pdf.agregar_seccion("I. EVALUACION Y PERFIL DE RECUPERACION")
            pdf.set_font('helvetica', '', 10)
            pdf.set_x(15)
            texto_recup = f"Nivel clasificado: {perfil_usuario}.\nCapacidad de recuperacion muscular: {cap_recuperacion}.\nEntorno de descanso analizado: Duerme {horas_sueno}h por noche con calidad {calidad_sueno}."
            pdf.multi_cell(180, 6, texto_recup)
            pdf.ln(4)
            
            pdf.agregar_seccion("II. INFORME BIOMECANICO & LIMITACIONES LIMITANTES")
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(180, 6, f"Dominancia Estructural Analizada: {dominancia_articular}", ln=1)
            pdf.set_font('helvetica', '', 10)
            pdf.set_x(15)
            texto_biomec = f"Riesgos de sobrecarga detectados: {riesgos_articulares}\nMovimientos contraindicados: {ejercicios_evitar}"
            pdf.multi_cell(180, 6, texto_biomec)
            
            # HOJA 2: RUTINA REESTRUCTURADA
            pdf.add_page()
            pdf.agregar_seccion("III. PLANIFICACION SEMANAL DE GIMNASIO")
            pdf.set_font('helvetica', 'B', 10)
            pdf.cell(180, 6, f"Metodo de Carga: Heavy Duty Modificado | Intensidad Objetivo: {RIR_pdf}", ln=1)
            pdf.ln(3)

            # Encabezados de Tabla
            pdf.set_font('helvetica', 'B', 9)
            pdf.set_fill_color(240, 240, 240)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(40, 7, "Dia", 1, 0, 'C', True)
            pdf.cell(75, 7, "Estrategia Mecanica / Ejercicios", 1, 0, 'C', True)
            pdf.cell(35, 7, "Volumen Serie Top", 1, 0, 'C', True)
            pdf.cell(30, 7, "Tempo", 1, 1, 'C', True)
            
            # Filas
            pdf.set_font('helvetica', '', 9)
            pdf.cell(40, 7, "LUNES: Push", 1, 0, 'L')
            ej_empuje = "Press Inclinado c/Mancuernas" if con_hombro else "Press de Banca Plano"
            pdf.cell(75, 7, f" {ej_empuje}", 1, 0, 'L')
            pdf.cell(35, 7, "1 Serie al Fallo", 1, 0, 'C')
            pdf.cell(30, 7, "4-2-4", 1, 1, 'C')
            
            pdf.cell(40, 7, "VIERNES: Legs", 1, 0, 'L')
            pdf.cell(75, 7, f" {ej_pierna}", 1, 0, 'L')
            pdf.cell(35, 7, "1 Serie al Fallo", 1, 0, 'C')
            pdf.cell(30, 7, "4-2-4", 1, 1, 'C')
            
            # HOJA 3: NUTRICIÓN
            pdf.add_page()
            pdf.agregar_seccion("IV. ESTRUCTURA DE LA DIETA DIARIA PERSONALIZADA")
            target_cal = int(peso * 33) if "Hipertrofia" in obj_principal else int(peso * 24)
            pdf.set_font('helvetica', 'B', 11)
            pdf.cell(180, 6, f"Prescripcion Calorica Basal Target: {target_cal} kcal / dia", ln=1)
            pdf.ln(3)
            
            pdf.set_font('helvetica', '', 10)
            pdf.set_x(15)
            texto_dieta = "- Comida 1 (Desayuno): 4 Huevos enteros + 70g avena pesada en seco + 1 Platano.\n- Comida 2 (Almuerzo): 200g pechuga de pollo cocida + 180g de arroz blanco + Vegetales verdes.\n- Comida 3 (Post-Entreno): 1 Medida de Whey Protein + 60g de arroz inflado.\n- Comida 4 (Cena): 180g de pescado blanco o filete magro + 150g de camote al horno."
            pdf.multi_cell(180, 6, texto_dieta)

            pdf_bytes = bytes(pdf.output())
            st.markdown("---")
            st.download_button(
                label="📥 DESCARGAR DIAGNÓSTICO FINAL (PDF)",
                data=pdf_bytes, file_name=f"Plan_{nombre.replace(' ', '_')}_MM.pdf", mime="application/pdf"
            )

    # Base de Datos integrada abajo
    st.markdown("---")
    st.header("📊 BASE DE DATOS HISTÓRICA DE CLIENTES")
    if os.path.isfile(ARCHIVO_DATOS):
        df_historico = pd.read_csv(ARCHIVO_DATOS)
        buscar_cliente = st.text_input("🔍 Filtrar por nombre del cliente:")
        if buscar_cliente:
            df_historico = df_historico[df_historico["Cliente"].str.contains(buscar_cliente, case=False, na=False)]
        st.dataframe(df_historico.sort_values(by="Fecha", ascending=False), width=None)