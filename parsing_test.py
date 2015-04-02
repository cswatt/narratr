import parser
from codegen import CodeGen
from node import Node

test = parser.ParserForNarratr()

ast = test.parse("""scene $1 {
	setup:
		say "Hello, World!"
	action:
        win "you win!"
	cleanup:
}

start:$1""")

# this is a function that visualizes the node structure of the abstract
# syntax tree.


def rec_print(node, indent):
    prefix = "    "*indent
    try:
        val = ""

        if node.value is not None:
            val = " (" + str(node.value) + ")"

        print prefix + node.type + val

        if not node.is_leaf():
            for n in node.children:
                rec_print(n, indent+1)
    except:
        print prefix + "[Something bad happened]"

rec_print(ast, 0)

# these commands generate the code for the AST
c = CodeGen()
c.process(ast)
c.construct("dev_test.ntrc")
