from pdf2docx import Converter # type: ignore

def convert_pdf_to_docx(pdf_file, docx_file):
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()

#convert_pdf_to_docx('/Users/r0n01gu/Documents/TM/Agenda/Meeting No. 931 Agenda.pdf', '/Users/r0n01gu/Documents/TM/Agenda/Meeting-No.932-Agenda.docx')

convert_pdf_to_docx('/Users/r0n01gu/Downloads/Resume-Rohith-N-Updated.pdf', '/Users/r0n01gu/Downloads/Resume-Rohith-N-Updated.docx')
