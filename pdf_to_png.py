import fitz
import os

# Function to convert PDF to PNG
def pdf_to_png(pdf_path, output_folder, dpi=300):
    # Check if the provided PDF path exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    # Loop through each page of the PDF
    for page_num in range(len(doc)):
        # Load the current page
        page = doc.load_page(page_num)
        
        # Create a pixmap (image) of the current page
        pixmap = page.get_pixmap(dpi=dpi)
        
        # Define the output file path
        output_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        
        # Save the image as PNG
        pixmap.save(output_path)
        print(f"Page {page_num + 1} saved as {output_path}")
    
    # Close the PDF file
    doc.close()
    print("PDF to PNG conversion completed!")

# Example usage
# pdf_path = "Offer_Letter_-_BM.pdf" # Replace with actual name of the input PDF document
# output_folder = "Offer_Letter_-_BM.png" # Replace with actual name of the output PNG document
# pdf_to_png(pdf_path, output_folder)
