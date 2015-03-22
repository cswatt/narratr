# -----------------------------------------------------------------------------
# narrtr: parser.py
# This file defines the Parser (Syntactic Analyzer) for the language narratr
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 21 March 2015
# Primary Author: Nivvedan Senthamil Selvan <nivvedan.s@columbia.edu>
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

import ply.yacc as yacc
from lexer import LexerForNarratr


class ParserForNarratr:

    def __init__(self, **kwargs):
        self.lexer = LexerForNarratr()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_program(self, p):
        '''program : newlines sceneblocks
                   | newlines sceneblocks startstate newlines'''

    def p_sceneblocks(self, p):
        '''sceneblocks : sceneblock newlines
                       | sceneblocks sceneblock newlines'''

    def p_newlines(self, p):
        '''newlines : NEWLINE
                    | '''

    def p_sceneblock(self, p):
        "sceneblock : SCENE SCENEID LCURLY NEWLINE INDENT setupblock actionblock cleanupblock DEDENT RCURLY"

    def p_startstate(self, p):
        'startstate : START COLON SCENEID'

    def p_setupblock(self, p):
        'setupblock : SETUP COLON NEWLINE INDENT statements DEDENT'

    def p_actionblock(self, p):
        'actionblock : ACTION COLON NEWLINE'

    def p_cleanupblock(self, p):
        'cleanupblock : CLEANUP COLON NEWLINE'

    def p_statements(self, p):
        'statements : SAY STRING NEWLINE'

    def p_error(self, p):
        print "Syntax Error in input at ", p

    def parse(self, string_to_parse, **kwargs):
        self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
