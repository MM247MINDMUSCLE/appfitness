import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. CONFIGURACIÓN
st.set_page_config(page_title="MINDMUSCLE247", page_icon="💪", layout="wide", initial_sidebar_state="expanded")

# 2. BARRA LATERAL (Con el QR aquí)
st.sidebar.title("🛡️ Sistema MINDMUSCLE247")
st.sidebar.markdown("**📲 Acceso Rápido a la App:**")
link_app = "https://appfitness-mindmuscle247.streamlit.app"
qr_url = f"https://chart.googleapis.com/chart?chs=200x200&cht=qr&chl={link_app}&choe=UTF-8"
st.sidebar.image(qr_url)
st.sidebar.markdown("---")

# 3. DEFINICIÓN DE PESTAÑAS (DEBE IR ANTES DE LOS "with tX:")
tabs = st.tabs(["⚡ 1. Info", "🏋️ 2. Exp", "🩺 3. Médico", "📐 4. Bio", "💥 5. Fuerza", "🥗 6. Nut", "📅 7. Log", "🎯 8. Pref", "📸 9. Foto"])
t1, t2, t3, t4, t5, t6, t7, t8, t9 = tabs

# 4. CONTENIDO DE PESTAÑAS
with t1:
    st.subheader("Datos Personales")
    # ... (Aquí va todo tu código original de t1) ...

with t2:
    st.subheader("Experiencia")
    # ... (Aquí va todo tu código original de t2) ...

with t3:
    st.subheader("Condiciones Médicas")
    # ... (Aquí va todo tu código original de t3) ...

# ... (Continúa con t4, t5, t6, t7, t8) ...

with t9:
    st.subheader("📸 Evaluación Visual Inicial")
    st.info("Sube tus fotos de frente, perfil y espalda.")
    uploaded_photos = st.file_uploader("📬 Selecciona tus fotos:", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    if st.button("🚀 ENVIAR EVALUACIÓN TÉCNICA"):
        st.success("Enviado con éxito.")
