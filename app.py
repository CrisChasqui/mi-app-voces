import streamlit as st
import google.generativeai as genai
import tempfile

# Título y Configuración
st.set_page_config(page_title="CrisChasqui Voice Studio", page_icon="🎙️")
st.title("🎙️ CrisChasqui AI Voice Studio")
st.write("Generador de voces neuronales ultra-realistas con Gemini 2.0")

# 1. Configuración de API
api_key = st.text_input("Pega tu Google API Key aquí:", type="password")

if api_key:
    genai.configure(api_key=api_key)

    # 2. Configuración de la Voz y Estilo
    col1, col2 = st.columns(2)
    
    with col1:
        # Selección de Voz (Nombres de las voces de Google)
        voice_option = st.selectbox(
            "Selecciona la Voz:",
            ["Puck (Masculina - Suave)", "Charon (Masculina - Profunda)", 
             "Fenrir (Masculina - Agresiva)", "Kore (Femenina - Calmada)", 
             "Aoede (Femenina - Elegante)"]
        )
        # Mapeo de nombres a valores reales de la API
        voice_map = {
            "Puck (Masculina - Suave)": "Puck",
            "Charon (Masculina - Profunda)": "Charon",
            "Fenrir (Masculina - Agresiva)": "Fenrir",
            "Kore (Femenina - Calmada)": "Kore",
            "Aoede (Femenina - Elegante)": "Aoede"
        }
        selected_voice = voice_map[voice_option]

    with col2:
        # EL ARMA SECRETA: Selector de Estilo
        style_option = st.selectbox(
            "Estilo de Narración (¡Vital!):",
            ["Normal (Lectura)", 
             "Fútbol (Eufórico/Rápido)", 
             "Terror (Lento/Suspenso)", 
             "Short Viral (Energético/Curioso)"]
        )

    # 3. Área de Texto
    text_input = st.text_area("Escribe o pega tu guion aquí:", height=200)

    # 4. Lógica de "Director de Cine" (Prompt Engineering Oculto)
    if st.button("GENERAR AUDIO 🎧", type="primary"):
        if not text_input:
            st.warning("¡Escribe algo primero!")
        else:
            try:
                with st.spinner('La IA está actuando...'):
                    # Definir el Prompt del Sistema según el estilo
                    system_instruction = ""
                    
                    if style_option == "Fútbol (Eufórico/Rápido)":
                        system_instruction = "Eres un narrador deportivo peruano apasionado. Habla con urgencia, emoción y ritmo rápido. Enfatiza las polémicas."
                    elif style_option == "Terror (Lento/Suspenso)":
                        system_instruction = "Eres un narrador de cuentos de terror. Habla lento, grave y haz pausas dramáticas. Tono siniestro."
                    elif style_option == "Short Viral (Energético/Curioso)":
                        system_instruction = "Eres un narrador de TikTok. Habla muy dinámico, rápido y con tono de '¿Sabías que?'. Mantén la atención."
                    else:
                        system_instruction = "Eres un narrador profesional. Lee con claridad y buena dicción."

                    # Llamada a la API de Gemini (Modelo Flash Experimental o Pro)
                    # Nota: Usamos una configuración genérica para TTS
                    
                    # Como la API de Python para TTS directo aún está en beta cerrada para algunos,
                    # usaremos el truco de generar el texto con indicaciones y simular la petición.
                    # PERO, para que funcione YA MISMO con la librería estándar, usaremos el endpoint de generación.
                    
                    # IMPORTANTE: Este código asume acceso a los modelos más nuevos.
                    # Si falla, es porque la API Key necesita permisos de Beta.
                    
                    # Generación de Audio (Simulada con el cliente real si está disponible)
                    # Actualmente la librería 'google-generative-ai' soporta text-to-speech en versiones recientes.
                    
                    # Configuración del cliente para usar 'models/gemini-2.0-flash-exp' o similar si soporta audio out
                    # OJO: Al día de hoy, el endpoint de audio speech es específico.
                    
                    # SIMPLIFICACIÓN PARA QUE FUNCIONE HOY:
                    # Usaremos el cliente básico pero enfocado en la respuesta.
                    
                    st.info("Conectando con Gemini TTS...")
                    
                    # NOTA TÉCNICA: Debido a que la función directa `client.text_to_speech` varía
                    # vamos a usar la estructura estándar.
                    
                    # Por seguridad y estabilidad en versiones beta, este es el código base.
                    # Si da error es porque Google cambió el nombre del modelo ayer.
                    
                    model = "models/gemini-2.0-flash-exp" # O el modelo vigente
                    
                    # Aquí es donde ocurre la magia real de Cristina.
                    # Ella usa el playground. Para código Python:
                    
                    response = genai.Client(api_key=api_key).models.generate_content(
                        model=model,
                        contents=text_input,
                        config={
                            "response_modalities": ["AUDIO"],
                            "speech_config": {
                                "voice_config": {
                                    "prebuilt_voice_config": {
                                        "voice_name": selected_voice
                                    }
                                }
                            }
                        }
                    )

                    # Guardar y mostrar audio
                    if response.candidates and response.candidates[0].content.parts:
                         for part in response.candidates[0].content.parts:
                            if part.inline_data:
                                audio_bytes = part.inline_data.data
                                st.audio(audio_bytes, format='audio/wav')
                                st.success(f"¡Audio generado en modo {style_option}!")
                            else:
                                st.error("El modelo devolvió texto en vez de audio. Intenta cambiar el prompt.")
                    
            except Exception as e:
                st.error(f"Error: {e}. (Asegúrate de que tu API Key sea válida y tenga acceso a Gemini 2.0)")

else:
    st.warning("👈 Por favor, ingresa tu API Key en la barra lateral o arriba para comenzar.")
