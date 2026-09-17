import os
from dotenv import load_dotenv
from crewai import LLM, Agent, Task, Crew

# 1. Cargamos la API Key de Groq de forma segura desde el archivo .env
load_dotenv()

# 2. Configuramos el modelo de IA (Qwen 3.6 a través de Groq)
# Este codigo no funciona ya que las versiones mas recientes de CrewAI requieren la configuración 
# de la API Key y el endpoint de Groq de forma explícita.
# cerebro_ia = LLM(
#     model="groq/qwen3.6-27b",
#     extra_body={
#         "reasoning_format": "hidden",  # Oculta el análisis interno largo
#         "reasoning_effort": "none"     # Fuerza a que sea directo y conciso
#     }
# )

# 2. Configuramos el modelo de IA de forma compatible
cerebro_ia = LLM(
    model="openai/qwen/qwen3.6-27b",                    # Formato de ruta estándar
    base_url="https://api.groq.com/openai/v1",          # Apuntamos directo al endpoint de Groq
    api_key=os.environ.get("GROQ_API_KEY"),             # Le pasamos la llave cargada del .env
    extra_body={
        "reasoning_format": "hidden",
        "reasoning_effort": "none"
    }
)
# 3. Definición de Agentes

# Agente 1: El Analista de Negocio / Product Owner
analista = Agent(
    role="Analista de Negocio Senior y Product Owner de Jira",
    goal="Transformar requisitos vagos del usuario en Historias de Usuario formales con Criterios de Aceptación claros.",
    backstory=(
        "Eres un experto en agilidad y gestión de productos en Jira. Tu especialidad es hablar "
        "con los clientes, entender sus necesidades ambiguas y estructurarlas de forma impecable "
        "utilizando el formato estándar Gherkin (Given/When/Then). Eres directo, técnico y estructurado."
    ),
    llm=cerebro_ia,      # Le asignamos el cerebro Qwen que configuramos arriba
    verbose=True         # Nos permite ver en la terminal cómo "piensa" el agente en tiempo real
)
# Agente 2: El Ingeniero de QA (Quality Assurance)
ingeniero_qa = Agent(
    role="Ingeniero de Automatización de Pruebas y QA Senior",
    goal="Auditar historias de usuario y diseñar casos de prueba técnicos exhaustivos para garantizar la calidad del software.",
    backstory=(
        "Eres un experto en control de calidad con años de experiencia en entornos empresariales. "
        "Tu trabajo es tomar las historias de usuario que escribe el Product Owner, analizar los "
        "criterios de aceptación y estructurar una lista clara de casos de prueba técnicos (casos de éxito, "
        "casos de error y condiciones límite). Tu enfoque es preventivo, riguroso y técnico."
    ),
    llm=cerebro_ia,      # Comparte el mismo cerebro Qwen de Groq
    verbose=True         # También veremos su proceso en la terminal
)
# 4. Definición de Tareas

# Tarea 1: El Analista procesa el requerimiento inicial del usuario
tarea_analisis = Task(
    description=(
        "Toma el siguiente requerimiento vago del usuario: 'Quiero un sistema para que los clientes "
        "puedan calificar los productos con estrellas y dejar un comentario corto'. "
        "Analízalo, ordénalo y redáctalo como una Historia de Usuario formal para Jira. "
        "Debe incluir una descripción clara y Criterios de Aceptación obligatorios."
    ),
    expected_output=(
        "Un documento estructurado con la Historia de Usuario (Como [rol], quiero [acción], para [beneficio]) "
        "y sus respectivos Criterios de Aceptación detallados en formato Gherkin (Given/When/Then)."
    ),
    agent=analista  # Asignamos explícitamente esta tarea al agente Analista
)
# Tarea 2: El QA audita la Historia de Usuario y genera los casos de prueba
tarea_qa = Task(
    description=(
        "Revisa detalladamente la Historia de Usuario y los Criterios de Aceptación que generó el Analista "
        "en la tarea anterior. Basándote exclusivamente en esa información, diseña los casos de prueba técnicos "
        "necesarios para validar que la funcionalidad cumpla con la calidad requerida."
    ),
    expected_output=(
        "Una lista técnica y ordenada de Casos de Prueba. Cada caso debe incluir: "
        "1. ID/Nombre del caso, 2. Precondición, 3. Pasos a ejecutar, 4. Resultado esperado."
    ),
    agent=ingeniero_qa  # Asignamos esta tarea al agente de QA
)
# 5. Orquestación y Ejecución de la Tripulación (Crew)

equipo_ingenieria = Crew(
    agents=[analista, ingeniero_qa],       # Lista ordenada de los actores
    tasks=[tarea_analisis, tarea_qa],       # Lista ordenada de las tareas secuenciales
    verbose=True                           # Muestra todo el log del debate en la terminal
)

print("\n🚀 Iniciando el pipeline autónomo Multi-Agente...")

# Lanzamos el proceso. CrewAI se encarga de coordinar a las IAs de forma interna
resultado_final = equipo_ingenieria.kickoff()

# 6. Automatización: Persistencia del reporte completo en un archivo local
nombre_reporte = "reporte_ingenieria.docx"

with open(nombre_reporte, "w", encoding="utf-8") as archivo:
    archivo.write("==================================================\n")
    archivo.write(" REPORTE COMPLETO DEL PIPELINE MULTI-AGENTE\n")
    archivo.write("==================================================\n\n")
    archivo.write(str(resultado_final))

print(f"\n[¡Éxito!] El pipeline ha finalizado.")
print(f"El archivo '{nombre_reporte}' fue creado de forma automática en tu carpeta local.")
