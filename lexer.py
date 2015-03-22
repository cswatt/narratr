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

    # Regular expression rules for simple tokens
    t_LCURLY = r'{'
    t_RCURLY = r'}'
    t_COLON = r':'
    t_TAB = r'\t'

    # Special ignore token to ignore whitespaces. All indentation is in tabs
    # only.
    t_ignore = ' '

    # This rule matches an Identifier except
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    def t_SCENEID(t):
        r'\$[0-9]+'
        t.value = int(t.value[1:])
        return t

    def t_STRING(t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t

    # Rule to track Line numbers
    def t_NEWLINE(t):
        r'\n+'
        t.value = len(t.value)
        t.lexer.lineno += t.value
        return t

    # Error handling rule
    def t_error(t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)
