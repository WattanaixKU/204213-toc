import sys

# token definitions
EOF = 0
ERROR = 1
LITERAL = 2
IDEN = 3
CONST = 4

# a map from tokenID to token name
tokname = {
    EOF:'EOF',
    ERROR:'ERROR',
    LITERAL:'LITERAL',
    IDEN:'IDEN',
    CONST:'CONST'
}

#=========================================================

START = 5
word = ""
LITERAL_LIST = ['+', '-', '*', '/', '(', ')']
D = [str(c) for c in range(10)]
L = [chr(i) for i in range(97, 123)] + D
class lexer():
    infile = ""
    state = None
    char = None

def next_char():
    global word
    try:
        char = word[0]
        word = word[1:]
        lexer.infile = word
        if char.strip() == "":
            return " "
        return char
    except:
        raise Exception('no more char')

def lexer():
    try:
        char = ""
        string = ""
        global word
        try:
            word = lexer.infile.read()
        except:
            word = lexer.infile
        while(char.strip() == ""):
            char = next_char()
        if char in LITERAL_LIST:
            return (2 , char)
        elif char in D:
            while(char in D):
                string += char
                char = next_char()
                if(char == '.'):
                    dot = False
                    while(char in D or not dot):
                        dot = True
                        string += char
                        char = next_char()
            if(char != ' '):
                lexer.infile = char + lexer.infile
            if(string[-1] == '.'):
                return (1, string)
            return (4, string)
        elif char in L:
            while(char in L):
                string += char
                char = next_char()
            if(char != ' '):
                lexer.infile = char + lexer.infile
            return (3, string)
        else:
            return (1, char)
    except Exception:
        return (0, None)

#=========================================================


infile = sys.stdin
lexer.infile = infile    # lexer's input file
lexer.state = START      # lexer's current state
lexer.char = None        # lexer's last character read
while True:
    tokenID, lexeme = lexer()
    if tokenID == EOF:
        break
    print('{}\t{}'.format(tokname[tokenID], lexeme))
