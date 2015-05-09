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
        self.frontmatter = "#!/usr/bin/env python\n" + \
                            "from __future__ import division\n" + \
                            "from sys import exit\n\n"
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
            self._process_warning("No start scene specified. " +
                                  "Defaulting to $1.")
            self._add_main(1)

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
            self.main = '''class pocket_class:
    def __init__(self):
        self.data = {}

    def add(self, key, val):
        self.data[key] = val

    def get(self, key):
        return self.data.get(key)

    def remove(self, key):
        del self.data[key]

pocket = pocket_class()\n'''
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

            if isinstance(startstate, Node):
                ss = startstate.value
            else:
                ss = startstate

            if ss in self.scene_nums:
                self.startstate = ss
            else:
                self._process_error("Start scene $" + str(startstate.value) +
                                    " does not exist.")

            self.main += "if __name__ == '__main__':\n    next = s_"\
                + str(self.startstate) + "_inst.setup()\n    while True:\n"\
                + "        exec 'next = ' + next"
        else:
            self._process_warning("Multiple start scene declarations. " +
                                  "Using scene $" + self.startstate + ".")

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
        for c in item.children:
            if c.type == "calllist":
                item_code = item_code + "def __init__(self"
                for exp in c.children:
                    item_code += "," + exp.children[0].value
                item_code += "):\n"
            elif c.type == "suite":
                commands += self._process_item_block(item)
        item_code = item_code + "    ".join(commands)
        return item_code

    def _process_item_block(self, c):
        commands = []
        if len(c.children) > 0:
            commands.append(self._process_suite(c, 2))
        return commands

    # Code for adding a setup block. Takes as input a single "setup block"
    # node. Adds boilerplate code (function definition, empty dictionary for
    # direction, and at the end, the code to move to the action block), and
    # sends the child nodes to _process_suite() to generate their code.
    def _process_setup_block(self, c):
        commands = []
        commands.append("def setup(self):" +
                        "\n        direction = {}")
        if len(c.children) not in [0, 1]:
            self._process_error("setup block has wrong number of children")
        if len(c.children) == 1:
            if c.children[0].type != "suite":
                self._process_error("setup block doesn't have suite child")
            else:
                commands.append(self._process_suite(c.children[0], 2))
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
        if len(c.children) not in [0, 1]:
            self._process_error("cleanup block has wrong number of children")
        if len(c.children) == 1:
            if c.children[0].type != "suite":
                self._process_error("cleanup block doesn't have suite child")
            else:
                commands.append(self._process_suite(c.children[0], 2))
        commands.append("    self.__namespace = {}")
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
        if len(c.children) not in [0, 1]:
            self._process_error("action block has wrong number of children")
        if len(c.children) == 1:
            if c.children[0].type != "suite":
                self._process_error("action block doesn't have suite child")
            else:
                commands.append(self._process_suite(c.children[0], 3)[5:])
        commands.append("        response = get_response(" +
                        "direction)\n            " +
                        "if isinstance(response, list):" +
                        "\n                self.cleanup()\n" +
                        "                return response[0]\n")
        return commands

    def _process_suite(self, suite, indentlevel=1):
        commands = ""
        if len(suite.children) != 1:
            self._process_error("Too many children in suite.")
        else:
            if suite.value == "simple":
                commands += self._process_simple_smt(suite.children[0],
                                                     indentlevel)
            else:
                commands += self._process_statements(suite.children[0],
                                                     indentlevel)
        return commands

    def _process_statements(self, statements, indentlevel=1):
        commands = ''
        for smt in statements.children:
            commands += self._process_statement(smt, indentlevel)
        return commands

    def _process_statement(self, statement, indentlevel=1):
        commands = ''
        if statement.value == "simple":
            commands += self._process_simple_smt(statement.children[0],
                                                 indentlevel)
        elif statement.value == "block":
            commands += self._process_block_smt(statement.children[0],
                                                indentlevel)
        else:
            self._process_error("Not accepted ")
        return commands

    # Statement is actually a suite node, but we're keeping the name for
    # backwards-compatability.
    def _process_simple_smt(self, smt, indentlevel=1):
        commands = ''
        prefix = "\n" + "    "*indentlevel
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'simple statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) == 0:
            self._process_error("Simple statement has no children to process.",
                                smt.lineno)
        if smt.value == "say":
            commands += prefix + self._process_say_smt(smt.children[0])
        elif smt.value == "exposition":
            commands += prefix + self._process_expo_smt(smt.children[0])
        elif smt.value == "win":
            commands += self._process_win_smt(smt.children[0], indentlevel)
        elif smt.value == "lose":
            commands += self._process_lose_smt(smt.children[0], indentlevel)
        elif smt.value == "expression":
            commands += self._process_expression_smt(smt.children[0],
                                                     indentlevel)
        elif smt.value == "flow":
            commands += self._process_flow_smt(smt.children[0], indentlevel)
        return commands

    def _process_block_smt(self, smt, indentlevel):
        commands = ''
        prefix = "\n" + "    "*indentlevel
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'block statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) != 1:
            self._process_error("Block statement has no children to process.",
                                smt.lineno)
        if smt.children[0].type == "if_statement":
            commands += prefix + \
                        self._process_ifstatement(smt.children[0], indentlevel)
        elif smt.children[0].type == "while_statement":
            commands += prefix + \
                        self._process_whilestatement(smt.children[0],
                                                     indentlevel)
        else:
            self._process_error("Block statement does not have valid child " +
                                "node.")
        return commands

    # Say statement function is called from simple statement and
    # passes node to _process_testlist()
    def _process_say_smt(self, smt):
        commands = 'print '
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'say statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) == 0:
            self._process_error("Say statement has no children to process.",
                                smt.lineno)
        commands += self._process_testlist(smt.children[0])
        return commands

    # Exposition statement passes node to _process_testlist
    def _process_expo_smt(self, smt):
        commands = 'print '
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'exposition statement'. Unfortunately, " +
                                "that is all we know.")
        if len(smt.children) == 0:
            self._process_error("Exposition statement has no children to" +
                                " process.", smt.lineno)
        commands += self._process_testlist(smt.children[0])
        return commands

    # Win tatement, print the smt if there is and exit the scene
    def _process_win_smt(self, smt, indentlevel):
        prefix = "\n" + "    "*indentlevel
        commands = ""
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'win statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) != 0:
            commands += prefix + "print "\
                        + self._process_testlist(smt.children[0])
        commands += prefix + "exit(0)"
        return commands

    # Lose tatement, print the smt if there is and exit the scene
    def _process_lose_smt(self, smt, indentlevel):
        prefix = "\n" + "    "*indentlevel
        commands = ""
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'lose statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) != 0:
            commands += prefix + "print "\
                        + self._process_testlist(smt.children[0])
        commands += prefix + "exit(0)"
        return commands

    # Expression statement
    def _process_expression_smt(self, smt, indentlevel):
        prefix = '\n' + '    '*indentlevel
        commands = ''
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'lose statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) == 0:
            self._process_error("Lose statement has no children to process.",
                                smt.lineno)
        elif smt.value == "testlist":
            commands += prefix + self._process_testlist(smt.children[0])
        elif smt.value == "is":
            entry = self.symtab.getWithKey(smt.children[0].v_type)
            if entry and entry.god:
                commands += prefix + "self." + smt.children[0].value
            else:
                commands += prefix + "self.__namespace['" + \
                            smt.children[0].value + "'] = "
            commands += self._process_testlist(smt.children[1])
        elif smt.value == "godis":
            commands += prefix + "try:"
            commands += prefix + "    " + smt.children[0].value
            commands += prefix + "except NameError:"
            commands += prefix + "    self." + smt.children[0].value + " = "
            commands += prefix + self._process_testlist(smt.children[1])
        return commands

    def _process_flow_smt(self, smt, indentlevel):
        prefix = "\n" + "    "*indentlevel
        commands = ""
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'flow statement'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) != 1:
            self._process_error("Flow statement has incorrect number of " +
                                "children to process.", smt.lineno)

        if smt.children[0].type == "continue_statement":
            commands += prefix + self._process_continue(smt.children[0])
        elif smt.children[0].type == "break_statement":
            commands += prefix + self._process_break(smt.children[0])
        elif smt.children[0].type == "moves_declaration":
            commands += prefix + self._process_moves_dec(smt.children[0])
        elif smt.children[0].type == "moveto_statement":
            commands += self._process_moveto(smt.children[0], indentlevel)
        else:
            self._process_error("flow statement has wrong type of child")
        return commands

    def _process_continue(self, smt):
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'continue statement'. Unfortunately, that " +
                                "is all we know.")
        return "continue"

    def _process_break(self, smt):
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'break statement'. Unfortunately, that is " +
                                "all we know.")
        return "break"

    def _process_moves_dec(self, smt):
        commands = "direction = {"
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'moves declaration'. Unfortunately, that " +
                                "is all we know.")
        if len(smt.children) != 1:
            self._process_error("moves declaration has wrong number of " +
                                "children")
        elif smt.children[0].type != "directionlist":
            self._process_error("moves declaration has wrong type of children")
        else:
            commands += self._process_directionlist(smt.children[0]) + "}"
        return commands

    def _process_directionlist(self, smt):
        commands = ""
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'directionlist'. Unfortunately, that is " +
                                "all we know.")
        if len(smt.children) < 1:
            self._process_error("directionlist has no children")
        l = len(smt.children) - 1
        for i, d in enumerate(smt.children):
            commands += "'" + str(self._process_direction(d)) + "': "
            if len(d.children) != 1:
                self._process_error("incorrect children of direction")
            else:
                commands += str(d.children[0].value)
                if l != i:
                    commands += ", "
        return commands

    def _process_moveto(self, smt, indentlevel):
        commands = ""
        prefix = "\n" + "    "*indentlevel
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'moveto statement'. Unfortunately, that is " +
                                "all we know.")
        commands += prefix + "self.cleanup()"
        if len(smt.children) != 1:
            self._process_error("moveto has the wrong number of children")
        elif smt.children[0].type != "sceneid":
            self._process_error("moveto has wrong kind of child")
        else:
            commands += prefix + "return 's_" + str(smt.children[0].value)
            commands += "_inst.setup()'"
        return commands

    def _process_direction(self, smt):
        if not isinstance(smt, Node):
            self._process_error("Something bad happened while processing " +
                                "'direction statement'. Unfortunately, that " +
                                "is all we know.")
        return smt.value

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
        if smt.children[0].type != "test":
            self._process_error("No test in while loop", smt.lineno)
        else:
            commands += self._process_test(smt.children[0]) + ":"
        if smt.children[1].type != "suite":
            self._process_error("No suite in while loop", smt.lineno)
        else:
            commands += self._process_suite(smt.children[1], indentlevel+1)
        return commands

    # This function takes statement node with "if" value, or an elif node.
    # Note, because of the embedding structure, we need to process it this
    # way, and the constructions are identical, except "if" vs "elif" token.
    def _process_ifstatement(self, smt, indentlevel):
        prefix = "\n" + "    "*indentlevel
        commands = prefix + "if "
        commands += self._process_test(smt.children[0]) + ":"
        commands += self._process_suite(smt.children[1], indentlevel+1)
        if smt.children[2]:
            commands += self._process_elifstatements(smt.children[2],
                                                     indentlevel)
        if smt.children[3]:
            commands += prefix + "else:"
            commands += self._process_suite(smt.children[3], indentlevel+1)
        return commands

    def _process_elifstatements(self, elif_smts, indentlevel):
        commands = ""
        for child in elif_smts:
            if child.type != "elif_statement":
                self._process_error("Invalid child of elif_statements",
                                    elif_smts.lineno)
            else:
                commands += self._process_elifstatement(child, indentlevel)
        return commands

    def _process_elifstatement(self, smt, indentlevel):
        prefix = "\n" + "    "*indentlevel
        commands = prefix + "elif "
        if smt.children[0].type != "test":
            self._process_error("Invalid elif tree", smt.lineno)
        else:
            commands += self._process_test(smt.children[0]) + ":"
        if smt.children[1].type != "suite":
            self._process_error("Invalid elif tree", smt.lineno)
        else:
            commands += self._process_suite(smt.children[1], indentlevel+1)
        return commands

    # This function takes "expression" node as argument
    def _process_expression(self, expression):
        return self._process_arithmetic_expression(expression.children[0])

    # This function processes atom nodes.
    def _process_atom(self, atom):
        if not isinstance(atom, Node) or atom.type != "atom":
            self._process_error("Something bad happened while processing " +
                                "'atom'. Unfortunately, that is all we " +
                                "know.")
        if atom.is_leaf():
            if atom.v_type == "string":
                return repr(str(atom.value))
            else:
                if not atom.v_type:
                    self._process_error("Name Error: " + str(atom.value) +
                                        " is not defined.", atom.lineno)
                else:
                    entry = self.symtab.getWithKey(atom.v_type)
                    if entry and entry.god:
                        return "self." + atom.value
                    else:
                        return "self.__namespace['" + atom.value + "']"
        if len(atom.children) != 1:
            self._process_error("'atom' has incorrect number of " +
                                "children.", atom.lineno)
        if atom.value == "test":
            return "(" + self._process_test(atom.children[0]) + ")"
        elif atom.value == "list":
            return self._process_list(atom.children[0])
        elif atom.value == "number":
            return self._process_number(atom.children[0])
        elif atom.value == "boolean":
            return self._process_boolean(atom.children[0])
        else:
            self._process_error("'atom' has unknown chid type.", atom.lineno)

    # This function processes number nodes.
    def _process_number(self, number):
        if not isinstance(number, Node) or number.type != "number":
            self._process_error("Something bad happened while processing " +
                                "'number'. Unfortunately, that is all we " +
                                "know.")
        if number.is_leaf():
            return str(number.value)
        else:
            self._process_error("'number' has children. It should be sterile.",
                                number.lineno)

    # This function processes boolean nodes.
    def _process_boolean(self, boolean):
        if not isinstance(boolean, Node) or boolean.type != "boolean":
            self._process_error("Something bad happened while processing " +
                                "'boolean'. Unfortunately, that is all we " +
                                "know.")
        if boolean.is_leaf():
            return str(number.value)
        else:
            self._process_error("'boolean' has children. It should be " +
                                "sterile.", boolean.lineno)

    # This function processes arithmetic expressions.
    def _process_arithmetic_expression(self, arith_exp):
        if not isinstance(arith_exp, Node) or \
           arith_exp.type != "arithmetic_expression":
            self._process_error("Something bad happened while processing " +
                                "'arithmetic_expression'. Unfortunately, " +
                                "that is all we know.")
        if len(arith_exp.children) not in [1, 2]:
            self._process_error("'arithmetic_expression' has incorrect " +
                                "number of children.", arith_exp.lineno)
        if arith_exp.value == "term":
            return self._process_term(arith_exp.children[0])
        elif arith_exp.value in ['+', '-']:
            return '(' + \
                self._process_arithmetic_expression(arith_exp.children[0]) + \
                ') ' + arith_exp.value + ' ' + \
                self._process_term(arith_exp.children[1])
        else:
            self._process_error("Illegal operation type for " +
                                "'arithmetic_expression'", arith_exp.lineno)

    # This function processes terms.
    def _process_term(self, term):
        if not isinstance(term, Node) or term.type != "term":
            self._process_error("Something bad happened while processing " +
                                "'term'. Unfortunately, " +
                                "that is all we know.")
        if len(term.children) not in [1, 2]:
            self._process_error("'term' has incorrect " +
                                "number of children.", term.lineno)
        if term.value == "factor":
            return self._process_factor(term.children[0])
        elif term.value in ['*', '/', '//']:
            return '(' + \
                self._process_term(term.children[0]) + \
                ') ' + term.value + ' ' + \
                self._process_factor(term.children[1])
        else:
            self._process_error("Illegal operation type for " +
                                "'term'", term.lineno)

    # This function processes factors.
    def _process_factor(self, factor):
        if not isinstance(factor, Node) or factor.type != "factor":
            self._process_error("Something bad happened while processing " +
                                "'factor'. Unfortunately, " +
                                "that is all we know.")
        if len(factor.children) != 1:
            self._process_error("'factor' has incorrect " +
                                "number of children.", factor.lineno)
        if factor.value == "power":
            return self._process_power(factor.children[0])
        elif factor.value in ['+', '-']:
            return '(' + factor.value + \
                self._process_factor(factor.children[0]) + ')'
        else:
            self._process_error("Illegal operation type for " +
                                "'factor'", factor.lineno)

    # This function processes powers.
    def _process_power(self, power):
        if not isinstance(power, Node) or power.type != "power":
            self._process_error("Something bad happened while processing " +
                                "'power'. Unfortunately, " +
                                "that is all we know.")
        if power.value == "atom":
            return self._process_atom(power.children[0])
        elif power.value == "trailer":
            atom = self._process_atom(power.children[0])
            if atom == "pocket":
                return _process_pocket(power)
            trailers = ''
            for trailer in power.children[1:]:
                trailers += self._process_trailer(trailer)
            return atom + trailer
        else:
            self._process_error("Illegal operation type for " +
                                "'power'", power.lineno)

    # This function processes trailers.
    def _process_trailer(self, trailer):
        if not isinstance(trailer, Node) or trailer.type != "trailer":
            self._process_error("Something bad happened while processing " +
                                "'trailer'. Unfortunately, " +
                                "that is all we know.")
        if len(trailer.children) != 1:
            self._process_error("'trailer' has incorrect " +
                                "number of children.", trailer.lineno)
        if trailer.value == "dot":
            return "." + str(trailer.children[0])
        elif trailer.value == "calllist":
            return self._process_calllist(trailer.children[0])
        else:
            self._process_error("Illegal value type for " +
                                "'trailer'", trailer.lineno)

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

    def _process_pocket(self, pocket_node):
        commands = ""
        if len(pocket_node.children) != 3:
            self._process_error("pocket has wrong number of children",
                                pocket_node.lineno)
        if pocket_node.children[1] != "dot":
            self._process_error("pocket must be followed by a dot",
                                pocket_node.lineno)
        if len(pocket_node.children[1].children) != 1:
            self._process_error("no method specified for pocket",
                                pocket_node.lineno)
        if pocket_node.children[1].children[0] == "add":
            commands += "pocket.add"
            commands += self._process_trailer(pocket_node.children[2])
        elif pocket_node.children[1].children[0] == "get":
            commands += "pocket.get"
            commands += self._process_trailer(pocket_node.children[2])
        elif pocket_node.children[1].children[0] == "remove":
            commands += "pocket.remove"
            commands += self._process_trailer(pocket_node.children[2])
        else:
            self._process_error("invalid method for pocket",
                                pocket_node.lineno)

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
