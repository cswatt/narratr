# -----------------------------------------------------------------------------
# narrtr: lexer.py
# This file defines the Lexical Analyser for the language narratr
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 18 March 2015
# Primary Author: Nivvedan Senthamil Selvan <nivvedan.s@columbia.edu>
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

import ply.lex as lex


class LexerForNarratr:

    # This dictionary defines all the reserved keyword in the language. They
    # are specified here to make keyword matching easy. All keywords must be
    # declared here. Alphanumeric patterns that is not declared as a keyword
    # here will be considered to be an identifier.
    reserved = {
        'scene': 'SCENE',
        'setup': 'SETUP',
        'action': 'ACTION',
        'cleanup': 'CLEANUP',
        'say': 'SAY',
        'start': 'START'
    }

    # All other tokens are declared here. Tokens not declared here would
    # produce an error.
    tokens = ['SCENEID', 'LCURLY', 'RCURLY', 'COLON', 'TAB',
              'NEWLINE', 'ID', 'STRING'] + list(reserved.values())

    # The constructor here builds the lexer.
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Regular expression rules for simple tokens are specified here.
    t_LCURLY = r'{'
    t_RCURLY = r'}'
    t_COLON = r':'
    t_TAB = r'\t'

    # Special ignore token to ignore whitespaces. All indentation is in tabs
    # only.
    t_ignore = ' '

    # This rule matches an Identifier except for the reserved words defined
    # above. The reserved words will be matched to their own tokens.
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    # This rule matches he Scene ID and stores the value as the integer ID.
    def t_SCENEID(self, t):
        r'\$[0-9]+'
        t.value = int(t.value[1:])
        return t

    # This rule matches strings.
    def t_STRING(self, t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t

    # This rule tracks line numbers
    def t_NEWLINE(self, t):
        r'\n+'
        t.value = len(t.value)
        t.lexer.lineno += t.value
        return t

    # This rule is triggered if an error is encountered. The lexer skips a line
    # after printing a message.
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    # This method provides an interface to the lexer's input(string) function
    def input(self, string_to_scan):
        self.lexer.input(string_to_scan)

    # This method provides an interface to the lexer's token() function
    def token(self):
        return self.lexer.token()

    # This method prints all tokens scanned by the lexer. This method should be
    # called only after passing some input through the input(string) function.
    # This method is for testing purposes only.
    def printAllTokens(self):
        nextToken = self.lexer.token()
        while nextToken:
            print nextToken
            nextToken = self.lexer.token()
