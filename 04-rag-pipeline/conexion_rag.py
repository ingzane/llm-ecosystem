import chromadb

CHROMA_PATH = "./chroma_db"

cliente_chroma = chromadb.PersistentClient(
    path=CHROMA_PATH
)

coleccion = cliente_chroma.get_or_create_collection(
    name="documentos_empresa"
)

print("✅ Conexión con ChromaDB establecida.")
print(f"📚 Documentos indexados: {coleccion.count()}")