class CodeGen:
    def __init__(self):
        self.frontmatter = "#!/usr/bin/env python\nimport sys\n"
        self.scenes = []
        self.scene_nums = []
        self.items = []
        self.main = ""

    # This function iterates through all the nodes of the tree since we know
    # the structure already
    def process(self, node):
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
    def _add_main(self, startstate=None):
        if self.main == "":
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
    # using boilerplate code. This should only be used internally.
    def _scene_gen(self, scene, sid):
        commands = []
        for c in scene.children:
            if c.type == "SCENEID":
                sid = c.value

            elif c.type == "setup_block":
                commands.append("def setup(self):\n" +
                                self._process_statements(c.children, 2) +
                                "\n        print 'hello word'\n"
                                "\n        self.action()\n")

            elif c.type == "cleanup_block":
                commands.append("def cleanup(self):\n        pass\n" +
                                self._process_statements(c.children, 2))

            elif c.type == "action_block":
                commands.append("def action(self):\n        " +
                                "response = \"\"\n        while(True):\n" +
                                self._process_statements(c.children, 3) +
                                "\n            response = raw_input(\">\")\n")

        self.scene_nums.append(sid)

        scene_code = "class s_" + str(sid) + ":\n    def __init__(self):"\
            + "\n        pass\n\n    " + "\n    ".join(commands)

        return scene_code

    # Takes a "statements" node, calls a function to find the "statement"
    # nodes that descend from it, and then figures out what kind of statement
    # it is and takes the appropriate action. Many of the new features we add
    # to the language will just be a matter of adding to this function.
    # Returns a string of statements that descended from the "statements"
    # node. This function should only be used internally. Indent level
    # specifies how many indents should appear before statements in the
    # sequence.
    def _process_statements(self, statements, indentlevel=1):
        # returns a list of statement nodes
        smts = self._find_statement(statements)
        commands = []
        prefix = "\n" + "    "*indentlevel

        for smt in smts:
            command = smt.children[0]
            if command.type == "say":
                commands.append("print \"" +
                                command.children[0].value + "\"")

            if command.type in ["win", "lose"]:
                # win with an argument
                if len(command.children) > 0:
                    commands.append("print \"" +
                                    command.children[0].value +
                                    "\"")
                commands.append("sys.exit(0)")
        if len(commands) > 0:
            commands[0] = "    "*indentlevel + commands[0]
        return prefix.join(commands)

    # This function finds all the "statement" children of a "statements" node.
    # It uses a non-recursive DFS algorithm, basically. It returns a list of
    # nodes, IN ORDER OF APPEARANCE. To be used internally.
    def _find_statement(self, statements):
            smts = []
            nodes_to_visit = statements
            while len(nodes_to_visit) > 0:
                cnode = nodes_to_visit.pop(0)
                if cnode.type == "simple_statement":
                    smts.insert(0, cnode)
                else:
                    for node in cnode.children:
                        nodes_to_visit.insert(0, node)
            return smts
