import cv2
from utils.face_embedder import extract_face_embedding

def test_embedding(image_path):
    # Read image with OpenCV
    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load image at {image_path}")
        return
    
    embedding = extract_face_embedding(img)
    
    if embedding is None:
        print("Embedding extraction failed.")
    else:
        print(f"Embedding length: {len(embedding)}")
        print(f"Embedding snippet: {embedding[:5]}")  # print first 5 values

if __name__ == "__main__":
    test_image_path = r"C:\Users\aaa_f\Datasets\real faces\images (8).jpeg"  # update with your image path
    test_embedding(test_image_path)
