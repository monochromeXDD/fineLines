# this uses a simple pdf text reader and saves the data to a local text file
# this can further be improved by using proper Document Loaders of other file formats too as given in the RAG Tut
# refer how-to-guides
'''doc = fitz.open(pdf_path)
pdf_path = "C:/Users/monochrome/Documents/finePrinter/test_doc.pdf"
output_path = "C:/Users/monochrome/Documents/finePrinter/text_out.txt"

with open(output_path, "w", encoding="utf-8") as f:
    for page_num, page in enumerate(doc):
        text = page.get_text()
        f.write(f"\n--- Page {page_num + 1} ---\n")
        f.write(text + "\n")
        print(text)
print("✅ Text extraction complete. Check text_out.txt.")
##
'''

from langchain_community.document_loaders import PyPDFLoader
import asyncio
pdf_path = "C:/Users/monochrome/Documents/finePrinter/test_doc.pdf"
loader = PyPDFLoader(pdf_path)
pages = []
async def main():
    async for page in loader.alazy_load():
        pages.append(page)

asyncio.run(main())
print(f"{pages[0].metadata}\n")
print(pages[0].page_content)

