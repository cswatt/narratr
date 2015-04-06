# -----------------------------------------------------------------------------
# narrtr: codegen.py
# This file defines the CodeGen class for narratr games.
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 1 April 2015
# Primary Author: Jonah Smith
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------


class CodeGen:
    def __init__(self):
        self.frontmatter = "import sys\n"
        self.scenes = []
        self.items = []
        self.main = ""

    # This function takes a node and sets the processing of the source in
    # motion. It takes as input the root node of the abstract syntax tree.
    # It is meant to be called externally (by the main compiler) and should
    # be called first before construct.
    # The general strategy: do dfs and process all of the sceneblocks [and
    # eventually itemblocks]. Also find the startstates and use them to
    # construct main. Add to the appropriate instance variables.
    def process(self, node):
        if node.type == "sceneblock":
            self.add_scene(self.scene_gen(node))

        # This is just a boilerplate example, it's not implemented yet.
        if node.type == "itemblock":
            item_gen(node)

        elif node.type == "startstate":
            self.add_main(node)

        if not node.is_leaf():
            for n in node.children:
                self.process(n)

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
            self.add_main()

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
    def add_scene(self, scene):
        self.scenes.append(scene)

    # This function generates the code for a start state given a start state
    # node. If start state code has already been generated, it produces a
    # warning and keeps the start state declared higher in the program. If
    # called without a node, it triggers the default action, which is a start
    # state of 1.
    def add_main(self, startstate=None):
        if self.main == "":
            if startstate is None:
                self.startstate = 1
            else:
                self.startstate = startstate.value

            self.main = "if __name__ == '__main__':\n    s = s_"\
                        + str(self.startstate) + "()\n    s.setup()"
        else:
            print "WARNING: You wrote multiple start states. State "\
                    + str(self.startstate) + " will be used."

    # This function takes a scene node and processes it, translating into
    # valid Python (really, a Python class). Iterates through the children
    # of the input node and constructs the setup, cleanup, and action blocks
    # using boilerplate code.
    def scene_gen(self, scene):
        commands = []
        for c in scene.children:
            if c.type == "sceneid":
                sid = c.value

            elif c.type == "setupblock":
                commands.append("def setup(self):\n" +
                                self.process_statements(c.children, 2) +
                                "\n        self.action()\n")

            elif c.type == "cleanupblock":
                commands.append("def cleanup(self):\n        pass\n" +
                                self.process_statements(c.children, 2))

            elif c.type == "actionblock":
                commands.append("def action(self):\n        " +
                                "response = \"\"\n        while(True):\n" +
                                self.process_statements(c.children, 3) +
                                "\n            response = raw_input(\">\")\n")

        scene_code = "class s_" + str(sid) + ":\n    def __init__(self):"\
            + "\n        pass\n\n    " + "\n    ".join(commands)

        return scene_code

    def process_statements(self, statements, indentlevel=1):
        # returns a list of statement nodes
        smts = self.find_statement(statements)
        commands = []
        prefix = "\n" + "    "*indentlevel

        # You pretty much just need to follow this scheme for statements
        for smt in smts:
            command = smt.children[0]
            if command.type == "say":
                commands.append("print \"" +
                                command.children[0].value + "\"")

            if command.type == "win":
                # win with an argument
                if len(command.children) > 0:
                    commands.append("print \"" +
                                    command.children[0].value +
                                    "\"")
                commands.append("sys.exit(0)")
        if len(commands) > 0:
            commands[0] = "    "*indentlevel + commands[0]
        return prefix.join(commands)

    # this is a function that finds all the "statement" children
    # of "statements" node
    def find_statement(self, statements):
            smts = []
            nodes_to_visit = statements
            while len(nodes_to_visit) > 0:
                cnode = nodes_to_visit.pop(0)
                if cnode.type == "statement":
                    smts.insert(0, cnode)
                else:
                    for node in cnode.children:
                        nodes_to_visit.insert(0, node)
            return smts
