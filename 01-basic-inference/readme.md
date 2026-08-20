# LLM Application Engineering - Experimental Lab 🤖

Este repositorio contiene el entorno experimental (Laboratorio) diseñado para el desarrollo, prueba y despliegue de aplicaciones basadas en Modelos de Lenguaje de Gran Escala (LLMs) y arquitecturas orientadas a agentes. El enfoque principal es la integración segura de modelos de inteligencia artificial en flujos de trabajo empresariales y automatizaciones locales.

## 🛠️ Stack Tecnológico

* **Language:** Python 3.12+
* **Inference Infrastructure:** Groq Cloud API
* **Core Model:** Qwen 3.6 (27B Parameters) - *Reasoning Engine*
* **Configuration & Security:** Python-Dotenv

## 📁 Estructura del Módulo (Fase 1)

* `pregunta_ia.py`: Pipeline principal que gestiona la conexión con la API de inferencia, aplica filtros de control de respuesta y automatiza la persistencia física local.
* `lista_modelos.py`: Script de auditoría dinámica para consultar el inventario de modelos activos y disponibles en el servidor remoto.
* `.env`: Archivo local y aislado para la inyección de credenciales mediante variables de entorno (excluido de control de versiones).

## 🚀 Arquitectura y Buenas Prácticas Implementadas

1. **Gestión Segura de Credenciales (Enterprise Ready):** Implementación de variables de entorno mediante `python-dotenv` y aislamiento de secretos usando `.gitignore` para cumplir con las políticas de *Push Protection* de GitHub.
2. **Control de Razonamiento Nativo (Model Taming):** Configuración avanzada del *payload* mediante parámetros nativos (`reasoning_format="hidden"`) para apagar el modo de pensamiento largo del modelo de razonamiento lógico, garantizando respuestas deterministas, cortas y predecibles.
3. **Persistencia Física Automatizada:** Flujo automatizado de captura de *outputs* que interactúa directamente con el sistema de archivos local, exportando las respuestas validadas a archivos planos `.txt`.

## 🔧 Configuración e Instalación

1. Clonar el repositorio.
2. Crear un archivo `.env` en la raíz del proyecto e inyectar tu API Key:
   ```env
   GROQ_API_KEY=tu_gsk_token_aqui
   ```
3. Instalar las dependencias requeridas:
   ```bash
   pip install groq python-dotenv
   ```
4. Ejecutar el pipeline de prueba:
   ```bash
   python pregunta_ia.py
   ```
