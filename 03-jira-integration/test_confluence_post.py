import requests
import os

url = "https://prgjira.atlassian.net/wiki/rest/api/content"
token = os.environ.get("JIRA_API_TOKEN")

cuerpo_html = """
<p><strong>Origen del Ticket:</strong> <a href="https://prgjira.atlassian.net/browse/SCRUM-218">SCRUM-218</a></p>
<hr/>
<h3>💡 Resumen:</h3>
<p>Este es un resumen de prueba generado para SCRUM-218.</p>
<h3>💡 Lecciones Aprendidas:</h3>
<p>Esta es una lección aprendida de prueba.</p>
<br/>
<p><em>Página generada de forma autónoma por el ecosistema LLM.</em></p>
"""

payload = {
    "type": "page",
    "title": "TEST SCRUM-218 HTML",
    "space": {"key": "LA"},
    "body": {
        "storage": {
            "value": cuerpo_html,
            "representation": "storage"
        }
    }
}

respuesta = requests.post(
    url,
    json=payload,
    auth=("ingzane@gmail.com", token),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

print("STATUS:", respuesta.status_code)
print("RESPONSE:", respuesta.text)