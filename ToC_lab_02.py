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
        input_string.append('')
        break
    elif tokenID == LITERAL:
        input_string.append(lexeme)
    elif tokenID == ERROR:
        input_string.append('?')
    else:
        input_string.append(tokenID)

#=========================================================

S = 10
E = 11
Ep = 12
T = 13
Tp = 14
F = 15
A = 16
Eps = 17

symbol_map = {
    S: 'S',
    E: 'E',
    Ep: 'Ep',
    T: 'T',
    Tp: 'Tp',
    F: 'F',
    A: 'A',
    IDEN: 'id',
    CONST: 'con'
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

PARSING_TBL = {
    "HEADER": [IDEN, CONST, '+', '-', '*', '/', '(', ')', '?', ';', ''],
    S: [[IDEN, '=', E, ';', S], [], [], [], [], [], [], [], ['?', S], [], [Eps]],
    E: [[T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep], [T, Ep]],
    Ep: [[Eps], [Eps], ['+', T, Ep], ['-', T, Ep], [Eps], [Eps], [Eps], [Eps], [Eps], [Eps], [Eps]],
    T: [[F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp], [F, Tp]],
    Tp: [[Eps], [Eps], [Eps], [Eps], ['*', F, Tp], ['/', F, Tp], [Eps], [Eps], [Eps], [Eps], [Eps]],
    F: [[IDEN, A], [CONST], [], [], [], [], ['(', E, ')'], [], [], [], []],
    A: [[Eps], [Eps], [Eps], [Eps], [Eps], [Eps], ['(', E, ')'], [Eps], [Eps], [Eps], [Eps]]
}

def parser(input_string):
    output_string = []
    stack = [S]
    while(input_string and stack):
        current_token = stack[-1]
        #print(input_string, current_token, stack)
        stack.pop(-1)
        if(input_string[0]== current_token):
            output_string.append(input_string[0])
            input_string = input_string[1:]
            continue
        print("L=>", ' '.join([symbol_map[char] if(char in symbol_map.keys()) else char for char in output_string]), end=' ' if output_string else '')
        print(symbol_map[current_token] if current_token in symbol_map else current_token, end = ' ')
        print(' '.join([symbol_map[char] if(char in symbol_map.keys()) else char for char in stack[::-1]]))
        if(input_string[0] not in PARSING_TBL['HEADER']):
            print("L=>")
            print("parse error")
            return None
        col_ind = PARSING_TBL['HEADER'].index(input_string[0])
        if(current_token not in PARSING_TBL):
            print("parse error")
            return None
        if(PARSING_TBL[current_token][col_ind] == []):
            print("parse error")
            return None
        if(PARSING_TBL[current_token][col_ind] == [Eps]):
            continue
        stack = stack + PARSING_TBL[current_token][col_ind][::-1]
    print("L=>", ' '.join([symbol_map[char] if(char in symbol_map.keys()) else char for char in output_string]))

parser(input_string)