import pytesseract
from PIL import Image

# Specify the correct path to tesseract
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Update according to your system

# Example to run OCR on an image
img = Image.open('WhatsApp Image 2024-11-09 at 14.23.31.jpeg') # Change input image for Pytesseract OCR
text = pytesseract.image_to_string(img)
print(text)
