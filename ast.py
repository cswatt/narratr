# -----------------------------------------------------------------------------
# narrtr: ast.py
# This file defines the Node class for the narratr AST.
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 31 March 2015
# Primary Author: Jonah Smith
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------


# Class for nodes in the narratr AST.
class Node:
    # to initialize, requires:
    #   val           the value of the node
    #   children      a list of children nodes
    def __init__(self, val, c):
        self.v = val
        self.children = c

    def is_leaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True
