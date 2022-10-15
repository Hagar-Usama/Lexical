from modules.color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET

STAR = 'STAR'
CONCAT = 'CONCAT'
OR = 'OR'
QSNMRK = 'QSNMRK'
PLUS = 'PLUS'


class RegExp:

    def __init__(self, exp_list,  operators, star=STAR):

        self.exp_list = exp_list
        self.cat_list = []
        self.star = star
        self.operators = operators
        self.post_list = []

    def handle_exp_2(self):

        exp_list = []
        exp = self.exp_list
        op = self.operators

        while len(exp) > 1:
            if len(exp) > 1:
                x, y = exp[0], exp[1]
                if y not in op:
                    if (x not in op) or (x == STAR) or (x == PLUS) or (x == QSNMRK) or (x == ")"):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                    else:
                        exp_list.append(exp.pop(0))

                else:
                    # y is operator
                    if (x == STAR) or (x == PLUS) or (x == QSNMRK):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")

                    elif (x not in op) and y == '(':
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
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

                if (x == STAR) or (x == PLUS) or (x == QSNMRK):
                    if (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == LBRKT):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")

                    elif y not in op:
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                    else:
                        exp_list.append(exp.pop(0))

                elif x == OR:
                    if y == LBRKT:
                        exp_list.append(exp.pop(0))
                    elif (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == OR) or (y == RBRKT):
                        print("Error!")
                    else:
                        exp_list.append(exp.pop(0))

                elif x == LBRKT:

                    if (y == STAR) or (y == PLUS) or (y == QSNMRK) or (y == OR):
                        print("Error!")

                    else:
                        exp_list.append(exp.pop(0))

                elif x == RBRKT:
                    if (y == LBRKT) or (y not in op):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                    else:
                        exp_list.append(exp.pop(0))

                elif x not in op:
                    # x is character
                    if (y == LBRKT) or (y not in op):
                        exp_list.append(exp.pop(0))
                        exp_list.append("CONCAT")
                    else:
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
                    if p_current < p_stack:
                        break
                    output.append(opstack.pop(-1))
                opstack.append(i)

        while opstack:
            output.append(opstack.pop(-1))

        return output

    def get_precedence(self, op):

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

    def compare(self, i, opstack):
        if not opstack:
            return True
        return self.get_precedence(i) < self.get_precedence(opstack[-1])


def postfix_me(exp_dict, operators):
    """
    consider removing operators (redundant)
    """
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
        r.handle_exp()
        post = r.get_postfix()
        tuple_list.insert(0, (key, post))

    post_dict = dict(tuple_list)
    return post_dict
