import narratr.lexer as lexer
import unittest


class TestLexer(unittest.TestCase):

    def test_lexer_helloworld(self):
        """Test Hello World tokens are as expected."""
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

    def test_lexer_andor(self):
        """Test And/Or tokens are as expected."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/andor.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # look at correct list of tokens
        with open('tests/lexed_andor') as f:
            for line in f:
                correctlist.append(line.rstrip())
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "And/Or lexing does not match expected tokens.")

    def test_lexer_elseif(self):
        """Test Else/If tokens are as expected."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/elseif.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # look at correct list of tokens
        with open('tests/lexed_elseif') as f:
            for line in f:
                correctlist.append(line.rstrip())
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Else/If lexing does not match expected tokens.")

    def test_lexer_exposition(self):
        """Test Exposition tokens are as expected."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/exposition.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # look at correct list of tokens
        with open('tests/lexed_exposition') as f:
            for line in f:
                correctlist.append(line.rstrip())
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Exposition lexing does not match expected tokens.")

    def test_lexer_if(self):
        """Test If tokens are as expected."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at correct list of tokens
        with open('tests/lexed_if') as f:
            for line in f:
                correctlist.append(line.rstrip())

        # look at what lexer outputs
        with open('sampleprograms/if.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "If lexing does not match expected tokens.")

    def test_lexer_truefalse(self):
        """Test True/False tokens are as expected."""
        # some lists
        correctlist = []
        tokenlist = []

        # look at correct list of tokens
        with open('tests/lexed_truefalse') as f:
            for line in f:
                correctlist.append(line.rstrip())

        # look at what lexer outputs
        with open('sampleprograms/truefalse.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "True/False lexing does not match expected tokens.")
