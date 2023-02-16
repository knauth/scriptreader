# ScriptReader
# June Knauth (github.com/knauth), 20230214

import sys
import Parser
import People
import Spoken

try:
    input_pdf = sys.argv[1]
except:
    pass
    # print("Error: No file provided")
    # raise Exception

#pdf_text = extract_text(input_pdf)
with open("./text") as f:
    pdf_text = f.read()

p = People.People('people.ods')
cast = p.people

parser = Parser.Parser('crucible.pdf', 16, 16, cast, '\n\n', ':', ',')
parser.parse()
