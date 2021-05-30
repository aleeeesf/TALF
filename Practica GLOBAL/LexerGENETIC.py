# Realizado por: Alejandro Serrano Fernández & Pedro Antonio Navas Luque. 
# Universidad de Cádiz, Mayo 2021.
# Proyecto: Lenguaje de programación para la configuración de algoritmos genéticos
# Este código incluye Lexer del código introducido en 
# el fichero "code.txt". La sintáxis y características del leguaje
# queda definida en el manual de usuario que se ofrece.

from sly import Lexer

class lexerGENETIC(Lexer):
    # Set of token names.   This is always required
    tokens = {  ID, EQUATION, BEGIN, END, POLICY_BEGIN, POLICY_END, POBLATION, FITNESS, 
                SELECTION, CROSSOVER, MUTATION, REPLACEMENT, INTERCHANGE, SEND, RECEIVE, GENERATIONS,
                TOURNAMENT, ROULETTE, RANKING, BITFLIP, POLYNOMIAL, WORST, RANDOM, BEST,
                NUMBER, LPAREN, RPAREN, PTOCOMA, AND
             }


    # String containing ignored characters between tokens
    ignore = ' \t'
    ignore_newline = '\n'
    
    
    # Regular expression rules for tokens   
    BEGIN           = 'BEGIN'
    END             = 'END'
    POLICY_BEGIN    = 'POLICY_BEGIN'
    POLICY_END      = 'POLICY_END'
    POBLATION       = 'POBLATION'
    FITNESS         = 'FITNESS'  
    SELECTION       = 'SELECTION' 
    CROSSOVER       = 'CROSSOVER' 
    MUTATION        = 'MUTATION'
    REPLACEMENT     = 'REPLACEMENT'
    INTERCHANGE     = 'INTERCHANGE'
    GENERATIONS     = 'GENERATIONS'
    SEND            = 'SEND'
    RECEIVE         = 'RECEIVE'


    TOURNAMENT      = 'TOURNAMENT'
    ROULETTE        = 'ROULETTE'
    RANKING         = 'RANKING'
    BITFLIP         = 'BITFLIP'
    POLYNOMIAL      = 'POLYNOMIAL'
    BEST            = 'BEST'
    WORST           = 'WORST'
    RANDOM          = 'RANDOM'


    NUMBER          = r'\d+'
    EQUATION        = r'(?:[0-9-+*/^()x])+'
    ID              = r'[a-zA-Z_][a-zA-Z0-9_]*'


    LPAREN          = r'\['
    RPAREN          = r'\]'
    PTOCOMA         = r'\;'
    AND             = r'\|'


    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    #Función para lanza error
    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1



if __name__ == '__main__':
    text_file = open('code.txt')
    data = text_file.read()
    text_file.close()
    lexer = lexerGENETIC()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
