"""
TestTooling
-----------
Unit testing the utility tools
"""

from metaqueue.utilities.tools import repeat


class TestTooling:
    def test_repeat_s01(self):
        def custom_func(value):
            return 2.0 * value

        funcs      = repeat(custom_func, 3)
        act_result = 0
        for func in funcs:
            act_result += func(2)

        expected = 12
        assert act_result == expected