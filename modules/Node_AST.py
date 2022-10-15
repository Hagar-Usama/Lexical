from enum import Enum
import copy

id = 0

class Operator(str, Enum):
    STAR = "STAR"          # *
    CONCAT = "CONCAT"      # .
    OR = "OR"              # |
    QSNMRK = "QSTMRK"      # ?
    PLUS = "PLUS"          # +
    EPSILLON = '𝛆'


class Node_AST:
    def __init__(self, name, parent=None):
        self.name = name
        self.id = 0
        self.parent = parent
        self.left = None
        self.right = None
        self.nullable = None
        self.firstpos = set()
        self.lastpos = set()
        self.followpos = set()
        self.leaves = []
        self.id_dict = {}

    def isRoot(self):
        return self.parent == None

    def isLeaf(self):
        return (self.left == None) and (self.right == None)

    def isRight(self):
        # TODO: recheck the logic in next pass
        return False if self.isRoot() else self.parent.right == self

    def isLeft(self):
        return False if self.isRoot() else self.parent.left == self

    def get_root(self):
        n = self
        while True:
            if not n.parent:
                break
            n = n.parent

        return n

    def find_key(self, key):
        found = []
        found = find_key(self, key, found)
        return found

    def assign_id(self):
        # TODO: refine this later
        assign_id(self)

    def attach_node(self, term, exp):

        found = self.find_key(term)
        # operators may be omitted from the function I guess
        # exp shall be postfix
        operators = {'(', ')', 'STAR', 'OR', 'PLUS'}

        branch = build_AST_tree(exp, operators)

        ##########################
        # trying to attach nodes
        ##########################

        for i in found:

            parent = i.parent
            lefty = i.isLeft()
            i.parent = None

            # free(i)
            del i

            if lefty:
                parent.left = copy.deepcopy(branch)
            else:
                parent.right = copy.deepcopy(branch)

    @staticmethod
    def implant_node(n, exp):
        """ implant node  <not implemented>"""
        root = n.get_root()
        #most_right = root.right
        left = root.left

        operators = {'(', ')', 'STAR', 'OR', 'PLUS'}
        branch = build_AST_tree(exp, operators)

        or_branch = Node_AST("OR", root)

        or_branch.right = branch
        branch.parent = or_branch

        or_branch.left = left
        left.parent = or_branch

        root.left = or_branch

    def get_DFA_dict(self):
        DFA_dict = {}
        for i in self.id_dict:
            DFA_dict[i] = (self.id_dict[i].name, self.id_dict[i].followpos)

        return DFA_dict

    def get_node_dict(self):
        get_node_dict(self)

    def pre_followpos(self):
        pre_followpos(self)

    def print_tree(self):
        print("🌲 .. tree .. 🌲")
        print_tree("", self, False)

    def show_tree(self):

        nodes_list = [self]
        current_node = self

        while nodes_list:
            current_node = nodes_list.pop(-1)
            if isinstance(current_node, Node_AST):
                print(current_node.name)
                l = []
                l.insert(0, current_node.left)
                l.insert(0, current_node.right)
            else:
                nodes_list.remove(current_node)

            for j in l:
                nodes_list.append(j)


def print_tree(prefix, n, isLeft):

    if n != None:

        lefty = "\\-- "
        lefty = "└└──"
        if isLeft:
            lefty = "|-- "
            lefty = "└── "

        print(prefix + lefty + "[" + n.name + "]  " + str(n.id) + " " + str(
            n.nullable) + "  " + str(n.firstpos) + str(n.lastpos) + "**" + str(n.followpos))

        lefty = "    "
        if isLeft:
            lefty = "|   "

        print_tree(prefix + lefty, n.left, True)
        print_tree(prefix + lefty, n.right, False)


def pre_followpos(cn):
    """
    gets nullable, firstpos and lastpos
    """
    # basecase if node is null
    if cn != None:

        if cn.isLeaf():
            # for leaves, epsillon or i
            if cn.name == Operator.EPSILLON:
                cn.nullable = True
                # firstpos is phi
            else:
                cn.nullable = False
                cn.firstpos.add(cn.id)
                cn.lastpos.add(cn.id)

        else:
            # if concat , (|) ,and (*)
            pre_followpos(cn.left)

            if cn.name == Operator.STAR:
                cn.nullable = True
                cn.firstpos.update(cn.left.firstpos)
                cn.lastpos.update(cn.left.lastpos)

            elif cn.name == Operator.PLUS:
                cn.nullable = cn.left.nullable
                cn.firstpos.update(cn.left.firstpos)
                cn.lastpos.update(cn.left.lastpos)

            elif cn.name == Operator.CONCAT:
                pre_followpos(cn.right)
                cn.nullable = cn.left.nullable and cn.right.nullable

                s1 = cn.left.firstpos
                s2 = cn.right.firstpos

                s2 = s1.union(s2) if cn.left.nullable else s1
                cn.firstpos.update(s2)

                s1 = cn.left.lastpos
                s2 = cn.right.lastpos

                s2 = s1.union(s2) if cn.right.nullable else s2
                cn.lastpos.update(s2)

            elif cn.name == Operator.OR:
                pre_followpos(cn.right)
                cn.nullable = cn.left.nullable or cn.right.nullable

                s1 = cn.left.firstpos
                s2 = cn.right.firstpos
                cn.firstpos.update(s1.union(s2))

                s1 = cn.left.lastpos
                s2 = cn.right.lastpos
                cn.lastpos.update(s1.union(s2))

            elif cn.name == Operator.QSNMRK:
                cn.nullable = True
                cn.firstpos.update(cn.left.firstpos)
                cn.lastpos.update(cn.left.lastpos)


def eval_followpos(cn):

    if cn != None:
        # eval code (post order)
        eval_followpos(cn.left)
        eval_followpos(cn.right)

        if cn.name == Operator.CONCAT:
            for i in cn.left.lastpos:

                cn.id_dict[i].followpos.update(cn.right.firstpos)

        elif (cn.name == Operator.STAR)\
                or (cn.name == Operator.PLUS):
            for i in cn.lastpos:
                cn.id_dict[i].followpos.update(cn.firstpos)


def get_node_dict(cn):

    if cn != None:
        if cn.isLeaf():
            cn.id_dict[cn.id] = cn
        else:
            # internal node
            get_node_dict(cn.left)
            get_node_dict(cn.right)

            if cn.left:
                cn.id_dict.update(cn.left.id_dict)
            if cn.right:
                cn.id_dict.update(cn.right.id_dict)


def build_AST_tree(postfix_exp, op_list):
    """ 
    initialize an empty stack S
    """

    if "(" in op_list:
        op_list.remove("(")
    if ")" in op_list:
        op_list.remove(")")

    node_list = []

    # create nodes
    for i in postfix_exp:
        n = Node_AST(i)
        node_list.append(n)

    s = []

    for current_node in node_list:
        if current_node.name in op_list:
            if (current_node.name == Operator.STAR)\
                    or (current_node.name == Operator.PLUS)\
                    or (current_node.name == Operator.QSNMRK):
                n = s.pop(-1)
                current_node.left = n
                n.parent = current_node

            else:
                # concat , |
                n = s.pop(-1)
                current_node.right = n
                n.parent = current_node

                n = s.pop(-1)
                current_node.left = n
                n.parent = current_node

        s.append(current_node)

    return s[0]


def find_key(n, key, found):
    """ returns a list of found leaves """

    if n != None:
        find_key(n.left, key, found)
        find_key(n.right, key, found)

        if n.name == key:
            found.append(n)

    return found


def assign_id(n):

    if n != None:
        assign_id(n.left)
        assign_id(n.right)

        if n.isLeaf() and n.name != '𝛆':
            global id
            n.id = id + 1
            id += 1
        else:
            n.id = 0
