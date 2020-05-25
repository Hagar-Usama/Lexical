class Node_AST:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.left = None
        self.right = None

    def isRoot(self):
        return self.parrent == None
    
    def isLeaf(self):
        return (self.left) == None and (self.right == None)
    
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


    

    
    def show_tree(self, option=0):

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

                
def print_tree(prefix, n, isLeft):

        if n != None:
            print(prefix, end='')

            if isLeft:
                print("|-- ", end='')
            else:
                print("\\-- ", end= '')
            
            print(n.name)

            print(prefix, end='')

            if isLeft:
                print("|-- ", end='')
            else:
                print("\\-- ", end= '')


            # recursively
            lefty = "    "
            if isLeft: lefty = "|   ";
            pre = prefix + lefty

            print_tree(pre, n.left, True)
            print_tree(pre, n.right, True)


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