from sly import Lexer

class lexerLOGO(Lexer):
    # Set of token names.   This is always required
    tokens = {BEGIN, END, FORWARD, RIGHT, LEFT, BACK, REPEAT, NUMBER, LPAREN, RPAREN, PTOCOMA}

    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_newline = '\n'
    # Regular expression rules for tokens

    BEGIN = 'BEGIN'
    END = 'END'
    FORWARD = 'FORWARD'
    RIGHT = 'RIGHT'  
    LEFT = 'LEFT' 
    BACK = 'BACK' 
    REPEAT = 'REPEAT'


    NUMBER  = r'\d+'
    LPAREN  = r'\['
    RPAREN  = r'\]'
    PTOCOMA  = r'\;'
    #NEWLINE = r'\n'
    #VACIO = r' '

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

if __name__ == '__main__':
    #data = 'REPEAT 60 [FORWARD 360; \n LEFT 40;]'
    text_file = open('code.txt')
    data = text_file.read()
    text_file.close()
    lexer = lexerLOGO()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
