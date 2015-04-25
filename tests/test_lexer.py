import narratr.lexer as lexer
import unittest


class TestLexer(unittest.TestCase):

    def test_lexer_helloworld(self):
        """Test that lexer can read Hello World."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at correct list of tokens
        with open('tests/lexed_helloworld') as f:
            for line in f:
                correctlist.append(line.rstrip())

        # look at what lexer outputs
        with open('sampleprograms/helloworld.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Hello World lexing does not match expected tokens.")
