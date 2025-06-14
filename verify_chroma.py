from chromadb import PersistentClient
import numpy as np

def verify_chroma():
    client = PersistentClient(path="db/chroma")

    print("Collections in ChromaDB:")
    collections = client.list_collections()
    for col in collections:
        print(f"- {col.name}")

    if not collections:
        print("No collections found! Make sure you inserted and persisted data.")
        return

    collection = client.get_collection(name=collections[0].name)

    dummy_embedding = np.random.rand(128).tolist()

    results = collection.query(
        query_embeddings=[dummy_embedding],
        n_results=1
    )

    print("Query results:", results)

if __name__ == "__main__":
    verify_chroma()
