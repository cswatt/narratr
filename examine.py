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
	# for f in tokenlist:
	# 	print f
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
			ast = str(p.parse(f.read()))
		print ast
	except:
		print "Yo that did not parse."
		traceback.print_exc()

def main():
	show_tokens(sys.argv[1])
	show_ast(sys.argv[1])

if __name__ == "__main__":
	main()