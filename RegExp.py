import ast
from color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET


STAR = 'STAR'
CONCAT = 'CONCAT'
OR = 'OR'
QSNMRK = 'QSNMRK'      
PLUS = 'PLUS'

class RegExp:

    def __init__(self, exp_list,  operators, star= STAR):

        #self.exp = exp_str
        self.exp_list = exp_list
        self.cat_list = []
        self.star = star
        self.operators = operators
        self.post_list = []


    def handle_exp_2(self):

        exp_list = []
       
        exp = self.exp_list
        op = self.operators

        last = exp[-1]
               
        while len(exp) > 1:

            if len(exp) > 1:
                x = exp[0]
                y = exp[1]


                #print(x,y)
                #print(x in op)
                #print(y in op)

                
                if y not in op:
                    #print("y is NOT operator")
                    if (x not in op) or (x == STAR) or (x == PLUS) or (x == QSNMRK) or (x == ")"):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                        #print("CONCAT")
                    else:
                        exp_list.append(exp.pop(0))
                        
                else:
                    # y is operator
                    #print("y is operator")

                    if (x == STAR) or (x == PLUS) or (x == QSNMRK):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                        #print("CONCAT")
                    
                    elif (x not in op) and y == '(':
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                        #print("CONCAT")

                    else:
                         exp_list.append(exp.pop(0))
        
        exp_list.append(exp.pop(0))
        self.cat_list = exp_list
        self.operators.add('CONCAT')
        return exp_list

    def handle_exp(self):

        exp_list = []
       
        exp = self.exp_list
        op = self.operators

        STAR = 'STAR'
        CONCAT = 'CONCAT'
        OR = "OR"
        PLUS = "PLUS"
        QSNMRK = "QSNMRK"
        LBRKT = "("
        RBRKT = ")"
                       
        while len(exp) > 1:

            if len(exp) > 1:
                x = exp[0]
                y = exp[1]

                #print(x,y)

                if (x == STAR) or (x == PLUS) or (x == QSNMRK):
                    if (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == LBRKT):
                        #print_red("case 1")
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                        
                        #print(CONCAT)
                    elif y not in op:
                        #print_red("case 2")
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")

                        #print(CONCAT)
                    else:
                        #print_red("case 3")
                        exp_list.append(exp.pop(0))
                
                elif x == OR:
                    if y == LBRKT:
                        #print_red("case 4")
                        exp_list.append(exp.pop(0))
                        #exp_list.append("CONCAT")
                    elif (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == OR) or (y == RBRKT):
                        #print_red("case 5")
                        print("Error!")
                    else:
                        #print_red("case 6")
                        exp_list.append(exp.pop(0))

                elif x == LBRKT:
                    
                    if (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == OR):
                        #print_red("case 7")
                        print("Error!")

                    else:
                        #print_red("case 8")
                        exp_list.append(exp.pop(0))
                
                elif x == RBRKT:
                    #if (y == LBRKT) or (y not in op):
                    if (y == LBRKT) or (y not in op):
                        #print_red("case 9")

                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")

                        #print(CONCAT)
                    else:
                        #print_red("case 10")
                        exp_list.append(exp.pop(0))

                elif x not in op:
                    # x is character
                    if (y == LBRKT) or (y not in op):
                        #print_red("case 11")
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")

                        #print(CONCAT)
                        
                    else:
                        #print_red("case 12")
                        exp_list.append(exp.pop(0))


        
        exp_list.append(exp.pop(0))
        self.cat_list = exp_list
        self.operators.add('CONCAT')
        return exp_list




    def get_postfix(self):
        """ 
        opstack = []
        output = []

        new_ip = input.split(" ")

        for i in new_ip:
            if i in operand:
                output.append(i)
            elif i == "(":
                opstack.push(i)
            elif i == ")":
                x = TOS(opstack)
                while(x != ")":
                    x = opstack.pop(i)
                    if x !=")":
                        output.append(i)
            elif i is operator:
                x = TOS(opstack)
                y = compare(x,i)

                while y:
                    output.append(y)
                    x = TOS(opstack)
                    y = compare(x,i)

                opstack.push(i)
                
                
        """
        opstack = []
        output = []
        operators = self.operators

        exp = self.cat_list
        #print(f"catlist = {self.cat_list}")

        for i in exp:
            if i == "(":
                opstack.append(i)
            elif i == ')':
                # pop stack til pop = (                
                while opstack:
                    p = opstack.pop(-1)
                    if p == '(':
                        break
                    output.append(p)

            elif i not in operators:
                # if it is an operand
                output.append(i)
            else:
                while opstack:
                    p_stack = self.get_precedence(opstack[-1])
                    p_current = self.get_precedence(i)
                    #print(f"current: {i},{p_current} , stack {opstack[-1]},{p_stack}")

                    if p_current >= p_stack:
                        output.append(opstack.pop(-1))
                    
                    else:
                        break
                
                opstack.append(i)
                #print(f"opstack : {opstack}")
   
                
        while opstack:
            output.append(opstack.pop(-1))   

        return output        
                    


    def get_precedence(self, op):

        #print(f"operand entered = {op}")
        STAR = "STAR"
        PLUS = "PLUS"
        QSTMRK = "QSTMRK"
        CONCAT = "CONCAT"
        OR = "OR"
        
        
        if (op == STAR) or (op == PLUS) or (op == QSNMRK):
            return 2
        elif (op == CONCAT):
            return 3
        elif (op == OR):
            return 4
        else:
            return 50

    def compare(self, i ,opstack):
        if not opstack:
            return True
        
        return self.get_precedence(i) < self.get_precedence(opstack[-1])



def postfix_me(exp_dict, operators):

    """
    consider removing operators (redundant)
    """

    new_dict = {}
    tuple_list = []
    """ 
    for k, v in ((k, exp_dict[k]) for k in reversed(exp_dict)):
        r = RegExp(v, operators, STAR)
        exp2 = r.handle_exp()
        print(exp2)
        post = r.get_postfix()
        new_dict[k] = post
    """

     
    for key, value in exp_dict.items():

        r = RegExp(value, operators, STAR)
        exp2 = r.handle_exp()
        #print(exp2)
        post = r.get_postfix()
        #new_dict[key] = post
        tuple_list.insert(0,(key,post))

    
    post_dict = dict(tuple_list)
    
    #print_blue(tuple_list)
    #print_green(post_dict)
    return post_dict
    


        

