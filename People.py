# ScriptReader
# June Knauth (github.com/knauth), 20230216
# People spreasheet parser and storage

import pandas as pd

class People():
    def __init__(self, path):
        self.raw_sheet = pd.read_excel(path)
        self.people = list(self.raw_sheet['Name'].apply(lambda x: x.lower()))

if __name__ == '__main__':
    p = People('people.ods')
