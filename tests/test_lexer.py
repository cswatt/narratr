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

    def test_lexer_andor(self):
        """Test that lexer can read and/or."""
        # some lists
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/andor.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        correctlist = ["LexToken(SCENE,'scene',1,0)",
                       'LexToken(SCENEID,1,1,6)',
                       "LexToken(LCURLY,'{',1,9)",
                       'LexToken(NEWLINE,1,1,10)',
                       'LexToken(INDENT,1,2,11)',
                       "LexToken(SETUP,'setup',2,12)",
                       "LexToken(COLON,':',2,17)",
                       'LexToken(NEWLINE,1,2,18)',
                       "LexToken(ACTION,'action',3,20)",
                       "LexToken(COLON,':',3,26)",
                       'LexToken(NEWLINE,1,3,27)',
                       'LexToken(INDENT,2,4,28)',
                       "LexToken(IF,'if',4,30)",
                       "LexToken(LPARAN,'(',4,33)",
                       'LexToken(INTEGER,1,4,34)',
                       "LexToken(EQUALS,'==',4,36)",
                       'LexToken(INTEGER,1,4,39)',
                       "LexToken(RPARAN,')',4,40)",
                       "LexToken(AND,'and',4,42)",
                       "LexToken(LPARAN,'(',4,46)",
                       'LexToken(INTEGER,2,4,47)',
                       "LexToken(EQUALS,'==',4,49)",
                       'LexToken(INTEGER,3,4,52)',
                       "LexToken(RPARAN,')',4,53)",
                       "LexToken(COLON,':',4,54)",
                       'LexToken(NEWLINE,1,4,55)',
                       'LexToken(INDENT,3,5,56)',
                       "LexToken(SAY,'say',5,59)",
                       "LexToken(STRING,'Okay.',5,63)",
                       'LexToken(NEWLINE,1,5,70)',
                       'LexToken(DEDENT,3,6,71)',
                       "LexToken(IF,'if',6,73)",
                       "LexToken(LPARAN,'(',6,76)",
                       'LexToken(INTEGER,1,6,77)',
                       "LexToken(EQUALS,'==',6,79)",
                       'LexToken(INTEGER,1,6,82)',
                       "LexToken(RPARAN,')',6,83)",
                       "LexToken(OR,'or',6,85)",
                       "LexToken(LPARAN,'(',6,88)",
                       'LexToken(INTEGER,2,6,89)',
                       "LexToken(EQUALS,'==',6,91)",
                       'LexToken(INTEGER,3,6,94)',
                       "LexToken(RPARAN,')',6,95)",
                       "LexToken(COLON,':',6,96)",
                       'LexToken(NEWLINE,1,6,97)',
                       'LexToken(INDENT,3,7,98)',
                       "LexToken(SAY,'say',7,101)",
                       "LexToken(STRING,'Okay.',7,105)",
                       'LexToken(NEWLINE,1,7,112)',
                       'LexToken(DEDENT,3,8,113)',
                       'LexToken(DEDENT,2,8,113)',
                       "LexToken(CLEANUP,'cleanup',8,114)",
                       "LexToken(COLON,':',8,121)",
                       'LexToken(NEWLINE,1,8,122)',
                       'LexToken(DEDENT,1,8,122)',
                       "LexToken(RCURLY,'}',9,123)",
                       'LexToken(NEWLINE,2,9,124)',
                       "LexToken(START,'start',11,126)",
                       "LexToken(COLON,':',11,131)",
                       'LexToken(SCENEID,1,11,133)',
                       'LexToken(NEWLINE,1,11,135)']
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "And/Or lexing does not match expected tokens.")

    def test_lexer_elseif(self):
        """Test that lexer can read else/if."""
        # some lists
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/elseif.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        correctlist = ["LexToken(SCENE,'scene',1,0)",
                       'LexToken(SCENEID,1,1,6)',
                       "LexToken(LCURLY,'{',1,9)",
                       'LexToken(NEWLINE,1,1,10)',
                       'LexToken(INDENT,1,2,11)',
                       "LexToken(SETUP,'setup',2,12)",
                       "LexToken(COLON,':',2,17)",
                       'LexToken(NEWLINE,1,2,18)',
                       "LexToken(ACTION,'action',3,20)",
                       "LexToken(COLON,':',3,26)",
                       'LexToken(NEWLINE,1,3,27)',
                       'LexToken(INDENT,2,4,28)',
                       "LexToken(IF,'if',4,30)",
                       "LexToken(LPARAN,'(',4,33)",
                       'LexToken(INTEGER,1,4,34)',
                       "LexToken(EQUALS,'==',4,35)",
                       'LexToken(INTEGER,2,4,37)',
                       "LexToken(RPARAN,')',4,38)",
                       "LexToken(COLON,':',4,39)",
                       'LexToken(NEWLINE,1,4,40)',
                       'LexToken(INDENT,3,5,41)',
                       "LexToken(ID,'Say',5,44)",
                       "LexToken(STRING,'something bad has happened',5,48)",
                       'LexToken(NEWLINE,1,5,76)',
                       'LexToken(DEDENT,3,6,77)',
                       "LexToken(ELSE,'else',6,79)",
                       "LexToken(COLON,':',6,83)",
                       'LexToken(NEWLINE,1,6,84)',
                       'LexToken(INDENT,3,7,85)',
                       "LexToken(ID,'Say',7,88)",
                       "LexToken(STRING,'Okay.',7,92)",
                       'LexToken(NEWLINE,2,7,99)',
                       'LexToken(DEDENT,3,9,101)',
                       'LexToken(DEDENT,2,9,101)',
                       "LexToken(CLEANUP,'cleanup',9,102)",
                       "LexToken(COLON,':',9,109)",
                       'LexToken(NEWLINE,1,9,110)',
                       'LexToken(DEDENT,1,9,110)',
                       "LexToken(RCURLY,'}',10,111)",
                       'LexToken(NEWLINE,2,10,112)',
                       "LexToken(START,'start',12,114)",
                       "LexToken(COLON,':',12,119)",
                       'LexToken(SCENEID,1,12,121)',
                       'LexToken(NEWLINE,1,12,123)']
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Else/If lexing does not match expected tokens.")

    def test_lexer_exposition(self):
        """Test that lexer can read exposition."""
        # some lists
        tokenlist = []

        # look at what lexer outputs
        with open('sampleprograms/exposition.ntr') as f:
            m = lexer.LexerForNarratr()
            m.input(f.read())
            t = m.token()
            while t:
                tokenlist.append(str(t))
                t = m.token()

        correctlist = ["LexToken(SCENE,'scene',1,0)",
                       'LexToken(SCENEID,1,1,6)',
                       "LexToken(LCURLY,'{',1,9)",
                       'LexToken(NEWLINE,1,1,10)',
                       'LexToken(INDENT,1,2,11)',
                       "LexToken(SETUP,'setup',2,12)",
                       "LexToken(COLON,':',2,17)",
                       'LexToken(NEWLINE,1,2,18)',
                       'LexToken(INDENT,2,3,19)',
                       "LexToken(EXPOSITION,'exposition',3,21)",
                       "LexToken(STRING,'Sadness is infinite.',3,32)",
                       'LexToken(NEWLINE,1,3,54)',
                       'LexToken(DEDENT,2,4,55)',
                       "LexToken(ACTION,'action',4,56)",
                       "LexToken(COLON,':',4,62)",
                       'LexToken(NEWLINE,1,4,63)',
                       "LexToken(CLEANUP,'cleanup',5,65)",
                       "LexToken(COLON,':',5,72)",
                       'LexToken(NEWLINE,1,5,73)',
                       'LexToken(DEDENT,1,5,73)',
                       "LexToken(RCURLY,'}',6,74)",
                       'LexToken(NEWLINE,2,6,75)',
                       "LexToken(START,'start',8,77)",
                       "LexToken(COLON,':',8,82)",
                       'LexToken(SCENEID,1,8,84)',
                       'LexToken(NEWLINE,1,8,86)']
        # check for equivalence
        self.assertEqual(cmp(tokenlist, correctlist), 0,
                         "Exposition lexing does not match expected tokens.")

    def test_lexer_if(self):
        """Test that lexer can read if."""
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
        """Test that lexer can read true/false."""
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
