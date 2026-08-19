import os
from groq import Groq
from dotenv import load_env  # <- Cargador de variables de entorno

# Buscamos el archivo .env local y cargamos sus variables al sistema
load_env()

# Inicializamos el cliente. Al no pasarle parámetros, Groq busca automáticamente 
# una variable de entorno llamada exactamente 'GROQ_API_KEY'
cliente = Groq()

# 2. Definimos las instrucciones y la pregunta en variables de texto
instruccion_del_sistema = "Eres un asistente experto en Jira. Respondes de forma corta y profesional."
pregunta_usuario = "¿Qué es un 'Epic' en Jira y para qué sirve?"

print("Enviando pregunta a la IA con Python...")

# 3. Hacemos la llamada real a la IA a través del código
respuesta = cliente.chat.completions.create(
    model="qwen/qwen3.6-27b", # ID oficial actualizado
    messages=[
        {"role": "system", "content": "Eres un diccionario técnico de Jira. Define el término solicitado por el usuario en una sola oración directa. No agregues introducciones, análisis ni saludos. Ve directo al grano."},
        {"role": "user", "content": "¿Qué es un 'Epic'?"}
    ],
    # --- AQUÍ ESTÁ LA SOLUCIÓN TÉCNICA REAL ---
    extra_body={
        "reasoning_format": "hidden",  # Oculta y descarta el análisis/repetición de instrucciones
        "reasoning_effort": "none"     # Apaga el modo "pensamiento largo" para que sea directo
    },
    temperature=0.5 # Volvemos a un estándar intermedio
    # Quitamos max_tokens para que la oración termine de forma natural y no se corte
)

# 4. Python recibe la respuesta de la IA y la muestra en tu pantalla
print("\n--- Respuesta de la IA ---")
print(respuesta.choices[0].message.content)
