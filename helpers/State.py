from  collections import defaultdict

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

        tokens = []
        tokens_accept = []
        
        
        s = self.init_state

        if (input_list) and ( len(input_list) != len(prev_list)):
            
            prev_list = input_list.copy()
        
            while input_list:
                tok = input_list.pop(0)

                tokens.append(tok)

                s = self.get_next_state(s, tok)

                
                if s != DEAD_STATE:
                    if self.is_accepted(s):
                        tokens_accept.append(tokens.copy())
                
                else:
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

        tokens = []
        tokens_accept = []
        
        s = self.init_state
        for i in input_list:

            tokens.append(i)

            s = self.get_next_state(s,i)
            if s != DEAD_STATE:
                if self.is_accepted(s):
                    tokens_accept.append(tokens.copy())
               
            else:
                tokens = []
                if tokens_accept:
                    self.accepted_tokens.append(tokens_accept[-1])
                tokens_accept = []
            
    def is_accepted(self, state):
        return state in self.accept_states

    def get_next_state(self, current_state, input_token):
        x = self.dfa_table.get(current_state,0)
        if x:
            return x.get(input_token, 0)
        return x




def build_DFA(DFA_dict, init_state):
    

    visited = set()
    istate = init_state
    state_list = [istate]
    accept_cond = get_accept_condition(DFA_dict)
    accept_states = set()
    dfa_table = defaultdict(dict)

    
    while state_list:

        state = state_list.pop(0)
        visited.add(frozenset(state))
       
        
        ip_dict = dfa_aux(DFA_dict, state)
        for i in ip_dict:
            if i != '#':
                to_state = set()

                # set for each character
                for j in ip_dict[i]:
                    # get its follow and update the set
                    to_state.update(DFA_dict[j][1])

                # check if it is an accept state   
                if accept_cond in to_state:
                    accept_states.add(frozenset(to_state))

                dfa_table[frozenset(state)][i] = frozenset(to_state)


                if (to_state not in state_list) and (to_state not in visited):
                    state_list.append(to_state)


    
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






