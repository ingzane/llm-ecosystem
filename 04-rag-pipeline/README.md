# Módulo 04 - Implementación de Canal de Datos Indexados - RAG Local

Sistema RAG (Retrieval-Augmented Generation) construido con Python.

El objetivo es permitir que un LLM responda preguntas utilizando información contenida en documentos internos.

## Arquitectura

```text
DOCUMENTOS
    ↓
CHUNKING
    ↓
EMBEDDINGS LOCALES
    ↓
CHROMADB
    ↓
PREGUNTA
    ↓
RETRIEVAL
    ↓
CHUNKS RELEVANTES
    ↓
QWEN / GROQ
    ↓
RESPUESTA
```

## Estructura

```text
04-rag-pipeline/
│
├── documentos/
│   └── manual.txt
│
├── chroma_db/
│
├── conexion_rag.py
├── ingest.py
├── preguntar.py
└── README.md
```

## Tecnologías

* Python
* Sentence Transformers
* `all-MiniLM-L6-v2`
* ChromaDB
* Qwen
* Groq

## Funcionamiento

### Ingesta

`ingest.py`:

1. Lee los documentos.
2. Divide el contenido en chunks.
3. Genera embeddings localmente.
4. Guarda los embeddings y documentos en ChromaDB.

Configuración actual:

```python
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

### Consulta

`preguntar.py`:

1. Recibe una pregunta.
2. Genera su embedding.
3. Busca los 3 chunks más relevantes en ChromaDB.
4. Envía esos chunks junto con la pregunta a Qwen.
5. Qwen genera la respuesta utilizando el contexto recuperado.

Si la información no está disponible en los documentos:

```text
La información no está disponible en los documentos.
```

## Ejecución

Primero ejecutar la ingesta:

```bash
python ingest.py
```

Después realizar consultas:

```bash
python preguntar.py
```

## Configuración

Groq requiere:

```text
GROQ_API_KEY=tu_token
```

La API key no debe almacenarse directamente en el código ni en Git.

## Estado

* Ingesta: completada
* Chunking: completado
* Embeddings locales: completado
* ChromaDB: completado
* Retrieval: completado
* Generación con Qwen: completado

## Próximos pasos

* Mejorar el chunking.
* Añadir soporte para más formatos de documentos.
* Mejorar el retrieval.
* Preparar una futura ejecución en infraestructura externa.
