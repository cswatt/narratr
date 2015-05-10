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

from sys import stderr, exit
import re
import ply.lex as lex


class LexerForNarratr:

    # This dictionary defines all the reserved keywords in the language. They
    # are specified here to make keyword matching easier. All keywords must be
    # declared here. Alphanumeric patterns that are not declared as a keyword
    # here will be considered an identifier.
    reserved = {
        'scene': 'SCENE',
        'setup': 'SETUP',
        'action': 'ACTION',
        'cleanup': 'CLEANUP',
        'say': 'SAY',
        'win': 'WIN',
        'lose': 'LOSE',
        'start': 'START',
        'exposition': 'EXPOSITION',
        'moves': 'MOVES',
        'moveto': 'MOVETO',
        'left': 'LEFT',
        'right': 'RIGHT',
        'up': 'UP',
        'down': 'DOWN',
        'is': 'IS',
        'item': 'ITEM',
        'if': 'IF',
        'elif': 'ELIF',
        'else': 'ELSE',
        'while': 'WHILE',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'true': 'TRUE',
        'false': 'FALSE',
        'god': 'GOD',
        'continue': 'CONTINUE',
        'break': 'BREAK',
        'pocket': 'ID'  # Pocket is a special kind of identifier.
    }

    # All other tokens are declared here. Tokens not declared here would
    # produce an error.
    tokens = ['SCENEID', 'LCURLY', 'RCURLY', 'LPARAN', 'RPARAN', 'COLON',
              'NEWLINE', 'INDENT', 'DEDENT', 'STRING', 'EQUALS', 'LESS',
              'GREATER', 'LESSEQUALS', 'GREATEREQUALS', 'PLUS', 'MINUS',
              'TIMES', 'DIVIDE', 'INTEGERDIVIDE', 'INTEGER', 'FLOAT', 'DOT',
              'COMMA', 'NOTEQUALS', 'LSQUARE', 'RSQUARE'] + \
        list(reserved.values())

    # The constructor here builds the lexer. The re.MULTILINE flag is critical
    # in matching indents.
    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, reflags=re.MULTILINE, **kwargs)
        self.indentstack = [0]
        self.dedenting = False
        self.lasttoken = None

    # Regular expression rules for simple tokens are specified here.
    t_LCURLY = r'{'
    t_RCURLY = r'}'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'
    t_LPARAN = r'\('
    t_RPARAN = r'\)'
    t_COLON = r':'
    t_EQUALS = r'==|='
    t_NOTEQUALS = r'!='
    t_LESS = r'<'
    t_GREATER = r'>'
    t_LESSEQUALS = r'<='
    t_GREATEREQUALS = r'>='
    t_PLUS = r'\+'
    t_TIMES = r'\*'
    t_MINUS = r'-'
    t_DIVIDE = r'/'
    t_INTEGERDIVIDE = r'//'
    t_COMMA = r','

    # Comments are ignored. Comments are defined as a % follwed by any
    # number of characters until a newline is encountered. If the token
    # generated just before the comment was a newline, no additional
    # newlines are generated. Else, one newline token is generated here.
    def t_comments(self, t):
        r'[ \t\r\f\v]*%[^\n]*\n'
        if self.lasttoken:
            if self.lasttoken.type != "NEWLINE":
                t.type = "NEWLINE"
                t.value = 1
                t.lexer.lineno += t.value
                return t
        t.lexer.lineno += 1

    # This rule matches an Identifier except for the reserved words defined
    # above. The reserved words will be matched to their own tokens.
    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')    # Check for reserved words
        if t.type == "TRUE":
            t.value = True
        elif t.type == "FALSE":
            t.value = False
        return t

    # This rule matches a floating point number.
    # The float defined by this rule has to have at least one digit either to
    # the left or the right of the decimal point.
    def t_FLOAT(self, t):
        r'(\+|-)?([0-9]*\.[0-9]+)|([0-9]+\.[0-9]*)'
        t.value = float(t.value)
        return t

    # This rule matches integers, signed and unsigned.
    def t_INTEGER(self, t):
        r'(\+|-)?(0|[1-9][0-9]*)'
        t.value = int(t.value)
        return t

    # This rule matches a period. Period is used to resolve into another scope.
    def t_DOT(self, t):
        r'\.'
        return t

    # This rule matches he Scene ID and stores the value as the integer ID.
    def t_SCENEID(self, t):
        r'\$[0-9]+'
        t.value = int(t.value[1:])
        return t

    # This rule matches string literals. String literals are enclosed only
    # within double quotes.
    def t_STRING(self, t):
        r'\"(?:\\.|[^\"\\])*\"'
        t.value = t.value[1:-1]
        return t

    # This function generates the INDENT token if a new indent is created,
    # generates no tokens if the indent level is the same, and generates a
    # DEDENT token for each indent level that is reduced.
    # All DEDENTs are not generated here. Only the DEDENTs on lines beginning
    # with a white space are geenrated here.
    # INDENTs and DEDENTs are generated by maintaining state with the help of
    # a stack.
    def t_INDENT(self, t):
        r'^[ \t\r\f\v]+'
        spaces = len(t.value)
        if spaces == self.indentstack[-1]:
            pass
        elif spaces > self.indentstack[-1]:
            t.value = spaces
            self.indentstack.append(t.value)
            return t
        else:
            t.value = self.indentstack.pop()
            t.type = 'DEDENT'
            t.lexer.lexpos -= spaces
            return t

    # This rule matches new lines and increments the line count.
    # If the indent level is lowered in a susequent line, this function also
    # generates an appropriate number of DEDENT tokens.
    # A state variable self.dedenting is used to maintain if the lexer is
    # currently in dedenting mode. This function is repeatedly encountered
    # until the stack is fully dendented. This is because there is no white
    # space at the beginning of the line.
    def t_NEWLINE(self, t):
        r'\n+[^ \t\r\f\v%]?'
        if t.value[-1] == '\n':
            t.value = len(t.value)
            t.lexer.lineno += t.value
            return t
        else:
            if self.dedenting:
                if self.indentstack[-1] > 0:
                    t.lexer.lexpos -= len(t.value)
                    t.value = self.indentstack.pop()
                    t.type = 'DEDENT'
                    return t
                else:
                    self.dedenting = False
                    t.lexer.lineno += len(t.value) - 1
                    t.lexer.lexpos -= 1
                    pass
            else:
                if self.indentstack[-1] > 0:
                    self.dedenting = True
                    t.lexer.lexpos -= len(t.value)
                    t.value = len(t.value) - 1
                    return t
                else:
                    t.value = len(t.value) - 1
                    t.lexer.lineno += t.value
                    t.lexer.lexpos -= 1
                    return t

    # All white spaces not at the beginning of a logical line are ignored.
    def t_ignore_whitespace(self, t):
        r'[ \t\r\f\v]+'

    # This rule is triggered if an error is encountered. The program exits with
    # an error code after printing an error
    def t_error(self, t):
        if isinstance(t, lex.LexToken):
            stderr.write("ERROR: Unrecognized character at Line " +
                         str(t.lexer.lineno) + ": '" + str(t.value) + "'\n")
        elif isinstance(t, str):
            stderr.write("ERROR: " + str(p) + "\n")
        exit(1)

    # This method provides an interface to the lexer's input(string) function
    def input(self, string_to_scan):
        self.lexer.input(string_to_scan)

    # This method provides an interface to the lexer's token() function
    def token(self):
        self.lasttoken = self.lexer.token()
        return self.lasttoken

    # This method prints all tokens scanned by the lexer. This method should be
    # called only after passing some input through the input(string) function.
    # This method is for testing purposes only.
    def printAllTokens(self):
        nextToken = self.token()
        while nextToken:
            print nextToken
            nextToken = self.token()
