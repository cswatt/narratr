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

    def add_main(self, main):
        if self.main == "":
            self.main = main

    def construct(self, outputfile):
        with open(outputfile, 'w') as f:
            f.write(self.frontmatter)
            f.write("\n")
            f.write("\n".join(self.scenes))
            f.write("\n")
            f.write(self.main)

    # basically, do dfs search and process all of the sceneblocks [and
    # eventually itemblocks]. Also find the startstates and use them to
    # construct main.
    def process(self, node):
        if node.type == "sceneblock":
            self.add_scene(self.scene_gen(node))

        if node.type == "itemblock":
            item_gen(node)

        # this needs to be modified in the case that there are >1 starts given
        elif node.type == "startstate":
            self.add_main(self.main_gen(node))

        if not node.is_leaf():
            for n in node.children:
                self.process(n)

    def scene_gen(self, scene):
        commands = []
        for c in scene.children:
            if c.type == "sceneid":
                sid = c.value

            elif c.type in ["setupblock", "cleanupblock"]:
                commands.append(self.process_statements(c.children))

            elif c.type == "actionblock":
                # there's a good chance this is going to have the wrong
                # indentation when there are multiple commands
                commands.append("while (True):\n    " +
                                self.process_statements(c.children))
                commands.append("    response = raw_input(\">\")")

        scene_code = "def s_" + str(sid) + "():\n    " \
            + "\n    ".join(commands)

        return scene_code

    def process_statements(self, statements):
        # this is where statements are going to get processed. right now,
        # only need to figure out "say" and "win"
        commands = []
        if len(statements) > 0:
            if statements[0].children[0].type == "statementlist":
                for s in statements[0].children[0].children:

                    if s.children[0].type == "say":
                        commands.append("print \"" +
                                        s.children[0].children[0].value + "\"")

                    if s.children[0].type == "win":
                        # win with an argument
                        if len(s.children[0].children) > 0:
                            commands.append("    print \"" +
                                            s.children[0].children[0].value +
                                            "\"")
                        commands.append("    sys.exit(0)")

        return "\n    ".join(commands)

    def main_gen(self, startstate):
        main = "if __name__ == '__main__':\n    s_" + str(startstate.value)\
            + "()"
        return main