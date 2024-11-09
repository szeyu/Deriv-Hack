import os
from PIL import Image
import numpy as np
from utils.image_vectorizer import image_to_vector

def compare_images(uploaded_image_path):
    image1 = Image.open(uploaded_image_path)
    vector1 = image_to_vector(image1)

    similarities = {}
    for filename in os.listdir("other_similar"):
        if filename.endswith(".png"):
            image_path = os.path.join("other_similar", filename)
            image2 = Image.open(image_path)
            vector2 = image_to_vector(image2)
            similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
            similarities[filename] = similarity

    print("Similarities:")
    for key, value in similarities.items():
        print(f"{key}: {value:.3f}")

    highest_similarity_file = max(similarities, key=similarities.get)
    highest_similarity = similarities[highest_similarity_file]

    return highest_similarity_file, highest_similarity