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

START = 0
IDEN_STATE = 1
INT_STATE = 2
DECIMAL_STATE = 3
FLOAT_STATE = 4

def my_isdigit(char):
    return char.isdigit()

def my_isspace(char):
    return char.isspace()

def my_isalpha(char):
    return char.isalpha()

def my_isliteral(char):
    return char in ['+', '-', '*', '/', '(', ')']

def other(char):
    return True

def my_is_eof(char):
    return char == '' or char == '\0'

def my_isdecimal(char):
    return char == '.'

STATE_DIAGRAM = {
    START: [
        {
            "check_function": my_is_eof,
            "append": False,
            "return": EOF,
            "next_state": START
        },
        {
            "check_function": my_isdigit,
            "append": True,
            "return": None,
            "next_state": INT_STATE
        },
        {
            "check_function": my_isspace,
            "append": True,
            "return": None,
            "next_state": START
        },
        {
            "check_function": my_isalpha,
            "append": True,
            "return": None,
            "next_state": IDEN_STATE
        },
        {
            "check_function": my_isliteral,
            "append": True,
            "return": LITERAL,
            "next_state": START
        }, 
        {
            "check_function": other,
            "append": True,
            "return": ERROR,
            "next_state": START
        }
    ],
    IDEN_STATE: [
        {
            "check_function": my_isliteral,
            "append": True,
            "return": None,
            "next_state": IDEN_STATE
        },
        {
            "check_function": my_isdigit,
            "append": True,
            "return": None,
            "next_state": IDEN_STATE
        },
        {
            "check_function": other,
            "append": False,
            "return": IDEN,
            "next_state": START
        },
    ],
    INT_STATE: [
        {
            "check_function": my_isdigit,
            "append": True,
            "return": None,
            "next_state": INT_STATE
        },
        {
            "check_function": my_isdecimal,
            "append": True,
            "return": None,
            "next_state": DECIMAL_STATE
        },
        {
            "check_function": other,
            "append": False,
            "return": CONST,
            "next_state": START
        }
    ],
    DECIMAL_STATE: [
        {
            "check_function": my_isdigit,
            "append": True,
            "return": None,
            "next_state": FLOAT_STATE
        },
        {
            "check_function": other,
            "append": False,
            "return": ERROR,
            "next_state": START
        }
    ],
    FLOAT_STATE: [
        {
            "check_function": my_isdigit,
            "append": True,
            "return": None,
            "next_state": FLOAT_STATE
        },
        {
            "check_function": other,
            "append": False,
            "return": CONST,
            "next_state": START
        }
    ]
}
# -------------------------------------------------------
word = ""

class lexer():
    infile = None
    state = None
    char = ""

def lexer():
    if(not lexer.char):
        lexer.char = lexer.infile.read(1)
    lexeme = ""
    while(True):
        # print(lexer.state)
        for action in STATE_DIAGRAM[lexer.state]:
            # print(action)
            if action["check_function"](lexer.char):
                lexer.state = action["next_state"]
                if(action["append"]):
                    lexeme += lexer.char
                    lexer.char = lexer.infile.read(1)
                if(action["return"]):
                    return(action["return"], lexeme.strip())
                break

"""
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
"""
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
