# Enterprise LLM Application Engineering - Experimental Lab 🤖

Este repositorio es un entorno modular diseñado para la investigación, desarrollo y prueba de arquitecturas basadas en Inteligencia Artificial y Modelos de Lenguaje de Gran Escala (LLMs).

## 🗂️ Índice de Módulos del Laboratorio

Cada carpeta contiene un laboratorio independiente con su propio código fuente y documentación técnica detallada:

* **[📂 Módulo 01: Inferencia Básica y Control de Parámetros](./01-basic-inference/)**
  * Validación de conectividad con la API de Groq, selección de modelos de razonamiento lógico (`Qwen 3.6`) y técnicas iniciales de persistencia local de texto.
* **[📂 Módulo 02: Sistemas Multi-Agente Autónomos](./02-multi-agent-crew/)**
  * Orquestación de pipelines secuenciales utilizando **CrewAI**. Simulación de flujos de ingeniería de software con agentes especializados colaborativos (Product Owner + QA Engineer).

## 🛠️ Stack Tecnológico Global

* **Language:** Python 3.12 (Standard Stable Version)
* **Core Frameworks:** CrewAI & CrewAI Tools
* **Inference Platform:** Groq Cloud API
* **Security:** Python-Dotenv

## ⚙️ Inicialización General del Repositorio

Para replicar cualquiera de los laboratorios, clona este repositorio, configura tu entorno virtual en la raíz e instala las dependencias:

```bash
python -m venv venv
# Activar entorno (PowerShell Windows):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1

# Instalar dependencias globales:
pip install -r requirements.txt
```
Crea tu archivo `.env` en la raíz con tu `GROQ_API_KEY=tu_token` y navega a la carpeta del módulo que desees probar.
