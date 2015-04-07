# -----------------------------------------------------------------------------
# narrtr: narratr.py
# This file compiles narratr games.
#
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 2 April 2015
# Primary Author: Jonah Smith
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

import sys
import parser
from codegen import CodeGen
from node import Node


def print_tree(node, indent):
    prefix = "    "*indent
    try:
        val = ""

        if node.value is not None:
            val = " (" + str(node.value) + ")"

        print prefix + node.type + val

        if not node.is_leaf():
            for n in node.children:
                print_tree(n, indent+1)
    except:
        print prefix + "[Something bad happened]"


def parse(source):
    print "parsing..."
    p = parser.ParserForNarratr()
    ast = p.parse(source)
    return ast


def generate_code(ast, outfile="stdout"):
    print "generating code..."
    c = CodeGen()
    c.process(ast)
    c.construct(outfile)
    print "success!"


def read(path):
    print "reading file..."
    try:
        with open(path, 'r') as f:
            source = f.read()
    except:
        print "Couldn't read file"
    return source


def main():
    args = sys.argv
    if len(args) == 3:
        source = read(args[1])
        ast = parse(source)
        generate_code(ast)

    elif len(args) == 4:
        if args[1] == "-t":
            source = read(args[2])
            ast = parse(source)
            print "\n------------------- AST ---------------------"
            print_tree(ast, 0)
            print "------------------- /AST ---------------------\n"
            generate_code(ast, args[3])


if __name__ == "__main__":
    main()
