# ScriptReaader
# June Knauth (knauth), 20230214

import nltk
import sys
from pdfminer.high_level import extract_text

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

try:
    input_pdf = sys.argv[1]
except:
    print("Error: No file provided")
    # raise Exception

#pdf_text = extract_text(input_pdf)
with open("./text") as f:
    pdf_text = f.read()

tokens = nltk.word_tokenize(pdf_text)
tagged = nltk.pos_tag(tokens)
entities = nltk.chunk.ne_chunk(tagged)

for en in entities:
    print(en)
    if en.label() == 'PERSON':
        print(en)