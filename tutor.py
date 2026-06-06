import streamlit as st
from google import genai
from PIL import Image

# 1. CONFIGURACIÓN DE LA PÁGINA (SIEMPRE VA PRIMERO)
st.set_page_config(
    page_title="Tutor IA - Tu Mentor Universitario 24/7", 
    page_icon="🧠", 
    layout="centered"
)

# Traer la clave segura desde los secretos de Streamlit
API_KEY = st.secrets["API_KEY"]

# === CONFIGURACIÓN DE NEGOCIO (CAMBIA ESTO) ===
# IMPORTANTE: Reemplaza este link por tu enlace REAL de Stripe en modo Live cuando estés listo
LINK_DE_STRIPE = "https://buy.stripe.com/test_6ok5n946D0ay0Ue000" 
LIMITE_GRATIS = 3
# ===============================================

# Inicializar el contador de mensajes gratis en la memoria del usuario si no existe
if "mensajes_enviados" not in st.session_state:
    st.session_state.mensajes_enviados = 0

# 2. BARRA LATERAL (PLAN PREMIUM)
with st.sidebar:
    st.title("🚀 Plan Premium Universal")
    st.write("¿Te quedaste sin preguntas gratis y necesitas salvar el cuatrimestre?")
    
    # Resaltar el precio de forma ejecutiva
    st.metric(label="Acceso Ilimitado Total", value="$25 MXN", delta="Al mes")
    
    st.markdown("""
    * 📚 **Todas las Materias:** Ciencias, Contabilidad, Leyes, Ingeniería y más.
    * 📸 **Escáner Multimodal:** Sube fotos de tus ejercicios o apuntes.
    * ⏱️ **Soporte 24/7:** Sin límites de preguntas ni bloqueos diarios.
    * 🎓 **Guía Paso a Paso:** Explicaciones diseñadas pedagógicamente para que pases tus exámenes.
    """)
    
    # Botón directo conectado a Stripe
    st.link_button("💳 Activar Acceso Ilimitado", LINK_DE_STRIPE, type="primary")
    
    st.divider()
    st.caption("🔒 Pagos 100% seguros y encriptados procesados por Stripe.")


# 3. DISEÑO DE LA LANDING PAGE (HERO SECTION)
st.title("🧠 Tu Tutor IA Universitario Universal")
st.subheader("🔥 ¡Deja de tronarte los dedos con las tareas difíciles!")
st.write(
    "Sube la foto de cualquier ejercicio, balance, organigrama, fórmula o lectura, "
    "y tu Tutor IA te guiará paso a paso para resolverlo y entenderlo hoy mismo."
)

st.divider()

# 4. SECCIÓN DE PRUEBA SOCIAL (TESTIMONIOS PARA DAR CONFIANZA)
st.caption("⚡ Lo que dicen otros universitarios:")
col1, col2 = st.columns(2)
with col1:
    st.info("⭐⭐⭐⭐⭐\n\n*\"Tenía un balance general descuadrado a las 2 AM, le tomé foto y esta IA me enseñó en qué cuenta me había equivocado. ¡Salvé la materia!\"*\n\n— **Carlos G.**, Admón. de Empresas.")
with col2:
    st.info("⭐⭐⭐⭐⭐\n\n*\"Las explicaciones de Derecho Fiscal son mil veces más claras y estructuradas que las de mi propio profesor del campus.\"*\n\n— **Ale V.**, Contaduría.")

st.divider()

# 5. CARGADOR DE ARCHIVOS (FUNCIÓN PREMIUM DE FOTOS)
foto_subida = st.file_uploader("📸 [PREMIUM] Sube la foto de tu ejercicio o tarea", type=["jpg", "jpeg", "png"])

# El chat solo se activa si le quedan créditos libres
creditos_restantes = LIMITE_GRATIS - st.session_state.mensajes_enviados

if creditos_restantes > 0:
    st.write(f"💡 Tienes **{creditos_restantes}** preguntas gratis restantes por hoy.")
else:
    st.error("🚨 Has agotado tus preguntas gratis de hoy. Para continuar chateando y usando el lector de fotos, activa tu Plan Premium en la barra lateral.")

if prompt := st.chat_input("Escribe tu pregunta aquí...", disabled=(creditos_restantes <= 0)):
    
    # Inicializar el cliente de Gemini
    client = genai.Client(api_key=st.secrets["API_KEY"])
    
    # CASO 1: El usuario subió una foto (Función Premium)
    if foto_subida is not None:
        st.info("🔮 Procesando archivo con motor multimodal Premium...")
        imagen = Image.open(foto_subida)
        st.image(imagen, caption="📷 Imagen cargada correctamente", use_container_width=True)
        
        contenido_bomba = [prompt, imagen]
        
        # CAMBIA ESTE BLOQUE DE ABAJO
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contenido_bomba,
            config={
                'system_instruction': (
                    "Eres Tutor IA, una Inteligencia Artificial de mentoría universitaria de élite, experta en todas las áreas del conocimiento. "
                    "REGLA CRÍTICA: Está ABSOLUTAMENTE PROHIBIDO dar la respuesta directa al inicio. Tu objetivo es guiar pedagógicamente al estudiante paso a paso para que él razone y aprenda. "
                    "Estructura tus respuestas de forma impecable: usa títulos limpios, listas con viñetas, tablas estructuradas si manejas números, y resalta conceptos clave en **negritas**."
                )
            }
        )
        st.success("🤖 Respuesta del Tutor Premium:")
        st.write(response.text)
        
    # CASO 2: Es una pregunta normal de texto (Abierto para todos)
    else:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': "Eres Tutor IA, un mentor universitario de élite. Explica de forma clara, didáctica, usando negritas y listas estructuradas."}
        )
        st.write(response.text)
    
    # Sumar el crédito consumido AL FINAL, para que no interfiera con la respuesta en pantalla
    st.session_state.mensajes_enviados += 1
