#we’ll split the Document into chunks for embedding and vector storage.
#we use a RecursiveCharacterTextSplitter, which will recursively split the document using common separators like new lines until each chunk is the appropriate size. This is the recommended text splitter for generic text use cases.
#this is simple document splitting method using common separatos, there are also other more efficient methods for larger files, read how-to-guides or RAG tut on langchain
#gaand fat gyi is sab ki theory samajhne mein
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdfLoader import pages #importing the page list format which contains the raw extracted data from the pdf 
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 400,
    add_start_index=True,
)
all_splits = text_splitter.split_documents(pages)
print(f"split the pdf into: {len(all_splits)} sub-documents")
