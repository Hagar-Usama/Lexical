from Scanner import Scanner, flatten_list, intersperse
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
from RegExp import RegExp, postfix_me
from Node_AST import build_AST_tree, eval_followpos, get_node_dict, pre_followpos
from State import DFA, build_DFA
from lexical_aux import build_my_tree, build_ouput_file, dfa_mine, eval_tree, get_current_directory
from lexical_aux import get_tokens_sole, reverse_dict, write_file, list_to_str


class Lexical:
    def __init__(self, operators={'(', ')', 'STAR', 'OR', 'PLUS','CONCAT'}):
        #self.lex_scan = scan
        #self.lex_path = lex_path
        #self.program_path = program_path
        self.operators = operators
        

    def run_scan(self):
        ## init scanner 
        lex_path = self.lex_path
        program_path = self.program_path

        lex_scan = Scanner(lex_path)
        lex_scan.analaze_lex()

        ## list the RD dict
        RD_list = lex_scan.get_RD_list()

        ## and OR in between
        RD_list = intersperse(RD_list,["OR"])
        
        flat_list = flatten_list(RD_list)
        self.flat_list = flat_list

        ## or keywords
        kw_exp = intersperse(lex_scan.keywords,"OR")

        ## or punctuations
        pn_exp = intersperse(lex_scan.punctuations,"OR")

        ## get postfix_exp of pn_kw
        pn_kw = lex_scan.postfix_keyword_punc()
        #print_red(pn_kw)

        ## read program file
        lex_scan.read_program_file(program_path)

        ## expand rd (subs re in rd)
        lex_scan.expand_rd(3)
        
        self.lex_scan = lex_scan


    def build_my_tree(self):

        exp = self.flat_list
        operators = self.operators

        #print_blue(self.flat_list)
        
        # build RE and concats
        r = RegExp(exp, operators, star="STAR")
        mod_list = r.handle_exp()

            
        ## eval postfix expression for the AST
        post = r.get_postfix()
        #print_red(post)


        ## I do not add # above to avoid some confusion
        post.append("#")
        post.append("CONCAT")
        #print_yellow(f"postfix exp: {post}")

        ## now build AST
        tree = build_AST_tree(post,operators)

        self.tree = tree
        return tree

    def expand_my_tree(self):

        ## tree, REs, pn_kw, operators
        tree = self.tree
        REs = self.lex_scan.RE
        pn_kw = self.lex_scan.postfix_keyword_punc()
        operators = self.operators
        
        ## add the REs !!
        REs = postfix_me(REs, operators)
        #print_red(REs)
        
        for term, exp in REs.items():
            tree.attach_node(term, exp)

        ## add keywords and punctuations
        tree.implant_node(tree, pn_kw)

        ## assign ids
        tree.assign_id()


    def eval_tree(self):
        
        tree = self.tree
        ## get firstpos and lastpos and nullables (+, ? not yet)
        pre_followpos(tree)
        
        ## store in root the ids for leaves
        get_node_dict(tree)

        ## evaluate followpos for the DFA
        eval_followpos(tree)

    def dfa_mine(self):
        tree = self.tree

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
        
        self.machine = machine
        return machine

    def get_tokens(self):


        machine = self.machine
        input_lists = self.lex_scan.program_list

        ac_tok = []
        for tok in input_lists:
            machine.accepted_tokens = []
            machine.simulate_dfa_2(tok,[])
            accepted_tokens = machine.accepted_tokens
            ac_tok = ac_tok + accepted_tokens

        self.ac_tok = ac_tok
        return ac_tok

    def dfa_stuff(self):
        self.build_my_tree()
        self.expand_my_tree()
        self.eval_tree()
        self.dfa_mine()
        ac_tok = self.get_tokens()

        return ac_tok




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
    print_yellow(symbol_table)
    output_path = cd + '/' + 'output1.txt'
    write_file(output_path, symbol_table)

    print_blue(list_to_str(accepted_tokens))
    lexeme_path = cd + '/' + 'lexemes.txt'
    write_file(lexeme_path, symbol_table)



    #for k,v in dfa_tab.items():
    #    print_blue(k)
        #print_yellow(v)
    #    for i in v:
    #        print(i,v[i])


    







if __name__ == "__main__":
    main()