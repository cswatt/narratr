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
# Primary Authors: Nivvedan Senthamil Selvan <nivvedan.s@columbia.edu>,
# Jonah Smith, Shloka Kini
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

from sys import stderr, exit
import ply.yacc as yacc
from ply.lex import LexToken
from lexer import LexerForNarratr
from node import Node
from symtab import SymTabEntry, SymTab

#Error checking: make sure when item added to list, the item is of the same
# type as the rest of the list

class ParserForNarratr:

    def __init__(self, **kwargs):
        self.lexer = LexerForNarratr()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self, **kwargs)
        self.symtab = SymTab()

    def p_program(self, p):
        "program : newlines_optional blocks"
        p[0] = Node(None, "program", [p[2]])

    # Assumes start state only given once--addressed in codegen.py
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
                          action_block cleanup_block DEDENT newlines_optional \
                          RCURLY
                       | SCENE SCENEID LCURLY newlines setup_block \
                          action_block cleanup_block RCURLY'''
        if isinstance(p[6], Node) and p[6].type == 'setup_block':
            children = [p[6], p[7], p[8]]
        elif isinstance(p[5], Node) and p[5].type == 'setup_block':
            children = [p[5], p[6], p[7]]
        p[0] = Node(p[2], "scene_block", children, lineno=p.lineno(2))
        try:
            self.symtab.insert(p[2], p[0], "scene", "GLOBAL", False)
        except:
            self.p_error("Error at line " + str(p.lineno(1)) +
                         ": A scene with the id '" + str(p[2]) + "' already" +
                         " exists.")
        self.pass_down(p[0], p[2])
        #check tokens to make sure that scene block is specificed correctly

    def p_item_block(self, p):
        '''item_block : ITEM ID calllist LCURLY newlines_optional RCURLY
                      | ITEM ID calllist LCURLY suite RCURLY'''
        if isinstance(p[5], Node) and p[5].type == "suite":
                children = [p[3], p[5]]
        else:
            children = [p[3]]
        p[0] = Node(p[2], "item_block", children, lineno=p.lineno(2))
        try:
            self.symtab.insert(p[2], p[0], "item", "GLOBAL", False)
        except:
            self.p_error("Error at line " + str(p.lineno(1)) +
                         ": An item with the id '" + str(p[2]) + "' already" +
                         " exists.")
        self.pass_down(p[0], p[2])
        #check tokens to make sure that item block is specified correctly

    def p_start_state(self, p):
        'start_state : START COLON SCENEID'
        p[0] = Node(p[3], "start_state", lineno=p.lineno(3))
        #check for syntax error in start state

    def p_setup_block(self, p):
        '''setup_block : SETUP COLON suite
                       | SETUP COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "setup_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "setup_block", lineno=p.lineno(1))
        #check tokens to make sure that setup block is specified

    def p_action_block(self, p):
        '''action_block : ACTION COLON suite
                        | ACTION COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "action_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "action_block", lineno=p.lineno(1))
        #make sure that action token is specified and color is used

    def p_cleanup_block(self, p):
        '''cleanup_block : CLEANUP COLON suite
                         | CLEANUP COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "cleanup_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "cleanup_block", lineno=p.lineno(1))
        #make sure that cleanup keyword and color both exist

    def p_suite(self, p):
        '''suite : simple_statement
                 | newlines INDENT statements DEDENT newlines_optional'''
        if isinstance(p[1], Node) and p[1].type == "simple_statement":
            p[0] = p[1]
        else:
            p[0] = p[3]
        p[0].type = "suite"
        #look for indent and dedent in suite

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
            if p[1].type == "say_statement":
                p[0] = p[1]
                p[0].value = "say"
            elif p[1].type == "exposition":
                p[0] = p[1]
                p[0].value = "exposition"
            elif p[1].type == "win_statement":
                p[0] = p[1]
                p[0].value = "win"
            elif p[1].type == "expression_statement":
                p[0] = p[1]
                p[0].value = "expression"
            elif p[1].type == "flow_statement":
                p[0] = p[1]
                p[0].value = "flow"
            elif p[1].type == "lose_statement":
                p[0] = p[1]
                p[0].value = "lose"

            p[0].type = "simple_statement"
        else:
            self.p_error("Syntax Error forming simple_statement.")

    def p_say_statement(self, p):
        '''say_statement : SAY testlist'''
        p[0] = Node(None, "say_statement", [p[2]], lineno=p[2].lineno)
        #look for say token for test list to be defined

    def p_exposition_statement(self, p):
        '''exposition_statement : EXPOSITION testlist'''
        if p[1] == "exposition":
            p[0] = Node(None, "exposition", [p[2]], lineno=p.lineno(1))

    def p_win_statement(self, p):
        '''win_statement : WIN
                         | WIN testlist'''
        if p[1] == "win":
            if len(p) == 2:
                children = []
            if len(p) == 3:
                children = [p[2]]
            p[0] = Node(None, "win_statement", children)
        #look for win token

    def p_lose_statement(self, p):
        '''lose_statement : LOSE
                          | LOSE testlist'''
        if p[1] == "lose":
            if len(p) == 2:
                children = []
            if len(p) == 3:
                children = [p[2]]
            p[0] = Node(None, "lose_statement", children)
        #look for lose token

    def p_flow_statement(self, p):
        '''flow_statement : break_statement
                          | continue_statement
                          | moves_declaration
                          | moveto_statement'''
        if isinstance(p[1], Node):
            if p[1].type == 'break_statement':
                temp_node = p[1]
                temp_node.value = 'break'
            elif p[1].type == 'continue_statement':
                temp_node = p[1]
                temp_node.value = 'continue'
            elif p[1].type == 'moves_declaration':
                p[0] = p[1]
                p[0].value = 'move'
                p[0].type = 'flow_statement'
                return p[0]
            elif p[1].type == 'moveto_statement':
                temp_node = p[1]
                temp_node.type = 'moveto'
            p[0] = Node(None, "flow_statement", [temp_node])

    def p_expression_statement(self, p):
        '''expression_statement : ID IS testlist
                                | GOD ID IS testlist
                                | testlist'''
        if isinstance(p[1], Node):
            p[0] = p[1]
            p[0].type = "expression_statement"
        elif p[1] == "god":
            children = [Node(p[2], "god_id"), p[4]]
            p[0] = Node("is", "expression_statement", children,
                        lineno=p[3].lineno)
        else:
            children = [Node(p[1], "id"), p[3]]
            p[0] = Node("is", "expression_statement", children,
                        lineno=p[3].lineno)
        #check for ID and is token look for god is token

    def p_break_statement(self, p):
        '''break_statement : BREAK'''
        p[0] = Node(p[1], 'break_statement', [])
        p[0].type = 'break_statement'
        #look for break token

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE'''
        p[0] = Node(p[1], 'continue_statement', [])
        p[0].type = 'continue_statement'
        #look for continue token

    def p_moves_declaration(self, p):
        '''moves_declaration : MOVES directionlist'''
        p[0] = p[2]
        p[0].type = 'moves_declaration'
        #look for moves and make sure there is something after it

    def p_directionlist(self, p):
        '''directionlist : direction LPARAN SCENEID RPARAN
                         | directionlist COMMA direction LPARAN SCENEID \
                                RPARAN'''
        if p[1].type == 'direction':
            p[1].children.append(Node(p[3], 'sceneid', [], lineno=p.lineno(3)))
            p[0] = Node(None, 'directionlist', [p[1]], lineno=p[1].lineno)
        else:
            p[3].children.append(Node(p[5], 'sceneid', [], lineno=p.lineno(5)))
            p[1].children.append(p[3])
            p[0] = p[1]
        p[0].type = 'directionlist'
        #look for parans around scene id, all three elements, and then comma

    def p_direction(self, p):
        '''direction : LEFT
                     | RIGHT
                     | UP
                     | DOWN'''
        p[0] = Node(p[1], 'direction', [], lineno=p.lineno(1))
        p[0].type = 'direction'
        #make sure this is defined in one of the four ways

    def p_moveto_statement(self, p):
        '''moveto_statement : MOVETO SCENEID'''
        p[0] = Node(None, 'moveto', [Node(p[2], "sceneid")], lineno=p.lineno(1))
        p[0].type = 'moveto_statement'
        # Make sure both moveto and scene id are found and make sure sceneid is
        # integer.

    def p_testlist(self, p):
        '''testlist : testlist COMMA test
                    | test'''
        if p[1].type == 'test':
            p[0] = Node(None, 'testlist', [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
            p[0].type = 'testlist'
        else:
            p[0] = p[1]
            p[0].children.append(p[3])
            p[0].type = 'testlist'
        #look for comma in case, 

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
        if p[1].type == 'and_test':
            p[0] = p[1]
            p[0].type = 'or_test'
        else:
            children = [p[1], p[3]]
            p[0] = Node(None, 'or', children, lineno=p[1].lineno)
            p[0].type = 'or_test'
        #look for or token in one case

    def p_and_test(self, p):
        '''and_test : and_test AND not_test
                    | not_test'''
        if p[1].type == 'not_test':
            p[0] = p[1]
            p[0].type = 'and_test'
        else:
            children = [p[1], p[3]]
            p[0] = Node(None, 'and', children, lineno=p[1].lineno)
            p[0].type = 'and_test'
        #look for and token

    def p_not_test(self, p):
        '''not_test : NOT not_test
                    | comparison'''
        if isinstance(p[1], Node) and p[1].type == 'comparison':
            p[0] = p[1]
            p[0].type = 'not_test'
        else:
            p[0] = Node(None, 'not', [p[2]], lineno=p[2].lineno)
            p[0].type = 'not_test'
        #look for not token

    def p_comparison(self, p):
        '''comparison : comparison comparison_op expression
                      | expression'''
        if p[1].type == 'comparison':
            p[0] = p[1]
            p[0].children.append(p[2])
            p[0].children.append(p[3])
        else:
            p[0] = Node(None, 'comparison', [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
        p[0].type = 'comparison'

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
        p[0] = Node(p[1], 'comparison_op', [], lineno=p.lineno(1))
        p[0].type = 'comparison_op'
        #make sure that comparison op is valid

    # In the first two productions for this rule, we need to ensure that
    # the two sides are combinable. We overload to PLUS operator to string
    # concatenation (which only allows two strings), and we allow floats
    # and integers to be combined freely.
    def p_arithmetic_expression(self, p):
        '''arithmetic_expression : arithmetic_expression PLUS term
                                 | arithmetic_expression MINUS term
                                 | term'''
        if p[1].type == 'term':
            p[0] = p[1]
            p[0].type = 'arithmetic_expression'
        else:
            # Extra condition for '+': allow string concatenation.
            if p[2] == "+":
                if p[1].v_type == "string":
                    if p[3].v_type == "string":
                        p[0] = Node(p[2], 'arithmetic_expression',
                                    [p[1], p[3]], "string", p.lineno(2))
                    elif p[3].v_type == "id":
                        p[0] = Node(p[2], 'arithmetic_expression',
                                    [p[1], p[3]], "id", p.lineno(2))
                    else:
                        self.combination_error(p)

            # Reject any expression trying to subtract strings.
            elif p[2] == "-":
                if p[1].v_type == "string" or p[3].v_type == "string":
                    self.combination_error(p)

            if p[0] is None:
                p[0] = self.combination_rules(p, 'arithmetic_expression')
        #look for plus and minus and make sure the second part is of type term

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | term INTEGERDIVIDE factor
                | factor '''
        if p[1].type == "term":
            # Reject anything with strings
            if (p[1].v_type in ["string", "list"] or
                    p[3].v_type in ["string", "list"]):
                self.combination_error(p)

            p[0] = self.combination_rules(p, 'term')
            # For integer division, we can just reset the v_type
            if p[2] == "//":
                p[0].v_type = "integer"
            p[0].lineno = p.lineno(3)
        else:
            p[0] = Node(None, 'term', [p[1]], p[1].v_type, lineno=p[1].lineno)
            p[0].type = 'term'
        # Look for the terms, times, divide, and integerdivide in the ones
        # longer than factor

    def p_factor(self, p):
        '''factor : PLUS factor
                  | MINUS factor
                  | power'''
        if p[1].type == 'power':
            p[0] = p[1]
            p[0].type = 'factor'
            if p[0].value == "str":
                p[0].v_type = "string"
        else:
            p[0] = Node(p[1], 'factor', [p[2]], p[2].v_type,
                        lineno=p.lineno(2))
        #look for plus and minus signs

    def p_power(self, p):
        '''power : power trailer
                 | atom'''
        if p[1].type == 'power':
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = p[1]
            p[0].type = 'power'

    def p_atom_node(self, p):
        '''atom : LPARAN test RPARAN
                | list
                | number
                | boolean'''
        if isinstance(p[1], Node):
            p[0] = p[1]
        else:
            p[0] = p[2]
        p[0].type = 'atom'
        #Look for parans around test in that one case
        #check to make sure first node is of type list, number, or boolean in the alternatecase

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = Node(p[1], 'atom', [], "string", lineno=p.lineno(1))
        #check type string

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = Node(p[1], 'atom', [], "id", lineno=p.lineno(1))
        #check type ID

    def p_trailer(self, p):
        '''trailer : calllist
                   | DOT ID'''
        if isinstance(p[1], Node) and p[1].type == "calllist":
            p[0] = p[1]
            p[0].type = 'trailer'
        else:
            p[0] = Node(None, 'trailer',
                        [Node(p[1], 'dot', [], lineno=p.lineno(1)),
                            Node(p[2], 'id',  [], lineno=p.lineno(2))])
        #check of type calllist or dot id tokens

    def p_list(self, p):
        '''list : LSQUARE RSQUARE
                | LSQUARE testlist RSQUARE'''
        if isinstance(p[2], Node) and p[2].type == 'testlist':
            p[0] = p[2]
            p[0].type = 'list'
            p[0].v_type = 'list'
            p[0].lineno = p.lineno(2)
        else:
            p[0] = Node(None, "list", [], "list", p[1].lineno)
        #check lsquare and rsquare balanced
        #check test list between or that they are empty

    def p_number_int(self, p):
        '''number : INTEGER'''
        p[0] = Node(p[1], 'number', [], "integer", lineno=p.lineno(1))
        #make sure of type integer

    def p_number_float(self, p):
        '''number : FLOAT'''
        p[0] = Node(p[1], 'number', [], "float", lineno=p.lineno(1))
        #make sure of float type

    def p_boolean(self, p):
        '''boolean : TRUE
                   | FALSE'''
        p[0] = Node(p[1], 'boolean', [], "boolean", lineno=p.lineno(1))
        # make sure token is true or false

    def p_calllist(self, p):
        '''calllist : LPARAN args RPARAN
                    | LPARAN RPARAN'''
        if isinstance(p[2], Node):
            p[0] = p[2]
        else:
            p[0] = Node(None, 'calllist', [])
        p[0].type = 'calllist'
        # make sure that calllist is Lparan and RParan balanced
        # check that args is bewteen then or that they are empty

    def p_args(self, p):
        '''args : args COMMA expression
                | expression'''
        if p[1].type == 'args':
            p[0] = p[1]
            p[0].children.append(p[3])
        else:
            p[0] = Node(None, 'args', [p[1]], lineno=p[1].lineno)
        p[0].type = 'args'
        #Check for comma to add expression and type of expression

    def p_block_statement(self, p):
        '''block_statement : if_statement
                           | while_statement'''

        if isinstance(p[1], Node):
            if p[1].type == 'if_statement':
                p[0] = p[1]
                p[0].value = 'if'
            elif p[1].type == 'while_statement':
                p[0] = p[1]
                p[0].value = 'while'
        p[0].type = 'block_statement'

    def p_if_statement(self, p):
        '''if_statement : IF test COLON suite elif_statements ELSE COLON suite
                        | IF test COLON suite ELSE COLON suite
                        | IF test COLON suite elif_statements
                        | IF test COLON suite'''
        if len(p) == 9:
            p[0] = Node(None, 'if_statement', [p[2], p[4], p[5], p[8]],
                        lineno=p[2].lineno)
            p[8].value = 'else'
        elif len(p) == 8:
            p[0] = Node(None, 'if_statement', [p[2], p[4], p[7]],
                        lineno=p[2].lineno)
            p[7].value = 'else'
        elif len(p) == 6:
            p[0] = Node(None, 'if_statement', [p[2], p[4], p[5]],
                        lineno=p[2].lineno)
        else:
            p[0] = Node(None, 'if_statement', [p[2], p[4]], lineno=p[2].lineno)
        p[0].type = 'if_statement'
        #Look for if token, colon, else, colon, and test is of type test

    def p_elif_statements(self, p):
        '''elif_statements : elif_statements ELIF test COLON suite
                           | ELIF test COLON suite'''
        if isinstance(p[1], Node) and p[1].type == 'elif_statements':
            p[0] = p[1]
            new_elif = Node(None, 'elif_statements', [p[3], p[5]])
            p[0].children.append(new_elif)
        else:
            p[0] = Node(None, 'elif_statements', [p[2], p[4]],
                        lineno=p[2].lineno)
        p[0].type = 'elif_statements'
        #look for elif token and colon token

    def p_while_statement(self, p):
        '''while_statement : WHILE test COLON suite'''
        p[0] = Node(p[2], 'while_statement', [p[2], p[4]], lineno=p[2].lineno)
        p[0].type = 'while_statement'

    # In order to create SymTab entries (in particular, in order to know
    # the appropriate scope) for named entities discovered below a main
    # branch (i.e. variables in a scene), we need to travel back down
    # the branches once we get to the main branch. This function does so,
    # creating symtab entries as it goes. It is called recursively on
    # every branch, looking for named entities. It takes as its argument
    # a branch and the scope to be assigned to all found named entities.
    def pass_down(self, branch, scope):
        if isinstance(branch, Node) and branch.type == "statement":
            if branch.value == "expression":
                for i, child in enumerate(branch.children):
                    if child.type == "id":
                        try:
                            self.symtab.insert(child.value,
                                               branch.children[i+1],
                                               branch.children[i+1].v_type,
                                               scope, False)
                        except:
                            pass
                    if child.type == "god_id":
                        try:
                            self.symtab.insert(child.value,
                                               branch.children[i+1],
                                               branch.children[i+1].v_type,
                                               scope, True)
                        except:
                            pass

        if isinstance(branch, Node):
            for child in branch.children:
                self.pass_down(child, scope)

    # Check numbers for interoperability. If they are of
    # differing types, the result is always the more general of
    # the two data types (i.e. float).
    def combination_rules(self, p, n_type):
        # Keep anything for "id", we'll have to check existance and resolve
        # type later.
        if p[1].v_type == "id" or p[3].v_type == "id":
            p[0] = Node(p[2], n_type, [p[1], p[3]], "id", p.lineno(2))
        elif p[1].v_type == "integer":
            if p[3].v_type == "integer":
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "integer", p.lineno(2))
            elif p[3].v_type == "float":
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "float", p.lineno(2))
            else:
                self.combination_error(p)
        elif p[1].v_type == "float":
            if p[3].v_type in ["integer", "float"]:
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "float", p.lineno(2))
            else:
                self.combination_error(p)
        elif p[1].v_type == "list":
            if p[3].v_type == "list":
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "list", p.lineno(2))
            else:
                self.combination_error(p)

        elif p[1].v_type == "boolean":
                self.combination_error(p)

        return p[0]

    def combination_error(self, p):
        self.p_error("Type error at line " + str(p.lineno(2)) +
                     ": cannot combine '" + p[1].v_type +
                     "' with '" + p[3].v_type + "'")

    def p_error(self, p):
        if isinstance(p, LexToken):
            stderr.write("Syntax Error at Line " + str(p.lineno) + ": " +
                         "at token '" + str(p.value) + "'\n")
        elif isinstance(p, str):
            stderr.write("Syntax Error: " + str(p) + "\n")
        exit(1)

    def parse(self, string_to_parse, **kwargs):
        return self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
