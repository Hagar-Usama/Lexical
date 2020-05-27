import pytest
from RegExp import RegExp
from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
from State import dfa_aux, build_DFA
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET


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

    case = 'test postfix [case 2]'
    exp = "(a|b)c*#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value =   ['a', 'b', '|', 'c', '*', 'concat', '#',  'concat'] 
    assert_it(correct_value, actual_value, case )

    case = 'test postfix [case 3]'
    exp = "dd*.(c|cEc)#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value =  ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'c', 'E', 'concat', 'c', 'concat', '|', 'concat', '#', 'concat']
    assert_it(correct_value, actual_value, case )


    case = 'test postfix [case 4]'
    exp = "dd*.c(𝛆|Ec)#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value =  ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']
    assert_it(correct_value, actual_value, case )


    case = 'test postfix [case 5]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    exp = list(exp)
    operators = {'(', ')', '*', '|'}
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print(mod_list)

    r.operators.add("concat")
    actual_value =  r.get_postfix()
    correct_value = ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']
    assert_it(correct_value, actual_value, case )


def test_AST_tree():
    case = 'test AST [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    operators = {'(', ')', '*', '|','concat'}
    post = ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']

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
    # mind concat
    operators = {'(', ')', '*', '|','concat'}
    post = ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']

    tree = build_AST_tree(post,operators)
    print_tree("", tree, False)
    


    actual_value = tree.left.right.left.name
    correct_value = '𝛆'
    assert_it(correct_value, actual_value, case )


def test_prefollow_tree():
    case = 'prefollow [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    # mind concat
    operators = {'(', ')', '*', '|','concat'}
    post = ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']


    tree = build_AST_tree(post,operators)
    pre_followpos(tree)
    print_tree("", tree, False)


    #get_node_dict(tree)
    #print_yellow(tree.id_dict)
    #print_purple(set(tree.id_dict.keys()))
     
    actual_value = tree.firstpos, tree.lastpos
    correct_value = ({32},{46})
    assert_it(correct_value, actual_value, case )


def test_eval_follow():

    case = 'Test eval follow [case 1]'
    # don't care for parentethis 
    exp = "dd*.c(((𝛆|Ec)))#"
    # mind concat
    operators = {'(', ')', '*', '|','concat'}
    post = ['d', 'd', '*', 'concat', '.', 'concat', 'c', 'concat', '𝛆', 'E', 'c', 'concat', '|', 'concat', '#', 'concat']


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
    

    r.operators.add("concat")
    operators = {'(', ')', '*', '|','concat'}
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
        
    r.operators.add("concat")
    operators = {'(', ')', '*', '|','concat'}
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
        

    r.operators.add("concat")
    operators = {'(', ')', '*', '|','concat'}
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
        

    r.operators.add("concat")
    operators = {'(', ')', '*', '|','concat'}
    post = r.get_postfix()
    post.append("#")
    post.append("concat")
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
    correct_value = {frozenset({103}) ,frozenset({103,98})}
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
        test_DFA()
        

        

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()

