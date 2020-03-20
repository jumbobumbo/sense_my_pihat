from pathlib import Path
import json
from copy import deepcopy


class PatternList:
    def __init__(self, json_file: str):
        self.pattern_json = Path('patterns/', json_file)
        self.rgb = {"red": 0, "green": 1, "blue": 2}

    @property
    def pattern_json(self) -> dict:
        return self.__pattern_json

    @pattern_json.setter
    def pattern_json(self, json_file):
        with open(json_file, "r") as f:
            self.__pattern_json = json.load(f)

    def _create_base_list(self) -> list:
        """
        creates list of 64 elements from the "base" key in pattern_json
        the key is then deleted from the dict
        :return: base list
        """
        base_list = [deepcopy(self.pattern_json["base"]) for _ in range(0, 64)]
        del self.pattern_json["base"]
        return base_list

    def create_pattern_list(self) -> list:
        """
        creates RGB list (of lists) for pattern
        :return: list
        """
        return_list = self._create_base_list()
        for colour, values in self.pattern_json.items():
            for intensity, idx in values.items():
                for i in idx:
                    return_list[i][self.rgb[colour]] = int(intensity)
        return return_list
