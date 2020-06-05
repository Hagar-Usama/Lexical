import re
from modules.color_print import print_blue, print_green, print_purple, print_red, print_yellow, ANSI_RED, ANSI_RESET
from itertools import chain
from copy import copy, deepcopy

class Scanner:
    def __init__(self, lexical_path):
        self.lex_path = lexical_path
        self.punctuations = set()
        self.keywords = set()
        self.RE = dict()
        self.RD = dict()
        self.buffer = ""
        self.input_list = []
        self.program_list = []
        self.operators = {'(', ')', 'STAR', 'OR', 'PLUS','CONCAT'}

        

    
    def analaze_lex(self):
        self.get_buffer()
        self.handle_file()
        self.handle_lexical()
        self.list_rules()
        self.sep_RD()
        
    def handle_file(self):
        self.buffer = self.buffer.replace("\\L", '𝛆')
        self.buffer = self.buffer.replace("\+", 'plusop')
        self.buffer = self.buffer.replace("\*", 'mulop')

        self.buffer = self.buffer.replace("+", 'PLUS')
        self.buffer = self.buffer.replace("*", 'STAR')
        self.buffer = self.buffer.replace("|", 'OR')

        self.buffer = self.buffer.replace("plusop", '+')
        self.buffer = self.buffer.replace("mulop", '*')

        self.buffer = self.buffer.replace("\\", '')
        
        
        self.buffer = self.buffer.replace('a-z',"( " + generate_equivalent_range("a-z") + " )")
        self.buffer = self.buffer.replace('A-Z',"( " + generate_equivalent_range("A-Z") + " )")
        self.buffer = self.buffer.replace('0-9',"( " + generate_equivalent_range("0-9") + " )")

        self.input_list = self.buffer.split('\n')

    def get_RD_list(self):
        return get_value_list(self.RD)
        
    def get_RE_list(self):
        return get_value_list(self.RE)

    def sep_RD(self):
        for k, v in self.RD.items():
        #print(k,v)
            a = v
            for i in v:
                
                if i not in self.RE:
                    if i not in self.operators:
                        if len(i) > 1:
                            #print_yellow(f"non-RE is: {i}")
                            # separate i, add it to its list, update 
                        
                            new_i = list(i)
                            a = list(chain.from_iterable(new_i if item == i else [item] for item in a))
                            #print(f"a is {a}")
                            self.RD[k] = a
        


    def expand_rd(self, r):
        
        rd_temp = copy(self.RD)
        new_rd = {}

        for i in range(1,r):
            for k,v in rd_temp.items():
                for key, value in self.RE.items():
                    #print_yellow(f"{i}, {j}")
                    a = rd_temp[k]
                    #print(a)
                    a = list(chain.from_iterable(value if item == key else [item] for item in a))
                    rd_temp[k] = a
            
        #print_purple(rd_temp)
        self.expanded_rd = rd_temp
     

    
    def handle_lexical(self):

        """
        handles lexical inputs

        returns Punctuation set
            Keywords set
            REs dict
            RDs dict
    
        """
        p,k,re,rd = sort_file(self.input_list)

        RDs = {}
        REs = {}
        pn = set()
        kw = set()

        for i in p:
            pn.update(handle_punctuations(i))

        for i in k:
            kw.update(handle_keyword(i))

        for i in rd:
            r = handle_rd(i)
            #print_blue(f"r= {r}")
            RDs[r[0]] = r[1]
            #print_purple(handle_rd(i))
        for i in re:
            r = handle_re(i)
            #print_green(f"r= {r}")
            REs[r[0]] = r[1]
            #print_purple(handle_re(i))
        

        #print_purple(pn)
        #print_blue(kw)

        self.punctuations = pn
        self.keywords = kw
        self.RD = RDs
        self.RE = REs

        #return pn, kw, REs, RDs

    def postfix_keyword_punc(self):

        kw_pn = self.keywords.union(self.punctuations)
        kw_pn = intersperse(list(kw_pn) ,"OR")
        kw_pn.remove("OR")
        kw_pn.append("OR")

        return kw_pn
    
    def get_buffer(self):
        file = open(self.lex_path)
        self.buffer = file.read().replace("\n", "\n")
        file.close()
        self.buffer = self.buffer.strip()

    @staticmethod
    def read_file(path):
        file = open(path)
        buffer = file.read().replace("\n", "\n")
        file.close()
        buffer = buffer.strip()
        return buffer

   
    def read_program_file(self, path):
        buffer = self.read_file(path)
        buffer = re.sub('\s+',' ',buffer)
        buffer = buffer.split(' ')
        self.program_list = buffer
        return buffer


    def list_rules(self):

        """
        make REs & RDs as lists

        ex:
        L = x | l --> ['x','|', 'l']

        return modified RE and RD
        
        """

        for key, value in self.RE.items():
            self.RE[key] = value.split(" ")

        for key, value in self.RD.items():
            self.RD[key] = value.split(" ")
        
        #return RE, RD



def sort_file(input_list):
    """ 
    sort it to RE, RD, Keywords and Punctuations
    """
    punctuations = []
    keywords = []
    RDs = []
    REs = []

    
    for i in input_list:
        
        if i.strip().startswith("{"):
            keywords.append(i.strip())

            #print("Keywords")
        elif i.strip().startswith("["):
            #print("Punctuations")
            punctuations.append(i.strip())
        else:
            x = re.search(r"[a-zA-Z]+[0-9]*:", i.strip())
            if x:
                RDs.append(i.strip())
                #print(f"RD {i.strip()}")
            else:
                x = re.search(r"[a-zA-Z]+[0-9]* =", i.strip())
                if x:
                    REs.append(i.strip())
                    #print(f"RE {i.strip()}")

    return punctuations, keywords, REs, RDs



def generate_equivalent_range(str_input):
    "generate ranges in ReExp"

    if str_input == "a-z":
        
        range_s = 'a'
        range_e = 'z'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 
            
    elif str_input == "A-Z":
        
        range_s = 'A'
        range_e = 'Z'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 

    elif str_input == "0-9":

        range_s = '0'
        range_e = '9'
        y = range_s

        for j in range(ord(range_s)+1, ord(range_e)+1):
            y += " OR " + chr(j) 

    return y

def handle_keyword(input_list):
    
    input_list = input_list.replace("{",'')
    input_list = input_list.replace("}",'')
    input_list = input_list.split(" ")
    input_list = [i.strip() for i in input_list]

    return set(input_list)

def handle_punctuations(input_list):
    input_list = input_list.replace("[",'')
    input_list = input_list.replace("]",'')
    input_list = input_list.split(" ")
    input_list = [i.strip() for i in input_list]

    return set(input_list)

def handle_rd(input_list):
    input_list = input_list.strip(" ")
    input_list = input_list.split(":", 1)

    input_list = [i.strip() for i in input_list]
    
    #print_red(f"input list RD: {input_list}")

    ## separating 
    #for i in input_list:
    #    if i not in RE:
    #        print(f"non-RE i is: {i}")
    
    return input_list
    
def handle_re(input_list):
    input_list = input_list.strip(" ")
    input_list = input_list.split("=", 1)
    input_list = [i.strip() for i in input_list]

    return input_list


def list_rules(RE, RD):

    """
    make REs & RDs as lists

    ex:
    L = x | l --> ['x','|', 'l']

    return modified RE and RD
    
    """

    for key, value in RE.items():
        RE[key] = value.split(" ")

    for key, value in RD.items():
        RD[key] = value.split(" ")
    
    return RE, RD

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def get_value_list(the_dict):

    """ coverts the dict into list of values 
        (with brackets for merging
    """

    val = []
    for key, value in the_dict.items():
        value = add_brackets(value)
        val.append(value)
    return val

def add_brackets(the_list):
    LBRKT = "("
    RBRKT = ")"
    if len(the_list) > 1:
        the_list.insert(0,LBRKT)
        the_list.append(RBRKT)
    return the_list

def flatten_list(the_list):
    flat_list = []
    flat_list = [item for sublist in the_list for item in sublist]
    """ 
    for i in range(len(the_list)):
        flat_list.append(the_list[i])
        print_yellow(the_list[i])
        if i != len(the_list) - 1:
            #flat_list.append("OR")
            pass
    """
    return flat_list

def main():
    lex_scan = Scanner("/home/u/git/last_chance/Lexical/lexical3.txt")
    lex_scan.analaze_lex()

    print_red(lex_scan.RE)
    
    for key, value in lex_scan.RD.items():
        print_yellow(f"{key}=>{value}")

    for key, value in lex_scan.RE.items():
        print_green(f"{key}=>{value}")

    print_blue(lex_scan.punctuations)
    print_purple(lex_scan.keywords)

    RD_list = lex_scan.get_RD_list()
    RD_list = intersperse(RD_list,["OR"])
    #print(flatten_list(RD_list))

    # this list contains all RDs ored
    flat_list = flatten_list(RD_list)
    kw_exp = intersperse(lex_scan.keywords,"OR")
    print_purple(kw_exp)
    pn_exp = intersperse(lex_scan.punctuations,"OR")
    print_blue(pn_exp)

    print_purple(flat_list)

    print_red(lex_scan.postfix_keyword_punc())


    lex_scan.read_program_file("/home/u/git/last_chance/Lexical/program3.txt")
    print_blue(lex_scan.program_list)


    lex_scan.expand_rd(3)
    print_green(lex_scan.expanded_rd)
    print(lex_scan.RD)

    print_blue("sep*"*10)

    operators={'(', ')', 'STAR', 'OR', 'PLUS','CONCAT'}

    """ for k, v in lex_scan.RD.items():
        #print(k,v)
        a = v
        for i in v:
            
            if i not in lex_scan.RE:
                if i not in operators:
                    if len(i) > 1:
                        print_yellow(f"non-RE is: {i}")
                        # separate i, add it to its list, update 
                       
                        new_i = list(i)
                        a = list(chain.from_iterable(new_i if item == i else [item] for item in a))
                        #print(f"a is {a}")
                        lex_scan.RD[k] = a
    """


    print(lex_scan.RD)
    for k,v in lex_scan.RD.items():
        print(k,v)



if __name__ == "__main__":
    main()
