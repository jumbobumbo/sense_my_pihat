from pathlib import Path
import json
from copy import deepcopy


class PatternList:
    """
    creates a pattern list from a json file
    """
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
        Example return list: [[213, 231, 1], [32, 1, 233], [65, 100, 190], [200, 190, 0]]
        """
        return_list = self._create_base_list()

        for colour, values in self.pattern_json.items():
            for intensity, idx in values.items():
                for i in idx:
                    return_list[i][self.rgb[colour]] = int(intensity)

        return return_list


class GeneratePatternFromList:
    """
    Generates a pattern from a list of nested lists, and a int value
    """
    def __init__(self, color_list: list, style: int):
        """
        :param color_list: list
        :param style: int (takes 0 or 1)
        """
        self.color_list = color_list
        self.style = style
        # dictionary of starting co-ords of each quarter row + 3 to complete each quarter row
        self.quarters_coords = {
            0: [0, 8, 16, 24],
            1: [4, 12, 20, 28],
            2: [32, 40, 48, 56],
            3: [36, 44, 52, 60]
        }

    def pattern_gen(self) -> list:
        """
        0 is stripes or single colour for whole panel
        1 is square
        """
        if self.style == 0:
            img = []

            for nested_list in self.color_list:
                # find the amount of pixels we need to cover
                for _ in range(0, int(64 / len(self.color_list))):
                    img.append(nested_list)

            # return the generated list
            return img

        elif self.style == 1:
            img = [deepcopy([]) for _ in range(0, 64)]  # create a list of 64 empty nested lists
            colour_list_index = 0  # starting index of quarter 1, incremented till 4

            for quarter in self.quarters_coords.values():
                # co_ord is the pixel number on the sense hat display (0 is top left)
                for co_ord in quarter:
                    # we need to block out 4 pixels in a row starting from co_ord (self inclusive)
                    for pixel in range(co_ord, co_ord + (3+1)):
                        img[pixel] = self.color_list[colour_list_index]

                colour_list_index += 1  # move onto the next quarter 
            
            # return the generated list
            return img
