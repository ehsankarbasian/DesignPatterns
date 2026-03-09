
# Abstract Product
class Document:
    def render(self):
        raise NotImplementedError

    # Concrete factory method
    @classmethod
    def create(cls, doc_type):
        if doc_type == "pdf":
            return PDFDocument()
        if doc_type == "word":
            return WordDocument()

        raise ValueError("Unsupported document type")


# Concrete products
class PDFDocument(Document):
    def render(self):
        print("Rendering PDF")

class WordDocument(Document):
    def render(self):
        print("Rendering Word document")


# Client
doc = Document.create("pdf")
doc.render()
