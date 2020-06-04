from Scanner import Scanner, flatten_list, intersperse
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
import os
from RegExp import RegExp, postfix_me
from Node_AST import build_AST_tree, eval_followpos, get_node_dict, pre_followpos
from State import DFA, build_DFA


def get_current_directory(): 
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path
    

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
        #print(flatten_list(RD_list))

        # this list contains all RDs ored
        ## flatten list or RD_list 
        flat_list = flatten_list(RD_list)
        self.flat_list = flat_list

        ## or keywords
        kw_exp = intersperse(lex_scan.keywords,"OR")
        #print_purple(kw_exp)

        ## or punctuations
        pn_exp = intersperse(lex_scan.punctuations,"OR")
        #print_blue(pn_exp)

        #print(flat_list)

        ## get postfix_exp of pn_kw
        pn_kw = lex_scan.postfix_keyword_punc()
        #print_red(pn_kw)

        ## read program file
        lex_scan.read_program_file(program_path)

        ## expand rd (subs re in rd)
        lex_scan.expand_rd(3)
        #print_green(lex_scan.expanded_rd)
        
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
        print_red(post)


        ## I do not add # above to avoid some confusion
        post.append("#")
        post.append("CONCAT")
        print_yellow(f"postfix exp: {post}")

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
    lex_file = 'lexical3.txt'
    lex_path = cd + '/' +  lex_file
    program_path = cd + '/' + 'program3.txt'

    ## build full dfa
    lx = Lexical()
    lx.lex_path = lex_path
    lx.program_path = program_path
    lx.run_scan()
    ac_tok = lx.dfa_stuff()

    for j in ac_tok:
        print(''.join(j),end='\t')

    print_yellow("RDs are")
    print_blue(lx.lex_scan.expanded_rd)

    DFAs = {}

    
    for key, val in lx.lex_scan.expanded_rd.items():
        print_green(val)
        #lex = Lexical()
        #lex.flat_list = val       
        #lex.build_my_tree()
        #lex.eval_tree()
        #lex.dfa_mine()

        #DFAs[key] = lex





if __name__ == "__main__":
    main()