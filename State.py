

class State:
    def __init__(self):
        self.visited = False




def build_DFA(DFA_dict, init_state):
    visited = []

    s = [init_state]
    
    print("*.*"*12)
    while s:

        
        
        state = s.pop(0)
        visited.append(state)

        ip_dict = dfa_aux(DFA_dict, state)
        # i = a , dict[i] = {90, 86}
        for i in ip_dict:
            if i == '#':
                pass

            g = set()

            # j = 90 
            for j in ip_dict[i]:
                # get it follow and update the set
                g.update(DFA_dict[j][1])
            print(i, g)
            #print("****")
            
            if g not in visited:
                s.append(g)
        print("*.*"*12)

            




        # state is a set
        # get element from
        # get its character
        # search for each equiv


        pass


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
            
    #print(d)
    return d






