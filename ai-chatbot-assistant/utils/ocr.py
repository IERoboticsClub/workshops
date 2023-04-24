import os
from io import StringIO
from sentence_transformers import SentenceTransformer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def ocr_files(tempDir):
    """This function reads the pdfs and returns a dictionary of sentences"""
    sentences = {}
    books = os.listdir(tempDir)
    
    for book in books:
        with open(f'{tempDir}/{book}', 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            sentences[book] = {}
            for i, page in enumerate(PDFPage.create_pages(doc)):
                output_string = StringIO()
                device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                interpreter.process_page(page)
                text = output_string.getvalue()
                sentences[book][i] = text.replace(".  \n", ".\n").split(".\n")
                for sentence in sentences[book][i]:
                    sentence_processed = sentence.replace("\n", "").replace("  ", " ").replace("-", "")
                    sentences[book][i][sentences[book][i].index(sentence)] = sentence_processed
            output_string.truncate(0)
            output_string.seek(0)
    return sentences


def load_tokenizer(preference="quality"):
    """This function loads the tokenizer"""
    if preference == "quality":
        model = SentenceTransformer('all-mpnet-base-v2')
    elif preference == "speed":
     model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
    elif preference == "more_speed":
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    return model


def get_embedding(model, sentence):
    """This function returns the embedding of a sentence"""
    embedding = model.encode(sentence)
    return embedding


def get_db_schema(sentences, preference="quality"):
    """This function returns a dictionary with all db schema values (including embeddings) for each sentence"""
    aux_dict = dict()
    model = load_tokenizer(preference)
    for doc in sentences.keys():
        for page in sentences[doc].keys():
            for sentence in sentences[doc][page]:
                embedded_text = get_embedding(model, sentence)
                print(len(embedded_text))
                aux_dict[str(doc + str(page) + sentence)] = [str(doc + str(page) + sentence), str(page), doc, sentence, embedded_text]
    return aux_dict