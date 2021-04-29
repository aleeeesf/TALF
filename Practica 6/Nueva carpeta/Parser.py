from sly import Parser
from CalcLexer import CalcLexer

class Gramatica(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens

    # Grammar rules and actions
    def __init__(self):
        self.names = { }



    @_('statement PTOCOMA')
    def total(self, p):
        return p.statement   




    @_('ID ASSIGN expr')
    def statement(self, p):
        self.names[p.ID] = p.expr
        return p.expr    

    @_('ID ASSIGN statement')
    def statement(self, p):
        self.names[p.ID] = p.statement
        return p.statement   

    @_('ID')
    def statement(self, p):
        return self.names[p.ID]   

    @_('expr')
    def statement(self, p):
        return p.expr






    @_('expr PLUS term')
    def expr(self, p):
        return p.expr + p.term

    @_('expr MINUS term')
    def expr(self, p):
        return p.expr - p.term
    
    @_('term')
    def expr(self, p):
        return p.term

    @_('MINUS expr')
    def expr(self, p):
        return -p.expr





    @_('term TIMES factor')
    def term(self, p):
        return p.term * p.factor

    @_('term DIVIDE factor')
    def term(self, p):
        return p.term / p.factor

    @_('factor')
    def term(self, p):
        return p.factor
    




    @_('NUMBER')
    def factor(self, p):
        return p.NUMBER

    @_('MINUS factor')
    def factor(self, p):
        return -p.factor

    @_('ID')
    def factor(self, p):
        return self.names[p.ID]

    @_('LPAREN statement RPAREN')
    def factor(self, p):
        return p.statement




if __name__ == '__main__':
    lexer = CalcLexer()
    parser = Gramatica()

    while True:
        try:
            text = input('calc > ')
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break