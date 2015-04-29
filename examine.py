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
import contextlib
import cStringIO

@contextlib.contextmanager
def nostdout():
	save_stdout = sys.stdout
	sys.stdout = cStringIO.StringIO()
	yield
	sys.stdout = save_stdout

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
	try:
		with open(filename) as f:
			ast = p.parse(f.read())
		print str(ast)
		return ast, p.symtab
	except:
		print "Yo that did not parse."
		if verbose:
			traceback.print_exc()

def show_code(ast, symtab):
	print "\n------------------- code ---------------------"
	try:
		c = codegen.CodeGen()
		c.process(ast, symtab)
		c.construct()
	except:
		print "Codegen did not gen the code."
		if verbose:
			traceback.print_exc()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbose', action="store_true", default=False)
	parser.add_argument('source', action="store")
	args = parser.parse_args(sys.argv[1:])

	global verbose
	verbose = args.verbose

	source = args.source

	show_tokens(source)
	ast, symtab = show_ast(source)
	show_code(ast, symtab)
	

if __name__ == "__main__":
	main()