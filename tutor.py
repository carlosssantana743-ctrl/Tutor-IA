import streamlit as st
from google import genai
from PIL import Image

# Configuración inicial de la página
st.set_page_config(page_title="Tutor IA - Universidad", layout="centered")

# Traer la clave segura desde los secretos de Streamlit
API_KEY = st.secrets["API_KEY"]

# Título principal de la plataforma
st.title("🎓 Tu Tutor IA Universitario")
st.write("Pregúntame sobre Contabilidad, Derecho Fiscal, Diseño Organizacional o lo que necesites.")

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
    
    # Caso 1: El usuario intentó subir una foto (Función Premium)
    if foto_subida is not None:
        st.warning("⚠️ La lectura de imágenes es una función exclusiva de **Tutor IA Premium**.")
        st.write("Para desbloquear esta herramienta y dejar que la IA resuelva tus ejercicios con solo una foto, suscríbete en la barra lateral por solo **$25 MXN al mes**.")
        st.write("Una vez que te hayas suscrito, escribe abajo: **'Activar mi pase Premium'** seguido de tu duda para procesar la imagen.")
        
        # Si el usuario ya pagó y escribe la palabra clave, lo dejamos pasar
        if "Activar mi pase Premium" in prompt:
            st.info("🔄 Procesando archivo como usuario Premium...")
            imagen = Image.open(foto_subida)
            st.image(imagen, caption="📄 Tarea cargada correctamente", use_container_width=True)
            
            # Enviar texto + imagen a Gemini
            contenido_bomba = [prompt.replace("Activar mi pase Premium", ""), imagen]
            
            client = genai.Client(api_key=API_KEY)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contenido_bomba
            )
            st.success("🤖 Respuesta del Tutor Premium:")
            st.write(response.text)
            
    # Caso 2: Es una pregunta normal de texto (Abierto para todos)
    else:
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt]
        )
        st.write(response.text)