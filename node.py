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
    # Constructor takes:
    #   v           the value of the node
    #   t           the variable type, defined by Lexer/Parser
    #   c           a list of children nodes (Optional)
    #   v_type      the type of the value (int, float, string, boolean, id).
    #               Technically optional, but include for all new nodes.
    #   lineno      The line number at which the node appears. Technically
    #               optional, but include for all new nodes.
    def __init__(self, v, t, c=[], v_type=None, lineno=0, key=None):
        self.value = v
        self.type = t
        self.children = c
        self.v_type = v_type
        self.lineno = lineno
        self.key = key

    # This method is helpful for string representations
    def __repr__(self):
        return "Node(%r, %r, %r)" % (self.value, self.type, self.children)

    # This method checks if a node is a leaf node.
    def is_leaf(self):
        if len(self.children) > 0:
            return False
        else:
            return True

    # This method overloads the indexing [] operator to return the child
    # corresponding to the index.
    def __getitem__(self, index):
        if self.is_leaf():
            raise Exception("Node has no children.")
        if index >= len(self.children) or index < 0:
            raise Exception("Node index out of bounds.")
        return self.children[index]

