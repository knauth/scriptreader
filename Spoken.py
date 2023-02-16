# ScriptReader
# June Knauth (github.com/knauth), 20230216
# Dataclass for line content

class Spoken():
    def __init__(self, content, speaker, tone):
        self.content = content
        self.speaker = speaker
        self.tone = tone

    def __repr__(self):
        out = f"Speaker: {str(self.speaker)} \n Tone: {str(self.tone)} \n Content: \n {str(self.content)}"
        return out
