import enum

id = 0
STAR = '*'
CONCAT = 'concat'
OR = '|'
QSNMRK = '?'      
PLUS = '+'

class Operator(enum.Enum):
    STAR = 1        # *
    CONCAT = 2      # .
    OR = 3          # |
    QSNMRK = 4      # ?
    PLUS = 5        # +

class Node_AST:
    def __init__(self, name, parent=None):
        self.name = name
        global id
        self.id = id
        id += 1
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
        return self.parrent == None
    
    def isLeaf(self):
        return (self.left == None) and (self.right == None)
    
    def isRight(self):
        if self.isRoot():
            return False
        else:
            if self.parent.right == self:
                return True

    def isLeft(self):
        if self.isRoot():
            return False
        else:
            if self.parent.left == self:
                return True

    
    def get_DFA_dict(self):
        DFA_dict = {}
        
        print(f"in DFA_dict: {self.id_dict}")
        for i in self.id_dict:
            print(f"{self.id_dict[i].name , self.id_dict[i].followpos}")

        for i in self.id_dict:
            DFA_dict[i] = (self.id_dict[i].name, self.id_dict[i].followpos)

        print(DFA_dict)
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
                #print(" |"*(current_node.depth), end='\n' )
                #print("|",end='')
                #print(" "*(current_node.depth*2), end='--' )

                if isinstance(current_node, Node_AST):
                    print(current_node.name)    
                    
                    l = []
               
                    l.insert(0,current_node.left)
                    l.insert(0,current_node.right)
                else:
                    nodes_list.remove(current_node)

                for j in l:
                    nodes_list.append(j)

# @staticmethod               
def print_tree(prefix, n, isLeft):

        if n != None:
            
            lefty = "\\-- "
            lefty = "└└──"
            if isLeft:
                lefty = "|-- "
                lefty = "└── "

            print( prefix+ lefty + "[" + n.name + "]  " + str(n.id) + " " + str(n.nullable) + "  " +  str(n.firstpos) + str(n.lastpos) + "**" +  str(n.followpos)  )


            lefty = "    "
            if isLeft:
                lefty = "|   "

            print_tree(prefix + lefty, n.left, True)
            print_tree(prefix + lefty, n.right, False)

           
def pre_followpos(cn):
        """
        gets nullable, firstpos and lastpos

        """

        #print("prefollow")

        STAR = "*"
        CONCAT = "concat"
        OR = "|"
        EPSILLON = '𝛆'

        # basecase if node is null
        if cn != None:

            if cn.isLeaf():
                # for leaves, epsillon or i
                if cn.name == EPSILLON:
                    cn.nullable = True
                    # firstpos is phi
                else:
                    cn.nullable = False
                    cn.firstpos.add(cn.id)
                    cn.lastpos.add(cn.id)
       

            else:
                # if concat , (|) ,and (*)
                pre_followpos(cn.left)

                if cn.name == STAR:
                    cn.nullable = True
                    cn.firstpos.update(cn.left.firstpos)
                    cn.lastpos.update(cn.left.lastpos)

                elif cn.name == CONCAT:
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
                    

                elif cn.name == OR:
                    pre_followpos(cn.right)
                    cn.nullable = cn.left.nullable or cn.right.nullable

                    s1 = cn.left.firstpos
                    s2 = cn.right.firstpos
                    cn.firstpos.update(s1.union(s2))

                    s1 = cn.left.lastpos
                    s2 = cn.right.lastpos
                    cn.lastpos.update(s1.union(s2))

def eval_followpos(cn):

    
    if cn != None:
        #eval code (post order)

        eval_followpos(cn.left)
        eval_followpos(cn.right)

        if cn.name == CONCAT:
            for i in cn.left.lastpos:
                
                cn.id_dict[i].followpos.update(cn.right.firstpos)
                """ 
                for j in cn.right.firstpos:
                    print(f"i is : {i}, {id_dict[i].name}")
                    print(f"j is : {j}, {id_dict[j].name}")
                    id_dict[i].followpos.add(j)
                """
        elif cn.name == STAR:
            for i in cn.lastpos:
                cn.id_dict[i].followpos.update(cn.firstpos)
                
                   






def get_node_dict(cn):

    #current_node = cn

    if cn != None:
        if cn.isLeaf():
            cn.id_dict[cn.id] = cn
            #print(f"id: {cn.id}: name: {cn.name}")
        else:
            # internal node
            get_node_dict(cn.left)
            get_node_dict(cn.right)
            
            if cn.left:
                cn.id_dict.update(cn.left.id_dict)
            if cn.right:
                cn.id_dict.update(cn.right.id_dict)


def build_AST_tree(postfix_exp , op_list):

        """ 
        initialize an empty stack S


        """

        if "(" in op_list:
            op_list.remove("(")
        if ")" in op_list:
            op_list.remove(")")

        STAR = '*'

        node_list = []

        # create nodes
        for i in postfix_exp:
            n = Node_AST(i)
            node_list.append(n)
        
        

        s = []

       
        for current_node in node_list:
            #print(f"current_node {current_node} , name: {current_node.name}")

            #print(f"Node Name: {current_node.name}")

            if current_node.name in op_list:
                if current_node.name == STAR:
                    n = s.pop(-1)
                    current_node.left = n
                    n.parent = current_node
                else:
                    # concat , |

                    #print("concat or |")
                    n = s.pop(-1)
                    current_node.right = n
                    n.parent = current_node

                    n = s.pop(-1)
                    current_node.left = n
                    n.parent = current_node
            
            s.append(current_node)

            """ 
            for i in s:
                print(i.name, end="  ")
            print("")
            """
        return s[0]