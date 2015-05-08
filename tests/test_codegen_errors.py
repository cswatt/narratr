import narratr.parser as parser
import narratr.codegen as codegen
import unittest
import subprocess


class TestCodeGenErrors(unittest.TestCase):

    def test_parser_nonexistent_start_scene(self):

        """Test that codegen has error for nonexistent_start_scene."""
        p = parser.ParserForNarratr()
        with open('sampleprograms/6_nonexistent_start_scene.ntr') as f:
            ast = p.parse(f.read())
        symtab = p.symtab
        c = codegen.CodeGen()
        self.assertRaises(Exception, lambda: c.process(ast, symtab))
