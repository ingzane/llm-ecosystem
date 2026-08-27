import os
from pathlib import Path
from dotenv import load_dotenv
from jira import JIRA
from groq import Groq
from publicar_confluence import crear_pagina_leccion # Importamos la función de publicación en Confluence desde el módulo externo

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
    # Buscamos los últimos 5 tickets cerrados
    tickets_cerrados = jira_client.search_issues(jql_automatizacion, maxResults=3)
    print(f"📋 Se encontraron {len(tickets_cerrados)} tickets en estado cerrado.")

    # [BUCLE PRINCIPAL]: Recorremos cada ticket detectado de forma automática
    for issue in tickets_cerrados:
        TICKET_ID = issue.key
        print(f"\nEvaluating ticket {TICKET_ID}...")

        # Traemos todos los comentarios de este ticket específico
        comentarios = jira_client.comments(issue)
        
        # 1. PASO A: Buscamos si el bot ya comentó antes en Jira
        comentario_ia_existente = None
        for com in comentarios:
            if "Resumen de cierre ejecutivo:" in com.body:
                comentario_ia_existente = str(com.body)  # <-- forzamos a string para evitar problemas de tipo
                break
        
        # Variable donde guardaremos el texto final para Confluence
        resumen_final = ""

        # 2. PASO B: Evaluación y Escritura en Jira
        if not comentario_ia_existente:
            print(f"🎯 ¡Ticket sin resumir detectado! {TICKET_ID} - {issue.fields.summary}")
            
            contexto_ticket = f"TÍTULO DEL TICKET: {issue.fields.summary}\n"
            contexto_ticket += f"DESCRIPCIÓN INICIAL: {issue.fields.description}\n\n"
            contexto_ticket += "--- DISCUSIÓN Y COMENTARIOS DEL EQUIPO ---\n"
            for com in comentarios:
                contexto_ticket += f"- {com.author.displayName}: {com.body}\n"

            print(f"🧠 Procesando resumen con Qwen 3.6 para {TICKET_ID}...")
            respuesta_ia = groq_client.chat.completions.create(
                model="qwen/qwen3.6-27b",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "Eres un auditor técnico senior de Jira. Tu único objetivo es redactar un resumen ejecutivo "
                            "y directo de lo que se hizo y resolvió en el ticket, basándote exclusivamente en la discusión provista.\n\n"
                            "REGLAS OBLIGATORIAS DE NEGOCIO:\n"
                            "1. Prohibido incluir fechas de actualizaciones.\n"
                            "2. Prohibido incluir historiales de cambios mecánicos.\n"
                            "3. Prohibido inventar o rellenar información sin sentido (sin alucinaciones).\n"
                            "4. Estructura el output estrictamente en dos partes:\n"
                            "   - Parte 1: Un párrafo corto con el resumen directo de lo que se hizo.\n"
                            "   - Parte 2: Si en los comentarios se detectan errores o consejos técnicos a futuro, agrega una sección titulada exactamente 'Lecciones aprendidas:' seguida de las recomendaciones. Si no hay, omite esta sección.\n"
                            "5. El tono debe ser profesional y directo al grano."
                        )
                    },
                    {
                        "role": "user", 
                        "content": f"Por favor, genera el resumen de cierre para el siguiente ticket:\n\n{contexto_ticket}"
                    }
                ],
                extra_body={"reasoning_format": "hidden", "reasoning_effort": "none"},
                temperature=0.2
            )
            
            resumen_final = respuesta_ia.choices[0].message.content
            
            print(f"🚀 Publicando comentario final en {TICKET_ID}...")
            comentario_formateado = f"Resumen de cierre ejecutivo:\n\n{resumen_final}"
            jira_client.add_comment(issue, comentario_formateado)
            print(f"✅ Ticket {TICKET_ID} resumido en Jira.")
        else:
            print(f"⏭️ El ticket {TICKET_ID} ya tiene resumen en Jira. Extraeremos el texto existente para evaluar Confluence.")
            resumen_final = comentario_ia_existente  # Ahora esto es un STRING real

        # 3. PASO C: FLUJO DE CONFLUENCE (A prueba de fallos)
        if "lecciones aprendidas" in resumen_final.lower():
            print(f"💡 Se detectaron Lecciones Aprendidas en {TICKET_ID}. Exportando a Confluence...")
            
            # Separamos el texto de forma segura usando minúsculas
            import re
            partes = re.split(r'(?i)lecciones aprendidas:', resumen_final)
            resumen_puro = re.sub(r'(?i)^Resumen de cierre ejecutivo:\s*', '', partes[0]).strip() # Saco el titulo inicial si existe
            lecciones_puras = partes[1].strip() if len(partes) > 1 else ""
            
            # Invocamos el script externo de Confluence
            crear_pagina_leccion(
                ticket_id=TICKET_ID,
                titulo_ticket=issue.fields.summary,
                contenido_resumen=resumen_puro,
                contenido_lecciones=lecciones_puras
            )
        else:
            print(f"☕ No hay lecciones aprendidas que exportar para el ticket {TICKET_ID}.")

except Exception as e:
    print(f"❌ Error en el proceso general: {e}")
