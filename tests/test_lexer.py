from lexer import LexerForNarratr
import unittest

class TestLexer(unittest.TestCase):

	def test_lexer_helloworld(self):
		"""Test that lexer can read Hello World."""
		m = LexerForNarratr()
		file = open('sampleprograms/helloworld.ntr', 'r')
		m.input(file.read())
		t = m.token()
		tokenlist = []
		correctlist = [
		"LexToken(SCENE,'scene',1,0)",
		"LexToken(SCENEID,1,1,6)",
		"LexToken(LCURLY,'{',1,9)",
		"LexToken(NEWLINE,1,1,10)",
		"LexToken(INDENT,1,2,11)",
		"LexToken(SETUP,'setup',2,12)",
		"LexToken(COLON,':',2,17)",
		"LexToken(NEWLINE,1,2,18)",
		"LexToken(INDENT,2,3,19)",
		"LexToken(SAY,'say',3,21)",
		"LexToken(STRING,'Hello, World!',3,25)",
		"LexToken(NEWLINE,1,3,40)",
		"LexToken(DEDENT,2,4,41)",
		"LexToken(ACTION,'action',4,42)",
		"LexToken(COLON,':',4,48)",
		"LexToken(NEWLINE,1,4,49)",
		"LexToken(INDENT,2,5,50)",
		"LexToken(WIN,'win',5,52)",
		"LexToken(NEWLINE,1,5,55)",
		"LexToken(DEDENT,2,6,56)",
		"LexToken(CLEANUP,'cleanup',6,57)",
		"LexToken(COLON,':',6,64)",
		"LexToken(NEWLINE,1,6,65)",
		"LexToken(DEDENT,1,6,65)",
		"LexToken(RCURLY,'}',7,66)",
		"LexToken(NEWLINE,2,7,67)",
		"LexToken(START,'start',9,69)",
		"LexToken(COLON,':',9,74)",
		"LexToken(SCENEID,1,9,76)",
		"LexToken(NEWLINE,1,9,78)"]
		while t:
		    tokenlist.append(str(t))
		    t = m.token()
		self.assertEqual(cmp(tokenlist, correctlist), 0, "Something did not work correctly.")
