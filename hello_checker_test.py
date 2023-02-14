import unittest
import astroid
import tempfile
import re

import subprocess
import unittest

from pylint import testutils, lint
from hello_checker import HelloWorldTokenChecker
from pylint import utils as pylint_utils 
from pylint.reporters.text import TextReporter

class HelloWorldTokenCheckTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.checker_test_object = testutils.CheckerTestCase()
        self.checker_test_object.CHECKER_CLASS = HelloWorldTokenChecker
        self.checker_test_object.setup_method()
        self.class_ = HelloWorldTokenChecker
        

    def msg(self,filename):
    
        msg_str = 'Uses a "Hello, world!" string.'
        msg_id = "hello-world-token"
        
        #print(msg_id_num, msg_id, msg_str)
        with open('pylint_output.txt', 'w') as f:
            args = ['--load-plugins', 'hello_checker','--disable','all','--enable',msg_id,filename]
            lint.Run(args, reporter=TextReporter(f), exit=False)
        with open('pylint_output.txt', 'r') as f:
            output = f.read() 
        #print(output)     
        id = 'C9002'  
        regex = id+r": (.*)\."
        match = re.search(regex, output)
        self.assertEqual(msg_str, match.group(1)+'.')
        f.close()


    def test_finds_hello_world_assignment(self):
        

        node = astroid.scoped_nodes.Module(
            name='test',
            doc='Custom test')
        temp_file = tempfile.NamedTemporaryFile()
        filename = temp_file.name
        with open(filename, 'w') as tmp:
            tmp.write('s = "hello world"')
        node.file = filename
        node.path = filename

        self.checker_test_object.checker.process_tokens(
            pylint_utils.tokenize_module(node))

        message = testutils.MessageTest(
            msg_id='hello-world-token'
            , line=1)

        with self.checker_test_object.assertAddsMessages(message):
            self.msg(filename)
            temp_file.close()
        

    def test_finds_hello_world_func_call(self):
        node = astroid.scoped_nodes.Module(
            name='test',
            doc='Custom test')
        temp_file = tempfile.NamedTemporaryFile()
        filename = temp_file.name
        with open(filename, 'w') as tmp:
            tmp.write('print("hello world")')
        node.file = filename
        node.path = filename

        self.checker_test_object.checker.process_tokens(
            pylint_utils.tokenize_module(node))

        message = testutils.MessageTest(
            msg_id='hello-world-token', line=1)

        with self.checker_test_object.assertAddsMessages(message):
            self.msg(filename)
            temp_file.close()

if __name__ == "__main__":
    unittest.main()