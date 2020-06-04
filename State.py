import collections
from color_print import print_blue, print_green, print_purple, print_red, print_yellow
import time

class State:
    def __init__(self):
        self.visited = False


class DFA:
    def __init__(self, dfa_table, accept_states, init_state):
        self.dfa_table = dfa_table
        self.accept_states = accept_states
        self.init_state = init_state
        self.accepted_tokens = []
        self.input_list = []

    def simulate_dfa_2(self, input_list, prev_list):

        """
            simulates a correct input and divides it into tokens
            it is recursive, stops when erroneous input

        """

        if isinstance(input_list, str):
            input_list = list(input_list)
        

        DEAD_STATE  = 0
        #print_blue("enter simulation")

        tokens = []
        tokens_accept = []
        
        
        s = self.init_state

        if (input_list) and ( len(input_list) != len(prev_list)):
            
            prev_list = input_list.copy()
        
            while input_list:
                tok = input_list.pop(0)
                #print_green(f"token is {tok}")

                tokens.append(tok)

                s = self.get_next_state(s, tok)

                #print_green(f"next state is: {s}")
                
                if s != DEAD_STATE:
                    if self.is_accepted(s):
                        tokens_accept.append(tokens.copy())
                        #print('accept')
                
                else:
                    #print("Dead state")
                    tokens = []
                    input_list.insert(0,tok)
                    
                    self.simulate_dfa_2(input_list, prev_list)
                    
                    break

            if tokens_accept:
                self.accepted_tokens.insert(0,tokens_accept[-1])



    def simulate_dfa(self, input_list):
        
        if isinstance(input_list , str):
            input_list = list(input_list)

        DEAD_STATE  = 0
        #print_blue("enter simulation")

        tokens = []
        tokens_accept = []
        
        s = self.init_state
        for i in input_list:

            #print_green(f"i is {i}")
            tokens.append(i)
            print_green(tokens)

            s = self.get_next_state(s,i)
            #print_green(f"next state is: {s}")
            if s != DEAD_STATE:
                if self.is_accepted(s):
                    tokens_accept.append(tokens.copy())
                    #tokens = []
                    print('accept')
                    #return 'accept'
               
            else:
                tokens = []
                if tokens_accept:
                    self.accepted_tokens.append(tokens_accept[-1])
                tokens_accept = []




                #print("Dead state")

        #print(tokens_accept)
        """ 
        if tokens_accept:
            print_purple(tokens_accept)
            return tokens_accept[-1]
        else:
            return []
        """
            
    def is_accepted(self, state):
        return state in self.accept_states

    def get_next_state(self, current_state, input_token):
        #a_dict.get('missing_key', 'default value')
        x = self.dfa_table.get(current_state,0)
        if x:
            return x.get(input_token, 0)
        return x




def build_DFA(DFA_dict, init_state):
    

    print_yellow(DFA_dict)
    visited = set()
    #istate = frozenset(init_state)
    istate = init_state
    state_list = [istate]
    accept_cond = get_accept_condition(DFA_dict)
    accept_states = set()
    trans = {}
    dfa_table = collections.defaultdict(dict)

    
    print("*.*"*12)
    while state_list:

        print(f"state_list: {state_list}")
        print_green(f"visited: {visited}")        
        state = state_list.pop(0)
        print_blue(f"current state is {state}")
        state_trans = set()
        
        visited.add(frozenset(state))
       
        
        ip_dict = dfa_aux(DFA_dict, state)
        print_purple(f"ip_dict is: {ip_dict}")
        # time.sleep(1)
        for i in ip_dict:
            if i != '#':
                to_state = set()

                # set for each character
                for j in ip_dict[i]:
                    # get its follow and update the set
                    #print_green(f"j is {j}")
                    print_yellow(f"follow of j{DFA_dict[j][1]}")
                    to_state.update(DFA_dict[j][1])
                    #to_state.update({"*"})

                # check if it is an accept state   
                if accept_cond in to_state:
                    print_red(f"it accept {to_state}")
                    accept_states.add(frozenset(to_state))

                    
                print(f"DFA[{state}][{i}] = {to_state}")

                dfa_table[frozenset(state)][i] = frozenset(to_state)


                if (to_state not in state_list) and (to_state not in visited):
                    state_list.append(to_state)

            else:
                print("#")

        print("*.*"*12)

    print(dfa_table)

    for key in dfa_table:
        print_yellow(f"key: {key} ---> value{dfa_table[key]}")

    
    return dfa_table, accept_states
   

     
def get_accept_condition(DFA_dict):

    for i in DFA_dict:
        if DFA_dict[i][0] == '#':
            return i


def dfa_aux(DFA_dict, state):
    """
    takes a state
    returns a tuple of:
    token(character),set of ids
    """

    d = {}
    
    for i in state:
        #print(i,DFA_dict[i])
        if DFA_dict[i][0] in d:
            #print("i in d")
            x = d[DFA_dict[i][0]]
            x.add(i)

            d[DFA_dict[i][0]] = x
        else:
            d[DFA_dict[i][0]] = {i}
            
    # convert set into frozenSet (no need)
    d.update((k, frozenset(v)) for k, v in d.items())
    return d






