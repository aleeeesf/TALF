from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { LIBRARY,NUMBER, ID,
               PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
               EQ, LT, LE, GT, GE, NE,  IF, ELSE, WHILE, 
                PRINT, RETURN, INT, FLOAT, STRING, 
                CHAR, BREAK, SCAN, POINT, COMMENT, CONST}

    literals = { '(', ')', '{', '}', ';', '.', ',', '"', ",", ':', '%', '&'}
    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_newline = r'\n+'
    ignore_comment = r'\/\/.*'
    ignore_comment2 = r'\/\*.*'
    ignore_comment3 = r'.*\*\/'
    ignore_string = r'\".*\"'


    # Regular expression rules for tokens    

    ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if']        = IF
    ID['else']      = ELSE
    ID['while']     = WHILE
    ID['printf']    = PRINT
    ID['return']    = RETURN
    ID['int']       = INT
    ID['float']     = FLOAT
    ID['char']      = CHAR
    ID['break']     = BREAK
    ID['scanf']     = SCAN

    LIBRARY = r'\#include\s\<.*\>'
    CONST   = r'\#define\s.*\s[0-9]*\.[0-9]*'
    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    EQ      = r'=='
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'
    GE      = r'>='
    GT      = r'>'
    NE      = r'!='



    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return columnN

    def error(self, t):
            self.index += 1

if __name__ == '__main__':
    accepted = ['IF', 'ELSE', 'WHILE', 'FOR', 'RETURN', 'INT', 'FLOAT', 'CHAR', 'ID', 'CONST', 'LIBRARY']
    lexer = CalcLexer()
    f = open('prime.c','r')
    Lines = f.readlines()
    f.close()
    linea = 0
    for data in Lines:
        linea += 1
        for tok in lexer.tokenize(data):
            if tok.type in accepted:
                print('type=%r, value=%r, line = %r' % (tok.type, tok.value, linea))

    

