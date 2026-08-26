import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Cargamos el entorno seguro desde la raíz
ruta_raiz = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ruta_raiz / ".env")

def crear_pagina_leccion(ticket_id, titulo_ticket, contenido_resumen, contenido_lecciones):

    JIRA_SERVER = "https://prgjira.atlassian.net"
    JIRA_USER = "ingzane@gmail.com"
    JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
    
    # IMPORTANTE: Aquí va la clave en letras de tu espacio (ej: "DS", "SCRUM", etc.)
    SPACE_KEY = "LA" 

    print(f"📄 [CONFLUENCE] Iniciando publicación para el ticket {ticket_id}...")
    
    # Endpoint oficial de la API v1 (Acepta el prefijo /wiki de forma estricta)
    url_confluence = f"{JIRA_SERVER}/wiki/rest/api/content"
    
    # Estructura del documento HTML para Confluence
    cuerpo_html = f"""
    <p><strong>Origen del Ticket:</strong> <a href="{JIRA_SERVER}/browse/{ticket_id}">{ticket_id}</a></p>
    <hr/>
    <h3>💡 Resumen:</h3>
    <p>{contenido_resumen.replace('\n', '<br/>')}</p>

    <h3>💡 Lecciones Aprendidas:</h3>
    <p>{contenido_lecciones.replace('\n', '<br/>')}</p>

    <br/>
    <p><em>Página generada de forma autónoma por el ecosistema LLM.</em></p>
    """
    
    # Payload oficial estructurado para la API v1
    payload = {
        "type": "page",
        "title": f"{ticket_id} - {titulo_ticket}",
        "space": {"key": SPACE_KEY},
        "body": {
            "storage": {
                "value": cuerpo_html,
                "representation": "storage"
            }
        }
    }

    print("USER:", JIRA_USER)
    print("TOKEN:", "OK" if JIRA_API_TOKEN else "NO ENCONTRADO")
    
    try:
        # Realizamos la petición POST usando autenticación HTTP Básica nativa de requests
        respuesta = requests.post(
            url_confluence,
            json=payload,
            auth=(JIRA_USER, JIRA_API_TOKEN),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        
        # Validamos los códigos de éxito (200 o 201)
        if respuesta.status_code in [200, 201]:
            print(f"✅ [CONFLUENCE] ¡Página creada con éxito en el espacio '{SPACE_KEY}'!")
            return True
        else:
            print(f"❌ [CONFLUENCE] Error de API ({respuesta.status_code}): {respuesta.text}")
            return False
            
    except Exception as e:
        print(f"❌ [CONFLUENCE] Error crítico en el módulo de publicación: {e}")
        return False

