import os
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA
from groq import Groq  # Conectamos con el motor de IA

# 1. Rutas y carga de entorno seguro
ruta_raiz = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ruta_raiz / ".env")

# 2. Inicialización de Clientes (Atlassian + Groq)
JIRA_SERVER = "https://prgjira.atlassian.net/"
JIRA_USER = "ingzane@gmail.com"  # Tu correo verificado
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

jira_client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
groq_client = Groq()  # Busca automáticamente GROQ_API_KEY en tu .env

# --- CONFIGURACIÓN DEL TICKET ---
TICKET_ID = "SCRUM-211"  # Pon aquí tu ID de ticket real para la prueba
# --------------------------------

print(f"🔄 1/3. Recuperando comentarios del ticket {TICKET_ID}...")

try:
    # Traemos el ticket de Jira
    issue = jira_client.issue(TICKET_ID)
    
    # Consolidamos título, descripción y comentarios del ticket (Omitimos historial de cambios)
    contexto_ticket = f"TÍTULO DEL TICKET: {issue.fields.summary}\n"
    contexto_ticket += f"DESCRIPCIÓN INICIAL: {issue.fields.description}\n\n"
    contexto_ticket += "--- DISCUSIÓN Y COMENTARIOS DEL EQUIPO ---\n"
    
    comentarios = jira_client.comments(issue)
    for com in comentarios:
        # Extraemos el autor y el cuerpo (Omitimos las fechas por tu regla de negocio)
        contexto_ticket += f"- {com.author.displayName}: {com.body}\n"
    
    print("✅ 2/3. Datos extraídos. Procesando resumen ejecutivo con Qwen 3.6...")
    
    # 3. Llamada a la IA con Prompt del Sistema altamente restrictivo
    respuesta_ia = groq_client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        messages=[
            {
                "role": "system", 
                "content": (
                    "Eres un auditor técnico senior de Jira. Tu único objetivo es redactar un resumen ejecutivo "
                    "y directo de lo que se hizo y resolvió en el ticket, basándote exclusivamente en la discusión provista.\n\n"
                    "REGLAS OBLIGATORIAS DE NEGOCIO:\n"
                    "1. Prohibido incluir fechas de actualizaciones o líneas de tiempo.\n"
                    "2. Prohibido incluir historiales de cambios mecánicos (ej. cambios de estado o asignaciones).\n"
                    "3. Prohibido inventar o rellenar información sin sentido (sin alucinaciones). Si un dato no está en el texto, no existe.\n"
                    "4. Sé extremadamente conciso. Entrega la respuesta en un único párrafo corto o en un formato de máximo 3 viñetas de puro valor.\n"
                    "5. El tono debe ser profesional y directo al grano para consumo de managers."
                )
            },
            {
                "role": "user", 
                "content": f"Por favor, genera el resumen de cierre para el siguiente ticket:\n\n{contexto_ticket}"
            }
        ],
        extra_body={
            "reasoning_format": "hidden",  # Filtro que dominas para apagar el pensamiento largo
            "reasoning_effort": "none"
        },
        temperature=0.2  # Temperatura baja para evitar creatividad y asegurar consistencia
    )
    
    resumen_final = respuesta_ia.choices[0].message.content
    
    print("\n--- RESUMEN GENERADO POR LA IA ---")
    print(resumen_final)
    
    print(f"\n🚀 3/3. Publicando comentario final en {TICKET_ID}...")
    
    # 4. Inyección automatizada del comentario de vuelta a Jira
    comentario_formateado = f"📝 **[AI] RESUMEN DE CIERRE EJECUTIVO:**\n\n{resumen_final}"
    jira_client.add_comment(issue, comentario_formateado)
    
    print(f"✅ ¡Éxito absoluto! El resumen ha sido publicado en el ticket {TICKET_ID} de tu Jira real.")

except Exception as e:
    print(f"❌ Error en el proceso: {e}")
