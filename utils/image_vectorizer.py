from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image

# Load the model and processor (this can be done once and reused)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def image_to_vector(image: Image.Image):
    # Preprocess the image
    inputs = processor(images=image, return_tensors="pt", padding=True)

    # Generate the image embedding
    with torch.no_grad():
        image_features = model.get_image_features(**inputs)

    # Convert to numpy array and flatten
    image_vector = image_features.numpy().flatten()

    return image_vector