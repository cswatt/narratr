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
        with open('sampleprograms/0_helloworld.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Hello World lexing does not match expected tokens.")

    def test_lexer_comments(self):
        """Test Comments tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/1_comments.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_comments') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Comments lexing does not match expected tokens.")

    def test_lexer_andor(self):
        """Test And/Or tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/3_andor.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_andor') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "And/Or lexing does not match expected tokens.")

    def test_lexer_arithmetic(self):
        """Test Arithmetic tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/3_arithmetic.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_arithmetic') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Arithmetic lexing does not match expected tokens.")

    def test_lexer_assignment(self):
        """Test Assignment tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/3_assignment.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_assignment') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Assignment lexing does not match expected tokens.")

    def test_lexer_comparison(self):
        """Test Comparison tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/3_comparison.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_comparison') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Comparison lexing does not match expected tokens.")

    def test_lexer_elseif(self):
        """Test Else/If tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/4_elseif.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_elseif') as f:
            for line in f:
                correctlist.append(line.rstrip())
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Else/If lexing does not match expected tokens.")

    def test_lexer_exposition(self):
        """Test Exposition tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/4_exposition.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_exposition') as f:
            for line in f:
                correctlist.append(line.rstrip())
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Exposition lexing does not match expected tokens.")

    def test_lexer_if(self):
        """Test If tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('tests/lexed_if') as f:
            for line in f:
                correctlist.append(line.rstrip())

        with open('sampleprograms/4_if.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "If lexing does not match expected tokens.")

    def test_lexer_truefalse(self):
        """Test True/False tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('tests/lexed_truefalse') as f:
            for line in f:
                correctlist.append(line.rstrip())

        with open('sampleprograms/4_truefalse.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "True/False lexing does not match expected tokens.")

    def test_lexer_while(self):
        """Test While tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/4_while.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_while') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "While lexing does not match expected tokens.")

    def test_lexer_moves(self):
        """Test Moves tokens are as expected."""
        correctlist = []
        tokenlist = []

        with open('sampleprograms/5_moves.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        with open('tests/lexed_moves') as f:
            for line in f:
                correctlist.append(line.rstrip())

        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Moves lexing does not match expected tokens.")
