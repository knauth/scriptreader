# ScriptReader
# June Knauth (github.com/knauth), 20230216
# PDF Handler/Parser

import sys
import pdfminer.high_level
import Spoken
import re
import unicodedata

MIN_CHAR_OCCURENCES = 2

class Parser():
    def __init__(self, path, first, last, line_delim, speak_delim, tone_delim):
        full_text = self.extract_text(path, None, None)
        self.find_characters(full_text, line_delim, speak_delim, tone_delim)

        pages_text = self.extract_text(path, first, last)
        self.parse(pages_text, self.people, line_delim, speak_delim, tone_delim)

    # Find characters. Look for the speaker delimiter, and count the number
    # of occurences of the string which precedes in the entire text.
    # Strings above a certain number of occurences are probably characters
    # Write that to a file to let the user edit the voices
    def find_characters(self, raw_text, line_delim, speak_delim, tone_delim):
        self.segments = []
        pars = raw_text.split(line_delim)
        candidates = {}
        people = []

        # For every paragraph
        for par in pars:
            parl = par.lower()
            # RegEx match for speaker or tone delimiter
            pattern = re.compile(f"^(.*?)([{speak_delim}{tone_delim}]).*")
            match = re.search(pattern, parl)

            if match:
                cand = match.group(1) # Everything before whichever comes first
                candidates[cand] = candidates.get(cand, 0) + 1 # Count

        # Find people
        self.candidates = candidates
        for k, v in candidates.items():
            if v > MIN_CHAR_OCCURENCES:
                people.append(k)

        self.people = people

    # Parse extracted text
    def parse(self, raw_text, people, line_delim, speak_delim, tone_delim):
        self.segments = []
        pars = raw_text.split(line_delim)
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
        self.cleanup_speaker()

    def cleanup_speaker(self):
        for i in self.segments:
            if i.speaker is not None:
                i.speaker = i.speaker.rstrip()
                i.speaker = i.speaker.lstrip()
                i.speaker = "".join(ch for ch in i.speaker if unicodedata.category(ch)[0]!="C")

    def cleanup_text(self):
        for i in self.segments:
            i.content = i.content.replace('\n', '')
            i.content = "".join(ch for ch in i.content if unicodedata.category(ch)[0]!="C")

    def extract_text(self, path, first, last):
        if first is not None and last is not None:
            return pdfminer.high_level.extract_text(path, page_numbers=range(first-1, last))
        else:
            return pdfminer.high_level.extract_text(path)

if __name__ == '__main__':
    parser = Parser('alchemist.pdf', 16, 17, '\n\n', ':', ',')
