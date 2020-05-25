import pytest
from RegExp import RegExp

ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"
ANSI_PURPLE = "\u001B[35m"
#ANSI_YELLOW = "\u001B[36m"



def print_yellow(msg):
    print(f"{ANSI_YELLOW}{msg}{ANSI_RESET}")

def print_purple(msg):
    print(f"{ANSI_PURPLE}{msg}{ANSI_RESET}")

def print_blue(msg):
    print(f"{ANSI_BLUE}{msg}{ANSI_RESET}")

def print_red(msg):
    print(f"{ANSI_RED}{msg}{ANSI_RESET}")

def print_green(msg):
    print(f"{ANSI_GREEN}{msg}{ANSI_RESET}")

def test_regex_input():

    case = 'test regex input [case 1]'
    
    operators = {'(', ')', '*', '|'}
    exp = "(a|bc)*#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
    

    actual_value =  r.handle_exp()
    correct_value = ['(', 'a', '|', 'b', 'concat', 'c', ')', '*', 'concat', '#']
    assert_it(correct_value, actual_value, case )

    case = 'test regex input [case 2]'
    exp = "a*b*a|babc#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
    

    actual_value =  r.handle_exp()
    correct_value =  ['a', '*', 'concat', 'b', '*', 'concat', 'a', '|', 'b', 'concat', 'a', 'concat', 'b', 'concat', 'c', 'concat', '#'] 
    assert_it(correct_value, actual_value, case )

    case = 'test regex input [case 3]'
    exp = "d*(c|(cEc))#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
   

    actual_value =  r.handle_exp()
    correct_value =   ['d', '*', 'concat', '(', 'c', '|', '(', 'c', 'concat', 'E', 'concat', 'c', ')', ')', 'concat', '#'] 
    assert_it(correct_value, actual_value, case )


def test_postfix():

    case = 'test postfix [case 1]'
    exp = "(a|bc)*#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()
    
    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value =   ['a', 'b', 'c', 'concat', '|', '*', '#',  'concat'] 
    assert_it(correct_value, actual_value, case )

    case = 'test postfix [case 1]'
    exp = "a|bc*#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value =   ['a', 'b', '|', 'c', '*', 'concat', '#',  'concat'] 
    assert_it(correct_value, actual_value, case )



   

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
       
        test_regex_input()
        print_blue('*.*.'*15)
        test_postfix()
        

        

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()

