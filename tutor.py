import os
import streamlit as st
from google import genai
from google.genai import types

# 1. Tu Llave API (Pon la tuya entre las comillas)
API_KEY = "AQ.Ab8RN6LOOyXiyzF_0RKCFKdad2ST93JCLH9JErMyDDPwqm1Rqw"

# Configurar la página web (Título e Icono en la pestaña)
st.set_page_config(page_title="Tutor IA - Universidad", page_icon="🎓")

# Inicializar el cliente de Google
@st.cache_resource
def get_genai_client():
    return genai.Client(api_key=API_KEY)

client = get_genai_client()

# 2. El Guion del Tutor Socrático
SYSTEM_PROMPT = """
Eres un Tutor de Meta-Aprendizaje experto para estudiantes universitarios. Tu único objetivo es guiarlos para que resuelvan sus tareas por sí mismos.
REGLA DE ORO: Está ABSOLUTAMENTE PROHIBIDO dar la respuesta final, resolver el problema o dar el resultado masticado.
Metodología: Guía paso a paso haciendo preguntas como "¿Qué tipo de problema es este?", "¿Qué fórmulas aplican?", "¿Dónde te trabaste?".
"""

# Barra lateral informativa y de MONETIZACIÓN
with st.sidebar:
    st.title("Plan Premium")
    st.write("¿Necesitas salvar la materia? Desbloquea el acceso ilimitado hoy mismo.")
    
    st.metric(label="Precio Especial", value="$25 MXN", delta="Al mes")
    st.write("Tendrás soporte paso a paso de tu Tutor IA las 24 horas del día.")
    
    # Pon tu link de Stripe aquí en medio de las comillas
    LINK_DE_STRIPE = "https://buy.stripe.com/test_6oUcN54bD4YqeuGf5YdMI00"
    
    st.link_button("🚀 Suscribirme Ahora", LINK_DE_STRIPE, type="primary")
    st.divider()
    st.caption("Pagos seguros procesados por Stripe.")
    st.title("Plan Premium")
    st.write("¿Necesitas salvar la materia? Desbloquea el acceso ilimitado hoy mismo.")
    
    st.metric(label="Precio Especial", value="$25 MXN", delta="Al mes")
    st.write("Tendrás soporte paso a paso de tu Tutor IA las 24 horas del día.")
    
    # Pon tu link de Stripe aquí en medio de las comillas
    LINK_DE_STRIPE = "https://buy.stripe.com/test_6oUcN54bD4YqeuGf5YdMI0"
    
    st.link_button("🚀 Suscribirme Ahora", LINK_DE_STRIPE, type="primary")
    st.divider()
    st.caption("Pagos seguros procesados por Stripe.")

st.title("🤖 Tu Tutor Universitario Paso a Paso")
st.write("Cuéntame en qué materia o tarea estás atorado hoy. ¡Vamos a resolverlo juntos!")

# Inicializar el historial del chat si no existe
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Crear el chat con el prompt del sistema
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )

# Mostrar los mensajes anteriores del chat en la pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Caja de texto para que el usuario escriba abajo (Como WhatsApp)
if prompt := st.chat_input("¿En qué te puedo ayudar con tu tarea?"):
    # Mostrar el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Enviar el mensaje a la IA y obtener respuesta
    respuesta = st.session_state.chat.send_message(prompt)
    
    # Mostrar la respuesta del Tutor
    with st.chat_message("assistant"):
        st.markdown(respuesta.text)
    st.session_state.messages.append({"role": "assistant", "content": respuesta.text})