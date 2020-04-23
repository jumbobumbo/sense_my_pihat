from parameterized import parameterized
import unittest
from sys import path
path.append('common')
from return_pattern_list import PatternList, GeneratePatternFromList
from testdata_test_return_pattern_list import TestPatternListData as TPLD
from testdata_test_return_pattern_list import TestGeneratePatternFromListData as TGPFLD

unittest.util._MAX_LENGTH = 160 

class TestPatternList(unittest.TestCase):
    """
    tests the PatternList class methods which create nested lists from json
    """
    @parameterized.expand([
        (TPLD.BaseListNoFile.input_0, TPLD.BaseListNoFile.res_l_0),
        (TPLD.BaseListNoFile.input_1, TPLD.BaseListNoFile.res_l_1),
        (TPLD.BaseListNoFile.input_2, TPLD.BaseListNoFile.res_l_2),
        (TPLD.BaseListNoFile.input_3, TPLD.BaseListNoFile.res_l_3)
    ])
    def test__create_base_list_no_file(self, input_data, expected_return):
        """
        Verifies output of the _create_base_list method via sending json data directly
        BaseListNoFile Class contains all input/expected output data
        """
        self.assertEqual(PatternList(input_data, False)._create_base_list(), expected_return)

    @parameterized.expand([
        ("creeper_head.json", TPLD.BaseListWithFile.res_b_creeper),
        ("jumble.json", TPLD.BaseListWithFile.res_b_jumble)
    ])
    def test__create_base_list_with_file(self, input_data, expected_return):
        """
        Verifies output of the _create_base_list method via sending json data from file
        BaseListWithFile Class contains all input/expected output data
        """
        self.assertEqual(PatternList(input_data, True)._create_base_list(), expected_return)

    @parameterized.expand([
        (TPLD.PatternListWithWithoutFile.input_creeper_dict, TPLD.PatternListWithWithoutFile.res_creeper),
        (TPLD.PatternListWithWithoutFile.input_jumble_dict, TPLD.PatternListWithWithoutFile.res_jumble)
    ])
    def test_create_pattern_list_no_file(self, input_data, expected_return):
        """
        Verifies output of the create_pattern_list method via input dict
        PatternListWithWithoutFile Class contains all expected output data
        """
        self.assertEqual(PatternList(input_data, False).create_pattern_list(), expected_return)

    @parameterized.expand([
        ("creeper_head.json", TPLD.PatternListWithWithoutFile.res_creeper),
        ("jumble.json", TPLD.PatternListWithWithoutFile.res_jumble)
    ])
    def test_create_pattern_list_with_file(self, input_data, expected_return):
        """
        Verifies output of the create_pattern_list method via sending json data from file
        PatternListWithWithoutFile Class contains all expected output data
        """
        self.assertEqual(PatternList(input_data, True).create_pattern_list(), expected_return)


class TestGeneratePatternFromList(unittest.TestCase):
    """
    tests GeneratePatternFromList class methods
    return generated list from 1 or 4 nested lists
    """
    # to save the file being huge, we re-use some data from TPLD.BaseListNoFile to assert against
    @parameterized.expand([
        ([[0, 0, 0]], 0, TPLD.BaseListNoFile.res_l_0),
        (TGPFLD.PatternGen.stripe_list_input, 0, TGPFLD.PatternGen.stripe_list_return),
        (TGPFLD.PatternGen.square_list_input, 1, TGPFLD.PatternGen.square_list_return)
    ])
    def test_pattern_gen(self, input_data, style, expected_return):
        """
        Verifies output of the pattern_gen method
        """
        self.assertEqual(GeneratePatternFromList(input_data, style).pattern_gen(), expected_return)

    @parameterized.expand([
        ([0, 0, 0], 0, ValueError, TGPFLD.PatternGenRaiseError.triple_zero_exp_return),
        ([{}, [], "nice", ()], 0, ValueError, TGPFLD.PatternGenRaiseError.mixed_type_exp_return),
        ([0, 0, 0], 1, ValueError, TGPFLD.PatternGenRaiseError.triple_zero_exp_return),
        ([{}, [], "nice", ()], 1, ValueError, TGPFLD.PatternGenRaiseError.mixed_type_exp_return)
    ])
    def test_pattern_gen_raise_error(self, input_data, style, expected_exception, expected_return):
        """
        Verifies the expected Exception is returned for the pattern_gen method (varies on input data)
        PatternGenRaiseError Class contains all expected output data
        """
        with self.assertRaises(expected_exception) as exp:
            GeneratePatternFromList(input_data, style).pattern_gen()

        self.assertEqual(exp.exception.args[0], expected_return)

if __name__ == "__main__":
    unittest.main()