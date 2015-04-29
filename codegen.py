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
# Primary Authors: Jonah Smith, Yelin Hong
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------


class CodeGen:
    def __init__(self):
        self.frontmatter = "#!/usr/bin/env python\n"
        self.scenes = []
        self.scene_nums = []
        self.items = []
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
        for c in node.children:
            if c.type == "blocks":
                for bc in c.children:
                    if type(bc) is dict:
                        for key, s_i in bc.iteritems():
                            if s_i.type == "scene_block":
                                self._add_scene(self._scene_gen(s_i, key))
                            elif s_i.type == "item_block":
                                pass
                    elif bc.type == "start_state":
                        self._add_main(bc)

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
        # defaults to scene labeled "1" (assume exists)
        if self.main == "":
            self._add_main()

        if outputfile == "stdout":
            print self.frontmatter
            print "\n".join(self.scenes)
            print self.main
        else:
            with open(outputfile, 'w') as f:
                f.write(self.frontmatter)
                f.write("\n")
                f.write("\n".join(self.scenes))
                f.write("\n\n")
                f.write(self.main)

    # This function is used internally to add a scene to the scene list. It
    # takes a string *with correct indentation*.
    def _add_scene(self, scene):
        self.scenes.append(scene)

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
    # is not confused.  If it does appear, it moves calls the cleanup function
    # of the previous scene and goes to the setup function of the called scene.
    def _add_main(self, startstate=None):
        if self.main == "":
            self.main = "pocket = []\n"
            self.main += '''def get_response(caller, direction):
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
            exec caller + "_inst.cleanup()"
            exec "s_" + str(direction[response.split(" ")[1]])\\
                + "_inst.setup()"
        else:
            print "\\"" + response.split(" ")[1] + "\\" is not a "\\
                + "valid direction from this scene."
    else:
        return response\n\n'''

            # Create an instance of each scene that has been declared.
            for s in self.scene_nums:
                self.main += "s_" + str(s) + "_inst = s_" + str(s) + "()\n"

            if startstate is None:
                self.startstate = 1
            elif startstate.value in self.scene_nums:
                self.startstate = startstate.value
            else:
                print "WARNING: You specified a start state that does not "\
                    + "exist. Defaulting to Scene 1."
                self.startstate = 1

            self.main += "if __name__ == '__main__':\n    s_"\
                + str(self.startstate) + "_inst.setup()"
        else:
            print "WARNING: You wrote multiple start states. State "\
                + str(self.startstate) + " will be used."

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
            + "\n        pass\n\n    " + "\n    ".join(commands)

        return scene_code

    # Code for adding a setup block. Takes as input a single "setup block"
    # node. Adds boilerplate code (function definition, empty dictionary for
    # direction, and at the end, the code to move to the action block), and
    # sends the child nodes to _process_statements() to generate their code.
    def _process_setup_block(self, c):
        commands = []
        commands.append("def setup(self):" +
                        "\n        direction = {}")

        if len(c.children) > 0:
            for child in c.children:
                commands.append(self._process_statements(child, 2))
        commands.append("    self.action(direction)\n")
        return commands

    # Code for adding a cleanup block. Takes as input a single "cleanup block"
    # node. Adds boilerplate code (function definition and "pass" if necessary,
    # explained below), then sends the child nodes to _process_statements() to
    # generate their code. "pass" is required in the scenario that there are no
    # child nodes, in which case Python syntactically requires code, we need to
    # be able to execute the function, but we don't want anything to happen. #
    # "pass" is a Python command that does nothing, so it fits the bill.
    def _process_cleanup_block(self, c):
        commands = []
        commands.append("def cleanup(self):")
        if len(c.children) > 0:
            commands.append(self._process_statements(c.children[0], 2))
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
                commands.append(self._process_statements(child, 3))
        commands.append("        response = get_response(" +
                        "self.__class__.__name__, direction)\n")
        return commands

    # Takes a "statements" node, calls a function to find the "statement"
    # nodes that descend from it, and then figures out what kind of statement
    # it is and takes the appropriate action. Many of the new features we add
    # to the language will just be a matter of adding to this function.
    # Returns a string of statements that descended from the "statements"
    # node. This function should only be used internally. Indent level
    # specifies how many indents should appear before statements in the
    # sequence.
    def _process_statements(self, statement, indentlevel=1):
        commands = ''
        prefix = "\n" + "    "*indentlevel
        indent = 1
        for smt in statement.children:
            if smt.value == "say":
                commands += prefix + "print "
                for testlist in smt.children:
                    commands += self._process_testlist(testlist, 2)
            elif smt.value == "exposition":
                commands += prefix + "print "
                for testlist in smt.children:
                    commands += self._process_testlist(testlist, 2)
            elif smt.value in ["win", "lose"]:
                if len(smt.children) > 0:
                    commands += prefix + "print "
                    for testlist in smt.children:
                        commands += self._process_testlist(testlist, 2)
                commands += prefix + "exit(0)"

            elif smt.value == "expression":
                print "match the expression"

            elif smt.value == "flow":
                commands += "    "*indentlevel
                if len(smt.children) > 0:
                    for child in smt.children:
                        i = 0
                        if child.type == "direction":
                            commands += prefix + '    direction = {"'
                            commands += self._process_direction(child, 2)
                            if i != len(smt.children) - 1:
                                commands += ', '
                            else:
                                commands += "}"

            elif smt.value == "lose":
                if len(smt.children) > 0:
                    for testlist in smt.children:
                        self._process_testlist(testlist, 2)

            elif smt.value is None:
                commands += self._process_testlist(smt, 2)

        # We need to remove the leading whitespace and first tab because of
        # the list constructed by _scene_gen(). It's possible this will mess
        # with the block statements later on, in which case this modification
        # should instead be made in that function.
        return commands[5:]

    # This function takes "testlist" node as argument
    def _process_testlist(self, testlist, indentlevel=1):
        commands = ''

        for test in testlist.children:
            if test.type == "test":
                for child in test.children:
                    if child.type == "expression":
                        commands += self._process_expression(child, 2)
                    if child.type == "and_test":
                        commands += self._process_expression(child, 2)
                    if child.type == "not_test":
                        commands += self._process_expression(child, 2)
                    if child.type == "or_test":
                        commands += self._process_expression(child, 2)
            elif test.type == "suite":
                commands += "    "*3 + "win"
        return commands

    # This function takes "expression" node as argument
    def _process_expression(self, exps, indentlevel=1):
        commands = ''

        for child in exps.children:
            if child.type == "factor":
                commands += '"' + child.value + '"'
            if child.type == "expression":
                if len(child.children) > 0:
                    for exex in child.children:
                        if exex.type == "factor":
                            commands += "\n" + "    "*indentlevel
                            commands += self._process_factor(exex, 2) + "\n"
        return commands

    # This function takes "factor" node as argument
    def _process_factor(self, factors, indentlevel=2):
        commands = ""
        if len(factors.children) > 0:
            if len(factors.children) == 3:
                for factor in factors.children[0].children:
                    commands += str(factor.value)
                commands += factors.children[1].value
                for factor in factors.children[2].children:
                    commands += str(factor.value)
        return commands

    # This function takes "direction" node as argument
    # Building a dictionary for direction, using the direction as key and
    # scene number as value
    def _process_direction(self, direction, indentlevel=1):
        commands = ''
        commands += direction.value
        commands += '": '
        for scene in direction.children:
            commands += str(scene.value)
        return commands
