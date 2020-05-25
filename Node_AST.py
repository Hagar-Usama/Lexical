class Node_AST:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.left = None
        self.right = None
    
    def build_tree(self, postfix_exp , op_list):

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
        
        self.name = postfix_exp[0]
        node_list[0] = self

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

            

            