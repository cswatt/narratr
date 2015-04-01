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
from node import Node


class ParserForNarratr:

    def __init__(self, **kwargs):
        self.lexer = LexerForNarratr()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_program(self, p):
        "program : optionalnewlines blocks"
        p[0] = Node(None, "program", p[1:3])

    def p_blocks(self, p):
        '''blocks : sceneblock optionalnewlines
                  | itemblock optionalnewlines
                  | startstate optionalnewlines
                  | blocks sceneblock optionalnewlines
                  | blocks itemblock optionalnewlines
                  | blocks startstate optionalnewlines'''
        p[0] = Node(None, "blocks", p[1:])

    def p_optionalnewlines(self, p):
        '''optionalnewlines : newlines
                            | '''
        p[0] = Node(None, "optionalnewlines", [])

    def p_newlines(self, p):
        '''newlines : newlines NEWLINE
                    | NEWLINE'''
        p[0] = Node(None, "newlines", [])

    def p_sceneblock(self, p):
        '''sceneblock : SCENE SCENEID LCURLY newlines INDENT \
                          setupblock actionblock cleanupblock DEDENT RCURLY
                      | SCENE SCENEID LCURLY newlines setupblock actionblock \
                          cleanupblock RCURLY'''
        # create a SCENE leaf node
        s = Node(None, "scene", [])
        # create a SCENEID leaf node
        sid = Node(p[2], "sceneid", [])

        children = [s, sid]

        if len(p) == 11:
            children += [p[6], p[7], p[8]]
        elif len(p) == 9:
            children += [p[5], p[6], p[7]]
        p[0] = Node(None, "sceneblock", children)

    def p_itemblock(self, p):
        '''itemblock : ITEM ID calllist LCURLY optionalnewlines statements \
                          RCURLY
                     | ITEM ID calllist LCURLY optionalnewlines INDENT \
                          statements DEDENT RCURLY'''

    def p_startstate(self, p):
        'startstate : START COLON SCENEID'
        p[0] = Node(p[3], "startstate", [])

    def p_setupblock(self, p):
        '''setupblock : SETUP COLON newlines INDENT statements DEDENT
                      | SETUP COLON newlines'''
        if len(p) == 7:
            children = [p[5]]
        if len(p) == 4:
            children = []
        p[0] = Node(None, "setupblock", children)

    def p_actionblock(self, p):
        '''actionblock : ACTION COLON newlines INDENT statements DEDENT
                       | ACTION COLON newlines'''
        if len(p) == 7:
            children = [p[5]]
        if len(p) == 4:
            children = []
        p[0] = Node(None, "actionblock", children)

    def p_cleanupblock(self, p):
        '''cleanupblock : CLEANUP COLON newlines INDENT statements DEDENT
                        | CLEANUP COLON newlines'''
        if len(p) == 7:
            children = [p[5]]
        if len(p) == 4:
            children = []
        p[0] = Node(None, "actionblock", children)

    def p_statements(self, p):
        '''statements : statementlist
                      | '''
        p[0] = Node(None, "statements", p[1:])

    def p_statementlist(self, p):
        '''statementlist : statementlist statement
                         | statement'''
        p[0] = Node(None, "statementlist", p[1:])

    def p_statement(self, p):
        '''statement : simplestatement
                     | blockstatement'''
        p[0] = Node(None, "statement", [p[1]])

    def p_simplestatement(self, p):
        # I think the grammar for "SAY", "WIN", "LOSE" might need a STRING
        # instead of args?
        #
        # The real problem is that args is made up of expressions, which are
        # only arithmetic and boolean at the moment.
        '''simplestatement : SAY STRING newlines
                           | WIN newlines
                           | WIN args newlines
                           | LOSE newlines
                           | LOSE args newlines
                           | EXPOSITION STRING newlines
                           | ID IS expression newlines
                           | GOD ID IS expression newlines
                           | MOVES directionlist newlines
                           | MOVE direction newlines
                           | BREAK newlines
                           | CONTINUE newlines
                           | POCKET DOT ID atom newlines'''
        if p[1] == "say":
            p[0] = Node(None, "say", [Node(p[2], "string", [])])

        if p[1] == "win":
            if len(p) == 3:
                children = []
            if len(p) == 4:
                children = [p[2]]
            p[0] = Node(None, "win", children)

    def p_directionlist(self, p):
        '''directionlist : direction LPARAN SCENEID RPARAN
                         | directionlist COMMA direction LPARAN SCENEID \
                                RPARAN'''

    def p_direction(self, p):
        '''direction : LEFT
                     | RIGHT
                     | UP
                     | DOWN'''

    def p_blockstatement(self, p):
        '''blockstatement : ifstatement
                          | WHILE booleanexpression COLON newlines INDENT \
                                statements DEDENT optionalnewlines'''

    def p_ifstatement(self, p):
        '''ifstatement : IF booleanexpression COLON newlines INDENT \
                                statements DEDENT optionalnewlines
                       | IF booleanexpression COLON newlines INDENT \
                                statements DEDENT ELSE COLON newlines \
                                INDENT statements DEDENT optionalnewlines
                       | IF booleanexpression COLON newlines INDENT \
                                statements DEDENT ELSE ifstatement'''

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

    def p_boolean(self, p):
        '''boolean : TRUE
                   | FALSE'''

    def p_booleanexpression(self, p):
        '''booleanexpression : booleanterm OR booleanexpression
                             | booleanterm'''

    def p_booleanterm(self, p):
        '''booleanterm : booleanfactor AND booleanfactor
                       | booleanfactor EQUALS booleanfactor
                       | booleanfactor'''

    def p_booleanfactor(self, p):
        '''booleanfactor : LPARAN booleanexpression RPARAN
                         | NOT factor
                         | conditional
                         | boolean'''

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
        return self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
