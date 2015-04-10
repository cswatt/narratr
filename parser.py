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
        "program : newlines_optional blocks"
        p[0] = Node(None, "program", [p[2]])

    def p_blocks(self, p):
        '''blocks : scene_block newlines_optional
                  | item_block newlines_optional
                  | start_state newlines_optional
                  | blocks scene_block newlines_optional
                  | blocks item_block newlines_optional
                  | blocks start_state newlines_optional'''
        children = p[1:-1]
        p[0] = Node(None, "blocks", children)

    def p_newlines_optional(self, p):
        '''newlines_optional : newlines
                             | '''
        p[0] = Node(None, "newlines_optional")

    def p_newlines(self, p):
        '''newlines : newlines NEWLINE
                    | NEWLINE'''
        p[0] = Node(None, "newlines")

    def p_scene_block(self, p):
        '''scene_block : SCENE SCENEID LCURLY newlines INDENT \
                          setup_block action_block cleanup_block DEDENT RCURLY
                       | SCENE SCENEID LCURLY newlines setup_block action_block \
                          cleanup_block RCURLY'''
        # create a SCENE leaf node
        s = Node(None, "scene")
        # create a SCENEID leaf node
        sid = Node(p[2], "sceneid")
        # probably add to the symbol table here

        children = [s, sid]

        if len(p) == 11:
            children += [p[6], p[7], p[8]]
        elif len(p) == 9:
            children += [p[5], p[6], p[7]]
        p[0] = Node(None, "scene_block", children)

    def p_item_block(self, p):
        '''item_block : ITEM ID calllist LCURLY newlines_optional RCURLY
                      | ITEM ID calllist LCURLY suite RCURLY'''

    def p_start_state(self, p):
        'start_state : START COLON SCENEID'
        p[0] = Node(p[3], "start_state", [])

    def p_setup_block(self, p):
        '''setup_block : SETUP COLON suite
                       | SETUP COLON newlines'''
        if isinstance(p[3], Node):
            if p[3].type == "suite":
                p[0] = Node(None, "setup_block", [p[3]])
            else:
                p[0] = Node(None, "setup_block")

    def p_action_block(self, p):
        '''action_block : ACTION COLON suite
                        | ACTION COLON newlines'''
        if isinstance(p[3], Node):
            if p[3].type == "suite":
                p[0] = Node(None, "action_block", [p[3]])
            else:
                p[0] = Node(None, "action_block")

    def p_cleanup_block(self, p):
        '''cleanup_block : CLEANUP COLON suite
                         | CLEANUP COLON newlines'''
        if len(p) == 7:
            children = [p[5]]
        if len(p) == 4:
            children = []
        p[0] = Node(None, "cleanup_block", children)

    def p_suite(self, p):
        '''suite : simple_statement
                 | newlines INDENT statements DEDENT'''
        if len(p) == 2:
            children = [p[1]]
        elif len(p) == 5:
            children = [p[3]]

        p[0] = Node(None, "suite", children)

    def p_statements(self, p):
        '''statements : statements statement
                      | statement'''
        p[0] = Node(None, "statements", p[1:])

    def p_statement(self, p):
        '''statement : simple_statement
                     | block_statement'''
        p[0] = Node(None, "statement", [p[1]])

    def p_simple_statement(self, p):
        '''simple_statement : say_statement newlines
                            | exposition_statement newlines
                            | win_statement newlines
                            | lose_statement newlines
                            | flow_statement newlines
                            | expression_statement newlines'''
        if isinstance(p[1], Node):
            p[0] = Node(None, "simple_statement", [p[1]])

    def p_say_statement(self, p):
        '''say_statement : SAY STRING'''
        if p[1] == "say":
            p[0] = Node(None, "say", [Node(p[2], "string")])
    
    def p_exposition_statement(self, p):
        '''exposition_statement : EXPOSITION STRING'''
        if p[1] == "exposition":
            p[0] = Node(None, "exposition", [Node(p[2], "string")])

    def p_win_statement(self, p):
        '''win_statement : WIN
                         | WIN STRING'''
        if len(p) == 2:
            children = []
        if len(p) == 3:
            children = [Node(p[2], "string")]
        p[0] = Node(None, "win", children)

    def p_lose_statement(self, p):
        '''lose_statement : LOSE
                          | LOSE STRING'''
        if p[1] == "lose":
            if len(p) == 2:
                children = []
            if len(p) == 3:
                children = [Node(p[2], "string", [])]
            p[0] = Node(None, "lose", children)

    def p_flow_statement(self, p):
        '''flow_statement : break_statement
                          | continue_statement
                          | moves_declaration
                          | moveto_statement'''

    def p_expression_statement(self, p):
        '''expression_statement : testlist IS testlist
                                | GOD testlist IS testlist'''

    def p_break_statement(self, p):
        '''break_statement : BREAK'''

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE'''

    def p_moves_declaration(self, p):
        '''moves_declaration : MOVES directionlist'''
    
    def p_directionlist(self, p):
        '''directionlist : direction LPARAN SCENEID RPARAN
                         | directionlist COMMA direction LPARAN SCENEID \
                                RPARAN'''

    def p_direction(self, p):
        '''direction : LEFT
                     | RIGHT
                     | UP
                     | DOWN'''

    def p_moveto_statement(self, p):
        '''moveto_statement : MOVETO SCENEID''' 

    def p_testlist(self, p):
        '''testlist : testlist COMMA test
                    | test'''

    def p_test(self, p):
        '''test : or_test'''

    def p_or_test(self, p):
        '''or_test : or_test OR and_test
                   | and_test'''

    def p_and_test(self, p):
        '''and_test : and_test AND not_test
                    | not_test'''

    def p_not_test(self, p):
        '''not_test : NOT not_test
                    | comparison'''

    def p_comparison(self, p):
        '''comparison : comparison comparison_op expression
                      | expression'''

    def p_expression(self, p):
        '''expression : arithmetic_expression'''

    def p_comparison_op(self, p):
        '''comparison_op : LESS
                         | GREATER
                         | LESSEQUALS
                         | GREATEREQUALS
                         | EQUALS
                         | NOTEQUALS
                         | NOT EQUALS'''


    def p_arithmetic_expression(self, p):
        '''arithmetic_expression : arithmetic_expression PLUS term
                                 | arithmetic_expression MINUS term
                                 | term'''

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | term INTEGERDIVIDE factor
                | factor '''

    def p_factor(self, p):
        '''factor : PLUS factor
                  | MINUS factor
                  | power'''

    def p_power(self, p):
        '''power : power trailer
                 | atom'''

    def p_atom(self, p):
        '''atom : number
                | strings
                | boolean
                | ID'''

    def p_trailer(self, p):
        '''trailer : LPARAN RPARAN
                   | LPARAN args RPARAN
                   | DOT ID'''

    def p_number(self, p):
        '''number : INTEGER
                  | FLOAT'''

    def p_strings(self, p):
        '''strings : strings PLUS STRING
                   | STRING'''

    def p_boolean(self, p):
        '''boolean : TRUE
                   | FALSE'''

    def p_calllist(self, p):
        '''calllist : LPARAN args RPARAN
                    | LPARAN RPARAN'''

    def p_args(self, p):
        '''args : args COMMA expression
                | expression'''

    def p_block_statement(self, p):
        '''block_statement : if_statement
                           | while_statement'''

    def p_if_statement(self, p):
        '''if_statement : IF test COLON suite elif_statements ELSE COLON suite
                        | IF test COLON suite ELSE COLON suite
                        | IF test COLON suite elif_statements
                        | IF test COLON suite'''

    def p_elif_statements(self, p):
        '''elif_statements : elif_statements ELIF test COLON suite
                           | ELIF test COLON suite'''

    def p_while_statement(self, p):
        '''while_statement : WHILE test COLON suite''' 

    def p_error(self, p):
        print "Syntax Error in input at ", p

    def parse(self, string_to_parse, **kwargs):
        return self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
