import PyPDF2

def extract_data_from_pdf(file_path):
    pdf_file_obj = open(file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    num_pages = len(pdf_reader.pages)
    text = []
    
    for page in range(num_pages):
        page_obj = pdf_reader.pages[page]
        text.append(page_obj.extract_text())
    pdf_file_obj.close()
    
    return text