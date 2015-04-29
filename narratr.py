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
import argparse


def print_tree(node, indent):
    prefix = "    " * indent
    try:
        val = ""
        if node.value is not None:
            val += " (value: " + str(node.value) + ")"
        if node.v_type is not None:
            val += " (value type: " + str(node.v_type) + ")"
        if node.lineno is not None:
            val += " (line num: " + str(node.lineno) + ")"

        print prefix + node.type + val

        if not node.is_leaf():
            for n in node.children:
                if type(n) is dict:
                    print "    " + prefix + "(dictionary)"
                    for key, value in n.iteritems():
                        print_tree(value, indent + 2)
                else:
                    print_tree(n, indent + 1)
    except:
        print prefix + "[Something bad happened]"


def print_symtab(symtab):
    print symtab


def parse(source):
    if verbose:
        print "parsing...",
    p = parser.ParserForNarratr()
    ast = p.parse(source)
    symtab = p.symtab
    if verbose:
        print u'\u2713'
    return ast, symtab


def generate_code(ast, symtab, outfile):
    if verbose:
        print "generating code...",
    c = CodeGen()
    c.process(ast, symtab)
    c.construct(outfile)
    if verbose:
        print u'\u2713'


def read(path):
    if verbose:
        print "reading file...",
    try:
        with open(path, 'r') as f:
            source = f.read()
    except IOError as e:
        print "\nERROR: Couldn't read source file " + path
        exit(1)
    else:
        if verbose:
            print u'\u2713'
        return source


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-t', '--tree', action='store_true',
                           help='print a representation of the abstract' +
                           ' syntax tree from the parser')
    argparser.add_argument('-v', '--verbose', action="store_true",
                           help='print updates on each step of the compile')
    argparser.add_argument('source', action="store", help='the source file')
    argparser.add_argument('-o', '--output', nargs=1, action="store",
                           help='specify an output file. defaults to' +
                           ' [input file].py')
    argparser.add_argument('-i', '--inert', action="store_true",
                           help='does not try to use code generator')
    argparser.add_argument('-s', '--symtab', action='store_true',
                           help='print the symbol table')
    args = argparser.parse_args(sys.argv[1:])

    global verbose
    verbose = args.verbose

    if args.output is None:
        outputfile = args.source + ".py"
    else:
        outputfile = args.output[0]

    source = read(args.source)
    ast, symtab = parse(source)
    if args.tree:
        print "\n------------------- AST ---------------------"
        print_tree(ast, 0)
        print "------------------- /AST ---------------------\n"

    if args.symtab:
        print "\n------------------- SymTab ---------------------"
        print_symtab(symtab)
        print "------------------- /Symtab ---------------------\n"

    if not args.inert:
        generate_code(ast, symtab, outputfile)
    if verbose:
        print "Your game is ready. Have fun!"

if __name__ == "__main__":
    main()
