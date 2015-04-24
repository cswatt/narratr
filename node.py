# -----------------------------------------------------------------------------
# narrtr: node.py
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
    # Constructor requires:
    #   v           the value of the node
    #   t           the variable type, defined by Lexer/Parser
    #   c           a list of children nodes (Optional)
    def __init__(self, v, t, c=[]):
        self.value = v
        self.type = t
        self.children = c

    # This method is helpful for string representations
    def __repr__(self):
        return "Node(%r, %r, %r)" % (self.value, self.type, self.children)

    # This method checks if a node is a leaf node.
    def is_leaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True
