
import pytest
from RegExp import RegExp
from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
from State import dfa_aux, build_DFA, DFA
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
import time

def run_example():

    # first add rd expersion
    exp = ["c","OR","c","E","c"]
    #rd = "program|var|integer|real|begin|end|if|else|then|while|do|read|write|:|;|,|.|\\"
    #exp = list(rd)

    operators = {'(', ')', 'STAR', 'OR'}

    # build RE and concats
    r = RegExp(exp, operators, star="STAR")
    mod_list = r.handle_exp()

    print_yellow(f"add concat {mod_list}")
        
    # actually those two lines are useless
    #r.operators.add("CONCAT")
    #operators = {'(', ')', 'STAR', 'OR','CONCAT'}

    # eval postfix expression for the AST
    post = r.get_postfix()
    # I do not add # above to avoid some confusion
    post.append("#")
    post.append("CONCAT")
    print_yellow(f"postfix exp: {post}")

    # now build AST
    tree = build_AST_tree(post,operators)
    # get firstpos and lastpos and nullables (+, ? not yet)
    pre_followpos(tree)
    # store in root the ids for leaves
    get_node_dict(tree)

    # evaluate followpos for the DFA
    eval_followpos(tree)

    # print tree to show
    tree.print_tree()

    # get a dict for id: (name , followpos)
    DFA_dict = tree.get_DFA_dict()
    #print_green(DFA_dict)

    # prepare for building the DFA
    # the firstpos of root is the first state in the DFA
    root_s = tree.firstpos
    
    # now, let's build our DFA
    dfa_table, accept_states = build_DFA(DFA_dict, root_s)
    #print_red(post)
    #print_blue(root_s)
    print_purple(dfa_table)
    print_purple(accept_states)

    # create your DFA machine
    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    # now simulate your input with the DFA
    input_list = "ccEccEcXcE"

    machine.simulate_dfa_2(input_list,[])
    # get the accepted tokens to compare it later with each pattern
    accepted_tokens = machine.accepted_tokens
    print_yellow(f"{accepted_tokens}")
    #print(accepted_tokens[1][0])

def run_example_2():
    exp = ['(', 'letter', '(', 'letter', 'OR', 'digit', ')', 'STAR', ')', 'OR',
           '(', 'digit', 'PLUS', ')', 'OR',
           '(', 'digit', 'PLUS', 'OR', 'digit', 'PLUS', '.', 'digits', '(', '𝛆', 'OR', 'E', 'digits', ')', ')'
        ]
    
    exp =[ '(', 'letter', '(', 'letter', 'OR', 'digit', ')', 'STAR', ')', 'OR',
           '(', 'digit', 'PLUS', ')', 'OR',
           '(', 'digit', 'PLUS', 'OR', 'digit', 'PLUS', '.', 'digits', '(', '𝛆', 'OR', 'E', 'digits', ')', ')', 'OR',
           '(', '=', 'OR', '<>', 'OR', '>', 'OR', '>=', 'OR', '<', 'OR', '<=', ')', 'OR',
           ':=', 'OR',
           '(', '+', 'OR', '-', ')', 'OR',
           '++', 'OR',
           '--'] 
   
    operators = {'(', ')', 'STAR', 'OR', 'PLUS'}

    # build RE and concats
    r = RegExp(exp, operators, star="STAR")
    mod_list = r.handle_exp()

    print_yellow(f"add concat {mod_list}")
        
    ## eval postfix expression for the AST
    post = r.get_postfix()

    print_red(check_postfix(post))

    ## I do not add # above to avoid some confusion
    post.append("#")
    post.append("CONCAT")
    print_yellow(f"postfix exp: {post}")

    ## now build AST
    tree = build_AST_tree(post,operators)
    
    ## get firstpos and lastpos and nullables (+, ? not yet)
    pre_followpos(tree)
    
    ## store in root the ids for leaves
    get_node_dict(tree)

    ## evaluate followpos for the DFA
    eval_followpos(tree)

    ## print tree to show
    tree.print_tree()

    ## get a dict for id: (name , followpos)
    DFA_dict = tree.get_DFA_dict()
    print_green(DFA_dict)

    ## prepare for building the DFA
    ## the firstpos of root is the first state in the DFA
    root_s = tree.firstpos
    print_blue(f"first of root:{root_s}")
    
    ## now, let's build our DFA
    dfa_table, accept_states = build_DFA(DFA_dict, root_s)

    
    #print_red(post)
    #print_blue(root_s)
    #print_yellow("DFA table is")
    #print_purple(dfa_table)
    print_purple(f"accept :{accept_states}")

    ## create your DFA machine
    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    
    ## now simulate your input with the DFA
    #input_list = "ccEccEcXcE"
    # digit + . digits ( \L | E digits )
    input_list = ['digit','digit','.','digits','E','digits']

    machine.simulate_dfa_2(input_list,[])
    
    ## get the accepted tokens to compare it later with each pattern
    accepted_tokens = machine.accepted_tokens
    print_yellow(f"{accepted_tokens}")
    #print(accepted_tokens[1][0])

def check_postfix(post_exp):
    if ("(" in post_exp) or (")" in post_exp):
        return False
    return True

def main():

    run_example_2()
    
    try:
        pass  

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()

