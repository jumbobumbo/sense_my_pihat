from collections import defaultdict
from copy import deepcopy


class ProcessMultiDict:
    """
    takes in a MultiDict from a flask POST
    """
    def __init__(self, post_data: dict):
        """
        :param post_data: MultiDict
        """
        self.post_data = post_data

    @property
    def post_data(self) -> list:
        """
        :return: list
        Example return:
        [('red', '1'), ('green', '3'), ('blue', '4')]
        """
        return self.__post_data

    @post_data.setter
    def post_data(self, post_data):
        """
        :param post_data: MultiDict
        creates a list of tuples (key, value)
        """
        self.__post_data = []

        for key, val in post_data.items(multi=True):
            self.__post_data.append((key, val))
    
    def post_data_to_nested_lists(self) -> list:
        """
        translates the items from a ImmutableMultiDict into nested lists
        Example input:
        [('red', '1'), ('red', '44'), ('red', '2'), ('red', '3'), 
        ('green', '55'), ('green', '1'), ('green', '2'), ('green', '3'), 
        ('blue', '1'), ('blue', '2'), ('blue', '3'), ('blue', '4')]
        Example output:
        [['1', '55', '1'], ['44', '1', '2'], ['2', '2', '3'], ['3', '3', '4']]
        """
        total_keys = len(set([key for key, _ in self.post_data]))  # total number of unique keys in data
        num_of_entries = int(len(self.post_data) / total_keys)  # total number of args sent
        arg_list = []

        # only 1 lot of data was sent
        if num_of_entries == 0:
            arg_list.append([int(val) for _, val in self.post_data])
            return arg_list
        # more than one data lot was sent
        else:
            colour_dict = defaultdict(list)  # create dict

            for key, val in self.post_data:
                colour_dict[key].append(val)  # add key:value or append to existing

            for i in range(0, num_of_entries):
                nest_list = []
                for key, val in colour_dict.items():
                    nest_list.append(int(val[i]))
                arg_list.append(nest_list)  # append finished nested list

            return arg_list
