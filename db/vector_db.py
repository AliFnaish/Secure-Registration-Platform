from chromadb import PersistentClient

# Set up persistent ChromaDB client
client = PersistentClient(path="db/chroma")  # path to store the data

# Create or get the collection for face embeddings
collection = client.get_or_create_collection(name="face_embeddings")

def add_embedding_to_chroma(user_id: str, embedding: list):
    """
    Adds a normalized face embedding vector to ChromaDB collection with the user_id as ID.
    
    Args:
        user_id (str): Unique user identifier (e.g., username or database user ID).
        embedding (list): Normalized face embedding vector (list of floats).
    """
    
    collection.upsert(
        documents=[user_id],
        embeddings=[embedding],
        ids=[user_id]
    )
