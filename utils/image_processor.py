import base64
from io import BytesIO

def image_to_base64(image):
    # Convert image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str