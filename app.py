import streamlit as st
import pandas as pd
import datetime
import random
import requests
from fpdf import FPDF

# =============================================================================
# 1. CONFIGURACIÓN, BRANDING Y CONTROL DE ERRORES DE BASE DE DATOS
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
        
        # Corrección definitiva al KeyError: Asegurar estructura básica si la hoja limpia no la tiene
        if "ID_Alumno" not in df.columns: df["ID_Alumno"] = []
        if "Tipo_Registro" not in df.columns: df["Tipo_Registro"] = []
        return df
    except Exception:
        return pd.DataFrame(columns=["Fecha", "Tipo_Registro", "ID_Alumno", "Nombre completo", "Sexo", "Edad", "Estatura", "Peso actual", "Objetivo principal"])

df_existente = cargar_base_datos()

# Estilos visuales Cyber-Gym MM247
st.markdown("""
    <style>
    body { background-color: #f4f6f9; }
    .main-title { font-size:40px; font-weight:900; background: linear-gradient(45deg, #FF4B4B, #111111); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align:center; margin-bottom:0px; }
    .subtitle { font-size:12px; color:#555555; text-align:center; margin-bottom:25px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;}
    .section-header { font-size:18px; font-weight:bold; color:#ffffff; background: linear-gradient(90deg, #111111, #FF4B4B); padding: 8px 12px; border-radius: 6px; margin-top:20px; margin-bottom:12px; }
    .sheet-box { background: #ffffff; border: 1px solid #e0e0e0; border-left: 5px solid #FF4B4B; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .id-box { background: #E8F5E9; border-left: 5px solid #2E7D32; padding: 15px; border-radius: 6px; font-size: 18px; color: #1B5E20; font-weight: bold; margin: 15px 0; text-align: center; }
    .avatar-container { background: linear-gradient(135deg, #111111, #2c3e50); padding: 20px; border-radius: 12px; color: white; display: flex; align-items: center; gap: 20px; }
    .avatar-circle { width: 75px; height: 75px; background: linear-gradient(45deg, #FF4B4B, #FF8585); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 34px; border: 3px solid #ffffff; }
    </style>
    """, unsafe_allow_html=True)

opcion = st.sidebar.selectbox("Módulos de Sistema MM247:", [
    "📝 Cuestionario 1: Evaluación Inicial y Prescripción", 
    "🔄 Cuestionario 2: Registro de Avances Semanales", 
    "📊 Dashboard Administrador (Coach)"
])

def generar_id_unico(nombre):
    partes = nombre.strip().split()
    iniciales = "".join([p[0].upper() for p in partes if p])[:3]
    if not iniciales: iniciales = "MM"
    return f"MM-{iniciales}-{random.randint(1000, 9999)}"

# =============================================================================
# MÓDULO 1: CUESTIONARIO 1 - MOTOR DE CÁLCULO METABÓLICO Y PRESCRIPCIÓN DE HOJAS
# =============================================================================
if opcion == "📝 Cuestionario 1: Evaluación Inicial y Prescripción":
    st.markdown("<div class='main-title'>MIND MUSCLE 247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Sistema de Alta Diagnóstica y Automatización Nutren-Biométrica</div>", unsafe_allow_html=True)
    
    with st.form("form_alta_inicial"):
        st.markdown("<div class='section-header'>Expediente Antropométrico y Clínico</div>", unsafe_allow_html=True)
        f_nombre = st.text_input("Nombre Completo del Alumno:").strip().upper()
        
        c1, c2, c3 = st.columns(3)
        with c1: f_edad = st.number_input("Edad (años):", min_value=12, max_value=90, value=25)
        with c2: f_sexo = st.selectbox("Sexo Biológico:", ["Masculino", "Femenino"])
        with c3: f_estatura = st.number_input("Estatura (cm):", min_value=100, max_value=230, value=170)
        
        c4, c5, c6 = st.columns(3)
        with c4: f_peso_inicial = st.number_input("Peso Actual en Ayunas (kg):", min_value=35.0, max_value=180.0, value=75.0, step=0.1)
        with c5: f_peso_meta = st.number_input("Peso Objetivo Meta (kg):", min_value=35.0, max_value=180.0, value=70.0, step=0.1)
        with c6: f_objetivo = st.selectbox("Estrategia / Meta:", ["Perder grasa", "Ganar masa muscular", "Recomposición corporal"])
        
        f_lesion = st.selectbox("Limitaciones Posturales o Lesiones Activas:", ["Ninguna", "Hombros / Complejo manguito rotador", "Rodilla / Desgaste / Tendinitis", "Espalda Baja / Lumbalgia"])
        f_dias = st.selectbox("Disponibilidad de Entrenamientos Semanales:", ["3 días por semana", "4 días por semana", "5 días por semana"])
        
        enviar_alta = st.form_submit_button("🚀 PROCESAR EXAMEN DIAGNÓSTICO Y GENERAR ID")

    if enviar_alta:
        if not f_nombre:
            st.error("❌ El nombre completo es indispensable para estructurar la base de datos.")
        else:
            # -----------------------------------------------------------------
            # LÓGICA DE CÁLCULO CIENTÍFICA (La esencia del Cuestionario 1)
            # -----------------------------------------------------------------
            # 1. Cálculo de TMB (Mifflin-St Jeor) y TDEE
            if f_sexo == "Masculino":
                tmb = (10 * f_peso_inicial) + (6.25 * f_estatura) - (5 * f_edad) + 5
            else:
                tmb = (10 * f_peso_inicial) + (6.25 * f_estatura) - (5 * f_edad) - 161
            
            factor_actividad = 1.375 if "3 días" in f_dias else 1.55
            tdee = tmb * factor_actividad
            
            # Ajuste calórico según objetivo establecido
            if f_objetivo == "Perder grasa": kcal_meta = tdee - 400
            elif f_objetivo == "Ganar masa muscular": kcal_meta = tdee + 300
            else: kcal_meta = tdee
            
            # 2. Distribución Exacta de Macronutrientes Obligatorios (2g Proteína, 1g Grasa)
            prot_g = round(2.0 * f_peso_inicial, 1)
            grasa_g = round(1.0 * f_peso_inicial, 1)
            
            kcal_prot_grasa = (prot_g * 4) + (grasa_g * 9)
            carbo_g = round(max(0.0, (kcal_meta - kcal_prot_grasa) / 4), 1)
            
            # 3. Determinación Automática del IMC
            estatura_m = f_estatura / 100
            imc = round(f_peso_inicial / (estatura_m ** 2), 1)
            estado_imc = "Normal" if imc < 25 else "Sobrepeso" if imc < 30 else "Obesidad"
            
            # Generación del ID único inmutable
            nuevo_id = generar_id_unico(f_nombre)
            
            # Guardar cálculos en caché de sesión para la impresión inmediata
            st.session_state["id_activo"] = nuevo_id
            st.session_state["diagnostico_cliente"] = {
                "Nombre": f_nombre, "Edad": f_edad, "Sexo": f_sexo, "Estatura": f_estatura, "ID": nuevo_id,
                "Peso": f_peso_inicial, "Meta_P": f_peso_meta, "Objetivo": f_objetivo, "Lesion": f_lesion,
                "IMC": imc, "Estado_IMC": estado_imc, "TMB": round(tmb,1), "TDEE": round(tdee,1), "Kcal": round(kcal_meta,1),
                "Prot": prot_g, "Grasa": grasa_g, "Carbo": carbo_g, "Dias": f_dias
            }
            
            # Empaquetado completo para Google Sheets via Webhook
            payload = {
                "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "INICIAL", "ID_Alumno": nuevo_id,
                "Nombre completo": f_nombre, "Edad": f"{f_edad} años", "Sexo": f_sexo, "Estatura": f"{f_estatura} cm",
                "Peso actual": str(f_peso_inicial), "Peso objetivo": str(f_peso_meta), "Objetivo principal": f_objetivo,
                "Días entrenar": f_dias, "Lesión actual": f_lesion, "IMC_Calculado": str(imc), "Calorías_Plan": str(round(kcal_meta,1))
            }
            
            try:
                requests.post(WEBHOOK_URL, json=payload)
                st.markdown(f"<div class='id-box'>💎 EXPEDIENTE CONFIGURADO CON ÉXITO<br><span style='font-size:24px;'>ID GENERADO: {nuevo_id}</span></div>", unsafe_allow_html=True)
                st.balloons()
            except Exception as e:
                st.error(f"Sincronización en la nube interrumpida: {e}")

    # Display e impresión de las 3 HOJAS Maestras Basadas en los Datos Reales del Alumno
    if "diagnostico_cliente" in st.session_state:
        dt = st.session_state["diagnostico_cliente"]
        
        st.markdown("<br>### 🛠️ Sistema de Edición y Prescripción de Hojas MM247", unsafe_allow_html=True)
        
        # --- HOJA 1: INFORME DIAGNÓSTICO ---
        with st.container():
            st.markdown("<div class='sheet-box'>", unsafe_allow_html=True)
            st.markdown(f"**🩺 HOJA 1: Informe Diagnóstico Avanzado (Metabólico, Clínico y Fisiológico)**")
            st.write(f"Punto de partida estadístico determinado mediante IMC: **{dt['IMC']} ({dt['Estado_IMC']})**.")
            st.write(f"Tasa Metabólica Basal (TMB): **{dt['TMB']} kcal** | Gasto Energético Diario (TDEE): **{dt['TDEE']} kcal**.")
            st.write(f"Intervención Planificada: **{dt['Kcal']} kcal** enfocadas en **{dt['Objetivo']}**.")
            st.write(f"Condición de limitaciones catalogada como: **{dt['Lesion']}**. Se autoriza entrenamiento bajo progresión milimétrica.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --- HOJA 2: RUTINA SEMANAL ---
        with st.container():
            st.markdown("<div class='sheet-box'>", unsafe_allow_html=True)
            st.markdown(f"**🏋️‍♂️ HOJA 2: Rutina Semanal Detallada (Músculo, Ejercicio y Series)**")
            st.write(f"Distribución recomendada para un bloque de **{dt['Dias']}**:")
            st.text(f"• Día 1/3 (Empuje/Fuerza): Press inclinado con mancuernas (4 Series x 8-10 reps) | Press Militar (3 Series)")
            st.text(f"• Día 2/4 (Tracción/Hipertrofia): Jalón al pecho con agarre prono (4 Series x 10-12 reps) | Remo con barra")
            st.text(f"• Día 3/5 (Pierna/Estabilidad): Sentadilla libre o prensa (4 Series x 10 reps) *Cuidando eje si reportó molestia*")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --- HOJA 3: DIETA DIARIA ---
        with st.container():
            st.markdown("<div class='sheet-box'>", unsafe_allow_html=True)
            st.markdown(f"**🍎 HOJA 3: Dieta Diaria Establecida (Comidas y Balance Energético)**")
            st.write(f"Macronutrientes Calculados: **Proteína: {dt['Prot']}g (2g/kg)** | **Grasas: {dt['Grasa']}g (1g/kg)** | **Carbohidratos: {dt['Carbo']}g**.")
            st.text(f"• Comida 1 (Pre-Entreno): {round(dt['Prot']*0.25)}g Proteína (Claras/Huevo) + {round(dt['Carbo']*0.3)}g Carbohidratos (Avena).")
            st.text(f"• Comida 2 (Post-Entreno): {round(dt['Prot']*0.35)}g Proteína (Pechuga de pollo) + {round(dt['Carbo']*0.4)}g Carbohidratos (Arroz blanco) + Vegetales.")
            st.text(f"• Comida 3 (Colación): {round(dt['Prot']*0.15)}g Proteína (Whey Protein) + {dt['Grasa']}g Grasas Saludables (Almendras).")
            st.text(f"• Comida 4 (Cena/Saciante): {round(dt['Prot']*0.25)}g Proteína magra + Ensalada verde libre.")
            st.markdown("</div>", unsafe_allow_html=True)

        # Compilación de PDF Inicial para el Alumno
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(190, 10, "MM247 - PLAN MAESTRO DE INGRESO", 0, 1, "C")
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(190, 8, f"ID UNICO INTERNO: {dt['ID']}", 1, 1, "C")
        pdf.ln(4)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(190, 6, f"Alumno: {dt['Nombre']}\nObjetivo: {dt['Objetivo']}\nKcal Asignadas: {dt['Kcal']} kcal\nMacros -> Prot: {dt['Prot']}g | Grasa: {dt['Grasa']}g | Carbo: {dt['Carbo']}g\nEstrategia Lesiones: {dt['Lesion']}")
        
        pdf_b = pdf.output(dest='S').encode('latin1', errors='ignore')
        st.download_button("📥 IMPRIMIR REPORTE INICIAL INDIVIDUAL (PDF)", data=pdf_b, file_name=f"Plan_Inicial_{dt['ID']}.pdf", mime="application/pdf")

# =============================================================================
# MÓDULO 2: CUESTIONARIO 2 - REVISIÓN DE AVANCES (SÓLO PIDE ID)
# =============================================================================
elif opcion == "🔄 Cuestionario 2: Registro de Avances Semanales":
    st.markdown("<div class='main-title'>BITÁCORA DE EVOLUCIÓN MM247</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Evaluación de Progreso Dinámico a Ritmo del Alumno</div>", unsafe_allow_html=True)
    
    with st.form("form_avances", clear_on_submit=True):
        st.markdown("<div class='section-header'>Llave de Acceso Única</div>", unsafe_allow_html=True)
        r_id = st.text_input("Ingresa tu ID de Alumno Asignado (Ej: MM-JDO-1234):").strip().upper()
        
        st.markdown("<div class='section-header'>Métricas de Control Semanal</div>", unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1: r_peso = st.number_input("Peso registrado esta mañana en ayunas (kg):", min_value=30.0, max_value=180.0, value=75.0, step=0.1)
        with col_r2: r_cintura = st.number_input("Perímetro de cintura a nivel umbilical (cm):", min_value=40.0, max_value=150.0, value=80.0, step=0.5)
        
        r_adherencia = st.selectbox("Porcentaje de cumplimiento de la dieta esta semana:", ["100% al 90%", "90% al 70%", "Menos del 70%"])
        r_fuerza = st.selectbox("Comportamiento de la sobrecarga progresiva en fuerza:", ["Aumenté kilos o repeticiones", "Estable / Mantuve cargas", "Fatiga / Disminución de cargas"])
        r_snc = st.slider("Nivel de energía y recuperación al despertar (1 al 10):", 1, 10, 8)
        r_notas = st.text_area("Reporte de sensaciones (Dolores articulares, estrés, dudas):")
        
        enviar_rev = st.form_submit_button("🔄 ENVIAR BITÁCORA DE CONTROL AL COACH")
        
        if enviar_rev:
            if not r_id:
                st.error("❌ No es posible procesar la bitácora sin vincular un ID de Alumno válido.")
            else:
                payload_rev = {
                    "Fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Tipo_Registro": "REVISION", "ID_Alumno": r_id,
                    "Peso_Revision": str(r_peso), "Cintura_Revision": str(r_cintura), "Adherencia_Dieta": r_adherencia,
                    "Progreso_Fuerza": r_fuerza, "Energia_SNC": str(r_snc), "Comentarios_Evolucion": r_notes
                }
                try:
                    requests.post(WEBHOOK_URL, json=payload_rev)
                    st.success("✅ Evolución enviada de manera encriptada. Tu Coach evaluará tus métricas desde el Dashboard.")
                except Exception as e:
                    st.error(f"Error de enlace: {e}")

# =============================================================================
# MÓDULO 3: DASHBOARD ADMINISTRADOR PRIVADO - CRUCE DE AVANCES E IMPRESIÓN
# =============================================================================
elif opcion == "📊 Dashboard Administrador (Coach)":
    st.markdown("<div class='main-title'>🔐 PANEL DE CONTROL MM247</div>", unsafe_allow_html=True)
    password = st.text_input("Introduce la Clave Maestra del Administrador:", type="password")
    
    if password == "MM247_Admin":
        if df_existente.empty or len(df_existente["ID_Alumno"].dropna().unique()) == 0:
            st.warning("No existen registros válidos almacenados en la base de datos central.")
        else:
            df_iniciales = df_existente[df_existente["Tipo_Registro"] == "INICIAL"]
            df_revisiones = df_existente[df_existente["Tipo_Registro"] == "REVISION"]
            
            ids_totales = df_existente["ID_Alumno"].dropna().unique()
            
            st.markdown("### 📊 Análisis Cruzado de Avance por ID de Alumno")
            id_seleccionado = st.selectbox("Seleccione el ID del Expediente a Evaluar:", ids_totales)
            
            perfil = df_iniciales[df_iniciales["ID_Alumno"] == id_seleccionado]
            
            if not perfil.empty:
                row = perfil.iloc[0]
                nombre_alumno = str(row.get("Nombre completo", "ALUMNO")).title()
                genero = row.get("Sexo", "Masculino")
                avatar = "🏋️‍♂️" if "Masculino" in genero else "🏋️‍♀️"
                
                # Despliegue de la Identidad Visual Premium del Alumno
                st.markdown(f"""
                <div class='avatar-container'>
                    <div class='avatar-circle'>{avatar}</div>
                    <div>
                        <h2 style='margin:0; font-size:24px;'>{nombre_alumno}</h2>
                        <p style='margin:4px 0 0 0; opacity:0.8;'><b>ID Oficial:</b> {id_seleccionado} | <b>Estrategia:</b> {row.get('Objetivo principal', 'Mantenimiento')}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Reconstrucción temporal de pesos para análisis de proyección a ritmo del cliente
                try: p_ini = float(str(row.get("Peso actual", "75")))
                except: p_ini = 75.0
                
                fechas = [pd.to_datetime(row["Fecha"]).strftime("%d/%m/%Y")]
                pesos = [p_ini]
                
                revs_filtradas = df_revisiones[df_revisiones["ID_Alumno"] == id_seleccionado].copy()
                if not revs_filtradas.empty:
                    revs_filtradas["Fecha_DT"] = pd.to_datetime(revs_filtradas["Fecha"])
                    revs_filtradas = revs_filtradas.sort_values(by="Fecha_DT")
                    for _, r_row in revs_filtradas.iterrows():
                        try:
                            pesos.append(float(r_row["Peso_Revision"]))
                            fechas.append(pd.to_datetime(r_row["Fecha"]).strftime("%d/%m/%Y"))
                        except: pass
                
                # Bloque Estadístico Comparativo
                st.markdown("<br>#### 📉 Métricas Comparativas de Evolución Física", unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                p_actual = pesos[-1]
                delta = round(p_actual - p_ini, 2)
                
                with m1: st.metric("Peso Base (Cuestionario 1)", f"{p_ini} kg")
                with m2: st.metric("Peso Última Revisión", f"{p_actual} kg", delta=f"{delta} kg")
                with m3: st.metric("Objetivo Trazado", f"{row.get('Peso objetivo', 'N/A')} kg")
                
                chart_data = pd.DataFrame({"Fecha": fechas, "Peso (kg)": pesos}).set_index("Fecha")
                st.line_chart(chart_data, color="#FF4B4B")
                
                # Mostrar Tabla de Respuestas Completas del Cuestionario 2 para Análisis del Coach
                st.markdown("#### 📋 Historial de Bitácoras de Rendimiento (Respuestas Exactas)")
                if not revs_filtradas.empty:
                    tabla_vista = revs_filtradas[["Fecha", "Peso_Revision", "Cintura_Revision", "Adherencia_Dieta", "Progreso_Fuerza", "Energia_SNC", "Comentarios_Evolucion"]].copy()
                    st.dataframe(tabla_vista, use_container_width=True)
                else:
                    st.info("💡 El alumno cuenta con ID activo pero aún no ha registrado bitácoras de avance semanal.")
                
                # --- CENTRO DE IMPRESIÓN INDEPENDIENTE ---
                st.markdown("---")
                st.markdown("### 🖨️ Centro de Impresión de Reportes MM247")
                cb1, cb2 = st.columns(2)
                
                with cb1:
                    # Imprimir Reporte Inicial por Alumno
                    pdf_i = FPDF()
                    pdf_i.add_page()
                    pdf_i.set_font("Helvetica", "B", 16)
                    pdf_i.cell(190, 10, "MM247 - EXPEDIENTE DIAGNOSTICO INICIAL", 0, 1, "C")
                    pdf_i.ln(5)
                    pdf_i.set_font("Helvetica", "B", 12)
                    pdf_i.cell(190, 8, f"ID CLIENTE: {id_seleccionado}", 1, 1, "C")
                    pdf_i.set_font("Helvetica", "", 11)
                    pdf_i.ln(4)
                    pdf_i.cell(190, 7, f"Nombre: {nombre_alumno}", 0, 1)
                    pdf_i.cell(190, 7, f"Edad/Sexo: {row.get('Edad')} | {genero}", 0, 1)
                    pdf_i.cell(190, 7, f"Estatura: {row.get('Estatura')}", 0, 1)
                    pdf_i.cell(190, 7, f"Peso de Entrada: {p_ini} kg | Meta: {row.get('Peso objetivo')} kg", 0, 1)
                    pdf_i.cell(190, 7, f"Estrategia Clinica Asignada: {row.get('Objetivo principal')}", 0, 1)
                    pdf_i.cell(190, 7, f"Calorias Planificadas: {row.get('Calorías_Plan', 'N/A')} kcal", 0, 1)
                    
                    bytes_i = pdf_i.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button("📥 IMPRIMIR REPORTE INICIAL INDIVIDUAL", data=bytes_i, file_name=f"Reporte_Inicial_{id_seleccionado}.pdf", mime="application/pdf")
                    
                with cb2:
                    # Imprimir Reporte Individual de Avances Cronológicos
                    pdf_a = FPDF()
                    pdf_a.add_page()
                    pdf_a.set_font("Helvetica", "B", 16)
                    pdf_a.cell(190, 10, "MM247 - BITACORA Y PROYECCION DE AVANCES", 0, 1, "C")
                    pdf_a.ln(5)
                    pdf_a.set_font("Helvetica", "B", 12)
                    pdf_a.cell(190, 8, f"Historial Cronologico para ID: {id_seleccionado}", 1, 1, "C")
                    pdf_a.set_font("Helvetica", "", 11)
                    pdf_a.ln(4)
                    pdf_a.cell(190, 7, f"Planificado para Alumno: {nombre_alumno}", 0, 1)
                    pdf_a.cell(190, 7, "Evolucion de Peso Reportado por el Alumno:", 0, 1)
                    for f, p in zip(fechas, pesos):
                        pdf_a.cell(190, 6, f" -> Fecha: {f}  |  Peso: {p} kg", 0, 1)
                    
                    bytes_a = pdf_a.output(dest='S').encode('latin1', errors='ignore')
                    st.download_button("📥 IMPRIMIR REPORTE INDIVIDUAL DE AVANCES", data=bytes_a, file_name=f"Reporte_Avances_{id_seleccionado}.pdf", mime="application/pdf")
            else:
                st.error("El ID seleccionado presenta inconsistencias en su registro inicial.")
    elif password != "":
        st.error("🔑 Acceso Denegado. Token inválido.")
