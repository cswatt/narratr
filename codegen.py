# -----------------------------------------------------------------------------
# narrtr: codegen.py
# This file contains the Code Generator to generate target Python code.
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 01 April 2015
# Primary Authors: Jonah Smith, Yelin Hong, Shloka Kini
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

from sys import stderr, exit
from node import Node


class CodeGen:
    def __init__(self):
        self.frontmatter = "#!/usr/bin/env python\n\nfrom sys import exit"
        self.scenes = []
        self.scene_nums = []
        self.items = []
        self.item_names = []
        self.main = ""

    # This function takes as its arguments the root node of the AST and the
    # symbol table. It saves the symbol table to a class variable (so it is
    # accessible anywhere in the code using self), and looks through the AST
    # to identify the high level nodes (i.e. scenes, items, and startstate),
    # sending the appropriate nodes to the appropriate functions for
    # processing. Note we know the structure of the AST, so we don't need
    # DFS or other tree searching algorithms, which improves efficiency.
    def process(self, node, symtab):
        self.symtab = symtab
        if len(node.children) != 1 or node.children[0].type != "blocks":
            self._process_error("Unexpected Parse Tree - Incorrect number" +
                                "or type of children for the top node",
                                node.lineno)
        blocks = node.children[0].children
        for block in blocks:
            if type(block) is dict:
                for key, s_i in block.iteritems():
                    if s_i.type == "scene_block":
                        self._add_scene(self._scene_gen(s_i, key))
                    elif s_i.type == "item_block":
                        self._add_item(self._item_gen(s_i, key))
            elif block.type == "start_state":
                self._add_main(block)
            else:
                self._process_error("Found unexpected block types.",
                                    block.lineno)

    # This function takes the instance variables constructed by the process()
    # function and writes them to an output file. (As such, it must be run
    # AFTER process()! It is intended to be called externally, within the
    # main compiler. It takes one argument, outputfile, which is a string of
    # the location where the file should be written. By convention, that file
    # should be in the form of *.ntrc. If no outputfile is specified
    # or the outputfile is specified as "stdout", the code prints to standard
    # out (e.g. usually the terminal window). That's mainly for debugging
    # purposes, and should not be used in the production compiler, as the
    # line breaks are only approximations.
    def construct(self, outputfile="stdout"):
        if self.main == "":
            raise Exception("No start scene specified")

        if outputfile == "stdout":
            print self.frontmatter
            print "\n".join(self.scenes)
            print "\n".join(self.items)
            print self.main
        else:
            with open(outputfile, 'w') as f:
                f.write(self.frontmatter)
                f.write("\n")
                f.write("\n".join(self.scenes))
                f.write("\n\n")
                f.write("\n".join(self.items))
                f.write("\n\n")
                f.write(self.main)

    # This function is used internally to add a scene to the scene list. It
    # takes a string *with correct indentation*.
    def _add_scene(self, scene):
        self.scenes.append(scene)

    # This function is used internally to add a item to the item list. It
    # takes a string *with correct indentation*.
    def _add_item(self, item):
        self.items.append(item)

    # This function generates the code for a start state given a start state
    # node. If start state code has already been generated, it produces a
    # warning and keeps the start state declared higher in the program. If
    # called without a node, it triggers the default action, which is a start
    # state of 1. This should only be used internally.
    # ABOUT THE RESPONSE CODE: the default response code, which is dropped
    # into a function called get_response(), waits for user input. When it
    # it receives this input, it strips the case (i.e. everything is made
    # lower case), removes all punctuation except double quotes (to allow
    # the programmer to add conversational capabilities), converts all
    # whitespace characters into a single space, and then checks for specific
    # situations we agree with the programmer to handle by default. 'exit'
    # will terminate the game (there is no current way to save game state),
    # and "move" followed by a single token will check the dictionary of
    # directions (which it takes as an argument) for an applicable direction.
    # If it does not appear in the dictionary, an error is reported so the user
    # is not confused.  If it does appear, it encodes the next scene's function
    # call within a list so that it can easily be identified by the caller
    # function, which will return that piece of code. This is a centerpiece of
    # our approach to avoiding an overflow of activation records in large
    # games.
    def _add_main(self, startstate):
        if self.main == "":
            self.main = "pocket = {}\n"
            self.main += '''def get_response(direction):
    response = raw_input(" -->> ")
    response = response.lower()
    response = response.translate(None,
                "!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~")
    response = ' '.join(response.split())
    if response == "exit":
        print "== GAME TERMINATED =="
        exit(0)
    elif response[:5] == "move " and len(response.split(" ")) == 2:
        if response.split(" ")[1] in direction:
            return ["s_" + str(direction[response.split(" ")[1]])\\
                + "_inst.setup()"]
        else:
            print "\\"" + response.split(" ")[1] + "\\" is not a "\\
                + "valid direction from this scene."
    else:
        return response\n\n'''

            # Create an instance of each scene that has been declared.
            for s in self.scene_nums:
                self.main += "s_" + str(s) + "_inst = s_" + str(s) + "()\n"

            if startstate.value in self.scene_nums:
                self.startstate = startstate.value
            else:
                raise Exception("Start scene $" + str(startstate.value) +
                                " does not exist")

            self.main += "if __name__ == '__main__':\n    next = s_"\
                + str(self.startstate) + "_inst.setup()\n    while True:\n"\
                + "        exec 'next = ' + next"
        else:
            raise Exception("Multiple start scene declarations.")

    # This function takes a scene node and processes it, translating into
    # valid Python (really, a Python class). Iterates through the children
    # of the input node and constructs the setup, cleanup, and action blocks
    # using boilerplate code. This should only be used internally. In the
    # action_block part, adding while(true) loop to get response and then
    # process it. def achition is now taking direction as argument, direction
    # is an empty dictionary by default.
    def _scene_gen(self, scene, sid):
        commands = []
        direction_sign = False
        for c in scene.children:
            if c.type == "SCENEID":
                sid = c.value

            elif c.type == "setup_block":
                commands += self._process_setup_block(c)

            elif c.type == "cleanup_block":
                commands += self._process_cleanup_block(c)

            elif c.type == "action_block":
                commands += self._process_action_block(c)

        self.scene_nums.append(sid)
        scene_code = "class s_" + str(sid) + ":\n    def __init__(self):"\
            + "\n        self.__namespace = {}\n\n    "\
            + "\n    ".join(commands)

        return scene_code

    def _item_gen(self, item, iid):
        commands = []
        iid = item.value
        self.item_names.append(iid)
        item_code = "class item_" + str(iid) + ":\n    "
        # "\n    ".join(commands)
        for c in item.children:
            if c.type == "calllist":
                item_code = item_code + "def __init__(self"
                for exp in c.children:
                    item_code += "," + exp.children[0].value
                item_code += "):\n"
            elif c.type == "suite":
                commands += self._process_item_block(item)
        item_code = item_code + "    ".join(commands)
        # + "\n        pass\n\n    "

        # Here modify code so that constructor takes args
        # in python:
# class key:
#     def __init__(self, identifier)
#         self.id = identifier
        return item_code

    def _process_item_block(self, c):
        commands = []
        if len(c.children) > 0:
            commands.append(self._process_suite(c, 2))
        return commands

# in narratr: k is key(1) (is the constructor call)
# ...
# item key(identifier){
# if identifier > 1:
#     id = identifier
# else:
#     id = identifier + 5
# }

# in python:
# class key:
#     def __init__(self, identifier):
#         if identifier > 1:
#             self.id = identifier
#         else:
#             self.id = identifier + 5

    # Code for adding a setup block. Takes as input a single "setup block"
    # node. Adds boilerplate code (function definition, empty dictionary for
    # direction, and at the end, the code to move to the action block), and
    # sends the child nodes to _process_suite() to generate their code.
    def _process_setup_block(self, c):
        commands = []
        commands.append("def setup(self):" +
                        "\n        direction = {}")

        if len(c.children) > 0:
            for child in c.children:
                commands.append(self._process_suite(child, 2))
        commands.append("    return self.action(direction)\n")
        return commands

    # Code for adding a cleanup block. Takes as input a single "cleanup block"
    # node. Adds boilerplate code (function definition and "pass" if necessary,
    # explained below), then sends the child nodes to _process_suite() to
    # generate their code. "pass" is required in the scenario that there are no
    # child nodes, in which case Python syntactically requires code, we need to
    # be able to execute the function, but we don't want anything to happen. #
    # "pass" is a Python command that does nothing, so it fits the bill.
    def _process_cleanup_block(self, c):
        commands = []
        commands.append("def cleanup(self):")
        if len(c.children) > 0:
            commands.append(self._process_suite(c.children[0], 3))
        else:
            commands.append("    pass")
        return commands

    # Code for adding an action block. Takes as input a single "action block"
    # node. Adds boilerplate code (function definition, initialize "response"
    # as an empty string so it does not trip up the REPL loop, and add a "while
    # True:" loop to get the REPL loop). The action block itself takes the
    # direction dictionary for that scene as a parameter so it can pass it to
    # the get_response() function. It also passes the name of the class so
    # get_response() knows which scene's cleanup block to call if the user is
    # trying to move between scenes.
    def _process_action_block(self, c):
        commands = []
        commands.append("def action(self, direction):")
        commands.append("    response = \"\"\n        while True:")
        if len(c.children) > 0:
            for child in c.children:
                commands.append(self._process_suite(child, 3)[5:])
        commands.append("        response = get_response(" +
                        "direction)\n            " +
                        "if isinstance(response, list):" +
                        "\n                self.cleanup()\n" +
                        "                return response[0]\n")
        return commands

    def _process_suite(self, statement, indentlevel=1):
        commands = ""
        for smt in statement.children:
            commands += self._process_statement(smt, indentlevel)
        return commands

    # Statement is actually a suite node, but we're keeping the name for
    # backwards-compatability.
    def _process_statement(self, smt, indentlevel=1):
        commands = ''
        prefix = "\n" + "    "*indentlevel
        if smt.value == "say":
            commands += prefix + "print "
            for testlist in smt.children:
                t = "String"
                tl = testlist
                commands += self._process_testlist(tl)
        elif smt.value == "exposition":
            commands += prefix + "print "
            for testlist in smt.children:
                commands += self._process_testlist(testlist)
        elif smt.value in ["win", "lose"]:
            if len(smt.children) > 0:
                for testlist in smt.children:
                    commands += prefix + "print "
                    commands += self._process_testlist(testlist)
            elif smt.value in ["win", "lose"]:
                if len(smt.children) > 0:
                    for testlist in smt.children:
                        commands += prefix + "print "
                        commands += self._process_testlist(
                            testlist,
                            indentlevel=indentlevel + 1, blocktype=blocktype)
                commands += prefix + "exit(0)"
        elif smt.value == "is":
            if len(smt.children) > 0:
                if smt.children[0].type == "god_id":
                    self.main = self._process_god_assign(
                        smt.children,
                        indentlevel=indentlevel + 1) + self.main
        elif smt.value == "expression":
            if len(smt.children) > 0:
                if smt.children[0].type == "id":
                    commands += prefix
                    commands += self._process_assign(
                        smt.children,
                        indentlevel=indentlevel + 1, blocktype=blocktype)
                elif smt.children[0].type == "test":
                    commands += prefix
                    commands += self._process_testlist(
                                        smt,
                                        blocktype=blocktype)

        elif smt.value == "flow":
            commands += prefix
            if len(smt.children) > 0:
                if smt.children[0].type in ["break_statement",
                                            "continue_statement"]:
                    commands += smt.children[0].value
                # direction list
                else:
                    i = 0
                    for child in smt.children:
                        if child.type == "direction":
                            if i == 0:
                                commands += 'direction = {"'
                            else:
                                commands += '"'
                            commands += self._process_direction(
                                child,
                                indentlevel=indentlevel + 1)
                            if (len(smt.children) - 1) != i:
                                commands += ', '
                            else:
                                commands += "}"
                        i += 1

        elif smt.value in ["if", "while"] or smt.type == "elif_statements":
            if smt.value is not None:
                commands += prefix + smt.value + " "
            else:
                commands += prefix + "elif "
            commands += self._process_test(smt.children[0], 0) + ":\n    "
            for c in smt.children[1:]:
                if c.value == "else":
                    commands += prefix + "else:\n    "
                    commands += self._process_statements(
                                        c,
                                        indentlevel=indentlevel+1,
                                        blocktype=blocktype)
                elif c.type == "elif_statements":
                    commands += "\n    "\
                             + self._process_statements(
                                        Node(None, "suite", [c]),
                                        indentlevel=indentlevel,
                                        blocktype=blocktype)
                else:
                    commands += self._process_statements(
                                        c,
                                        indentlevel=indentlevel+1,
                                        blocktype=blocktype)

        elif smt.value is None:
            commands += self._process_testlist(smt)

        return commands

    # This function takes "testlist" node as argument
    def _process_testlist(self, testlist):
        if not isinstance(testlist, Node):
            self._process_error("Something bad happened while processing " +
                                "'testlist'. Unfortunately, that is all we " +
                                "know.")
        if len(testlist.children) == 0:
            self._process_error("Testlist has no children to process.",
                                testlist.lineno)
        tests = testlist.children
        testcode = []
        for test in tests:
            testcode.append(self._process_test(test))
        return ",".join(testcode)

    def _process_test(self, test):
        if not isinstance(test, Node) or test.type != "test":
            self._process_error("Something bad happened while processing " +
                                "'test'. Unfortunately, that is all we know.")
        if len(test.children) != 1:
            self._process_error("'test' has incorrect number of children.",
                                test.lineno)
        return self._process_or_test(test.children[0])

    def _process_or_test(self, or_test):
        if not isinstance(or_test, Node) or or_test.type != "or_test":
            self._process_error("Something bad happened while processing " +
                                "'or_test'. Unfortunately, that is all we " +
                                "know.")
        if len(or_test.children) not in [1, 2]:
            self._process_error("'or_test' has incorrect number of children.",
                                or_test.lineno)
        if or_test.value == 'or':
            return '(' + self._process_or_test(or_test.children[0]) + ') or ' \
                    + self._process_and_test(or_test.children[1])
        else:
            return self._process_and_test(or_test.children[0])

    def _process_and_test(self, and_test):
        if not isinstance(and_test, Node) or and_test.type != "and_test":
            self._process_error("Something bad happened while processing " +
                                "'and_test'. Unfortunately, that is all we " +
                                "know.")
        if len(and_test.children) not in [1, 2]:
            self._process_error("'and_test' has incorrect number of children.",
                                and_test.lineno)
        if and_test.value == 'and':
            return '(' + self._process_and_test(and_test.children[0]) + \
                    ') and ' + self._process_not_test(and_test.children[1])
        else:
            return self._process_not_test(and_test.children[0])

    def _process_not_test(self, not_test):
        if not isinstance(not_test, Node) or not_test.type != "not_test":
            self._process_error("Something bad happened while processing " +
                                "'not_test'. Unfortunately, that is all we " +
                                "know.")
        if len(not_test.children) != 1:
            self._process_error("'not_test' has incorrect number of children.",
                                not_test.lineno)
        if not_test.value == 'not':
            return 'not ' + self._process_not_test(not_test.children[0])
        else:
            return self._process_comparison(not_test.children[0])

    def _process_comparison(self, comparison):
        if not isinstance(comparison, Node) or comparison.type != "comparison":
            self._process_error("Something bad happened while processing " +
                                "'comparison'. Unfortunately, that is all we" +
                                " know.")
        if len(comparison.children) not in [1, 3]:
            self._process_error("'comparison' has incorrect number of " +
                                "children.", comparison.lineno)
        if comparison.value == 'comparison':
            return '(' + self._process_comparison(comparison.children[0]) + \
                   ') ' + self._process_comparisonop(comparison.children[1]) \
                   + " " + self._process_expression(comparison.children[2])
        else:
            return self._process_expression(comparison.children[0])

    def _process_comparisonop(self, comparisonop):
        return comparisonop.value

    # This function takes statement node with "while" value.
    def _process_whilestatement(self, smt, indentlevel=1):
        commands = "while "
        commands += self._process_test(smt.children[0], 0) + ":\n    "
        for c in smt.children[1:]:
            commands += self._process_suite(c, indentlevel+1)
        return commands

    # This function takes statement node with "if" value, or an elif node.
    # Note, because of the embedding structure, we need to process it this
    # way, and the constructions are identical, except "if" vs "elif" token.
    def _process_ifstatement(self, smt, indentlevel=1):
        if smt.value is not None:
            commands = "if "
        else:
            commands = "elif "
        commands += self._process_test(smt.children[0], 0) + ":\n    "
        for c in smt.children[1:]:
            if c.value == "else":
                commands += "\n" + "    "*indentlevel + "else:\n    "
                commands += self._process_suite(c, indentlevel+1)
            elif c.type == "elif_statements":
                commands += "\n    "\
                         + self._process_suite(Node(None, "suite", [c]),
                                               indentlevel)
            else:
                commands += self._process_suite(c, indentlevel+1)
        return commands

    def _process_assign(self, ass, indentlevel=1, blocktype='scene'):
        commands = ''
        if ass[0].value == "list":
            commands += "nlist" + " = "
            commands += self._process_testlist(ass[1])
        else:
            commands += "self.__namespace['" + ass[0].value + "'] = "
            commands += self._process_testlist(ass[1])
        return commands

    def _process_god_assign(self, ass, indentlevel=1, blocktype='scene'):
        commands = ''
        commands += ass[0].value + " = "
        commands += self._process_testlist(ass[1])
        return commands

    # This function takes "expression" node as argument
    def _process_expression(self, exps):
        commands = ''
        if exps.value in ["*", "/", "//", "+", "-"]:
            tempv = exps.value
            i = indentlevel + 1
            temp = self._process_arithmetic(exps, str(tempv))
            commands += temp
            if len(exps.children) > 1:
                if exps.children[0].v_type == 'id':
                    if blocktype == 'scene':
                        term1 = "self.__namespace['"
                        term1 += str(exps.children[0].value) + "']"
                    elif blocktype == 'item':
                        term1 += str(exps.children[0].value)
        else:
            for child in exps.children:
                if child.type == "factor":
                    commands += self._process_factor(child)
                elif child.type == "arithmetic_expression":
                    # there should be a _process_arithmetic_expression()
                    # function that is called here.
                    if child.v_type in ["integer", "float"]:
                        commands += str(child.children[0].value) + ' '
                    elif child.v_type == "id":
                        if blocktype == 'scene':
                            commands += "self.__namespace['"\
                                    + child.children[0].value + "'] "
                        elif blocktype == 'item':
                            commands += child.children[0].value
                    else:
                        commands += child.children[0].value + ' '
                    commands += exps.value + ' '
                elif child.type == "term":
                    if child.v_type == "integer":
                        commands += str(child.children[0].value) + ' '
                    elif child.v_type == "id":
                        if blocktype == 'scene':
                            commands += "self.__namespace['"\
                                    + child.children[0].value + "'] "
                elif child.type == "expression":
                    commands += self._process_expression(child, indentlevel)
        return commands

    # This function takes "factor" node as argument
    def _process_factor(self, factors):
        commands = ""
        # When is this triggered, if ever? Is there a better way to write
        # it?
        if len(factors.children) > 0:
            if len(factors.children) == 3:
                for factor in factors.children[0].children:
                    commands += str(factor.value) + ' '
                if factors.children[1].type == "comparison_op":
                    commands += factors.children[1].value
                for factor in factors.children[2].children:
                    commands += ' ' + str(factor.value)

            elif factors.children[0].v_type == "boolean":
                if factors.children[0].children[0].value == "true":
                    commands += "True"
                elif factors.children[0].children[0].value == "false":
                    commands += "False"

        if factors.v_type in ["integer", "float"]:
            commands += str(factors.value)

        elif factors.v_type == "string":
            commands += '"' + factors.value + '"'

        elif factors.v_type == "list":
            commands += "["
            count = 0
            for lchild in factors.children:
                tl = lchild.children[0]
                commands += self._process_expression(tl)
                count += 1
                if count != len(child.children):
                    commands += ', '
            commands += "]"

        elif factors.value == "list":
            commands += "nlist"
            if len(factors.children) > 0:
                for fchild in child.children:
                    if fchild.type == "trailer":
                        if len(fchild.children) > 0:
                            fcount = 0
                            for ffchild in fchild.children:
                                if ffchild.type == "dot":
                                    commands += ffchild.value
                                elif ffchild.type == "id":
                                    if ffchild.value == "add":
                                        commands += "append("
                                elif ffchild.type == "expression":
                                    t = ffchild
                                    temp = self._process_expression(t)
                                    commands += temp
                                    fcount += 1
                                    if fcount != len(fchild.children):
                                        commands += ', '
                                    else:
                                        commands += ')'

        elif factors.v_type == "id":
            if factors.value == "pocket":
                commands += self._process_pocket(factors)
            elif(self.symtab.get(factors.value, 'GLOBAL')):
                if len(factors.children[0].children) > 0:
                    commands += "("
                    for c in factors.children[0].children:
                        commands += self._process_expression(c) + ","
                        commands = commands[:-1] + ")"
            else:
                if blocktype == 'scene':
                    commands += "self.__namespace['" + factors.value + "']"
                elif blocktype == 'item':
                    commands += factors.value
        elif factors.value is None:
            commands += self._process_factor(factors)
        elif factors.v_type == "string":
            if factors.value == "str":
                commands += "str("
                commands += self._process_expression(
                            factors.children[0].children[0])
                commands += ")"
            else:
                commands += '"' + factors.value + '"'
        elif factors.v_type == "integer":
            commands += str(factors.value)
        return commands

    # This function recursively deals with arithmetic node
    def _process_arithmetic(self, expr, expvalue):
        commands = ''
        if len(expr.children) > 0:
            for child in expr.children:
                if child.type == "arithmetic_expression":
                    if child.value not in ['+', '-', '*', '/']:
                        if len(child.children) > 0:
                            if child.children[0].type == "factor":
                                tempc = child.children[0]
                                temp = self._process_factor(tempc)
                                if datatype == "String":
                                    if tempc.v_type == 'string':
                                        commands += temp
                                    else:
                                        commands += 'str(' + temp + ')'
                                else:
                                    commands += temp
                                commands += ' ' + expvalue + ' '
                    else:
                        if child.v_type == "integer":
                            tv = child.value
                            c = child
                            temp = self._process_arithmetic(c, tv)
                            commands += temp + ' '
                            if datatype == "String":
                                commands += 'str(' + str(tv) + ')' + ' '
                            else:
                                commands += str(tv) + ' '
                        elif child.v_type == 'id':
                            tv = child.value
                            c = child
                            temp = self._process_arithmetic(c, tv)
                            commands += temp + ' '
                            commands += str(tv) + ' '
                elif child.type == "term":
                    if child.value is None:
                        if len(child.children) > 0:
                            if child.children[0].type == "factor":
                                tc = child.children[0]
                                if (datatype == "String" and
                                        tc.v_type != 'string'):
                                    commands += 'str('
                                commands += self._process_factor(tc)
                                if (datatype == "String" and
                                        tc.v_type != 'string'):
                                    commands += ')'
                    elif child.value in ['*', '/']:
                        tv = str(child.value)
                        temp = self._process_arithmetic(child, tv)
                        commands += temp
                elif child.type == "factor":
                    if child.v_type == 'id':
                        commands += ' ' + expvalue + ' '
                        if blocktype == 'scene':
                            commands += "self.__namespace['"
                            commands += str(child.value) + "']"
                        elif blocktype == 'item':
                            commands += str(child.value)
                    if child.v_type == 'integer':
                        if datatype == "String":
                            commands += ' str(' + expvalue + ') '
                        else:
                            commands += ' ' + expvalue + ' '
                        commands += str(child.value)
        return commands

    # This function takes "direction" node as argument
    # Building a dictionary for direction, using the direction as key and
    # scene number as value
    def _process_direction(self, direction):
        commands = ''
        commands += direction.value
        commands += '": '
        for scene in direction.children:
            commands += str(scene.value)
        return commands

    def _process_pocket(self, pocket_node, indentlevel=1):
        commands = ""
        add = get = remove = False
        if len(pocket_node.children) != 2:
            self._process_error("Pocket has the wrong structure.",
                                pocket_node.lineno)

        if pocket_node.children[0].children[1].value == "add":
            if len(pocket_node.children[1].children) != 2:
                l = len(pocket_node.children[1].children)
                self._process_error("Adding to the pocket requires" +
                                    " exactly two arguments. " +
                                    str(l) + " given.", pocket_node.lineno)
            else:
                commands += "pocket['"
                commands += self._process_expression(
                                    pocket_node.children[1].children[0])
                commands += "] = "
                commands += self._process_expression(
                                    pocket_node.children[1].children[1])

        elif pocket_node.children[0].children[1].value == "get":
            if len(pocket_node.children[1].children) != 1:
                l = len(pocket_node.children[1].children)
                self._process_error("Adding to the pocket requires" +
                                    " exactly one argument. " +
                                    str(l) + " given.", pocket_node.lineno)
            else:
                commands += "pocket['"
                commands += self._process_expression(
                                    pocket_node.children[1].children[0])
                commands += "]"

        elif pocket_node.children[0].children[1].value == "remove":
            if len(pocket_node.children[1].children) != 1:
                l = len(pocket_node.children[1].children)
                self._process_error("Removing from pocket requires" +
                                    " exactly one argument. " +
                                    str(l) + " given.", pocket_node.lineno)
            else:
                commands += "del pocket['"
                commands += self._process_expression(
                                    pocket_node.children[1].children[0])
                commands += "]"
        else:
            self._process_error("Cannot '" +
                                str(pocket_node.children[0].children[1]) +
                                "' the pocket.", child.children[1].lineno)
        return commands

    def _process_error(self, error, lineno=0):
        if lineno != 0:
            stderr.write("ERROR: Line " + str(lineno) + ": " + str(error) +
                         "\n")
        else:
            stderr.write("ERROR: " + str(error) + "\n")
        exit(1)

    def _process_warning(self, warning, lineno=0):
        if lineno != 0:
            stderr.write("WARNING: Line " + str(lineno) + ": " + str(warning) +
                         "\n")
        else:
            stderr.write("WARNING: " + str(warning) + "\n")
