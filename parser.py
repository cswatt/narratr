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

    # assumes start state only given once
    def p_blocks(self, p):
        '''blocks : scene_block newlines_optional
                  | item_block newlines_optional
                  | start_state newlines_optional
                  | blocks scene_block newlines_optional
                  | blocks item_block newlines_optional
                  | blocks start_state newlines_optional'''
        if p[1].type == "blocks" and p[2].type == "scene_block":
            p[1].children[0][p[2].value] = p[2]
            p[0] = p[1]
        elif p[1].type == "blocks" and p[2].type == "item_block":
            p[1].children[1][p[2].value] = p[2]
            p[0] = p[1]
        elif p[1].type == "blocks" and p[2].type == "start_state":
            p[1].children.append(p[2])
            p[0] = p[1]
        elif p[1].type == "scene_block":
            if(not isinstance(p[0], Node)):
                p[0] = Node(None, "blocks", [{}, {}])
            p[0].children[0][p[1].value] = p[1]
        elif p[1].type == "item_block":
            if(not isinstance(p[0], Node)):
                p[0] = Node(None, "blocks", [{}, {}])
            p[0].children[1][p[1].value] = p[1]
        elif p[1].type == "start_state":
            if(not isinstance(p[0], Node)):
                p[0] = Node(None, "blocks", [{}, {}])
            p[0].children.append(p[2])

    def p_newlines_optional(self, p):
        '''newlines_optional : newlines
                             | '''

    def p_newlines(self, p):
        '''newlines : newlines NEWLINE
                    | NEWLINE'''

    def p_scene_block(self, p):
        '''scene_block : SCENE SCENEID LCURLY newlines INDENT setup_block \
                          action_block cleanup_block DEDENT RCURLY
                       | SCENE SCENEID LCURLY newlines setup_block \
                          action_block cleanup_block RCURLY'''
        # This is set, but it still needs symbol table (SCENEID).
        if p[6].type == 'setup_block':
            children = [p[6], p[7], p[8]]
        elif p[5].type == 'setup_block':
            children = [p[5], p[6], p[7]]
        p[0] = Node(p[2], "scene_block", children)

    def p_item_block(self, p):
        '''item_block : ITEM ID calllist LCURLY newlines_optional RCURLY
                      | ITEM ID calllist LCURLY suite RCURLY'''
        if isinstance(p[3], Node):
            if p[5].type == "suite":
                children = [p[3], p[5]]
            else:
                children = [p[3]]
        p[0] = Node(p[2], "item_block", children)

    def p_start_state(self, p):
        'start_state : START COLON SCENEID'
        p[0] = Node(p[3], "start_state")

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
        if isinstance(p[3], Node):
            if p[3].type == 'suite':
                p[0] = Node(None, "cleanup_block", [p[3]])
            else:
                p[0] = Node(None, "cleanup_block")

    def p_suite(self, p):
        '''suite : simple_statement
                 | newlines INDENT statements DEDENT'''
        if p[3].type == "statements":
            p[0] = p[3]
        else:
            p[0] = p[1]
        p[0].type = "suite"

    def p_statements(self, p):
        '''statements : statements statement
                      | statement'''
        if p[1].type == "statements":
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = Node(None, "statements", [p[1]])

    def p_statement(self, p):
        '''statement : simple_statement
                     | block_statement'''
        # print p[1].type
        p[0] = p[1]
        p[0].type = "statement"

    def p_simple_statement(self, p):
        '''simple_statement : say_statement newlines
                            | exposition_statement newlines
                            | win_statement newlines
                            | lose_statement newlines
                            | flow_statement newlines
                            | expression_statement newlines'''
        if isinstance(p[1], Node):
            print p[1].type
            if p[1].type == "say_statement":
                p[0] = p[1]
                p[0].value = "say"

            if p[1].type == "exposition":
                p[0] = p[1]
                p[0].value = "exposition"

            if p[1].type == "win_statement":
                p[0] = p[1]
                p[0].value = "win"
            if p[1].type == "expression_statement":
                p[0] = p[1]
                p[0].value = "expression"
            if p[1].type == "flow_statement":
                p[0] = p[1]
                p[0].value = "flow"
            if p[1].type == "lose_statement":
                p[0] = p[1]
                p[0].value = "lose"

            p[0].type = "simple_statement"

    def p_say_statement(self, p):
        '''say_statement : SAY STRING'''
        p[0] = Node(None, "say_statement", [Node(p[2], "string")])

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
            children = [Node(p[2], "string", [])]
        p[0] = Node(None, "win_statement", children)

    def p_lose_statement(self, p):
        '''lose_statement : LOSE
                          | LOSE STRING'''
        if p[1] == "lose":
            if len(p) == 2:
                children = []
            if len(p) == 3:
                children = [Node(p[2], "string", [])]
            p[0] = Node(None, "lose_statement", children)

    def p_flow_statement(self, p):
        '''flow_statement : break_statement
                          | continue_statement
                          | moves_declaration
                          | moveto_statement'''
        if isinstance(p[1], Node):
            if p[1].type == 'break_statement':
                p[0] = p[1]
                p[0].value = 'break'
            if p[1].type == 'continue_statement':
                p[0] = p[1]
                p[0].value = 'continue'
            if p[1].type == 'moves_declaration':
                p[0] = p[1]
                p[0].value = 'moves'
            if p[1].type == 'moveto_statement':
                p[0] = p[1]
                p[0].type = 'moveto'
            p[0].type = 'simple_statement'

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
        p[0] = Node(None, p[1], [])
        p[0].type = 'direction'

    def p_moveto_statement(self, p):
        '''moveto_statement : MOVETO SCENEID'''

    def p_testlist(self, p):
        '''testlist : testlist COMMA test
                    | test'''

    # If there is just one possible rule and one child, the type of the node
    # still needs to be updated because parent AST nodes may check the type to
    # make decisions.
    def p_test(self, p):
        '''test : or_test'''
        p[0] = p[1]
        p[0].type = "test"

    def p_or_test(self, p):
        '''or_test : or_test OR and_test
                   | and_test'''
        if len(p) == 4:
            children = [p[1], p[3]]
            p[0] = Node(None, 'or', children)
            p[0].type = 'test'
        else:
            p[0] = p[1]
            p[0].type = 'test'

    def p_and_test(self, p):
        '''and_test : and_test AND not_test
                    | not_test'''
        if len(p) == 4:
            children = [p[1], p[3]]
            p[0] = Node(None, 'and', children)
            p[0].type = 'test'
        else:
            p[0] = p[1]
            p[0].type = 'test'

    def p_not_test(self, p):
        '''not_test : NOT not_test
                    | comparison'''

    def p_comparison(self, p):
        '''comparison : comparison comparison_op expression
                      | expression'''

    def p_expression(self, p):
        '''expression : arithmetic_expression'''
        p[0] = p[1]
        p[0].type = "expression"

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
        if len(p) == 4:
            p[0] = Node(None, p[2], [p[1], p[3]])
        else:
            p[0] = p[1]
        p[0].type = 'arithmetic_expression'

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
