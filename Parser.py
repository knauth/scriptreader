# ScriptReader
# June Knauth (github.com/knauth), 20230216
# PDF Handler/Parser

import sys
import pdfminer.high_level
import Spoken

class Parser():
    def __init__(self, path, first, last, people, line_delim, speak_delim, tone_delim):
        self.extract_text(path, first, last)
        self.parse(people, line_delim, speak_delim, tone_delim)

    def parse(self, people, line_delim, speak_delim, tone_delim):
        self.segments = []
        pars = self.raw_text.split(line_delim)


        for par in pars:
            is_line = False

            for c in people:
                if par.lower().startswith(c):
                    is_line = True
                    speaker = c

            if not is_line:
                speaker = None
                tone = None
                content = par

            else:
                pre, content = par.split(speak_delim, 1)

                if tone_delim in pre:
                    speaker, tone = pre.split(tone_delim, 1)

                else:
                    speaker = pre
                    tone = None

            seg = Spoken.Spoken(content, speaker, tone)
            self.segments.append(seg)


    def extract_text(self, path, first, last):
        if first is not None and last is not None:
            self.raw_text = pdfminer.high_level.extract_text(path, page_numbers=range(first-1, last))
        else:
            self.raw_text = pdfminer.high_level.extract_text(path)

if __name__ == '__main__':
    import People
    p = People.People('people.ods')
    cast = p.people

    parser = Parser('crucible.pdf', 16, 16, cast, '\n\n', ':', ',')
