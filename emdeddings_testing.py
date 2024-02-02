from pdfminer_testing import convert_pdf_to_text
import os
import chromadb

# Iterate through all the PDFs in the directory and convert them to text.
# Return a list of the text from each PDF. Texts are returned in text list, 
# and the source of each text is returned in the sources list.
def get_text_from_pdfs(directory):
    text = []
    sources = [] # list of strings, each string is the name of a PDF
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            text_file= convert_pdf_to_text(directory + filename)[0]
            source_list = [f"{filename}_page: {i+1}" for i in range(len(text_file))]
            #print (f"source_list: {source_list}")
            text+=text_file
            sources+=source_list
    return text, sources

text, sources = get_text_from_pdfs("sample_files/") 
print(f"Number of texts: {len(text)}")
print(f"Number of sources: {len(sources)}")

chroma_client = chromadb.Client()
collection = chroma_client.create_collection("test_collection")

# create a list of sources dictionaries
sources_list = []
for source in sources:
    sources_list.append({"source": source})

# create a list of ids for the inserted documents
ids_list = []
for i in range(len(text)):
    ids_list.append(str(i+1))
print(f"Number of ids: {len(ids_list)}")

# insert the documents into the collection
collection.add(
    documents=text,
    ids=ids_list,
    metadatas=sources_list
)
print(collection.peek(5))