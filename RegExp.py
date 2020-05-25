import ast

class RegExp:

    def __init__(self, exp_list,  operators, star='*'):

        #self.exp = exp_str
        self.exp_list = exp_list
        self.cat_list = []
        self.star = star
        self.operators = operators
        self.post_list = []


    def handle_exp(self):

        exp_list = []
       
        exp = self.exp_list
        op = self.operators

               
        while len(exp) > 1:

            if len(exp) > 1:
                x = exp[0]
                y = exp[1]

                #print(x,y)

                if y not in op:
                    if (x not in op) or (x == self.star) or (x == ")"):
                        exp_list.append(exp.pop(0))
                        exp_list.append("concat")
                        print("concat")
                    else:
                        exp_list.append(exp.pop(0))
                        
                else:
                    if x == self.star:
                        exp_list.append(exp.pop(0))
                        exp_list.append("concat")
                        print("concat")
                    else:
                         exp_list.append(exp.pop(0))
        
        exp_list.append(exp.pop(0))
        self.cat_list = exp_list
        self.operators.add('concat')
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

        print(f"catlist = {self.cat_list}")

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
                    print(f"current: {i},{p_current} , stack {opstack[-1]},{p_stack}")

                    if p_current >= p_stack:
                        output.append(opstack.pop(-1))
                    
                    else:
                        break
                
                opstack.append(i)
                print(f"opstack : {opstack}")


        
                     
                
        while opstack:
            output.append(opstack.pop(-1))   

        return output        
                    


    def get_precedence(self, op):

        #print(f"operand entered = {op}")
        
        if (op == '*') or (op == '+') or (op == '?'):
            return 2
        elif (op == 'concat'):
            return 3
        elif (op == '|'):
            return 4
        else:
            return 50

    def compare(self, i ,opstack):
        if not opstack:
            return True
        
        return self.get_precedence(i) < self.get_precedence(opstack[-1])

                                                 



        

