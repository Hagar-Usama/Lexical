
import pytest
from RegExp import RegExp, postfix_me
from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
from State import dfa_aux, build_DFA, DFA
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
import time
import copy 

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

    REs = {
        'digits': ['digit', 'PLUS'],
        'digit': ['0', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', 'OR'],
        'letter': ['a', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j', 'OR',
        'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't', 'OR', 'u',
        'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', 'OR', 'A', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR', 'F',
        'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J', 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR',
        'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U', 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', 'OR', 'OR']
        }

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


def run_example_3():
    """
    attach re nodes
    """
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

    REs = {
        'digits': ['digit', 'PLUS'],
        'digit': ['0', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', 'OR'],
        'letter': ['a', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j', 'OR',
        'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't', 'OR', 'u',
        'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', 'OR', 'A', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR', 'F',
        'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J', 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR',
        'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U', 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', 'OR', 'OR']
        }



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

    #found = tree.find_key("digits")
    #tree.print_tree()
    #branch = build_AST_tree(RE_, operators)
    #branch = found[0]
    #branch.parent.print_tree()

    ##########################
    ## trying to attach nodes
    ##########################

    """     
    for i in found:

        parent = i.parent
        lefty = i.isLeft()
        i.parent = None
        del i

        if lefty:
            parent.left = copy.deepcopy(branch)
        else:
            parent.right = copy.deepcopy(branch)

    parent.print_tree()
    """
    #for i in range(len(found)):
        #found[i].name = branch.name
        #parent = found[i].parent
        #found[i].name = branch.parent
        #found[i].left = branch.left
        #found[i].right = branch.right
        #found[i].id = 0
        #print_yellow(found[i])
        #found[i] = copy.copy(branch)
        #print_blue(found[i].name)
        #print_yellow(found[i])
        

    tree.assign_id()
    tree.print_tree()
    #print_green(found)


    
    ## get firstpos and lastpos and nullables (+, ? not yet)
    #pre_followpos(tree)
    
    ## store in root the ids for leaves
    #get_node_dict(tree)

    ## evaluate followpos for the DFA
    #eval_followpos(tree)

    ## print tree to show
    #tree.print_tree()

    ## get a dict for id: (name , followpos)
    #DFA_dict = tree.get_DFA_dict()
    #print_green(DFA_dict)

    ## prepare for building the DFA
    ## the firstpos of root is the first state in the DFA
    #root_s = tree.firstpos
    #print_blue(f"first of root:{root_s}")
    
    ## now, let's build our DFA
    #dfa_table, accept_states = build_DFA(DFA_dict, root_s)

    
    #print_red(post)
    #print_blue(root_s)
    #print_yellow("DFA table is")
    #print_purple(dfa_table)
    #print_purple(f"accept :{accept_states}")

    ## create your DFA machine
    #machine = DFA(dfa_table, accept_states, frozenset(root_s))
    
    ## now simulate your input with the DFA
    #input_list = "ccEccEcXcE"
    # digit + . digits ( \L | E digits )
    #input_list = ['digit','digit','.','digits','E','digits']
    # digit + . digits ( \L | E digits )
    #input_list = ['digit','digit', '.', 'digit','digit']

    #machine.simulate_dfa_2(input_list,[])
    
    ## get the accepted tokens to compare it later with each pattern
    #accepted_tokens = machine.accepted_tokens
    #print_yellow(f"{accepted_tokens}")

def run_example_4():
    """
    attach re nodes
    """
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

    REs = {
        'digits': ['digit', 'PLUS'],
        'digit': ['0', '1', 'OR', '2', 'OR', '3', 'OR', '4', 'OR', '5', 'OR', '6', 'OR', '7', 'OR', '8', 'OR', '9', 'OR'],
        'letter': ['a', 'b', 'OR', 'c', 'OR', 'd', 'OR', 'e', 'OR', 'f', 'OR', 'g', 'OR', 'h', 'OR', 'i', 'OR', 'j', 'OR',
        'k', 'OR', 'l', 'OR', 'm', 'OR', 'n', 'OR', 'o', 'OR', 'p', 'OR', 'q', 'OR', 'r', 'OR', 's', 'OR', 't', 'OR', 'u',
        'OR', 'v', 'OR', 'w', 'OR', 'x', 'OR', 'y', 'OR', 'z', 'OR', 'A', 'B', 'OR', 'C', 'OR', 'D', 'OR', 'E', 'OR', 'F',
        'OR', 'G', 'OR', 'H', 'OR', 'I', 'OR', 'J', 'OR', 'K', 'OR', 'L', 'OR', 'M', 'OR', 'N', 'OR', 'O', 'OR', 'P', 'OR',
        'Q', 'OR', 'R', 'OR', 'S', 'OR', 'T', 'OR', 'U', 'OR', 'V', 'OR', 'W', 'OR', 'X', 'OR', 'Y', 'OR', 'Z', 'OR', 'OR']
        }
 

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

    t = tree.left.left.left.left.left
    print_blue(t.get_root())
    print_blue(tree)
    ## add the REs !!
    for term, exp in REs.items():
        tree.attach_node(term, exp)

    ## add keywords and punctuations
    key_pun = ['(', 'do', 'OR', 'integer', 'OR', ';', 'OR', ':', 'OR', 'end',
               'OR', '.', 'OR', 'program', 'OR', 'while', 'OR', 'then', 'OR',
               'if', 'OR', 'var', 'OR', 'begin', 'OR', 'read', 'OR', ')', 'OR',
               'else', 'OR', ',', 'OR', 'write', 'OR', 'real', 'OR']

    tree.implant_node(tree, key_pun)


        

    tree.assign_id()
    tree.print_tree()
    

    
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
    #print_purple(f"accept :{accept_states}")

    ## create your DFA machine
    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    
    ## now simulate your input with the DFA
    #input_list = "ccEccEcXcE"
    # digit + . digits ( \L | E digits )
    #input_list = ['digit','digit','.','digits','E','digits']
    # digit + . digits ( \L | E digits )
    #input_list = ['digit','digit', '.', 'digit','digit']
    input_list = "program example;"
    input_list = list(input_list)


    machine.simulate_dfa_2(input_list,[])
    
    ## get the accepted tokens to compare it later with each pattern
    accepted_tokens = machine.accepted_tokens
    print_yellow(f"{accepted_tokens}")


def check_postfix(post_exp):
    if ("(" in post_exp) or (")" in post_exp):
        return False
    return True

def main():

    run_example_4()
    
    try:
        pass  

    except AssertionError as e:
        print("Test case failed:\n", str(e))
        exit(-1)


if __name__ == "__main__":
    main()

