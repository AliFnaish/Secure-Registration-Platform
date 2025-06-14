from utils.utils import process_face, process_card
from db.vector_db import add_embedding_to_chroma
from chromadb import Client
from chromadb.config import Settings

def main():
    face_img_path = r"C:\Users\aaa_f\Datasets\real faces\0004_01.jpg"
    card_img_path = r"C:\Users\aaa_f\Project\Complete_System(v2)\Registration\assets\id_card.jpg"

    # Step 1: Extract embedding
    _, face_embedding = process_face(face_img_path)

    # Step 2: Extract user ID from ID card
    card_result = process_card(card_img_path)
    if not card_result:
        print("❌ Failed to extract ID card data.")
        return

    user_id = card_result.get("الاسم")  # or use "name" if you've mapped it

    if face_embedding is not None and user_id:
        # Step 3: Store in vector DB
        add_embedding_to_chroma(user_id, face_embedding)
        print(f"✅ Stored embedding for user: {user_id}")
    else:
        print("❌ Face embedding or user ID not found.")
        return

    # Step 4: Query ChromaDB with the same embedding
    print("\n🔍 Verifying ChromaDB Query...")

    client = Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="db/chroma"))
    collection = client.get_collection(name="face_embeddings")

    results = collection.query(
        query_embeddings=[face_embedding],
        n_results=1
    )

    print("🎯 Query Result:")
    print(results)

    if results and results["ids"][0][0] == user_id:
        print("✅ Verification successful: Matching user found in DB.")
    else:
        print("❌ Verification failed: No matching user found.")

if __name__ == "__main__":
    main()
