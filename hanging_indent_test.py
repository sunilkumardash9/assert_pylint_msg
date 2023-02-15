
import tempfile
import unittest



from hanging_indent_check import HangingIndentChecker

import astroid  # isort:skip
from pylint import interfaces  # isort:skip
from pylint import testutils  # isort:skip

from pylint import utils as pylint_utils  # isort:skip

import re
import utils
from pylint import lint
from pylint.reporters.text import TextReporter




class HangingIndentCheckerTests(unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.checker_test_object = testutils.CheckerTestCase()
        self.checker_test_object.CHECKER_CLASS = (HangingIndentChecker)
        self.checker_test_object.setup_method()
        self.class_ = HangingIndentChecker

    def assert_msg(self, filename):
       
        msg_str = 'There should be a break after parenthesis when content within parenthesis spans multiple lines.'
        msg_id = 'no-break-after-hanging-indent'
        with open('pylint_output.txt', 'w') as f:
            args = ['--load-plugins', 'hanging_indent_check',"--disable",'all','--enable',msg_id,filename]
            lint.Run(args, reporter=TextReporter(f), exit=False)
        with open('pylint_output.txt', 'r') as f:
            output = f.read()      
        print(output,)
        id = 'C0002'
        regex = id+r": (.*)\."
        
        match = re.search(regex, output)
        self.assertEqual(msg_str, match.group(1)+'.')
        

    def test_no_break_after_hanging_indentation(self) -> None:
        node_break_after_hanging_indent = astroid.scoped_nodes.Module(
            name='test',
            doc='Custom test')
        temp_file = tempfile.NamedTemporaryFile()
        filename = temp_file.name
        with utils.open_file(filename,'w') as tmp:
            tmp.write(
                u"""self.post_json ('/ml/\\trainedclassifierhandler',
                self.payload, expect_errors=True, expected_status_int=401)
                #if (a>1 and 
                #       b > 2):
                """)
        node_break_after_hanging_indent.file = filename
        node_break_after_hanging_indent.path = filename

        self.checker_test_object.checker.process_tokens(
           pylint_utils.tokenize_module(node_break_after_hanging_indent))

        message = testutils.MessageTest(
            msg_id='no-break-after-hanging-indent', line=1)
        self.assert_msg(filename)
        with self.checker_test_object.assertAddsMessages(message):
            
            temp_file.close()
        
    def test_no_break_after_hanging_indentation_with_comment(self) -> None:
        node_break_after_hanging_indent = astroid.scoped_nodes.Module(
            name='test',
            doc='Custom test')
        temp_file = tempfile.NamedTemporaryFile()
        filename = temp_file.name
        with utils.open_file(filename, 'w') as tmp:
            tmp.write(
                u"""self.post_json('/ml/\\trainedclassifierhandler',
                self.payload, expect_errors=True, expected_status_int=401)

                if (a > 1 and
                        b > 2):
                        pass  # pylint: disable=invalid-name
                """)
        node_break_after_hanging_indent.file = filename
        node_break_after_hanging_indent.path = filename

        self.checker_test_object.checker.process_tokens(
           pylint_utils.tokenize_module(node_break_after_hanging_indent))

        message = testutils.MessageTest(
            msg_id='no-break-after-hanging-indent', line=1)

        with self.checker_test_object.assertAddsMessages(message):
            #self.assert_msg(filename)
            temp_file.close()
