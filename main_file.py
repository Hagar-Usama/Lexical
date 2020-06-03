from RegExp import RegExp, postfix_me
from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
from State import dfa_aux, build_DFA, DFA
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
import os
import re
from Scanner import Scanner, flatten_list, intersperse


def get_current_directory(): 
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path


def main():

    ## get directory for lexical file and program file
    cd = get_current_directory()
    lex_file = 'lexical3.txt'
    lex_path = cd + '/' +  lex_file
    program_path = cd + '/' + 'program3.txt'

    ## init scanner 
    lex_scan = Scanner(lex_path)
    lex_scan.analaze_lex()

    # print_red(lex_scan.RE)
    
    ## print RD, RE dicts, punctuations, and keywords
    #for key, value in lex_scan.RD.items():
    #    print_yellow(f"{key}=>{value}")

    #for key, value in lex_scan.RE.items():
    #    print_green(f"{key}=>{value}")

    #print_blue(lex_scan.punctuations)
    #print_purple(lex_scan.keywords)

    ## list the RD dict
    RD_list = lex_scan.get_RD_list()

    ## and OR in between
    RD_list = intersperse(RD_list,["OR"])
    #print(flatten_list(RD_list))

    # this list contains all RDs ored
    ## flatten list or RD_list 
    flat_list = flatten_list(RD_list)

    ## or keywords
    kw_exp = intersperse(lex_scan.keywords,"OR")
    #print_purple(kw_exp)

    ## or punctuations
    pn_exp = intersperse(lex_scan.punctuations,"OR")
    #print_blue(pn_exp)

    #print(flat_list)

    ## get postfix_exp of pn_kw
    pn_kw = lex_scan.postfix_keyword_punc()
    print_red(pn_kw)

    ## read program file
    lex_scan.read_program_file(program_path)

    ## expand rd (subs re in rd)
    lex_scan.expand_rd(3)
    print_green(lex_scan.expanded_rd)
    

    #######################
    # now lets build AST 
    #######################

    operators = {'(', ')', 'STAR', 'OR', 'PLUS'}

    # build RE and concats

    exp = flat_list

    r = RegExp(exp, operators, star="STAR")
    mod_list = r.handle_exp()

        
    ## eval postfix expression for the AST
    post = r.get_postfix()


    ## I do not add # above to avoid some confusion
    post.append("#")
    post.append("CONCAT")
    print_yellow(f"postfix exp: {post}")

    ## now build AST
    tree = build_AST_tree(post,operators)
    
    ## add the REs !!
    REs = lex_scan.RE
    REs = postfix_me(REs, operators)
    print_red(REs)
    
     
    for term, exp in REs.items():
        tree.attach_node(term, exp)

    ## add keywords and punctuations
    tree.implant_node(tree, pn_kw)
    
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
    #print_green(DFA_dict)

    ## prepare for building the DFA
    ## the firstpos of root is the first state in the DFA
    root_s = tree.firstpos
    #print_blue(f"first of root:{root_s}")
    
    ## now, let's build our DFA
    dfa_table, accept_states = build_DFA(DFA_dict, root_s)

    
    ## create your DFA machine
    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    
    input_lists = lex_scan.program_list

    ac_tok = []
    for tok in input_lists:
        machine.accepted_tokens = []
        machine.simulate_dfa_2(tok,[])
        accepted_tokens = machine.accepted_tokens
        ac_tok = ac_tok + accepted_tokens

    for j in ac_tok:
        print(''.join(j),end='\t')


if __name__ == "__main__":
    main()