import unittest
from nfp import Parser, InvalidInput


class ParserImpl(Parser):
    def get_status(self):
        return []


class Tests(unittest.TestCase):
    def setUp(self):
        self.p = ParserImpl()

    def test_parse_input(self):
        with self.assertRaises(InvalidInput):
            self.p.parse_input("--")


if __name__ == "__main__":
    unittest.main()
