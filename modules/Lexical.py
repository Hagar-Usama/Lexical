from modules.Scanner import Scanner, flatten_list, intersperse
from modules.color_print import print_blue, print_green, print_purple, print_red, print_yellow, print_dark_cyan
from modules.color_print import ANSI_RED, ANSI_RESET
from modules.RegExp import RegExp, postfix_me
from modules.Node_AST import Operator, build_AST_tree, eval_followpos, get_node_dict, pre_followpos
from modules.State import DFA, build_DFA
from modules.lexical_aux import build_my_tree, build_ouput_file, dfa_mine, eval_tree, get_current_directory
from modules.lexical_aux import get_start_accept, get_table_dict, get_tokens_sole, list_to_str, print_dfa_trans, reverse_dict, write_file
from itertools import chain


class Lexical:
    def __init__(self, operators={'(', ')', 'STAR', 'OR', 'PLUS', 'CONCAT'}):
        self.operators = operators

    def run_scan(self):
        # init scanner
        lex_path = self.lex_path
        program_path = self.program_path

        lex_scan = Scanner(lex_path)
        lex_scan.analaze_lex()

        # list the RD dict
        RD_list = lex_scan.get_RD_list()

        # and OR in between
        RD_list = intersperse(RD_list, ["OR"])

        flat_list = flatten_list(RD_list)
        self.flat_list = flat_list

        # or keywords
        kw_exp = intersperse(lex_scan.keywords, "OR")

        # or punctuations
        pn_exp = intersperse(lex_scan.punctuations, "OR")

        # ored key-pn:
        kw_pn = lex_scan.keywords.union(lex_scan.punctuations)
        kw_pn = intersperse(kw_pn, "OR")

        #######################
        # get_new_kn_pn
        #######################
        new_kw_pn = list(chain.from_iterable(
            ["lbracket"] if item == '(' else [item] for item in kw_pn))
        new_kw_pn = list(chain.from_iterable(["rbracket"] if item == ')' else [
                         item] for item in new_kw_pn))
        new_op = {"lbracket", "rbracket", "OR"}
        new_kw_pn = list(chain.from_iterable(
            list(item) if item not in new_op else [item] for item in new_kw_pn))

        kp_r = RegExp(new_kw_pn, {"OR"})
        kp_r.handle_exp()

        # postfix keyword-punctuations to add
        kp_post = kp_r.get_postfix()
        # now replace lbracket and rbracket with ( and )
        kp_post = list(chain.from_iterable(
            ['('] if item == 'lbracket' else [item] for item in kp_post))
        kp_post = list(chain.from_iterable([')'] if item == 'rbracket' else [
                       item] for item in kp_post))

        self.kp_post = kp_post

        # read program file
        lex_scan.read_program_file(program_path)

        # expand rd (subs re in rd)
        lex_scan.expand_rd(3)

        self.lex_scan = lex_scan

    def build_my_tree(self):

        exp = self.flat_list
        operators = self.operators
        # build RE and concats
        r = RegExp(exp, operators, star="STAR")
        r.handle_exp()

        # eval postfix expression for the AST
        post = r.get_postfix()

        # I do not add # above to avoid some confusion
        post.append("#")
        post.append(Operator.CONCAT)

        # now build AST
        tree = build_AST_tree(post, operators)

        self.tree = tree
        return tree

    def expand_my_tree(self):

        ## tree, REs, pn_kw, operators
        tree = self.tree
        REs = self.lex_scan.RE
        operators = self.operators

        # add the REs !!
        REs = postfix_me(REs, operators)

        for term, exp in REs.items():
            tree.attach_node(term, exp)

        # add keywords and punctuations
        tree.implant_node(tree, self.kp_post)

        # assign ids
        tree.assign_id()

    def eval_tree(self):

        tree = self.tree
        # get firstpos and lastpos and nullables (+, ? not yet)
        pre_followpos(tree)

        # store in root the ids for leaves
        get_node_dict(tree)

        # evaluate followpos for the DFA
        eval_followpos(tree)

    def dfa_mine(self):
        tree = self.tree

        # get a dict for id: (name , followpos)
        DFA_dict = tree.get_DFA_dict()
        # print_green(DFA_dict)

        # prepare for building the DFA
        # the firstpos of root is the first state in the DFA
        root_s = tree.firstpos
        self.start_state = root_s

        # now, let's build our DFA
        dfa_table, accept_states = build_DFA(DFA_dict, root_s)
        self.accept_states = accept_states

        # create your DFA machine
        machine = DFA(dfa_table, accept_states, frozenset(root_s))

        self.machine = machine
        return machine

    def get_tokens(self):

        machine = self.machine
        input_lists = self.lex_scan.program_list

        ac_tok = []
        for tok in input_lists:
            machine.accepted_tokens = []
            machine.simulate_dfa_2(tok, [])
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
