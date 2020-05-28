from RegExp import RegExp
from Node_AST import Node_AST, build_AST_tree, print_tree, pre_followpos, get_node_dict, eval_followpos
from State import dfa_aux, build_DFA, DFA
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
import os
import re


def get_current_directory(): 
    current_path = os.path.dirname(os.path.abspath(__file__))
    return current_path


def run_example():


    # first add rd expersion
    exp = ["c","|","c","E","c"]
    rd = "program|var|integer|real|begin|end|if|else|then|while|do|read|write|:|;|,|.|\\"
    exp = list(rd)

    operators = {'(', ')', '*', '|'}

    # build RE and concats
    r = RegExp(exp, operators, star="*")
    mod_list = r.handle_exp()

    print_yellow(f"add concat {mod_list}")
        
    # actually those two lines are useless
    r.operators.add("concat")
    operators = {'(', ')', '*', '|','concat'}

    # eval postfix expression for the AST
    post = r.get_postfix()
    # I do not add # above to avoid some confusion
    post.append("#")
    post.append("concat")
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
    #print_green(dfa_table)
    #print_purple(accept_states)

    # create your DFA machine
    machine = DFA(dfa_table, accept_states, frozenset(root_s))
    # now simulate your input with the DFA
    input_list = "begin;endread\else"

    machine.simulate_dfa_2(input_list,[])
    # get the accepted tokens to compare it later with each pattern
    accepted_tokens = machine.accepted_tokens
    print_yellow(f"{accepted_tokens}")
    print(accepted_tokens[1][0])

def sort_file(input_list):
    """ 
    sort it to RE, RD, Keywords and Punctuations
    """
    punctuations = []
    keywords = []
    RDs = []
    REs = []

    
    for i in input_list:
        
        if i.strip().startswith("{"):
            keywords.append(i.strip())

            #print("Keywords")
        elif i.strip().startswith("["):
            #print("Punctuations")
            punctuations.append(i.strip())
        else:
            x = re.search(r"[a-zA-Z]+[0-9]*:", i.strip())
            if x:
                RDs.append(i.strip())
                #print(f"RD {i.strip()}")
            else:
                x = re.search(r"[a-zA-Z]+[0-9]* =", i.strip())
                if x:
                    REs.append(i.strip())
                    #print(f"RE {i.strip()}")

    return punctuations, keywords, REs, RDs

def handle_lexical(input_list):

    """
    handles lexical inputs

    returns Punctuation set
           Keywords set
           REs dict
           RDs dict
   
    """
    p,k,re,rd = sort_file(input_list)

    RDs = {}
    REs = {}
    pn = set()
    kw = set()

    for i in p:
        pn.update(handle_punctuations(i))

    for i in k:
        kw.update(handle_keyword(i))

    for i in rd:
        r = handle_rd(i)
        #print_blue(f"r= {r}")
        RDs[r[0]] = r[1]
        #print_purple(handle_rd(i))
    for i in re:
        r = handle_re(i)
        #print_green(f"r= {r}")
        REs[r[0]] = r[1]
        #print_purple(handle_re(i))


    #for i in REs:
    #    print_yellow(f"{i}={REs[i]}")

    #for i in RDs:
    #    print_green(f"{i}:{RDs[i]}")

    print_purple(pn)
    print_blue(kw)

    return pn, kw, REs, RDs


def handle_range(rules):


    for i in rules:
        #print(i)
        x = re.search(r"([a-zA-Z]+[0-9])+-([a-zA-Z]+[0-9])+", i)

        if x:
            x = x.split('-')
            print_red(f"range: {x[0]} - {x[1]}")

        if i == "a-z":

            range_s = 'a'
            range_e = 'z'
            y = range_s

            for j in range(ord(range_s)+1, ord(range_e)):
                y += " OR " + chr(j)

            print(y)

def generate_equivalent_range(str_input):

    "generate ranges in ReExp"

    if str_input == "a-z":
        
        range_s = 'a'
        range_e = 'z'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 
            
    elif str_input == "A-Z":
        
        range_s = 'A'
        range_e = 'Z'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 

    elif str_input == "0-9":

        range_s = '0'
        range_e = '9'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 

    return y



    
def list_rules(RE, RD):

    """
    make REs & RDs as lists

    ex:
    L = x | l --> ['x','|', 'l']

    return modified RE and RD
    
    """

    for key, value in RE.items():
        RE[key] = value.split(" ")

    for key, value in RD.items():
        RD[key] = value.split(" ")

    #for i in RE:
    #    print_yellow(f"{i}={RE[i]}")

    #for i in RD:
    #    print_green(f"{i}:{RD[i]}")
    
    return RE, RD


def handle_keyword(input_list):
    
    input_list = input_list.replace("{",'')
    input_list = input_list.replace("}",'')
    input_list = input_list.split(" ")
    input_list = [i.strip() for i in input_list]

    return set(input_list)

def handle_punctuations(input_list):
    input_list = input_list.replace("[",'')
    input_list = input_list.replace("]",'')
    input_list = input_list.split(" ")
    input_list = [i.strip() for i in input_list]

    return set(input_list)

def handle_rd(input_list):
    input_list = input_list.strip(" ")
    input_list = input_list.split(":", 1)

    input_list = [i.strip() for i in input_list]
    
    return input_list
    
def handle_re(input_list):
    input_list = input_list.strip(" ")
    input_list = input_list.split("=", 1)
    input_list = [i.strip() for i in input_list]

    return input_list
    

def main():
    # get the directory of the lexical file
    lx = get_current_directory()
    output_file = 'lexical.txt'
    input_path = lx + '/' +  output_file


    # read lexical file as a whole
    file = open(input_path)
    line = file.read().replace("\n", "\n")
    file.close()
    line = line.strip()

    # handle file
    line = line.replace("\\L", '𝛆')
    line = line.replace("\+", 'plusop')
    line = line.replace("\*", 'mulop')

    line = line.replace("+", 'PLUS')
    line = line.replace("*", 'STAR')
    line = line.replace("|", 'OR')

    line = line.replace("plusop", '+')
    line = line.replace("mulop", '*')

    line = line.replace("\\", '')
    #print_yellow(line)

    
    line = line.replace('a-z',"( " + generate_equivalent_range("a-z") + " )")
    line = line.replace('A-Z',"( " + generate_equivalent_range("A-Z") + " )")
    line = line.replace('0-9',"( " + generate_equivalent_range("0-9") + " )")
    lex_list = line.split('\n')
    
    
    # split lexical as punctuations, keywords, REs and RD
    _,_,RE,RD = handle_lexical(lex_list)

    # continue hanlding RE and RD to fully list
    RE, RD = list_rules(RE,RD)

    print(RE)
    
    for key, value in RE.items():
        print_yellow(f"{key}==>{value}")

    for key, value in RD.items():
        print_green(f"{key}==>{value}")

   


if __name__ == "__main__":
    main()

