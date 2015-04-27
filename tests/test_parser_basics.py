import narratr.parser as parser
import unittest


class TestParser(unittest.TestCase):

    def test_parser_helloworld(self):
        """Test that parser can parse Hello World."""
        """Test that AST for Hello World is as expected."""
        ast = ""
        correct_ast = ""
        with open('tests/parsed_helloworld') as f:
            correct_ast = f.read()

        p = parser.ParserForNarratr()
        with open('sampleprograms/0_helloworld.ntr') as f:
            ast = str(p.parse(f.read()))
        self.assertEqual(ast, correct_ast,
                         "Hello World not parsed as expected")

    def test_parser_comments(self):

        """Test that parser can parse comments."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/1_comments.ntr') as f:
            ast = str(p.parse(f.read()))
