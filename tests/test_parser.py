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
		with open('sampleprograms/helloworld.ntr') as f:
			ast = str(p.parse(f.read()))
		self.assertEqual(ast, correct_ast, 
						 "Hello World not parsed as expected")

	def test_parser_andor(self):
		
		"""Test that parser can parse and/or."""
		ast = ""

		p = parser.ParserForNarratr()
		with open('sampleprograms/andor.ntr') as f:
			ast = str(p.parse(f.read()))

	def test_parser_elseif(self):
		
		"""Test that parser can parse else/if."""
		ast = ""

		p = parser.ParserForNarratr()
		with open('sampleprograms/elseif.ntr') as f:
			ast = str(p.parse(f.read()))

	def test_parser_exposition(self):
		
		"""Test that parser can parse exposition."""
		"""Test that AST for exposition is as expected."""
		ast = ""
		correct_ast = ""
		with open('tests/parsed_exposition') as f:
			correct_ast = f.read()

		p = parser.ParserForNarratr()
		with open('sampleprograms/exposition.ntr') as f:
			ast = str(p.parse(f.read()))
		self.assertEqual(ast, correct_ast, 
						 "Exposition not parsed as expected")

	def test_parser_if(self):
		
		"""Test that parser can parse if."""
		ast = ""

		p = parser.ParserForNarratr()
		with open('sampleprograms/if.ntr') as f:
			ast = str(p.parse(f.read()))

	def test_parser_truefalse(self):
		
		"""Test that parser can parse true/false."""
		ast = ""

		p = parser.ParserForNarratr()
		with open('sampleprograms/truefalse.ntr') as f:
			ast = str(p.parse(f.read()))
			