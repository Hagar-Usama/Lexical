"""
{'letter': ['(', 'a', 'OR', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j',
 'OR', 'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't',
 'OR', 'u', 'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', ')',
 'OR', '(', 'A', 'OR', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR', 'F', 'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J',
 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR', 'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U',
 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', ')'],
 'digit': ['(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', ')'],
 'digits': ['digit', 'PLUS']}

"""

import pytest
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
from RegExp import postfix_me

def test_postfix_me():
    case = "postfix me [case 1]"

    re_dict = {'letter': ['(', 'a', 'OR', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j',
                'OR', 'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't',
                'OR', 'u', 'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', ')',
                'OR', '(', 'A', 'OR', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR', 'F', 'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J',
                'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR', 'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U',
                'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', ')'],
                'digit': ['(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', ')'],
                'digits': ['digit', 'PLUS']}

    operators = {"OR", "STAR","PLUS","CONCAT", "(", ")"}
    post_dict = postfix_me(re_dict,operators)
    #print_blue(post_dict)

    for i, v in post_dict.items():
        print_blue(v)

    actual_value = post_dict
    correct_value = None

    assert_it(correct_value, actual_value, case)

def assert_it(correct_value, actual_value, case=""):
        assert correct_value == actual_value,\
        f"{ANSI_RED}[failed] {case}"\
        f" Expected ( {correct_value} )\n got\n ( {actual_value} ){ANSI_RESET}"
        print_green(f"[success] {case}")


def main():
    ###################
    # Run tests
    ###################
    # Sorted by checklist order, feel free to comment/un-comment
    # any of those functions.
    try:
       
        test_postfix_me()
        print_blue('*.*.'*15)
        

        

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()
