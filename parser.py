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

# Error checking: make sure when item added to list, the item is of the same
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

    # Start state may be given multiple times. This is handled in the code
    # generator.
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
            self._semantic_error("Error at line " + str(p.lineno(1)) +
                                 ": A scene with the id '" + str(p[2]) +
                                 "' already exists.")
        self.pass_down(p[0], p[2])

    def p_item_block(self, p):
        '''item_block : ITEM ID itemparams LCURLY newlines_optional RCURLY
                      | ITEM ID itemparams LCURLY suite RCURLY'''
        if isinstance(p[5], Node) and p[5].type == "suite":
            children = [p[3], p[5]]
        else:
            children = [p[3]]
        p[0] = Node(p[2], "item_block", children, lineno=p.lineno(2))
        try:
            self.symtab.insert(p[2], p[0], "item", "GLOBAL", False)
        except:
            self._semantic_error("Error at line " + str(p.lineno(1)) +
                                 ": An item with the id '" + str(p[2]) +
                                 "' already exists.")
        self.pass_down(p[0], p[2])

    def p_start_state(self, p):
        'start_state : START COLON SCENEID'
        p[0] = Node(p[3], "start_state", lineno=p.lineno(3))

    def p_setup_block(self, p):
        '''setup_block : SETUP COLON suite
                       | SETUP COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "setup_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "setup_block", lineno=p.lineno(1))

    def p_action_block(self, p):
        '''action_block : ACTION COLON suite
                        | ACTION COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "action_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "action_block", lineno=p.lineno(1))

    def p_cleanup_block(self, p):
        '''cleanup_block : CLEANUP COLON suite
                         | CLEANUP COLON newlines'''
        if isinstance(p[3], Node) and p[3].type == "suite":
            p[0] = Node(None, "cleanup_block", [p[3]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, "cleanup_block", lineno=p.lineno(1))

    def p_suite(self, p):
        '''suite : simple_statement
                 | newlines INDENT statements DEDENT newlines_optional'''
        if isinstance(p[1], Node) and p[1].type == "simple_statement":
            p[0] = Node("simple", "suite", [p[1]], lineno=p[1].lineno)
        else:
            p[0] = Node("statements", "suite", [p[3]], lineno=p.lineno(2))

    def p_statements(self, p):
        '''statements : statements statement
                      | statement'''
        if p[1].type == "statements":
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = Node(None, "statements", [p[1]], lineno=p[1].lineno)

    def p_statement(self, p):
        '''statement : simple_statement
                     | block_statement'''
        if p[1].type == 'simple_statement':
            value = 'simple'
        else:
            value = 'block'
        p[0] = Node(value, 'statement', [p[1]], lineno=p[1].lineno)

    def p_simple_statement(self, p):
        '''simple_statement : say_statement newlines
                            | exposition_statement newlines
                            | win_statement newlines
                            | lose_statement newlines
                            | flow_statement newlines
                            | expression_statement newlines'''
        if isinstance(p[1], Node):
            if p[1].type == "say_statement":
                value = "say"
            elif p[1].type == "exposition":
                value = "exposition"
            elif p[1].type == "win_statement":
                value = "win"
            elif p[1].type == "expression_statement":
                value = "expression"
            elif p[1].type == "flow_statement":
                value = "flow"
            elif p[1].type == "lose_statement":
                value = "lose"
        else:
            self._semantic_error("Syntax Error forming simple_statement.")
        p[0] = Node(value, 'simple_statement', [p[1]], lineno=p[1].lineno)

    def p_say_statement(self, p):
        '''say_statement : SAY testlist'''
        p[0] = Node(None, "say_statement", [p[2]], lineno=p[2].lineno)

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
            p[0] = Node("win", "win_statement", children)

    def p_lose_statement(self, p):
        '''lose_statement : LOSE
                          | LOSE testlist'''
        if p[1] == "lose":
            if len(p) == 2:
                children = []
            if len(p) == 3:
                children = [p[2]]
            p[0] = Node("lose", "lose_statement", children)

    def p_flow_statement(self, p):
        '''flow_statement : break_statement
                          | continue_statement
                          | moves_declaration
                          | moveto_statement'''
        if isinstance(p[1], Node):
            if p[1].type == 'break_statement':
                value = "break"
            elif p[1].type == 'continue_statement':
                value = "continue"
            elif p[1].type == 'moves_declaration':
                value = "moves"
            elif p[1].type == 'moveto_statement':
                value = "moveto"
        else:
            self._semantic_error("Parse error in flow_statement.")
        p[0] = Node(value, "flow_statement", [p[1]], lineno=p[1].lineno)

    def p_expression_statement(self, p):
        '''expression_statement : ID IS testlist
                                | GOD ID IS testlist
                                | testlist'''
        if isinstance(p[1], Node):
            p[0] = Node("testlist", "expression_statement", [p[1]],
                        lineno=p[1].lineno)
        elif p[1] == "god":
            p[0] = Node("godis", "expression_statement", [Node(p[2], "god_id"),
                        p[4]], lineno=p.lineno(1))
        else:
            p[0] = Node("is", "expression_statement", [Node(p[1], "id"), p[3]],
                        lineno=p.lineno(1))

    def p_break_statement(self, p):
        '''break_statement : BREAK'''
        p[0] = Node(p[1], 'break_statement', [], lineno=p.lineno(1))

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE'''
        p[0] = Node(p[1], 'continue_statement', [], lineno=p.lineno(1))

    def p_moves_declaration(self, p):
        '''moves_declaration : MOVES directionlist'''
        p[0] = Node("moves", 'moves_declaration', [p[2]], lineno=p.lineno(1))

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

    def p_direction(self, p):
        '''direction : LEFT
                     | RIGHT
                     | UP
                     | DOWN'''
        p[0] = Node(p[1], 'direction', [], lineno=p.lineno(1))

    def p_moveto_statement(self, p):
        '''moveto_statement : MOVETO SCENEID'''
        p[0] = Node('moveto', 'moveto_statement', [Node(p[2], "sceneid")],
                    lineno=p.lineno(1))

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

    def p_test(self, p):
        '''test : or_test'''
        p[0] = Node(None, 'test', [p[1]], lineno=p[1].lineno)

    def p_or_test(self, p):
        '''or_test : or_test OR and_test
                   | and_test'''
        if p[1].type == 'and_test':
            p[0] = Node(None, 'or_test', [p[1]], lineno=p[1].lineno)
        else:
            children = [p[1], p[3]]
            p[0] = Node('or', 'or_test', children, lineno=p[1].lineno)

    def p_and_test(self, p):
        '''and_test : and_test AND not_test
                    | not_test'''
        if p[1].type == 'not_test':
            p[0] = Node(None, 'and_test', [p[1]], lineno=p[1].lineno)
        else:
            children = [p[1], p[3]]
            p[0] = Node('and', 'and_test', children, lineno=p[1].lineno)

    def p_not_test(self, p):
        '''not_test : NOT not_test
                    | comparison'''
        if isinstance(p[1], Node) and p[1].type == 'comparison':
            p[0] = Node(None, 'not_test', [p[1]], lineno=p[1].lineno)
        else:
            p[0] = Node('not', 'not_test', [p[2]], lineno=p[2].lineno)

    def p_comparison(self, p):
        '''comparison : comparison comparison_op expression
                      | expression'''
        if p[1].type == 'comparison':
            p[0] = Node('comparison', 'comparison', [p[1], p[2], p[3]],
                        p[1].v_type, lineno=p[1].lineno)
        else:
            p[0] = Node(None, 'comparison', [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
        p[0].type = 'comparison'

    def p_expression(self, p):
        '''expression : arithmetic_expression'''
        p[0] = Node(p[1].value, "expression", [p[1]], lineno=p[1].lineno)

    def p_comparison_op(self, p):
        '''comparison_op : LESS
                         | GREATER
                         | LESSEQUALS
                         | GREATEREQUALS
                         | EQUALS
                         | NOTEQUALS
                         | NOT EQUALS'''
        p[0] = Node(p[1], 'comparison_op', [], lineno=p.lineno(1))

    # In the first two productions for this rule, we need to ensure that
    # the two sides are combinable. We overload to PLUS operator to string
    # concatenation (which only allows two strings), and we allow floats
    # and integers to be combined freely.
    def p_arithmetic_expression(self, p):
        '''arithmetic_expression : arithmetic_expression PLUS term
                                 | arithmetic_expression MINUS term
                                 | term'''
        if p[1].type == 'term':
            p[0] = Node("term", "arithmetic_expression", [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
        else:
            # Extra condition for '+': allow string concatenation.
            if p[1].v_type == "string":
                if p[2] == "+":
                    if p[3].v_type in ["string", "id"]:
                        p[0] = Node(p[2], 'arithmetic_expression',
                                    [p[1], p[3]], "string", p.lineno(2))
                    else:
                        self._semantic_error(p, err_type="combination_error")
                # Reject any expression trying to subtract strings.
                elif p[2] == "-":
                    self._semantic_error(p, err_type="combination_error")
            else:
                p[0] = self.combination_rules(p, 'arithmetic_expression')

    def p_term(self, p):
        '''term : term TIMES factor
                | term DIVIDE factor
                | term INTEGERDIVIDE factor
                | factor '''
        if p[1].type == "term":
            # Type checking: reject anything with strings
            if (p[1].v_type in ["string", "list"] or
                    p[3].v_type in ["string", "list"]):
                self._semantic_error(p, err_type="combination_error")

            p[0] = self.combination_rules(p, 'term')
            # For integer division, we can just reset the v_type
            if p[2] == "//":
                p[0].v_type = "integer"
            p[0].lineno = p.lineno(1)
        else:
            p[0] = Node("factor", 'term', [p[1]], p[1].v_type,
                        lineno=p[1].lineno)

    def p_factor(self, p):
        '''factor : PLUS factor
                  | MINUS factor
                  | power'''
        if p[1].type == 'power':
            p[0] = Node("power", "factor", [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
        else:
            p[0] = Node(p[1], 'factor', [p[2]], p[2].v_type,
                        lineno=p.lineno(1))

    def p_power(self, p):
        '''power : power trailer
                 | atom'''
        if p[1].type == 'power':
            p[1].value = "trailer"
            p[1].children.append(p[2])
            p[0] = p[1]
        else:
            p[0] = Node("atom", 'power', [p[1]], p[1].v_type,
                        lineno=p[1].lineno)

    def p_atom_node(self, p):
        '''atom : LPARAN test RPARAN
                | list
                | number
                | boolean'''
        if isinstance(p[1], Node):
            p[0] = Node(p[1].type, "atom", [p[1]], p[1].v_type,
                        lineno=p[1].lineno)
        else:
            p[0] = Node("test", "atom", [p[2]],  p[2].v_type,
                        lineno=p.lineno(1))

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = Node(p[1], 'atom', [], "string", lineno=p.lineno(1))

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = Node(p[1], 'atom', [], "id", lineno=p.lineno(1))

    def p_trailer(self, p):
        '''trailer : calllist
                   | DOT ID'''
        if isinstance(p[1], Node) and p[1].type == "calllist":
            p[0] = Node("calllist", "trailer", [p[1]], lineno=p[1].lineno)
        else:
            p[0] = Node("dot", 'trailer', [p[2]], p.lineno(1))

    def p_list(self, p):
        '''list : LSQUARE RSQUARE
                | LSQUARE testlist RSQUARE'''
        if isinstance(p[2], Node) and p[2].type == 'testlist':
            p[0] = Node(None, "list", [p[2]], "list", p.lineno(1))
        else:
            p[0] = Node(None, "list", [], "list", p.lineno(1))

    def p_number_int(self, p):
        '''number : INTEGER'''
        p[0] = Node(p[1], 'number', [], "integer", lineno=p.lineno(1))

    def p_number_float(self, p):
        '''number : FLOAT'''
        p[0] = Node(p[1], 'number', [], "float", lineno=p.lineno(1))

    def p_boolean(self, p):
        '''boolean : TRUE
                   | FALSE'''
        p[0] = Node(p[1], 'boolean', [], "boolean", lineno=p.lineno(1))

    def p_calllist(self, p):
        '''calllist : LPARAN args RPARAN
                    | LPARAN RPARAN'''
        if isinstance(p[2], Node):
            p[0] = Node("args", "calllist", [p[2]], lineno=p.lineno(1))
        else:
            p[0] = Node(None, 'calllist', [], lineno=p.lineno(1))

    def p_args(self, p):
        '''args : args COMMA expression
                | expression'''
        if p[1].type == 'args':
            p[0] = p[1]
            p[0].value = "args"
            p[0].children.append(p[3])
        else:
            p[0] = Node("expression", 'args', [p[1]], lineno=p[1].lineno)

    def p_itemparams(self, p):
        '''itemparams : LPARAN RPARAN
                      | LPARAN fparams RPARAN'''
        if isinstance(p[2], Node):
            p[0] = Node('fparams', 'itemparams', [p[2]], lineno=p[2].lineno)
        else:
            p[0] = Node(None, 'itemparams', lineno=p.lineno(1))

    def p_fparams(self, p):
        '''fparams : fparams COMMA ID
                   | ID'''
        if isinstance(p[1], Node):
            p[1].value = "fparams"
            p[1].children.append(Node(p[3], "id"))
            p[0] = p[1]
        else:
            p[0] = Node("id", "fparams", [Node(p[1], "id")],
                        lineno=p.lineno(1))

    def p_block_statement(self, p):
        '''block_statement : if_statement
                           | while_statement'''
        if isinstance(p[1], Node):
            if p[1].type == 'if_statement':
                p[0] = Node('if', 'block_statement', [p[1]],
                            lineno=p[1].lineno)
            elif p[1].type == 'while_statement':
                p[0] = Node('while', 'block_statement', [p[1]],
                            lineno=p[1].lineno)

    def p_if_statement(self, p):
        '''if_statement : IF test COLON suite elif_statements ELSE COLON suite
                        | IF test COLON suite ELSE COLON suite
                        | IF test COLON suite elif_statements
                        | IF test COLON suite'''
        if len(p) == 9:
            p[0] = Node(None, 'if_statement', [p[2], p[4], p[5], p[8]],
                        lineno=p[2].lineno)
        elif len(p) == 8:
            p[0] = Node(None, 'if_statement', [p[2], p[4], None, p[7]],
                        lineno=p[2].lineno)
        elif len(p) == 6:
            p[0] = Node(None, 'if_statement', [p[2], p[4], p[5], None],
                        lineno=p[2].lineno)
        else:
            p[0] = Node(None, 'if_statement', [p[2], p[4], None, None],
                        lineno=p[2].lineno)

    def p_elif_statements(self, p):
        '''elif_statements : elif_statements ELIF test COLON suite
                           | ELIF test COLON suite'''
        if isinstance(p[1], Node) and p[1].type == 'elif_statements':
            p[0] = p[1]
            new_elif = Node(None, 'elif_statement', [p[3], p[5]])
            p[0].children.append(new_elif)
        else:
            elif_statement = Node(None, 'elif_statement', [p[2], p[4]],
                                  lineno=p.lineno(1))
            p[0] = Node(None, 'elif_statements', [elif_statement],
                        lineno=elif_statement.lineno)

    def p_while_statement(self, p):
        '''while_statement : WHILE test COLON suite'''
        p[0] = Node(p[2], 'while_statement', [p[2], p[4]], lineno=p[2].lineno)
        p[0].type = 'while_statement'

    # In order to create SymTab entries (in particular, in order to know
    # the appropriate scope) for named entities discovered below a main
    # branch (i.e. variables in a scene), we need to travel back down
    # the branches once we get to the main node. This function does so,
    # creating symtab entries as it goes. It is called recursively on
    # every branch, looking for named entities. It takes as its argument
    # a branch and the scope to be assigned to all found named entities.
    def pass_down(self, branch, scope):
        for i, child in enumerate(branch.children):
            if not isinstance(child, Node):
                continue
            if child.type == "expression_statement":
                if child[0].type == "id":
                    child[0].key = self.symtab.getKey(child[0].value, scope)
                    entry = self.symtab.getWithKey(child[0].key)
                    if not entry:
                        self.symtab.insert(child[0].value, None, None, scope,
                                           False)
                elif child[0].type == "god_id":
                    child[0].key = self.symtab.getKey(child[0].value, scope)
                    entry = self.symtab.getWithKey(child[0].key)
                    if not entry:
                        self.symtab.insert(child[0].value, None, None, scope,
                                           True)
                    else:
                        if entry.god:
                            self._semantic_error("Re-declaring god " +
                                                 "variable in same scope",
                                                 lineno=child.lineno)
                        else:
                            self._semantic_error("Declaring previously " +
                                                 "declared variable as god",
                                                 lineno=child.lineno)
            else:
                self.pass_down(child, scope)

    # Check numbers for interoperability. If they are of
    # differing types, the result is always the more general of
    # the two data types (i.e. float). For now, we allow
    # anything with id's, but later would intend to type check
    # those as well.
    def combination_rules(self, p, n_type):
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
                self._semantic_error(p, "combination_error")
        elif p[1].v_type == "float":
            if p[3].v_type in ["integer", "float"]:
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "float", p.lineno(2))
            else:
                self._semantic_error(p, "combination_error")
        elif p[1].v_type == "list":
            if p[3].v_type == "list":
                p[0] = Node(p[2], n_type, [p[1], p[3]],
                            "list", p.lineno(2))
            else:
                self._semantic_error(p, "combination_error")
        elif p[1].v_type == "boolean":
            self.p_error(p, "combination_error")
        else:
            p[0] = Node(p[2], n_type, [p[1], p[3]], "unknown", p.lineno(2))

        return p[0]

    def p_error(self, p):
        stderr.write("ERROR: Syntax Error at Line " + str(p.lineno) +
                     ": " + "at token '" + str(p.value) + "'\n")
        exit(1)

    def _semantic_error(self, p, err_type=None):
        if err_type == "combination_error":
            stderr.write("ERROR: Type error at line " + str(p.lineno(2)) +
                         ": cannot combine '" + p[1].v_type +
                         "' with '" + p[3].v_type + "'\n")
        elif isinstance(p, LexToken):
            stderr.write("ERROR: Syntax Error at Line " + str(p.lineno) +
                         ": " + "at token '" + str(p.value) + "'\n")
        elif isinstance(p, str):
            stderr.write("ERROR: " + p + "\n")
        exit(1)

    def parse(self, string_to_parse, **kwargs):
        return self.parser.parse(string_to_parse, lexer=self.lexer, **kwargs)
