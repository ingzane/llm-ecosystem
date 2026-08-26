import os
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA
from groq import Groq

# 1. Rutas y carga de entorno seguro
ruta_raiz = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ruta_raiz / ".env")

# 2. Inicialización de Clientes (Atlassian + Groq)
JIRA_SERVER = "https://prgjira.atlassian.net/"
JIRA_USER = "ingzane@gmail.com"  # Tu correo verificado
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

jira_client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_API_TOKEN))
groq_client = Groq()

# --- CONFIGURACIÓN DINÁMICA DE BÚSQUEDA ---
# Buscamos tickets en tu estado de cierre técnico
jql_automatizacion = "status = 'Done' ORDER BY created DESC"
# ------------------------------------------

print("🔍 1/3. Escaneando tickets cerrados en tu tablero...")

try:
    # Buscamos los últimos 10 tickets cerrados
    tickets_cerrados = jira_client.search_issues(jql_automatizacion, maxResults=10)
    print(f"📋 Se encontraron {len(tickets_cerrados)} tickets en estado cerrado.")

    # [BUCLE PRINCIPAL]: Recorremos cada ticket detectado de forma automática
    for issue in tickets_cerrados:
        TICKET_ID = issue.key
        print(f"\nEvaluating ticket {TICKET_ID}...")

        # Traemos todos los comentarios de este ticket específico
        comentarios = jira_client.comments(issue)
        
        # Bandera de control para evitar duplicados
        ya_tiene_resumen = False
        for com in comentarios:
            if "[AI-LAB] RESUMEN DE CIERRE" in com.body:
                ya_tiene_resumen = True
                break
        
        if ya_tiene_resumen:
            print(f"⏭️ El ticket {TICKET_ID} ya cuenta con un resumen de IA. Saltando...")
            continue  # Salta directo al siguiente ticket de la lista

        # --- TICKET ELEGIBLE DETECTADO ---
        print(f"🎯 ¡Ticket elegible detectado! {TICKET_ID} - {issue.fields.summary}")
        
        # Consolidamos los datos específicos del ticket actual para la IA
        contexto_ticket = f"TÍTULO DEL TICKET: {issue.fields.summary}\n"
        contexto_ticket += f"DESCRIPCIÓN INICIAL: {issue.fields.description}\n\n"
        contexto_ticket += "--- DISCUSIÓN Y COMENTARIOS DEL EQUIPO ---\n"
        
        for com in comentarios:
            contexto_ticket += f"- {com.author.displayName}: {com.body}\n"

        print(f"🧠 Procesando resumen con Qwen 3.6 para {TICKET_ID}...")
        
        # Llamada a Groq dentro del bucle para que se ejecute por cada ticket pendiente
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
                "reasoning_format": "hidden",
                "reasoning_effort": "none"
            },
            temperature=0.2
        )
        
        resumen_final = respuesta_ia.choices[0].message.content  # <- Corregido: Se agregó [0]

        
        # Inyección automatizada del comentario en Atlassian para el ticket actual
        print(f"🚀 Publicando comentario final en {TICKET_ID}...")
        comentario_formateado = f"📝 **[AI] RESUMEN DE CIERRE EJECUTIVO:**\n\n{resumen_final}"
        jira_client.add_comment(issue, comentario_formateado)
        print(f"✅ Ticket {TICKET_ID} completado.")

    print("\n🏁 Proceso de automatización finalizado para todo el lote de tickets.")

except Exception as e:
    print(f"❌ Error en el proceso general: {e}")
