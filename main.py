from utils.utils import process_face, process_card
from db.database import create_table, insert_user, get_all_users
from db.vector_db import add_embedding_to_chroma

def main(face_path, card_path):
    _ , face_embedding = process_face(face_path)
    card_result = process_card(card_path)
    
    insert_user(
        name = card_result.get("name"),
        father_name = card_result.get("father_name"),
        family_name = card_result.get("family_name"),
        mother_name = card_result.get("mother_name"),
        place_birth = card_result.get("place_birth"),
        image_path = card_path,
        embedding = face_embedding  # Replace with actual embedding if available
    )
    
# Add embedding to ChromaDB vector store with a unique ID
user_id = card_result.get("name")  # or any unique ID
add_embedding_to_chroma(user_id, face_embedding)
    