from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTOS_DIR = BASE_DIR / "documentos"
CHROMA_PATH = BASE_DIR / "chroma_db"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Modelo de embeddings local
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------------------------------
# CHROMADB
# --------------------------------------------------

cliente_chroma = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

coleccion = cliente_chroma.get_or_create_collection(
    name="documentos_empresa"
)

# --------------------------------------------------
# CHUNKING
# --------------------------------------------------

def crear_chunks(texto):
    chunks = []

    inicio = 0

    while inicio < len(texto):
        fin = inicio + CHUNK_SIZE

        chunk = texto[inicio:fin].strip()

        if chunk:
            chunks.append(chunk)

        inicio += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks

# --------------------------------------------------
# INGESTA
# --------------------------------------------------

def procesar_documento(ruta_documento):

    print(f"📄 Procesando: {ruta_documento.name}")

    texto = ruta_documento.read_text(
        encoding="utf-8"
    )

    chunks = crear_chunks(texto)

    print(f"✂️ Chunks creados: {len(chunks)}")

    embeddings = modelo_embeddings.encode(
        chunks
    ).tolist()

    ids = [
        f"{ruta_documento.stem}-{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
        {
            "source": ruta_documento.name
        }
        for _ in chunks
    ]

    coleccion.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Documento indexado: {ruta_documento.name}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    archivos = list(DOCUMENTOS_DIR.glob("*.txt"))

    if not archivos:
        print("⚠️ No se encontraron documentos.")
    else:
        for archivo in archivos:
            procesar_documento(archivo)

    print()
    print(f"📚 Total de chunks en ChromaDB: {coleccion.count()}")