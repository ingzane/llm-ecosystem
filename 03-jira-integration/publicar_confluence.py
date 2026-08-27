import os
import time
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

    # Clave del espacio de Confluence
    SPACE_KEY = "LA"

    print(f"📄 [CONFLUENCE] Iniciando publicación para el ticket {ticket_id}...")

    # Endpoint oficial de la API v1
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

    titulo_pagina = f"{ticket_id} - {titulo_ticket}"

    payload = {
        "type": "page",
        "title": titulo_pagina,
        "space": {"key": SPACE_KEY},
        "body": {
            "storage": {
                "value": cuerpo_html,
                "representation": "storage"
            }
        }
    }

    try:
        time.sleep(3)
        # Sesión HTTP independiente para Confluence
        with requests.Session() as session:
            respuesta = session.post(
                url_confluence,
                json=payload,
                auth=(JIRA_USER, JIRA_API_TOKEN),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Connection": "close"
                },
                timeout=30
            )

        # Página creada correctamente
        if respuesta.status_code in [200, 201]:
            print(
                f"✅ [CONFLUENCE] ¡Página creada con éxito "
                f"en el espacio '{SPACE_KEY}'!"
            )
            return True

        # Página ya existente
        elif (
            respuesta.status_code == 400
            and "already exists" in respuesta.text.lower()
        ):
            print(
                f"⏭️ [CONFLUENCE] La página '{titulo_pagina}' "
                f"ya existe. Se omite la publicación."
            )
            return True

        # Cualquier otro error de API
        else:
            print(
                f"❌ [CONFLUENCE] Error de API "
                f"({respuesta.status_code}): {respuesta.text}"
            )
            return False

    except Exception as e:
        print(
            f"❌ [CONFLUENCE] Error crítico en el módulo "
            f"de publicación: {e}"
        )
        return False

