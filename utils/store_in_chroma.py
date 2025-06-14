from utils.face_embedder import extract_face_embedding
from db.vector_db import add_embedding_to_chroma

def store_embedding_in_chroma(image_path, user_id, metadata=None):
    embedding = extract_face_embedding(image_path)
    if embedding is None:
        print("❌ Embedding extraction failed.")
        return

    # Add embedding to chroma using vector_db.py function
    add_embedding_to_chroma(user_id, embedding)
    print(f"✅ Successfully stored embedding for user: {user_id}")
