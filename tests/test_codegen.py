import narratr.parser as parser
import narratr.codegen as codegen
from nose.tools import *
import subprocess
import sys


def tests_output():

    cases = {"sampleprograms/0_helloworld.ntr": "Hello, World!\n -->> ",
             "sampleprograms/1_comments.ntr": "Hello.\n -->> ",
             "sampleprograms/2_list.ntr":
             "['apple', 'banana', 'orange', 'peach']\n -->> ",
             "sampleprograms/2_derived.ntr":
             " ** 'key' is now in your pocket. **\n5\n1\n -->> ",
             "sampleprograms/3_andor.ntr": "okay.\n -->> ",
             "sampleprograms/3_arithmetic.ntr":
             "6\n6\n3\n4\n3.0\n3\n3 three\n -->> ",
             "sampleprograms/3_assignment.ntr": "Oh, hello.\n -->> ",
             "sampleprograms/3_comparison.ntr":
             "okay.\nokay.\nokay.\nokay.\nokay.\n -->> ",
             "sampleprograms/4_break.ntr": "Okay.\nOkay.\n -->> ",
             "sampleprograms/4_continue.ntr": "2\n3\n -->> ",
             "sampleprograms/4_elseif.ntr": "Okay.\n -->> ",
             "sampleprograms/4_if.ntr": "Okay.\n -->> ",
             "sampleprograms/4_truefalse.ntr": "Okay.\n -->> ",
             "sampleprograms/4_while.ntr": "Okay.\nOkay.\nOkay.\n -->> ",
             }
    for fname in cases:
        yield check_expected_output, fname, cases[fname]


def test_nonexistent_start_scene_error():

    p = parser.ParserForNarratr()
    with open('sampleprograms/6_nonexistent_start_scene.ntr') as f:
        ast = p.parse(f.read())
    symtab = p.symtab
    c = codegen.CodeGen()
    assert_raises(SystemExit, lambda: c.process(ast, symtab))


def check_expected_output(fname, output):

    p = parser.ParserForNarratr()
    try:
        with open(fname) as f:
            ast = p.parse(f.read())
        symtab = p.symtab
        c = codegen.CodeGen()
        c.process(ast, symtab)
        c.construct('temp.py')
    except:
        e = sys.exc_info()[0]
        assert_equal(0, 1, ("Exception: " + str(e)))
    else:
        proc = subprocess.Popen(['python', 'temp.py'],
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        proc.stdin.write('hello')
        p_output = proc.communicate()[0]
        expected_output = output
        assert_equal(p_output, expected_output,
                     fname + " printed:\n" + p_output +
                     "instead of:\n" + expected_output)
