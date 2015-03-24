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
        "program : newlines blocks"

    def p_blocks(self, p):
        '''blocks : sceneblock newlines
                  | itemblock newlines
                  | startstate newlines
                  | blocks sceneblock newlines
                  | blocks itemblock newlines
                  | blocks startstate newlines'''

    def p_newlines(self, p):
        '''newlines : NEWLINE
                    | '''

    def p_sceneblock(self, p):
        "sceneblock : SCENE SCENEID LCURLY NEWLINE INDENT setupblock actionblock cleanupblock DEDENT RCURLY"

    def p_itemblock(self, p):
        "itemblock : ITEM ID calllist LCURLY newlines statements RCURLY"

    def p_startstate(self, p):
        'startstate : START COLON SCENEID'

    def p_setupblock(self, p):
        '''setupblock : SETUP COLON NEWLINE INDENT statements DEDENT
                      | SETUP COLON NEWLINE'''

    def p_actionblock(self, p):
        '''actionblock : ACTION COLON NEWLINE INDENT statements DEDENT
                       | ACTION COLON NEWLINE'''

    def p_cleanupblock(self, p):
        '''cleanupblock : CLEANUP COLON NEWLINE INDENT statements DEDENT
                        | CLEANUP COLON NEWLINE'''

    def p_statements(self, p):
        '''statements : statementlist
                      | '''

    def p_statementlist(self, p):
        '''statementlist : statementlist statement
                         | statement'''

    def p_statement(self, p):
        '''statement : simplestatement
                     | blockstatement'''

    def p_simplestatement(self, p):
        '''simplestatement : SAY STRING NEWLINE
                           | WIN NEWLINE
                           | WIN STRING NEWLINE
                           | LOSE NEWLINE
                           | LOSE STRING NEWLINE
                           | EXPOSITION STRING NEWLINE
                           | assignstatement'''

    def p_blockstatement(self, p):
        '''blockstatement : IF booleanexpression COLON NEWLINE INDENT statements DEDENT
                          | WHILE booleanexpression COLON NEWLINE INDENT statements DEDENT'''

    def p_assignstatement(self, p):
        '''assignstatement : ID IS expression'''

    def p_expression(self, p):
        '''expression : arithmeticexpression
                      | booleanexpression'''

    def p_arithmeticexpression(self, p):
        '''arithmeticexpression : arithmeticexpression PLUS term
                                | arithmeticexpression MINUS term
                                | term'''

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | term INTEGERDIVIDE factor
                | factor '''

    def p_factor(self, p):
        '''factor : LPARAN arithmeticexpression RPARAN
                  | atom
                  | number
                  | STRING'''

    def p_atom(self, p):
        '''atom : atom calllist
                | atom DOT ID
                | ID'''

    def p_calllist(self, p):
        '''calllist : LPARAN args RPARAN
                    | LPARAN RPARAN'''

    def p_number(self, p):
        '''number : INTEGER
                  | FLOAT'''

    def p_booleanexpression(self, p):
        '''booleanexpression : booleanterm OR booleanexpression
                             | booleanterm'''

    def p_booleanterm(self, p):
        '''booleanterm : booleanfactor AND booleanfactor
                       | booleanfactor'''

    def p_booleanfactor(self, p):
        '''booleanfactor : LPARAN booleanexpression RPARAN
                         | conditional
                         | FALSE
                         | TRUE'''

    def p_conditional(self, p):
        '''conditional : factor conditionalop factor'''

    def p_conditionalop(self, p):
        '''conditionalop : LESS
                         | GREATER
                         | LESSEQUALS
                         | GREATEREQUALS
                         | EQUALS'''

    def p_args(self, p):
        '''args : args COMMA expression
                | expression'''

    def p_error(self, p):
        print "Syntax Error in input at ", p

    def parse(self, string_to_parse, **kwargs):
        self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
