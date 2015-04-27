import unittest
import pep8


class TestCodeFormat(unittest.TestCase):

    def test_pep8_conformance_lexer(self):
        """Test that lexer conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['lexer.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_parser(self):
        """Test that parser conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['parser.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_codegen(self):
        """Test that codegen conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['codegen.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_node(self):
        """Test that node conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['node.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_symtab(self):
        """Test that symtab conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['symtab.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_narratr(self):
        """Test that narratr conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['narratr.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_lexertest(self):
        """Test that lexer test conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['tests/test_lexer.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_parser_general(self):
        """Test that parser_basics test conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['tests/test_parser_basics.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_parser_expressions(self):
        """Test that parser_expressions test conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['tests/test_parser_expressions.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_parser_statements(self):
        """Test that parser_statements test conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['tests/test_parser_statements.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_pep8test(self):
        """Test that pep8 test conforms to PEP8."""
        pep8style = pep8.StyleGuide(quiet=False)
        result = pep8style.check_files(['tests/test_pep8.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")
