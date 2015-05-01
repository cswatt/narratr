import narratr.parser as parser
import unittest


class TestParserForExpressions(unittest.TestCase):

    def test_parser_andor(self):

        """Test that parser can parse and/or."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/3_andor.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_arithmetic(self):

        """Test that parser can parse arithmetic"""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/3_arithmetic.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_assignment(self):

        """Test that parser can parse assignment."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/3_assignment.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_comparison(self):

        """Test that parser can parse comparison."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/3_comparison.ntr') as f:
            ast = str(p.parse(f.read()))

    def test_parser_precedence(self):

        pass
