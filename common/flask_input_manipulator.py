from json import load
from pathlib import Path
from collections import defaultdict


def load_json(*args, parent_dir: str = 'patterns'):
    """
    loads json file from a 'parent' DIR, supports sub DIRs
    param: args: str (sub dirs and file under parent DIR)
    param: parent_dir: str - Parent folder of your json files
    """
    file_path = Path(parent_dir)
    for arg in args:
        file_path = Path.joinpath(file_path, arg)

    with open(file_path, "r") as f:
        return load(f)


class ImgTempDict:
    def __init__(self, temp: int, path_list: list = ["temps.json"]):
        """
        takes in a temp value and the temps json file (or file that matches the same internal format)
        function X will return a Dict that can be sent to PatternList()

        Arguments:
            temp {int} -- temp value from sense hat

        Keyword Arguments:
            input_file {list} -- list of path objects (dirs, file) (default: {["temps.json"]})
            example: ["subdir1", "subdir2", "file.txt"]
        """
        self.temp = temp
        self.input_file = load_json(*path_list)
        self.output = defaultdict(list)

    def _create_base_from_temp(self):
        """
        creates the base colour dict for output from temp reading
        """
        for temps_range, color_dict in self.input_file["temps"].items():
            t_range = temps_range.split("_")
            if self.temp in range(int(t_range[0]), int(t_range[1])+1):
                for key, values in color_dict.items():
                    self.output[key].extend(values)

    def _map_temp_char_to_position(self) -> list:
        """
        takes temp int(s), maps them to side a or b of the canvas
        returns: list - char str(int), side mapping
        example:
         - [["1", "a"], ["1", "b"]] would be 11
         - [["1", "b"]] would be 1
        """
        temp = str(self.temp)
        if len(temp) == 1:
            return [[temp, "b"]]
        elif len(temp) == 2:
            return [[temp[0], "a"], [temp[1], "b"]]
        else:
            raise ValueError(f"max of two digits, not: {len(temp)}")

    def _map_temp_chars_to_output_dict(self):
        """
        based of the temprature, fetch the required chars from input file
        create output dict to work with PatternList()
        Requires keys to be present in input_file
         - "RGBKeys"
         - "digits"
        """
        rgb_keys = ["red", "green", "blue"]

        # create RGB dicts
        for color, intensity in zip(rgb_keys, self.input_file["RGBKeys"]):
            self.output[color] = {str(intensity): []}

        # get temp value mapping
        temp = self._map_temp_char_to_position()

        for char in temp:
            for color in rgb_keys:
                for key, _ in self.output[color].items():
                    self.output[color][key].extend(
                        self.input_file["digits"][char[0]][char[1]])

    def return_formatted_dict(self) -> dict:
        """
        wrapper for internal functions
        returns the formatted dict - ready for posting to PatternList()
        """
        self._create_base_from_temp()
        self._map_temp_chars_to_output_dict()
        return self.output
