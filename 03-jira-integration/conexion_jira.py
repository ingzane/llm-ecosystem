import os
from pathlib import Path  # Manejo de rutas nativo de Python
from dotenv import load_dotenv
from jira import JIRA

# 1. Calculamos la ruta exacta a la raíz del proyecto para encontrar el .env
ruta_raiz = Path(__file__).resolve().parent.parent
ruta_env = ruta_raiz / ".env"

# Cargamos el archivo usando su ruta absoluta verificada
load_dotenv(dotenv_path=ruta_env)

# 2. Configuramos los parámetros de conexión con Atlassian
JIRA_SERVER = "https://prgjira.atlassian.net/"
JIRA_USER = "ingzane@gmail.com"
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")

# --- LÍNEAS DE AUDITORÍA ---
print(f"DEBUG -> Correo cargado: {JIRA_USER}")
print(f"DEBUG -> ¿El Token está vacío?: {JIRA_API_TOKEN is None}")
if JIRA_API_TOKEN:
    print(f"DEBUG -> Primeros 5 caracteres del Token: {JIRA_API_TOKEN[:5]}")


# 3. Inicializamos el cliente oficial de Jira con tu autenticación básica
jira_client = JIRA(
    server=JIRA_SERVER,
    basic_auth=(JIRA_USER, JIRA_API_TOKEN)
)

print("✅ ¡Conexión inicial configurada!")

# 4. Consulta JQL definitiva para traer tus últimos 5 tickets
# "assignee = currentUser()" filtra solo tus tareas asignadas
jql_query = "assignee = currentUser() order by created DESC"

print("\n🔍 Buscando tus tickets asignados más recientes...")

try:
    # Ejecutamos la búsqueda a través de la API oficial
    tickets = jira_client.search_issues(jql_query, maxResults=5)
    
    print(f"--- ÚLTIMOS TICKETS DETECTADOS ({len(tickets)}) ---")
    
    # Recorremos la lista y mostramos la clave y el título
    for ticket in tickets:
        print(f"- [{ticket.key}] {ticket.fields.summary}")
        
    if len(tickets) == 0:
        print("💡 Conexión exitosa, pero no tienes tareas asignadas a tu nombre en este momento.")
        
except Exception as e:
    print(f"❌ Error al consultar Jira: {e}")


