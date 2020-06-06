from modules.lexical_aux import build_my_tree, build_ouput_file, dfa_mine, eval_tree, get_current_directory, get_start_accept, get_table_dict, get_tokens_sole, list_to_str, print_dfa_trans, reverse_dict, write_file
from modules.Lexical import Lexical
from modules.color_print import print_blue, print_yellow


def main():

    ## get directory for lexical and program
    cd = get_current_directory()
    lex_file = 'lexical1.txt'
    lex_path = cd + '/' +  lex_file
    program_path = cd + '/' + 'program1.txt'

    ## build full dfa
    lx = Lexical()
    lx.lex_path = lex_path
    lx.program_path = program_path
    lx.run_scan()
    
    
    ac_tok = lx.dfa_stuff()

    for j in ac_tok:
        print(''.join(j),end='\t')

    dfa_tab = lx.machine.dfa_table

    print(len(dfa_tab))
    print("*"*20)
    
    ######################
    ## build symbol table
    ######################

    operators={'(', ')', 'STAR', 'OR', 'PLUS','CONCAT'}

     
    exp_rd_rev = reverse_dict(lx.lex_scan.expanded_rd)
    exp_rd_rev = lx.lex_scan.expanded_rd
    accepted_tokens = ac_tok.copy()

    visited_tokens = set()
    detection_table = {}

  
    #print_blue(lx.lex_scan.keywords)
    for k in accepted_tokens:
        k_str = ''.join(k)
        if k_str in lx.lex_scan.keywords:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    for k in accepted_tokens:
        k_str = ''.join(k)
        if k_str in lx.lex_scan.punctuations:
            visited_tokens.add(tuple(k))
            detection_table[k_str] = k_str

    for key, val in exp_rd_rev.items():

        tree1 = build_my_tree(val,operators.copy())
        tree1.assign_id()
        eval_tree(tree1)
        m = dfa_mine(tree1)
        # tree1.print_tree()

       
        acc_tokens = []
        for j in accepted_tokens:
           if tuple(j) not in visited_tokens:
               c =  get_tokens_sole(m, j.copy())
               if c:
                   visited_tokens.add(tuple(j))
                   detection_table[''.join(j)] = key
    
    
    symbol_table = build_ouput_file(accepted_tokens, detection_table)
    print("")
    
    print_blue(list_to_str(accepted_tokens))
    lexeme_path = cd + '/' + 'lexemes.txt'
    write_file(lexeme_path, list_to_str(accepted_tokens))



    #print(len(dfa_tab))
    print("*"*20)

    print("*.*. Stream of Tokens .*.*")
    print_yellow(symbol_table)
    output_path = cd + '/' + 'tokens.txt'
    quote_tokens = []

    for i in symbol_table:
        quote_tokens.append("'" + str(i) + "'")


    write_file(output_path, quote_tokens)

    
    table_dict = get_table_dict(frozenset(dfa_tab))
    #print_dark_cyan(table_dict)

    print("\n*.*. Transition Table .*.*")
    print_dfa_trans(dfa_tab, table_dict)
    start, accept = get_start_accept(frozenset(lx.start_state), lx.accept_states, table_dict)
    print_yellow(f"Start State: {start}")
    print_yellow(f"Accept States: {accept}\n")
    
    







if __name__ == "__main__":
    main()