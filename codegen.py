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
            self.main = '''
            def get_response():
                response = raw_input(" -->> ")
                response = response.lower()
                response = response.translate(None,
                            "!#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~")
                response = ' '.join(response.split())
                if response == "exit":
                    print "== GAME TERMINATED =="
                    exit(0)
                else:
                    return response

            '''

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
                #add suite block node here
                commands.append("def setup(self):\n")
                if len(c.children) > 0:
                    print "confusing?"
                    for child in c.children:
                        print child
                        commands.append(self._process_statements(child, 1))
                print "setup block commands here"
                commands.append("\n        self.action()\n")

            elif c.type == "cleanup_block":
                commands.append("def cleanup(self):\n        pass\n") 
                if len(c.children) > 0:
                    commands.append(self._process_statements(c.children[0], 2))

            elif c.type == "action_block":
                if len(c.children) > 0:
                    for child in c.children:
                        self._process_statements(child, 2)
                        print "child of action"
                        print child
                print "action block here"
                print c.children
                #commands.append("def action(self):\n        " +
                #                "response = \"\"\n        while(True):\n" +
                #                self._process_statements(c.children[0], 3) +
                #                "\n            response = get_response()\n")

        self.scene_nums.append(sid)
        #delete the join(commands) for debuggung reason, the original one is
        #scene_code = "class s_" + str(sid) + ":\n    def __init__(self):"\
        #    + "\n        pass\n\n    " + "\n    ".join(commands)
        scene_code = "class s_" + str(sid) + ":\n    def __init__(self):"\
            + "\n        pass\n\n    " + "\n    ".join(commands)
        print "want commands are like"
        print commands

        return scene_code


    #Takes a "suite" node, calls the function to process "statemant"    
    def _process_suite(self , suite, indentlevel=1):
        commands = []
        if len(suite.children) > 0:
            for smt in suite.children:
                if smt.type == "statement":
                    commands.append(self._process_statements(smt, 2))
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
        for smt in statement.children:
            if smt.value == "say":
                commands += "    "*indentlevel + "print "
                print "match the say statement"
                print smt
                for testlist in smt.children:
                    print "tests are here"
                    commands += self._process_testlist(testlist, 2)
            elif smt.value == "exposition":
                print "match the exposition"
                for testlist in smt.children:
                    self._process_testlist(testlist, 2)

            elif smt.value == "win":
                print "match the win statement"
                if len(smt.children) > 0:
                    for testlist in smt.children:
                        self._process_testlist(testlist, 2)

            elif smt.value == "expression":
                print "match the expression"

            elif smt.value == "flow":
                print "match the flow statement"

            elif smt.value == "lose":
                print "match the lose statement"
                if len(smt.children) > 0:
                    for testlist in smt.children:
                        self._process_testlist(testlist, 2)

                commands.append("exit(0)")
                commands.append("sys.exit(0)")

        #if len(commands) > 0:
        #    commands[0] = "    "*indentlevel + commands[0]
        #return prefix.join(commands)
        print "want to know why can not join"
        print commands
        return commands
    #This function takes "testlist" node as argument
    def _process_testlist(self, testlist, indentlevel=1):
        commands = ''
        for test in testlist.children:
            if test.type == "test":
                for child in test.children:
                    if child.type == "expression":
                        commands += self._process_expression(child, 2)

                print "test are here"
                print test
        return commands
    #This function takes "expression" node as argument
    def _process_expression(self, exps, indentlevel=1):
        commands = ''
        for child in exps.children:
            if child.type == "factor":
                commands += '"'+ child.value + '"'
        return commands


    

