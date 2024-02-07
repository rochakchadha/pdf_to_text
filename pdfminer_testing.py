from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_text(input_path):
    output_string = StringIO()

    # Open a PDF file and read each page into a list
    #input_path = r'sample_files\1502.03167.pdf'
    # extract file name form input_path
    file_name = input_path.split('\\')[-1]
    print(f"File name: {file_name}")
    file_name_list = file_name.split('.')
    file_name_list = []
    with open(input_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page) # appends the page to the output_string
            file_name_list.append(output_string.getvalue()) # appends the page to the list
            output_string.truncate(0) # clears the string for the next page
        device.close()

    # convert each page to utf-8 encoding and remove the null characters, remove the lines with only 1 character
    for i in range(len(file_name_list)):
        file_name_list[i] = file_name_list[i].encode('utf-8').decode('utf-8').replace('\x00','')
        file_name_list[i] = '\n'.join([line for line in file_name_list[i].split('\n') if len(line) > 1])
    
    return file_name_list, file_name

def convert_pdf_to_text_clean(input_path, page_length=512, overlap=20):
    output_string = StringIO()

    # Open a PDF file and read each page into a list
    #input_path = r'sample_files\1502.03167.pdf'
    # extract file name form input_path
    file_name = input_path.split('\\')[-1]
    print(f"File name: {file_name}")
    file_name_list = file_name.split('.')
    file_name_list = []
    with open(input_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page) # appends the page to the output_string
            file_name_list.append(output_string.getvalue()) # appends the page to the list
            output_string.truncate(0) # clears the string for the next page
        device.close()

    # convert each page to utf-8 encoding and remove the null characters, 
    # remove the lines with only 1 character or with just a number like 60.3
    for i in range(len(file_name_list)):
        file_name_list[i] = file_name_list[i].encode('utf-8').decode('utf-8').replace('\x00','')
        file_name_list[i] = '\n'.join([line for line in file_name_list[i].split('\n') if len(line) > 1])
        file_name_list[i] = '\n'.join([line for line in file_name_list[i].split('\n') if not line.replace('.','',1).isdigit()])
    return file_name_list, file_name

    
# Recursively split the pages into smaller pages. Each page should be 
# upto page_length words long. The split pages should overlap by overlap words.
def split_page(page, page_length, overlap):
    if len(page.split()) <= page_length:
        return [page]
    else:
        words = page.split()
        split_page1 = ' '.join(words[:page_length])
        split_page2 = ' '.join(words[page_length-overlap:])
        return split_page(split_page1, page_length, overlap) + split_page(split_page2, page_length, overlap)
        
def split_pages(file_name_list, page_length, overlap):
# takes a list of pages as input, and returns a list of pages where 
# each page is upto page_length words long. The split pages should overlap by overlap words.    
    split_file_name_list = []
    for page in file_name_list:
        split_file_name_list += split_page(page, page_length, overlap)
    return split_file_name_list



# test code
def test_convert_pdf_to_text():
    #file_name_list, file_name = convert_pdf_to_text(r'sample_files\1502.03167.pdf')
    file_name_list, file_name = convert_pdf_to_text_clean(r'sample_files\1502.03167.pdf')
    file_name_list = split_pages(file_name_list, 512, 20)
    
    # check the number of words in each page
    
    word_count = 0
    page_count = 0
    for page in file_name_list:
        word_count += len(page.split())
        page_count += 1
        print(f"Page {page_count} has {len(page.split())} words")
    
    #write the output to a text file
    output_file_name = file_name.split('.pdf')[0]
    output_path = f'sample_files\\{output_file_name}.txt'
    print(f"Output path: {output_path}")
    with open(output_path, 'w', encoding ='utf-8') as out_file:
        for page in file_name_list:
            out_file.write(page)
    print(f"File {file_name} has {word_count} words in {page_count} pages")
    


if __name__ == "__main__":
    test_convert_pdf_to_text()
