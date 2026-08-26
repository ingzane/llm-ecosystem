# Módulo 03: Integración Avanzada con Atlassian (Jira & Confluence) 🎯

Este laboratorio implementa un pipeline de automatización asíncrono y condicional orientado a la auditoría técnica para managers. El sistema escanea el tablero de actividades de forma desatendida, genera resúmenes y extrae valor post-mortem utilizando Inteligencia Artificial.

## 🚀 Funcionalidades Clave

* **Escaneo Automatizado por Lotes:** Utiliza consultas JQL dinámicas para identificar de forma autónoma los últimos 10 tickets cerrados (`status = 'Done'`).
* **Filtro de Idempotencia Fijo:** Analiza el texto plano de los comentarios buscando la firma `[AI]`. Si el ticket ya fue procesado, evita la duplicación en Jira pero mantiene la evaluación para Confluence.
* **Extracción de Lecciones Aprendidas:** Configura un *System Prompt* de baja temperatura (`0.2`) en `Qwen 3.6` para aislar de forma estricta errores técnicos, bloqueos o sugerencias a futuro.
* **Desacoplamiento Arquitectónico (Confluence):** Aplica el Principio de Responsabilidad Única mediante un submódulo aislado (`publicar_confluence.py`) que inyecta documentación HTML nativa directo en el espacio corporativo `LA` de Confluence Cloud.

## 📁 Estructura del Módulo

* `resumen_cierre.py`: Orquestador principal del pipeline. Gestiona el ciclo de control, la extracción de comentarios de Jira y la llamada a Groq.
* `publicar_confluence.py`: Submódulo especializado de red. Realiza las peticiones HTTP POST nativas autenticadas para la creación de páginas wiki.

## 🔧 Configuración y Uso

Para ejecutar esta automatización, asegúrate de estar en la raíz del proyecto con el entorno virtual `(venv)` activo y lanza el script utilizando su ruta relativa:

```bash
python 03-jira-integration\resumen_cierre.py
```


## 📐 Arquitectura del Flujo Unificado (Jira ➡️ Confluence)

```text
                                       ARCHITECTURE DIAGRAM: MODULE 03
                     
┌──────────────────────┐             1. JQL Batch Query             ┌────────────────────────┐
│                      │ ─────────────────────────────────────────> │                        │
│                      │                                            │   Atlassian Jira API   │
│                      │ <───────────────────────────────────────── │    (Cloud Endpoint)    │
│                      │             2. Issues & Comments           └────────────────────────┘
│                      │
│                      │ ── 3. Idempotency Check ("[AI]" in body) ──┐
│                      │                                            │
│                      │ <──────────────────────────────────────────┘
│                      │
│                      │     [IF Ticket is Clean]
│  resumen_cierre.py   │ ─────────────────────────────────────────> ┌────────────────────────┐
│     (Python 3.12)    │             4. Compute Summary             │        Groq API        │
│                      │ <───────────────────────────────────────── │      (Qwen 3.6)        │
│                      │             5. Executive Text Block        └────────────────────────┘
│                      │
│                      │ ─────────────────────────────────────────> ┌────────────────────────┐
│                      │             6. Add Comment [AI]            │   Atlassian Jira API   │
│                      │                                            └────────────────────────┘
│                      │
│                      │     [IF "lecciones" in text (Always Evaluated)]
│                      │ ─────────────────────────────────────────> ┌────────────────────────┐
│                      │             7. Invoke Module               │ publicar_confluence.py │
└──────────────────────┘                                            └────────────────────────┘
                                                                                 │
                                                                                 │ 8. Native POST
                                                                                 │    (Basic Auth)
                                                                                 ▼
                                                                    ┌────────────────────────┐
                                                                    │  Atlassian Confluence  │
                                                                    │      (Space: LA)       │
                                                                    └────────────────────────┘
```
