# -*- coding: utf-8 -*-
import pytest
from helpers.RegExp import RegExp
from helpers.Node_AST import Node_AST
from helpers.State import State
from helpers.color_print import color_print
# import modules
# #from RegExp import RegExp
# from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
# from State import dfa_aux, build_DFA, DFA
# from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET


def test_regex_input():

    case = 'test regex input [case 1]'
    
    operators = {'(', ')', '*', '|'}
    exp = "(a|bc)*#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
    

    actual_value =  r.handle_exp()
    correct_value = ['(', 'a', '|', 'b', 'CONCAT', 'c', ')', '*', 'CONCAT', '#']
    assert_it(correct_value, actual_value, case )

    case = 'test regex input [case 2]'
    exp = "a*b*a|babc#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
    

    actual_value =  r.handle_exp()
    correct_value =  ['a', '*', 'CONCAT', 'b', '*', 'CONCAT', 'a', '|', 'b', 'CONCAT', 'a', 'CONCAT', 'b', 'CONCAT', 'c', 'CONCAT', '#'] 
    assert_it(correct_value, actual_value, case )

    case = 'test regex input [case 3]'
    exp = "d*(c|(cEc))#"
    exp = list(exp)
    r = RegExp(exp, operators, star="*")
   

    actual_value =  r.handle_exp()
    correct_value =   ['d', '*', 'CONCAT', '(', 'c', '|', '(', 'c', 'CONCAT', 'E', 'CONCAT', 'c', ')', ')', 'CONCAT', '#'] 
    assert_it(correct_value, actual_value, case )


def test_postfix():

    case = 'test postfix [case 1]'
    exp = "(a|bc)*#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()
    
    print(mod_list)

    r.operators.add("CONCAT")
    actual_value =  r.get_postfix()
    correct_value =   ['a', 'b', 'c', 'CONCAT', '|', '*', '#',  'CONCAT'] 
    assert_it(correct_value, actual_value, case )

    case = 'test postfix [case 2]'
    exp = "(a|b)c*#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("CONCAT")
    actual_value =  r.get_postfix()
    correct_value =   ['a', 'b', '|', 'c', '*', 'CONCAT', '#',  'CONCAT'] 
    assert_it(correct_value, actual_value, case )

    case = 'test postfix [case 3]'
    exp = "dd*.(c|cEc)#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("CONCAT")
    actual_value =  r.get_postfix()
    correct_value =  ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'c', 'E', 'CONCAT', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']
    assert_it(correct_value, actual_value, case )


    case = 'test postfix [case 4]'
    exp = "dd*.c(𝛆|Ec)#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("CONCAT")
    actual_value =  r.get_postfix()
    correct_value =  ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']
    assert_it(correct_value, actual_value, case )


    case = 'test postfix [case 5]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("CONCAT")
    actual_value =  r.get_postfix()
    correct_value = ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']
    assert_it(correct_value, actual_value, case )


def test_AST_tree():
    case = 'test AST [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    operators = {'(', ')', '*', '|','CONCAT'}
    post = ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']

    # ast_node = Node_AST(post[0])
    tree = build_AST_tree(post,operators)

    actual_value = tree.left.right.left.name
    correct_value = '𝛆'
    assert_it(correct_value, actual_value, case )

    case = 'test AST [case 2]'

    actual_value = tree.left.right.right.right.name
    correct_value = 'c'
    assert_it(correct_value, actual_value, case )


    case = 'test AST [case 3]'

    actual_value = tree.right.name
    correct_value = '#'
    assert_it(correct_value, actual_value, case )


    case = 'test AST [case 4]'

    actual_value = tree.left.left.left.right.name
    correct_value = '.'
    assert_it(correct_value, actual_value, case )
   

def test_show_tree():
    case = 'Tree show [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    # mind CONCAT
    operators = {'(', ')', '*', '|','CONCAT'}
    post = ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']

    tree = build_AST_tree(post,operators)
    print_tree("", tree, False)
    


    actual_value = tree.left.right.left.name
    correct_value = '𝛆'
    assert_it(correct_value, actual_value, case )


def test_prefollow_tree():
    case = 'prefollow [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    # mind CONCAT
    operators = {'(', ')', '*', '|','CONCAT'}
    post = ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']


    tree = build_AST_tree(post,operators)
    pre_followpos(tree)
    print_tree("", tree, False)


    actual_value = tree.firstpos, tree.lastpos
    # may differ 
    correct_value = ({15},{21})
    assert_it(correct_value, actual_value, case )


def test_eval_follow():

    case = 'Test eval follow [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    # mind CONCAT
    operators = {'(', ')', '*', '|','CONCAT'}
    post = ['d', 'd', '*', 'CONCAT', '.', 'CONCAT', 'c', 'CONCAT', '𝛆', 'E', 'c', 'CONCAT', '|', 'CONCAT', '#', 'CONCAT']


    tree = build_AST_tree(post,operators)
    pre_followpos(tree)

    get_node_dict(tree)
    print_purple(set(tree.id_dict.keys()))


    #print_tree("", tree, False)

    eval_followpos(tree)

    #print_yellow("🌲 tree 🌲")
    #print_tree("", tree, False)
    tree.print_tree()
    
    
    val1 = tree.left.left.left.left.left.followpos
    val2 = tree.left.left.left.left.right.left.followpos
     
    actual_value = val1
    correct_value = val2
    assert_it(correct_value, actual_value, case )

    case = 'Test eval follow [case 2]'
    # don't care for parentethis 
    exp = "(a|b)*abb#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}

    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    #print(mod_list)
    

    r.operators.add("CONCAT")
    operators = {'(', ')', '*', '|','CONCAT'}
    post = r.get_postfix()
    #print(post)

    tree = build_AST_tree(post,operators)
    pre_followpos(tree)

    get_node_dict(tree)

    eval_followpos(tree)

    tree.print_tree()
    print(tree.id_dict)


    actual_value = tree.left.left.left.left.left.right.followpos
    correct_value = tree.left.left.left.left.left.right.followpos

    assert_it(correct_value, actual_value, case )


def test_trial():
    case = 'Trial [case 1]'

    exp = ["d","num",'(',"a", "|", "b", ")","#"]
    operators = {'(', ')', '*', '|'}

    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)
        
    r.operators.add("CONCAT")
    operators = {'(', ')', '*', '|','CONCAT'}
    post = r.get_postfix()
    print(post)

    tree = build_AST_tree(post,operators)
    pre_followpos(tree)
    get_node_dict(tree)

    eval_followpos(tree)
    tree.print_tree()

    
    case = 'Trial [case 2]'

    exp = ["d","(","a","|","b",")",'(',"a", "|", "b", ")","#"]
    operators = {'(', ')', '*', '|'}

    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)
        

    r.operators.add("CONCAT")
    operators = {'(', ')', '*', '|','CONCAT'}
    post = r.get_postfix()
    print(post)

    tree = build_AST_tree(post,operators)
    pre_followpos(tree)
    get_node_dict(tree)

    eval_followpos(tree)
    tree.print_tree()

    tree.get_DFA_dict()


    case = 'Trial [case 3]'

    # c|cEc

    exp = ["c","|","c","E","c"]
    operators = {'(', ')', '*', '|'}

    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print_red(mod_list)
        

    r.operators.add("CONCAT")
    operators = {'(', ')', '*', '|','CONCAT'}
    post = r.get_postfix()
    post.append("#")
    post.append("CONCAT")
    print(post)

    tree = build_AST_tree(post,operators)
    pre_followpos(tree)
    get_node_dict(tree)

    eval_followpos(tree)
    tree.print_tree()

    DFA_dict = tree.get_DFA_dict()
    print_green(DFA_dict)

    #DFA_dict = {96: ('c', set()), 97: ('c', {98}), 98: ('E', {100}), 100: ('c', {102}), 102: ('#', set())}
    root_s = tree.firstpos
    
    dfa_table, accept_states = build_DFA(DFA_dict, root_s)
    print_red(post)
    print_blue(root_s)
    print_green(dfa_table)
    print_purple(accept_states)

    actual_value = accept_states
    correct_value = {frozenset({50}) ,frozenset({48, 50})}

    
    assert_it(correct_value, actual_value, case )

    case = 'Trial [case 4]'

    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    actual_value = machine.simulate_dfa_2("cEcccEc",[])
    actual_value = machine.accepted_tokens
    correct_value = [list("cEc")]
    assert_it(correct_value, actual_value, case )




   



def test_DFA():

    case = 'Build_DFA [case 1]'



    root_s = {85,90,86}
    dfa_dict = {85: ('d', {86, 87}),
     86: ('a', {90, 91}),
     87: ('b', {90, 91}),
     90: ('a', {94}),
     91: ('b', {94}),
     94: ('#', set())}

    print(dfa_aux(dfa_dict, root_s))
    dfa_table, accept_states = build_DFA(dfa_dict, root_s)
    #print_green(dfa_table.get(frozenset({90,98}),-1).get('c',-1))

    actual_value = accept_states
    correct_value = {frozenset({90, 91, 94}), frozenset({94})}

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
        print_blue('*.*.'*15)
        test_AST_tree()
        print_blue('*.*.'*15)
        test_show_tree()
        print_blue('*.*.'*15)
        test_prefollow_tree()
        print_blue('*.*.'*15)
        test_eval_follow()
        print_blue('*.*.'*15)
        test_trial()
        print_blue('*.*.'*15)
        #test_DFA()
        

        

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()


"""
lexical 3

{'id': ['(', '(', 'a', 'OR', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j',
 'OR', 'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't', 'OR', 'u',
 'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', ')', 'OR', '(', 'A', 'OR', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E',
 'OR', 'F', 'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J', 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 
 'OR', 'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U', 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', ')',
 '(', '(', 'a', 'OR', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j', 'OR',
 'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't', 'OR', 'u', 'OR',
 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', ')', 'OR', '(', 'A', 'OR', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR',
 'F', 'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J', 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR',
 'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U', 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', ')', 'OR',
 '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', ')',
 ')', 'STAR', ')'],
 'num': ['(', '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9',
 ')', 'PLUS', ')'], 
 'floatNum': ['(', '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7',  'OR', '8', 'OR',
 '9', ')', 'PLUS', 'OR', '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8',
 'OR', '9', ')', 'PLUS', '.', '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR',
 '8', 'OR', '9', ')', 'PLUS', '(', '𝛆', 'OR', 'E', '(', '0', 'OR', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR',
 '6', 'OR', '7', 'OR', '8', 'OR', '9', ')', 'PLUS', ')', ')'], 
 'relop': ['(', '=', 'OR', '<>', 'OR', '>', 'OR', '>=', 'OR', '<', 'OR', '<=', ')'], 
 'assign': [':='], 
 'addop': ['(', '+', 'OR', '-', ')'], 
 'incop': ['++'], 
 'decop': ['--']}
 
"""