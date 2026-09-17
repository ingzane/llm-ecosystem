# Enterprise LLM Application Engineering - Experimental Lab 🤖

Este repositorio contiene un entorno de desarrollo local (Laboratorio) diseñado para la investigación, diseño e implementación de aplicaciones avanzadas basadas en Modelos de Lenguaje de Gran Escala (LLMs) y arquitecturas orientadas a **Sistemas Multi-Agente Autónomos**.

El objetivo principal es la automatización de flujos de trabajo de ingeniería de software complejos mediante la orquestación cognitiva de IAs especializadas.

## 🛠️ Stack Tecnológico

* **Language:** Python 3.12 (Standard Stable Version)
* **Agent Framework:** CrewAI & CrewAI Tools
* **Inference Infrastructure:** Groq Cloud API (OpenAI-compatible connection interface)
* **Core Model:** Qwen 3.6 (27B Parameters) - *Reasoning Engine*
* **Security & Environment:** Python-Dotenv

## 📐 Arquitectura del Sistema (Subtask 2)

El laboratorio implementa un pipeline secuencial asíncrono donde dos agentes de IA con perfiles de ingeniería de software colaboran para transformar un requerimiento de negocio en entregables técnicos en menos de 30 segundos:

```text
  [ Requerimiento Vago ]
            │
            ▼
┌──────────────────────────────────────┐
│  Agente 1: Product Owner (Senior)     │ ──> Genera: Historia de Usuario (Gherkin)
└──────────────────────────────────────┘
            │
            │ (Output inyectado automáticamente como Contexto)
            ▼
┌──────────────────────────────────────┐
│  Agente 2: QA Engineer (Senior)      │ ──> Genera: Casos de Prueba Técnicos
└──────────────────────────────────────┘
            │
            ▼
  [ reporte_ingenieria.txt ] (Persistencia Física Local)
```

### Componentes Clave de la Arquitectura:
1. **Model Taming (Filtros de Razonamiento):** Configuración del payload del LLM mediante `extra_body` (`reasoning_format: hidden`, `reasoning_effort: none`) para inhabilitar el formateo de pensamiento largo del modelo de razonamiento lógico, asegurando outputs deterministas y estables.
2. **Encadenamiento de Contexto:** CrewAI gestiona la transferencia de datos entre el Analista y el QA sin intervención del usuario.
3. **Persistencia Automatizada:** El módulo final utiliza el sistema de archivos nativo de Python para volcar la sesión consolidada en un reporte físico `.txt`.

## 📁 Estructura del Proyecto

* `equipo_agentes.py`: Orquestador principal del pipeline multi-agente (CrewAI Core).
* `pregunta_ia.py`: Script base lineal de la Fase 1 para validación de conectividad.
* `lista_modelos.py`: Utilidad de auditoría dinámica para listar modelos permitidos en el servidor remoto.
* `requirements.txt`: Índice indexado de dependencias precompiladas para el entorno de producción.
* `.env`: Archivo aislado (protegido por `.gitignore`) para inyección de credenciales.

## 🔧 Configuración e Instalación (Windows / VS Code)

Sigue estos pasos secuenciales para replicar el laboratorio en tu entorno local:

1. **Clonar el repositorio y acceder a la carpeta:**
   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>
   ```

2. **Crear el entorno virtual aislado (Python 3.12):**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual en PowerShell (Desbloqueando políticas de ejecución):**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   .\venv\Scripts\Activate.ps1
   ```
   *(Verificarás que el indicador `(venv)` se muestra en verde al inicio de tu terminal).*

4. **Instalar las dependencias indexadas:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar las credenciales de seguridad:**
   Crea un archivo `.env` en la raíz del proyecto y agrega tu API Key de Groq:
   ```env
   GROQ_API_KEY=tu_gsk_token_aquí
   ```

6. **Ejecutar el pipeline de agentes autónomos:**
   ```bash
   python equipo_agentes.py
   ```

El sistema procesará las tareas y generará el archivo `reporte_ingenieria.txt` de forma automática.
