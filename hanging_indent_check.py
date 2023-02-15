from pylint import interfaces
from pylint import lint
import tokenize
from pylint import utils as pylint_utils
from typing import (
    Dict, Final, Generator, List, Optional, Pattern, Set, Tuple, TypedDict
)
from pylint import checkers


class HangingIndentChecker(checkers.BaseChecker):  # type: ignore[misc]
    """Custom pylint checker which checks for break after parenthesis in case
    of hanging indentation.
    """

    __implements__ = interfaces.ITokenChecker

    name = 'hanging-indent'
    priority = -1
    msgs = {
        'C0002': (
            (
                'There should be a break after parenthesis when content within '
                'parenthesis spans multiple lines.'),
            'no-break-after-hanging-indent',
            (
                'If something within parenthesis extends along multiple lines, '
                'break after opening parenthesis.')
        ),
    }
   

    def process_tokens(self, tokens: List[tokenize.TokenInfo]) -> None:
        """Process tokens to check if there is a line break after the bracket.

        Args:
            tokens: List[TokenInfo]. Object to process tokens.
        """
        
        escape_character_indicator = '\\'
        string_indicator = '\''
        excluded = False
        for (token_type, token, (line_num, _), _, line) in tokens:
            # Check if token type is an operator and is either a
            # left parenthesis '(' or a right parenthesis ')'.
            if token_type == tokenize.OP and token in ('(', ')'):
                line = line.strip()

                # Exclude 'if', 'elif', 'while' statements.
                if line.startswith(('if ', 'while ', 'elif ')):
                    excluded = True
                # Skip check if there is a comment at the end of line.
                if excluded:
                    split_line = line.split()
                    if '#' in split_line:
                        comment_index = split_line.index('#')
                        if (split_line[comment_index - 1].endswith(':') or
                                split_line[comment_index - 1].endswith('):')):
                            excluded = False
                    elif line.endswith(':') or line.endswith('):'):
                        excluded = False
                if excluded:
                    continue

                bracket_count = 0
                line_length = len(line)
                escape_character_found = False
                in_string = False
                for char_num in range(line_length):
                    char = line[char_num]
                    if in_string and (
                            char == escape_character_indicator or
                            escape_character_found):
                        escape_character_found = not escape_character_found
                        continue

                    # Check if we found the string indicator and flip the
                    # in_string boolean.
                    if char == string_indicator:
                        in_string = not in_string

                    # Ignore anything inside a string.
                    if in_string:
                        continue

                    if char == '(':
                        if bracket_count == 0:
                            position = char_num
                        bracket_count += 1
                    elif char == ')' and bracket_count > 0:
                        bracket_count -= 1

                if bracket_count > 0 and position + 1 < line_length:
                    # Allow the use of '[', ']', '{', '}' after the parenthesis.
                    separators = set('[{( ')
                    if line[line_length - 1] in separators:
                        continue
                    content = line[position + 1:]
                    # Skip check if there is nothing after the bracket.
                    split_content = content.split()
                    # Skip check if there is a comment at the end of line.
                    if '#' in split_content:
                        comment_index = split_content.index('#')
                        if comment_index == 0:
                            continue

                        last_content_before_comment = (
                            split_content[comment_index - 1])
                        if last_content_before_comment.endswith(
                                ('(', '[', '{')
                        ):
                            continue
                    self.add_message(
                        'no-break-after-hanging-indent', line=line_num)

def register(linter: lint.PyLinter):
    linter.register_checker(HangingIndentChecker(linter))