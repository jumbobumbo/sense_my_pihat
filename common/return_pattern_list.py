from pathlib import Path
import json


class PatternList:
    def __init__(self, json_file: str):
        self.pattern_json = Path('patterns/', json_file)

    @property
    def pattern_json(self) -> dict:
        return self.__pattern_json

    @pattern_json.setter
    def pattern_json(self, json_file):
        with open(json_file, "r") as f:
            self.__pattern_json = json.load(f)


