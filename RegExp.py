import ast

class RegExp:

    def __init__(self, exp_list,  operators, star='*'):

        #self.exp = exp_str
        self.exp_list = exp_list
        self.star = star
        self.operators = operators


    def handle_exp(self):

        exp_list = []
       
        exp = self.exp_list
        op = self.operators

               
        while len(exp) > 1:

            if len(exp) > 1:
                x = exp[0]
                y = exp[1]


                if y not in op:
                    if (x not in op) or (x == self.star) or (x == ")"):
                        exp_list.append(exp.pop(0))
                        exp_list.append("concat")
                    else:
                        exp_list.append(exp.pop(0))
                else:
                        exp_list.append(exp.pop(0))


        exp_list.append(exp[-1])
        self.exp_list = exp_list       



