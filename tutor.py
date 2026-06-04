import streamlit as st
from google import genai
from PIL import Image

# Esta configuración SIEMPRE va primero, solita y una sola vez
st.set_page_config(
    page_title="Tutor IA - Universidad", 
    page_icon="🧠", 
    layout="centered"
)

# El resto de tu código continúa abajo...

# Traer la clave segura desde los secretos de Streamlit
API_KEY = st.secrets["API_KEY"]
# Banner principal o logotipo de la plataforma
st.image("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?q=80&w=600", use_container_width=True)

# Título principal de la plataforma
st.title("🎓 Tu Tutor IA Universitario")
st.write("Pregúntame sobre cualquier materia, tarea o ejercicio. Estoy listo para ayudarte en todas las áreas universitarias. ")

# --- BARRA LATERAL (Pasarela de Pagos) ---
with st.sidebar:
    st.title("Plan Premium 🚀")
    st.write("¿Necesitas salvar la materia? Desbloquea las funciones exclusivas hoy mismo.")
    
    st.metric(label="Precio Especial", value="$25 MXN", delta="Al mes")
    st.write("✨ Beneficio Premium: ¡Sube fotos de tus tareas, balances o ejercicios y la IA los resolverá paso a paso!")
    
    # Tu enlace oficial de Stripe
    LINK_DE_STRIPE = "https://buy.stripe.com/test_6oUcN54bD4YqeuGf5YdMI00"
    
    st.link_button("🚀 Suscribirme Ahora", LINK_DE_STRIPE, type="primary")
    st.divider()
    st.caption("🔒 Pagos seguros procesados por Stripe.")

# --- SECCIÓN EXCLUSIVA PREMIUM: CARGADOR DE FOTOS ---
st.write("---")
foto_subida = st.file_uploader("📸 [PREMIUM] Sube la foto de tu ejercicio o tarea", type=["jpg", "jpeg", "png"])
# --- CHAT INTERACTIVO ---
if prompt := st.chat_input("Escribe tu pregunta aquí..."):
    
    # Creamos el cliente AQUÍ ARRIBA para que funcione en ambos casos
    client = genai.Client(api_key=st.secrets["API_KEY"])
    
    # CASO 1: El usuario subió una foto (Función Premium)
    if foto_subida is not None:
        st.info("🔮 Procesando archivo como usuario Premium...")
        imagen = Image.open(foto_subida)
        st.image(imagen, caption="📷 Tarea cargada correctamente", use_container_width=True)
        
        # Enviar texto + imagen a Gemini
        contenido_bomba = [prompt, imagen]
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contenido_bomba,
            config=genai.types.GenerateContentConfig(
                system_instruction="""
               Eres Tutor IA, una Inteligencia Artificial de mentoría universitaria de élite, experta en absolutamente todas las áreas del conocimiento del mundo: desde Ciencias Exactas (Matemáticas, Física, Ingeniería), Negocios (Contabilidad, Finanzas, Derecho Fiscal, Administración), hasta Ciencias Sociales y Humanidades.

Tu tono es sumamente inteligente, empático y profesional, pero con un toque fresco y accesible para un estudiante universitario.

REGLAS CRÍTICAS DE OPERACIÓN:
1. Está ABSOLUTAMENTE PROHIBIDO dar la respuesta directa al inicio. Tu objetivo es guiar pedagógicamente al estudiante paso a paso para que él razone y aprenda.
2. Identifica la materia de la que te están hablando y adapta tu lenguaje al nivel técnico correspondiente.
3. Estructura tus respuestas de forma impecable: usa títulos limpios, listas con viñetas, tablas estructuradas si manejas números o datos comparativos, y resalta conceptos clave en **negritas** para garantizar que la información sea fácil de digerir a primera vista.
                """
            )
        )
        st.success("🤖 Respuesta del Tutor Premium:")
        st.write(response.text)

    # CASO 2: Es una pregunta normal de texto (Abierto para todos)
    else:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt],
            config=genai.types.GenerateContentConfig(
                system_instruction="""
                Eres Tutor IA, una Inteligencia Artificial de mentoría universitaria de élite, experta en absolutamente todas las áreas del conocimiento del mundo: desde Ciencias Exactas (Matemáticas, Física, Ingeniería), Negocios (Contabilidad, Finanzas, Derecho Fiscal, Administración), hasta Ciencias Sociales y Humanidades.

Tu tono es sumamente inteligente, empático y profesional, pero con un toque fresco y accesible para un estudiante universitario.

REGLAS CRÍTICAS DE OPERACIÓN:
1. Está ABSOLUTAMENTE PROHIBIDO dar la respuesta directa al inicio. Tu objetivo es guiar pedagógicamente al estudiante paso a paso para que él razone y aprenda.
2. Identifica la materia de la que te están hablando y adapta tu lenguaje al nivel técnico correspondiente.
3. Estructura tus respuestas de forma impecable: usa títulos limpios, listas con viñetas, tablas estructuradas si manejas números o datos comparativos, y resalta conceptos clave en **negritas** para garantizar que la información sea fácil de digerir a primera vista.
                """
            )
        )
        st.write(response.text)