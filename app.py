import streamlit as st
import pandas as pd
import datetime
import random
import requests

# =============================================================================
# 1. CONFIGURACIÓN DE PÁGINA Y BRANDING (MM247)
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
        return df
    except Exception:
        return pd.DataFrame()

df_existente = cargar_base_datos()

# Estilos visuales optimizados
st.markdown("""
    <style>
    body { background-color: #f4f6f9; }
    .main-title { font-size:42px; font-weight:900; background: linear-gradient(45deg, #FF4B4B, #111111); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:13px; color:#555555; text-align:center; margin-bottom:30px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;}
    .section-header { font-size:20px; font-weight:bold; color:#ffffff; background: linear-gradient(90deg, #111111, #FF4B4B); padding: 8px 12px; border-radius: 6px; margin-top:20px; margin-bottom:12px; }
    .id-box { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 6px; font-size: 18px; color: #1B5E20; font-weight: bold; margin: 15px 0; }
    
    .metric-card-custom { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border-top: 4px solid #FF4B4B; text-align: center; }
    .avatar-container { background: linear-gradient(135deg, #111111, #2c3e50); padding: 20px; border-radius: 12px; color: white; display: flex; align-items: center; gap: 20px; }
    .avatar-circle { width: 70px; height: 70px; background: linear-gradient(45deg, #FF4B4B, #FF8585); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 32px; border: 3px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Módulos del Sistema MM247:", [
    "📝 Cuestionario 1: Evaluación Inicial", 
    "🔄 Cuestionario 2: Revisión de Avances", 
    "📊 Dashboard Administrador (Coach)"
])

# Función auxiliar para generar IDs limpios
def generar_id_unico(nombre):
    partes = nombre.strip().split()
    iniciales = "".join([p[0].upper() for p in partes if p])[:3]
    if not iniciales: iniciales = "UX"
    numero = random.randint(1000, 9999)
    return f"MM-{iniciales}-{numero}"

# =============================================================================
# MÓDULO 1: CUESTIONARIO INTEGRAL DE EVALUACIÓN INICIAL (GENERA ID)
# =============================================================================
if opcion == "📝 Cuestionario 1: Evaluación Inicial":
    st.markdown("<div class='main-title'>MINDMUSCLE247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Fase 1: Registro de Roster Clínico-Deportivo</div>", unsafe_allow_html=True)
    
    with st.form("form_registro_inicial", clear_on_submit=False):
        st.markdown("<div class='section-header'>Identificación Obligatoria</div>", unsafe_allow_html=True)
        f_nombre = st.text_input("Nombre completo del alumno:")
        
        c1, c2, c3 = st.columns(3)
        with c1: f_edad = st.selectbox("Edad actual:", [f"{i} años" for i in range(14, 80)], index=11)
        with c2: f_sexo = st.selectbox("Sexo biológico:", ["Masculino", "Femenino"])
        with c3: f_estatura = st.selectbox("Estatura base:", [f"{i} cm" for i in range(120, 220)], index=55)
        
        c4, c5, c6 = st.columns(3)
        with c4: f_peso_actual = st.selectbox("Peso actual (kg):", [f"{i} kg" for i in range(40, 160)], index=40)
        with c5: f_peso_obj = st.selectbox("Peso objetivo meta:", [f"{i} kg" for i in range(40, 160)], index=35)
        with c6: f_objetivo = st.selectbox("Objetivo principal:", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal"])
        
        st.markdown("<div class='section-header'>Parámetros de Frecuencia Semanal</div>", unsafe_allow_html=True)
        f_dias = st.selectbox("Días de entrenamiento muscular semanal comprometidos:", ["3 días por semana", "4 días por semana", "5 días por semana"])
        f_lesion = st.selectbox("Zonas propensas a molestia o lesiones activas:", ["Ninguna", "Rodilla / Desgaste / Tendinitis", "Hombro / Manguito rotador", "Espalda Baja / Lumbalgia"])
        
        enviar_inicial = st.form_submit_button("🚀 DAR DE ALTA Y GENERAR MI ID UNICO")
        
        if enviar_inicial:
            if not f_nombre.strip():
                st.error("❌ Por favor escribe tu nombre completo para procesar la identidad.")
            else:
                nuevo_id = generar_id_unico(f_nombre)
                payload = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "INICIAL",
                    "ID_Alumno": nuevo_id,
                    "Nombre completo": str(f_nombre.strip().upper()),
                    "Edad": str(f_edad), "Sexo": str(f_sexo), "Estatura": str(f_estatura),
                    "Peso actual": str(f_peso_actual), "Peso objetivo": str(f_peso_obj),
                    "Objetivo principal": str(f_objetivo), "Días entrenar": str(f_dias), "Lesión actual": str(f_lesion)
                }
                
                with st.spinner("Vinculando con servidores centrales MM247..."):
                    try:
                        response = requests.post(WEBHOOK_URL, json=payload)
                        st.markdown(f"""
                        <div class='id-box'>
                            🎉 ¡REGISTRO EXITOSO!<br>
                            Tu ID Personal Inmutable es: 💎 {nuevo_id}<br>
                            <small>Guarda bien este código. Lo necesitarás para ingresar a todas tus Revisiones Semanales.</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error de sincronización de datos: {e}")

# =============================================================================
# MÓDULO 2: CUESTIONARIO 2: REVISIÓN DE AVANCES (LLENADO EXCLUSIVO CON ID)
# =============================================================================
elif opcion == "🔄 Cuestionario 2: Revisión de Avances":
    st.markdown("<div class='main-title'>REVISIÓN DE AVANCES</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Fase 2: Monitoreo Periódico y Ajuste de Carga Biomecánica</div>", unsafe_allow_html=True)
    
    with st.form("form_revision_periodica", clear_on_submit=True):
        st.markdown("<div class='section-header'>Llave de Acceso del Alumno</div>", unsafe_allow_html=True)
        r_id = st.text_input("Introduce tu ID de Alumno (Ej: MM-JD-4820):").strip().upper()
        
        st.markdown("<div class='section-header'>Métricas de Control de Avance Exacto</div>", unsafe_allow_html=True)
        r_peso_hoy = st.number_input("Peso registrado esta mañana en ayunas (kg):", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
        r_cintura = st.number_input("Medida de perímetro de cintura a la altura del ombligo (cm):", min_value=40.0, max_value=160.0, value=80.0, step=0.5)
        
        st.markdown("<div class='section-header'>Análisis de Rendimiento y Recuperación Fisiológica</div>", unsafe_allow_html=True)
        r_adherencia = st.select_slider("Porcentaje de cumplimiento de la dieta asignada esta semana:", options=["0-25%", "25-50%", "50-75%", "75-100%"], value="75-100%")
        r_fuerza = st.selectbox("Progreso en los niveles de fuerza en ejercicios básicos:", ["Aumentó (Sobrecarga progresiva lograda)", "Se mantuvo estable", "Disminuyó ligeramente (Fatiga acumulada)"])
        r_energia = st.slider("Nivel de fatiga del Sistema Nervioso Central al despertar (1 = Agotado, 10 = Recuperado Máximo):", 1, 10, 8)
        r_comentarios = st.text_area("Notas adicionales (Molestias articulares, dolores post-entrenamiento o dudas):")
        
        enviar_revision = st.form_submit_button("🔄 ENVIAR BITÁCORA DE CONTROL")
        
        if enviar_revision:
            if not r_id:
                st.error("❌ No puedes enviar una revisión sin un ID válido asignado.")
            else:
                payload_rev = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tipo_Registro": "REVISION",
                    "ID_Alumno": r_id,
                    "Peso_Revision": str(r_peso_hoy),
                    "Cintura_Revision": str(r_cintura),
                    "Adherencia_Dieta": str(r_adherencia),
                    "Progreso_Fuerza": str(r_fuerza),
                    "Energia_SNC": str(r_energia),
                    "Comentarios_Evolucion": str(r_comentarios)
                }
                with st.spinner("Validando ID y subiendo actualización..."):
                    try:
                        requests.post(WEBHOOK_URL, json=payload_rev)
                        st.success(f"✅ Revisión sincronizada perfectamente bajo el ID: {r_id}. Tu Coach analizará estos cambios biomecánicos.")
                    except Exception as e:
                        st.error(f"Error de red: {e}")

# =============================================================================
# MÓDULO 3: DASHBOARD ADMINISTRADOR COMPLETO CON COMPARATIVO HISTÓRICO
# =============================================================================
elif opcion == "📊 Dashboard Administrador (Coach)":
    st.markdown("<div class='main-title'>🔐 Panel de Control MM247</div>", unsafe_allow_html=True)
    pass_admin = st.text_input("Ingresa la clave de acceso del Coach:", type="password")
    
    if pass_admin == "MM247_Admin":
        if df_existente.empty:
            st.warning("Aún no existen registros en el Spreadsheet central.")
        else:
            # Separar Base Inicial de Revisiones por la columna Tipo_Registro si existe, o simularla
            if "Tipo_Registro" not in df_existente.columns:
                df_existente["Tipo_Registro"] = "INICIAL" # Respaldo estructural
                
            df_iniciales = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
            df_revisiones = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
            
            st.markdown("### 📊 Análisis Cruzado de Avance por ID de Alumno")
            
            # El selector despliega los IDs únicos para evitar mezclar datos
            ids_disponibles = df_existente["ID_Alumno"].dropna().unique()
            id_sel = st.selectbox("Selecciona el ID Único del alumno a evaluar:", ids_disponibles)
            
            # Buscar info estática del alumno
            datos_perfil = df_iniciales[df_iniciales["ID_Alumno"] == id_sel]
            
            if not datos_perfil.empty:
                row_p = datos_perfil.iloc[0]
                genero = row_p.get("Sexo", "Masculino")
                avatar = "🏋️‍♂️" if "Masculino" in genero else "🏋️‍♀️"
                
                # Desplegar tarjeta de identidad deportiva premium
                st.markdown(f"""
                <div class='avatar-container'>
                    <div class='avatar-circle'>{avatar}</div>
                    <div>
                        <h2 style='margin:0; font-size:24px;'>{str(row_p.get('Nombre completo', 'ALUMNO')).title()}</h2>
                        <p style='margin:2px 0 0 0; opacity:0.8;'><b>ID Oficial:</b> {id_sel} | <b>Meta:</b> {row_p.get('Objetivo principal', 'No definido')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Recolectar Historial de Peso Inicial vs Revisiones Cronológicas
                try:
                    peso_inicial = float(str(row_p.get("Peso actual", "80")).replace(" kg", "").split()[0])
                except Exception:
                    peso_inicial = 80.0
                    
                fechas_progreso = [pd.to_datetime(row_p["Fecha"]).strftime("%d/%m/%Y")]
                valores_peso = [peso_inicial]
                
                # Filtrar las revisiones específicas de este ID ordenadas por fecha
                rev_alumno = df_revisiones[df_revisiones["ID_Alumno"] == id_sel].copy()
                if not rev_alumno.empty:
                    rev_alumno["Fecha_DT"] = pd.to_datetime(rev_alumno["Fecha"])
                    rev_alumno = rev_alumno.sort_values(by="Fecha_DT")
                    
                    for _, r_row in rev_alumno.iterrows():
                        try:
                            val_p = float(str(r_row.get("Peso_Revision", peso_inicial)))
                            fechas_progreso.append(pd.to_datetime(r_row["Fecha"]).strftime("%d/%m/%Y"))
                            valores_peso.append(val_p)
                        except Exception: pass
                
                # --- GRÁFICO DE COMPARATIVA EXACTA TEMPORAL ---
                st.markdown("<br>#### 📈 Curva Histórica de Peso y Evolución Física", unsafe_allow_html=True)
                chart_data = pd.DataFrame({
                    "Fecha de Registro": fechas_progreso,
                    "Peso Corporal (kg)": valores_peso
                }).set_index("Fecha de Registro")
                
                st.line_chart(chart_data, color="#FF4B4B")
                
                # --- TABLA DE RESPUESTAS EXACTAS PARA EL COACH ---
                st.markdown("#### 📋 Historial de Bitácoras Enviadas (Preguntas Exactas)")
                if not rev_alumno.empty:
                    tabla_vista = rev_alumno[["Fecha", "Peso_Revision", "Cintura_Revision", "Adherencia_Dieta", "Progreso_Fuerza", "Energia_SNC", "Comentarios_Evolucion"]].copy()
                    tabla_vista.columns = ["Fecha", "Peso (kg)", "Cintura (cm)", "Dieta %", "Evolución Fuerza", "SNC Energía", "Notas Alumno"]
                    st.dataframe(tabla_vista, use_container_width=True)
                else:
                    st.info("💡 El alumno tiene un ID activo pero no ha completado su primer Cuestionario 2 de Revisión aún.")
                    
            else:
                st.error("Este ID se encuentra registrado en revisiones pero carece de hoja de alta inicial.")
                
    elif pass_admin != "": st.error("🔑 Token incorrecto.")
