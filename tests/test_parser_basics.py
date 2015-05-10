import narratr.parser as parser
import unittest


class TestParser(unittest.TestCase):

    def test_parser_helloworld(self):
        """Test that parser can parse Hello World."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/0_helloworld.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_comments(self):

        """Test that parser can parse comments."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/1_comments.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_costantsliterals(self):

        """Test that parser can parse constants, literals."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/1_constantsliterals.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_list(self):

        """Test that parser can parse list."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/2_list.ntr') as f:
            ast = str(p.parse(f.read()))
