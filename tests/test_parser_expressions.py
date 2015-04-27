import narratr.parser as parser
import unittest


class TestParserForExpressions(unittest.TestCase):

    def test_parser_andor(self):

        """Test that parser can parse and/or."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/3_andor.ntr') as f:
            ast = str(p.parse(f.read()))
