import os
from groq import Groq
from dotenv import load_env  # <- Cargador de variables de entorno

# Buscamos el archivo .env local y cargamos sus variables al sistema
load_env()

# Inicializamos el cliente. Al no pasarle parámetros, Groq busca automáticamente 
# una variable de entorno llamada exactamente 'GROQ_API_KEY'
cliente = Groq()

print("Consultando la lista oficial de modelos en tu cuenta de Groq...\n")

try:
    # Le pedimos al servidor de Groq su lista actualizada
    lista = cliente.models.list()
    
    print("--- MODELOS DISPONIBLES EN TU CUENTA ---")
    for modelo in lista.data:
        print(f"- {modelo.id}")
        
except Exception as e:
    print(f"Ocurrió un error al conectar: {e}")
