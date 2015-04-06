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

    def add_scene(self, scene):
        self.scenes.append(scene)

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

    def construct(self, outputfile):
        # defaults to scene labeled "1" (assume exists)
        if self.main == "":
            self.add_main()

        with open(outputfile, 'w') as f:
            f.write(self.frontmatter)
            f.write("\n")
            f.write("\n".join(self.scenes))
            f.write("\n\n")
            f.write(self.main)

    # basically, do dfs and process all of the sceneblocks [and
    # eventually itemblocks]. Also find the startstates and use them to
    # construct main.
    def process(self, node):
        if node.type == "sceneblock":
            self.add_scene(self.scene_gen(node))

        if node.type == "itemblock":
            item_gen(node)

        # it uses the first one it finds (prevents overwrite)
        elif node.type == "startstate":
            self.add_main(node)

        if not node.is_leaf():
            for n in node.children:
                self.process(n)

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

    def find_statement(self, statements):
            # this is a function that finds all the "statement" children
            # of "statements" node
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
