import narratr.parser as parser
import unittest


class TestParserForOtherthings(unittest.TestCase):

    def test_parser_moves(self):

        """Test that parser can parse moves."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/5_moves.ntr') as f:
            ast = str(p.parse(f.read()))
