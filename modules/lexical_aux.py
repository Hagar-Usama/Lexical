import os
from helpers.RegExp import RegExp, postfix_me
from helpers.Node_AST import build_AST_tree, eval_followpos, get_node_dict, pre_followpos
from helpers.State import DFA, build_DFA
from helpers.color_print import print_yellow


def get_current_directory(): 
    #current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.getcwd() 
    return path
    
def write_file(path_file, output_list):

    os.makedirs(os.path.dirname(path_file), exist_ok=True)
    with open(path_file, 'w+') as filehandle:
        for listitem in output_list:
            filehandle.write('%s\n' % listitem)

def build_my_tree(exp, operators):
    
    # build RE and concats
    #print_yellow(f"operators: {operators}")
    r = RegExp(exp, operators, star="STAR")
    mod_list = r.handle_exp()
    #print_green(mod_list)

        
    ## eval postfix expression for the AST
    post = r.get_postfix()


    ## I do not add # above to avoid some confusion
    post.append("#")
    post.append("CONCAT")
    #print_yellow(f"postfix exp: {post}")

    ## now build AST
    tree = build_AST_tree(post,operators)

    return tree

def reverse_dict(the_dict):
    keys = list(the_dict.keys())
    keys.reverse()
    values = list(the_dict.values())
    values.reverse()
    new_dict = dict(zip(keys, values))

    return new_dict

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
    ## get firstpos and lastpos and nullables
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

def build_ouput_file(accepted_tokens, detection_table):

    symbol_table = []
    
    for i in accepted_tokens:
        str_d = detection_table[''.join(i)]
        symbol_table.append(str_d)
    return symbol_table

def get_tokens_sole(machine, tok):
    ac_tok = []
    token_temp = tok.copy()
    machine.accepted_tokens = []
    machine.simulate_dfa_2(tok,[])
    accepted_tokens = machine.accepted_tokens
    ac_tok = ac_tok + accepted_tokens

    #print_red(f"toks are: {token_temp}, {ac_tok}")
    ac_tok2 = [''.join(x) for x in ac_tok]
    ac_tok2 = ''.join(ac_tok2)
    token_temp2 = ''.join(token_temp)

    #print_green(f"ac_tok {ac_tok2}, {token_temp2}")
    if ac_tok2 == token_temp2:       
        return True
    return False


def list_to_str(the_list):
    new_list = []

    for i in the_list:
        new_list.append(''.join(i))

    return new_list

######################################
## consider adding to Lexical Class ##
######################################

def get_table_dict(dfa_tab):
    """
    takes dfa table and returns dict of unique names for states
    """
    identifier = 0
    table_dict = {}

    for i in dfa_tab:
        table_dict[i] = 's' + str(identifier)
        identifier +=1

    return table_dict

def print_dfa_trans(dfa_tab, table_dict):

    for k,v in dfa_tab.items():
        #print_yellow(table_dict[k])
        d = table_dict.get(k)
        if d:
            #print_yellow(f"\n{d}")
            pass
        else:
            #print_yellow('\ns' + str(len(dfa_tab)))
            d = 's' + str(len(dfa_tab))

        print_yellow(f"\n{d}")

        for key, value in v.items():
            #print(key, end="->")
            #print_blue(table_dict.get(value))
            d = table_dict.get(value)
            if d:
                #print(d + " | ", end ="\t")
                pass
            else:
                #print('s' + str(len(dfa_tab)) +  " | " , end ="\t")
                d = 's' + str(len(dfa_tab))
            t = (key, d)

            print(t,end = '\t')

    print("")

def get_start_accept(start_state, accept_states, table_dict):
    """ returns start and accept states with unique names """
    s = table_dict.get(start_state)
    accept = set()

    for i in accept_states:
        a = table_dict.get(i)
        #print_blue(a)
        if a:
            accept.add(a)
    return s, accept


def get_arg(param_index, default=None):
    """
        Gets a command line argument by index (note: index starts from 1)
        If the argument is not supplies, it tries to use a default value.

        If a default value isn't supplied, an error message is printed
        and terminates the program.
    """
    try:
        return sys.argv[param_index]
    except IndexError as e:
        if default:
            return default
        else:
            print(e)
            print(
                f"[FATAL] The comand-line argument #[{param_index}] is missing")
            exit(-1)    # Program execution failed.




