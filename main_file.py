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

def build_my_tree(exp, operators):
    
    # build RE and concats
    print_yellow(f"operators: {operators}")
    r = RegExp(exp, operators, star="STAR")
    mod_list = r.handle_exp()
    print_green(mod_list)

        
    ## eval postfix expression for the AST
    post = r.get_postfix()


    ## I do not add # above to avoid some confusion
    post.append("#")
    post.append("CONCAT")
    print_yellow(f"postfix exp: {post}")

    ## now build AST
    tree = build_AST_tree(post,operators)

    return tree

def expand_my_tree(tree, REs, pn_kw, operators):
    ## add the REs !!
    REs = postfix_me(REs, operators)
    #print_red(REs)
    
    for term, exp in REs.items():
        tree.attach_node(term, exp)

    ## add keywords and punctuations
    tree.implant_node(tree, pn_kw)
    
    tree.assign_id()

def eval_tree(tree):
    ## get firstpos and lastpos and nullables (+, ? not yet)
    pre_followpos(tree)
    
    ## store in root the ids for leaves
    get_node_dict(tree)

    ## evaluate followpos for the DFA
    eval_followpos(tree)

def dfa_mine(tree):

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
    
    return machine

def get_tokens(machine, input_lists):
    ac_tok = []
    for tok in input_lists:
        machine.accepted_tokens = []
        machine.simulate_dfa_2(tok,[])
        accepted_tokens = machine.accepted_tokens
        ac_tok = ac_tok + accepted_tokens
    
    return ac_tok

def get_tokens_sole(machine, tok):
    ac_tok = []

    machine.accepted_tokens = []
    machine.simulate_dfa_2(tok,[])
    accepted_tokens = machine.accepted_tokens
    ac_tok = ac_tok + accepted_tokens

    if ac_tok:
        return True
    else:
        return False
    
    return True if ac_tok else False


def reverse_dict(the_dict):
    keys = list(the_dict.keys())
    keys.reverse()
    values = list(the_dict.values())
    values.reverse()
    new_dict = dict(zip(keys, values))

    return new_dict

def build_ouput_file(accepted_tokens, detection_table):

    symbol_table = []
    
    for i in accepted_tokens:
        str_d = detection_table[''.join(i)]
        symbol_table.append(str_d)
    return symbol_table

def write_file(path_file, output_list):

    with open(path_file, 'w') as filehandle:
        for listitem in output_list:
            filehandle.write('%s\n' % listitem)


def main():

    ## get directory for lexical file and program file
    cd = get_current_directory()
    lex_file = 'lexical3.txt'
    lex_path = cd + '/' +  lex_file
    program_path = cd + '/' + 'program3.txt'

    ## init scanner 
    lex_scan = Scanner(lex_path)
    lex_scan.analaze_lex()

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

    operators = {'(', ')', 'STAR', 'OR', 'PLUS', 'CONCAT'}
    tree = build_my_tree(flat_list, operators.copy())
    expand_my_tree(tree, lex_scan.RE , pn_kw, operators)
    eval_tree(tree)
    
    ## print tree to show
    tree.print_tree()

    machine = dfa_mine(tree)
    input_lists = lex_scan.program_list.copy()
    ac_tok = get_tokens(machine, input_lists)


    for j in ac_tok:
        print(''.join(j),end='\t')

    print_red(ac_tok)

    
    exp_rd_rev = reverse_dict(lex_scan.expanded_rd)
    accepted_tokens = ac_tok.copy()

    #print_blue(accepted_tokens)

    visited_tokens = set()
    detection_table = {}

    """
    for i in accepted_tokens:
        for j in lex_scan.keywords:
            if tuple(i) not in visited_tokens:
                if tuple(i) == tuple(j):
                    visited_tokens.append(tuple(i))
                    detection_table.append((i,tuple(j)))

        for key, val in exp_rd_rev.items():
            tree1 = build_my_tree(val,operators.copy())
            tree1.assign_id()
            eval_tree(tree1)
            m = dfa_mine(tree1)

            if tuple(i) not in visited_tokens:
               c =  get_tokens_sole(m, i.copy())
               if c:
                   visited_tokens.append(tuple(i))
                   detection_table.append((key,tuple(i)))

    """

    """  
    for i in lex_scan.keywords:
        for j in accepted_tokens:
            if tuple(j) not in visited_tokens:
                if tuple(i) == tuple(j):
                    visited_tokens.add(tuple(j))
                    #detection_table.append((i, ''.join(j)))
                    detection_table[''.join(j)] = i
                    print_green(f"{''.join(j)}, {i}")
    """
    print_blue(lex_scan.keywords)
    for k in accepted_tokens:
        k_str = ''.join(k)
        if k_str in lex_scan.keywords:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    for k in accepted_tokens:
        k_str = ''.join(k)
        print_purple(f"tok is ")
        if k_str in lex_scan.punctuations:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    """ 
    for i in lex_scan.punctuations:
        for j in accepted_tokens:
            if tuple(j) not in visited_tokens:
                if tuple(i) == tuple(j):
                    visited_tokens.add(tuple(j))
                    #detection_table.append((i, ''.join(j)))
                    detection_table[''.join(j)] = i
                    print_green(f"{''.join(j)}, {i}")

    """
    for key, val in exp_rd_rev.items():

        #print_green(val)
        tree1 = build_my_tree(val,operators.copy())
        tree1.assign_id()
        eval_tree(tree1)
        m = dfa_mine(tree1)
        # tree1.print_tree()

       
        acc_tokens = []
        for j in accepted_tokens:
            #print_green(f"j of inpj")
           print_red(f"j is {j}")
           if tuple(j) not in visited_tokens:
               c =  get_tokens_sole(m, j.copy())
               if c:
                   visited_tokens.add(tuple(j))
                   #detection_table.append((key, ''.join(j)))
                   detection_table[''.join(j)] = key
                   print_green(f"{''.join(j)}, {key}")
    
           #print(f"c is {c}, <{j}>",end='   ')
           
    """     if c:
               print_yellow(f"*.* accepted: {j}, {exp_rd_rev[key]} *.*") 
    """
           #print("*")

        
    
    for key, value in detection_table.items():
        print_green(f"{key} , {value}")

    symbol_table = build_ouput_file(accepted_tokens, detection_table)
    print_yellow(symbol_table)
    output_path = cd + '/' + 'output3.txt'
    write_file(output_path, symbol_table)


if __name__ == "__main__":
    main()