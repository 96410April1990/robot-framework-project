from pdf2image import convert_from_path
from PIL import Image
import pytesseract

def convert_pdf_to_image(pdfFilePath, imgFilePath):
    pages = convert_from_path(pdfFilePath, 500)
    
    for i, page in enumerate(pages):
        image_file = f"{imgFilePath}_{i}.jpg"
        page.save(image_file, 'JPEG')
        # Apply OCR to the image
        text = pytesseract.image_to_string(Image.open(image_file))
        return text
