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
    return char in ['+', '-', '*', '/', '(', ')', ';', '=']

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
            "check_function": my_isalpha,
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

class lexer():
    infile = None
    state = None
    char = None

def lexer():
    if(not lexer.char):
        lexer.char = lexer.infile.read(1)
    lexeme = ""
    while(True):
        # print(lexer.state)
        for action in STATE_DIAGRAM[lexer.state]:
            # print("action:", action, "lexeme:", f'"{lexeme}"')
            if action["check_function"](lexer.char):
                lexer.state = action["next_state"]
                if(action["append"]):
                    lexeme += lexer.char
                    lexer.char = lexer.infile.read(1)
                if(action["return"] or action["return"] == EOF):
                    return(action["return"], lexeme.strip())
                break

#=========================================================

input_string = []
infile = sys.stdin
lexer.infile = infile    # lexer's input file
lexer.state = START      # lexer's current state
lexer.char = None        # lexer's last character read
while True:
    tokenID, lexeme = lexer()
    if tokenID == EOF:
        break
    # print('{}\t{}'.format(tokname[tokenID], lexeme))
    elif tokenID == LITERAL:
        input_string.append(lexeme)
    elif tokenID == ERROR:
        input_string.append('?')
    else:
        input_string.append(tokname[tokenID])
print(input_string)

#=========================================================

S = 0
E = 1
Ep = 2
T = 3
Tp = 4
F = 5
A = 6

symbol_name = {
    S: 'S',
    E: 'E',
    Ep: 'Ep',
    T: 'T',
    Tp: 'Tp',
    F: 'F',
    A: 'A'
}

GRAMMAR = {
    # S  -> id = E ; S | ? S | epsilon
    S: [
        ['IDEN', '=', E, ';', S],
        ['?', S],
        []
    ],
    # E  -> T Ep
    E: [
        [T, Ep]
    ],
    # Ep -> + T Ep | - T Ep | epsilon
    Ep: [
        ['+', T, Ep],
        ['-', T, Ep],
        []
    ],
    # T  -> F Tp
    T: [
        [F, Tp]
    ],
    # Tp -> * F Tp | / F Tp | epsilon
    Tp: [
        ['*', F, Tp],
        ['/', F, Tp],
        []
    ],
    # F  -> id A | con | ( E )
    F: [
        ['IDEN', A],
        ['CONST'],
        ['(', E, ')']
    ],
    # A  -> ( E ) | epsilon
    A: [
        ['(', E, ')'],
        []
    ]
}

def parser(output_string, input_string):
    # print(symbol_name[symbol], input_string)
    output_ind = 0
    token_ind = 0
    current_token = input_string[token_ind]
    while(output_ind < len(output_string)):
        print(' '.join([symbol_name[char] if(type(char)==type(0)) else char for char in output_string]), output_ind, current_token)
        if(output_string[output_ind] not in GRAMMAR.keys()):
            output_ind += 1
            token_ind += 1
            current_token = input_string[token_ind]
            continue
        find_rule = False
        for rule in GRAMMAR[output_string[output_ind]]:
            if(len(rule) == 0):
                find_rule = True
                output_string = output_string[:output_ind] + output_string[output_ind+1:]
                break
            elif(rule[0] == current_token or rule[0] in GRAMMAR.keys()):
                find_rule = True
                output_string = output_string[:output_ind] + rule + output_string[output_ind+1:]
                break
        if(not find_rule):
            return ERROR
                    
    
    """
    if symbol in GRAMMAR.keys():
        for rule in GRAMMAR[symbol]:
            ind = 0
            this_rule = True
            for char in rule:
                if(char in GRAMMAR.keys()):
                    result = parser(char, input_string[ind:])
                    ind += len(result)-1
                    input_string[:ind-len(result)+1]+result+input_string[ind:]
                elif(input_string[ind] != char):
                    this_rule = False
                    break
                ind+=1
            if(this_rule):
                return rule+input_string[ind:]
    else:
        return symbol
    """            



parser([S], input_string)