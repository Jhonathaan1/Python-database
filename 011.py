import fitz  # PyMuPDF
from docx import Document
from tkinter import Tk, filedialog, Button, Label

class PDFtoWordConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Word Converter")

        self.pdf_path = ""
        self.word_path = ""

        self.label = Label(root, text="Selecione o arquivo PDF:")
        self.label.pack()

        self.btn_browse = Button(root, text="Procurar", command=self.browse_pdf)
        self.btn_browse.pack()

        self.btn_convert = Button(root, text="Converter", command=self.convert_pdf_to_word)
        self.btn_convert.pack()

    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        self.label.config(text=f"Arquivo PDF selecionado: {self.pdf_path}")

    def convert_pdf_to_word(self):
        if not self.pdf_path:
            self.label.config(text="Por favor, selecione um arquivo PDF.")
            return

        self.word_path = filedialog.asksaveasfilename(defaultextension=".docx",
                                                        filetypes=[("Arquivos Word", "*.docx")])

        pdf_to_word(self.pdf_path, self.word_path)
        self.label.config(text=f"Conversão concluída. O Word foi salvo em: {self.word_path}")

def pdf_to_word(pdf_path, word_path):
    doc = Document()
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text = page.get_text("text")
        doc.add_paragraph(text)

    doc.save(word_path)

    print(f"Conversão concluída. O Word foi salvo em: {word_path}")

if __name__ == "__main__":
    root = Tk()
    converter = PDFtoWordConverter(root)
    root.mainloop()
