# ScriptReader
# June Knauth (github.com/knauth), 20230214

import sys
from pdfminer.high_level import extract_text
import pandas as pd

class Spoken():
    def __init__(self, content):
        self.content = content

class Line(Spoken):
    def __init__(self, content, speaker, tone):
        Spoken.__init__(content)
        self.speaker = speaker
        self.tone = tone

try:
    input_pdf = sys.argv[1]
except:
    pass
    # print("Error: No file provided")
    # raise Exception

#pdf_text = extract_text(input_pdf)
with open("./text") as f:
    pdf_text = f.read()

people = pd.read_excel("./people.ods")

