import narratr.parser as parser
import unittest


class TestParserForErrors(unittest.TestCase):

    def test_parser_different_order(self):

        """Test that parser has error when parsing different_order."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_different_order.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_missing_action(self):

        """Test that parser has error when parsing missing_action."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_missing_action.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_missing_cleanup(self):

        """Test that parser has error when parsing missing_cleanup."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_missing_cleanup.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_missing_setup(self):

        """Test that parser has error when parsing missing_setup."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_missing_setup.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_misspelled_start(self):

        """Test that parser has error when parsing misspelled_start."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_misspelled_start.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_multiple_actions(self):

        """Test that parser has error when parsing multiple_actions."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_multiple_actions.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_multiple_cleanups(self):

        """Test that parser has error when parsing multiple_cleanups."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_multiple_cleanups.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_multiple_setups(self):

        """Test that parser has error when parsing multiple_setups."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_multiple_setups.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_rogue_semicolon(self):

        """Test that parser has error when parsing rogue_semicolon."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_rogue_semicolon.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_scene_name_conflict(self):

        """Test that parser has error when parsing scene_name_conflict."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_scene_name_conflict.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))

    def test_parser_unmatched_braces(self):

        """Test that parser has error when parsing unmatched_braces."""
        ast = ""

        p = parser.ParserForNarratr()
        with open('sampleprograms/6_unmatched_braces.ntr') as f:
            self.assertRaises(SystemExit, lambda: p.parse(f.read()))
