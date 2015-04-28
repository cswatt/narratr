# -----------------------------------------------------------------------------
# narrtr: examine.py
# quickly see how a particular ntr file is processed
# Copyright (C) 2015 Team narratr
# All Rights Reserved
# Team narratr: Yelin Hong, Shloka Kini, Nivvedan Senthamil Selvan, Jonah
# Smith, Cecilia Watt
#
# File Created: 27 April 2015
# Primary Authors: Cecilia Watt
#
# Any questions, bug reports and complaints are to be directed at the primary
# author.
#
# -----------------------------------------------------------------------------

import sys
import lexer
import parser
import traceback
import argparse
import codegen

def show_tokens(filename):
	tokenlist = []
	print "\n------------------- tokens ---------------------"
	with open(filename) as f:
	    m = lexer.LexerForNarratr()
	    m.input(f.read())
	    t = m.token()
	    while t:
	        tokenlist.append(str(t))
	        t = m.token()
	if verbose:
		for f in tokenlist:
			print f
	else:
		pretty_print_tokens(tokenlist)

def pretty_print_tokens(tokenlist):
	from csv import reader
	for t in tokenlist:
		t = t[9:-1].rsplit(',', 3)
		print t[0] + " " + t[1]

def show_ast(filename):
	ast = ""
	p = parser.ParserForNarratr()
	print "\n------------------- ast ---------------------"
	
	with open(filename) as f:
		ast = p.parse(f.read())
	print str(ast)
	return ast

def show_code(ast):
	c = codegen.CodeGen()
	print "\n------------------- idk what this is ---------------------"
	c.process(ast)
	print "\n------------------- code ---------------------"
	c.construct()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action="store_true", default=False)
	parser.add_argument('source', action="store")
	args = parser.parse_args(sys.argv[1:])

	global verbose
	verbose = args.verbose

	source = args.source

	show_tokens(source)
	try:
		ast = show_ast(source)
		show_code(ast)
	except:
		print "Yo that did not parse."
		if verbose:
			traceback.print_exc()

if __name__ == "__main__":
	main()