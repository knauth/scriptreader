# ScriptReader
# June Knauth (github.com/knauth), 20230216
# PDF Handler/Parser

import sys
import pdfminer.high_level
import Spoken
import re
import unicodedata

class Parser():
    def __init__(self, path, first, last, people, line_delim, speak_delim, tone_delim):
        self.extract_text(path, first, last)
        self.parse(people, line_delim, speak_delim, tone_delim)

    # Parse extracted text
    def parse(self, people, line_delim, speak_delim, tone_delim):
        self.segments = []
        pars = self.raw_text.split(line_delim)
        self.pars_store = pars

        # For every paragraph
        for par in pars:
            try:
                is_line = False

                # Does this line begin with the name of a character followed by a delimiter?
                for c in people:
                    if par.lower().startswith(c + speak_delim) or par.lower().startswith(c + tone_delim):
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
            except:
                content = par
                speaker = None
                tone = None

            # Spoken stores content, speaker, tone, non-lines have no speaker or tone.
            # Lines have a speaker and optionally a tone
            seg = Spoken.Spoken(content, speaker, tone)
            self.segments.append(seg)

        self.cleanup_text()

    def cleanup_text(self):
        for i in self.segments:
            i.content = i.content.replace('\n', '')
            i.content = "".join(ch for ch in i.content if unicodedata.category(ch)[0]!="C")

    def extract_text(self, path, first, last):
        if first is not None and last is not None:
            self.raw_text = pdfminer.high_level.extract_text(path, page_numbers=range(first-1, last))
        else:
            self.raw_text = pdfminer.high_level.extract_text(path)

if __name__ == '__main__':
    import People
    p = People.People('people.ods')
    cast = p.people

    parser = Parser('crucible.pdf', 16, 17, cast, '\n\n', ':', ',')
