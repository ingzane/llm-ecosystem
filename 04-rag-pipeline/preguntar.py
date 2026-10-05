import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer
from groq import Groq

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PATH = BASE_DIR / "chroma_db"

modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

groq_client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# --------------------------------------------------
# CHROMADB
# --------------------------------------------------

cliente_chroma = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

coleccion = cliente_chroma.get_collection(
    name="documentos_empresa"
)

# --------------------------------------------------
# BÚSQUEDA
# --------------------------------------------------

def buscar_documentos(pregunta, cantidad=3):

    embedding_pregunta = modelo_embeddings.encode(
        pregunta
    ).tolist()

    resultados = coleccion.query(
        query_embeddings=[embedding_pregunta],
        n_results=cantidad
    )

    return resultados

# --------------------------------------------------
# GENERACIÓN DE RESPUESTA
# --------------------------------------------------

def generar_respuesta(pregunta, documentos):

    contexto = "\n\n".join(
        f"Fragmento {i + 1}:\n{documento}"
        for i, documento in enumerate(documentos)
    )

    respuesta = groq_client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente que responde preguntas utilizando "
                    "exclusivamente la información proporcionada en los "
                    "fragmentos recuperados de los documentos internos.\n\n"
                    "Reglas obligatorias:\n"
                    "1. No utilices conocimiento externo.\n"
                    "2. No inventes información.\n"
                    "3. Si la respuesta no está contenida en los fragmentos, "
                    "responde exactamente: "
                    "'La información no está disponible en los documentos.'\n"
                    "4. Responde de forma clara y directa."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Pregunta:\n{pregunta}\n\n"
                    f"Información recuperada:\n{contexto}"
                )
            }
        ],
        extra_body={
            "reasoning_format": "hidden",
            "reasoning_effort": "none"
        },
        temperature=0.1
    )

    return respuesta.choices[0].message.content

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    pregunta = input("❓ Pregunta: ")

    resultados = buscar_documentos(pregunta)

    documentos = resultados["documents"][0]

 #   print("\n🔎 Fragmentos recuperados:\n")

 #   for i, documento in enumerate(documentos, start=1):
 #       print(f"--- Fragmento {i} ---")
 #       print(documento)
 #       print()

    respuesta = generar_respuesta(
        pregunta,
        documentos
    )

    print("\n🤖 Respuesta Qwen:\n")
    print(respuesta)