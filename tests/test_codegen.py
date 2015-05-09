import narratr.parser as parser
import narratr.codegen as codegen
from nose.tools import *
import subprocess
import sys


def tests_output():

    cases = {"sampleprograms/0_helloworld.ntr": "Hello, World!\n",
             "sampleprograms/1_comments.ntr": "Hello.\n",
             "sampleprograms/3_andor.ntr": "okay.\n",
             "sampleprograms/3_arithmetic.ntr": "2\n4\n4\n3\n3\n",
             "sampleprograms/3_assignment.ntr": "Oh, hello.\n",
             "sampleprograms/3_comparison.ntr": "okay.\nokay.\nokay.\nokay.\nokay.\n",
             "sampleprograms/4_break.ntr": "Okay.\nOkay.\n",
             "sampleprograms/4_continue.ntr": "2\n3\n",
             "sampleprograms/4_elseif.ntr": "Okay.\n",
             "sampleprograms/4_for.ntr": "Sadness is infinite.\n",
             "sampleprograms/4_if.ntr": "Okay.\nhaha\n",
             "sampleprograms/4_truefalse.ntr": "Okay.\n",
             "sampleprograms/4_while.ntr": "Okay.\nOkay.\nOkay.\n",
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
        real_output = subprocess.check_output(['python', 'temp.py'])
        expected_output = output
        assert_equal(real_output, expected_output, fname + " is messed up.")
