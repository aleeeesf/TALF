import turtle
import copy
from sly import Parser
from LexerLOGO import lexerLOGO

t = turtle.Turtle()

class Gramatica(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = lexerLOGO.tokens
    start = 'total'

    
    @_('BEGIN expr END')
    def total(self, p):
        return p.expr 
        
    
    @_('BEGIN  END')
    def total(self, p):
        print("FINALIZADO")  
    
    
    @_('expr term')
    def expr(self, p):
        return ("next",p.expr,p.term)
   
    
    @_('term')
    def expr(self, p):
        return p.term
  

    @_('FORWARD NUMBER PTOCOMA')
    def term(self, p):
        return ("term",expression("FORWARD",p.NUMBER))
        

    @_('RIGHT NUMBER PTOCOMA')
    def term(self, p):
        return ('term',expression("RIGHT",p.NUMBER))
        

    @_('LEFT NUMBER PTOCOMA')
    def term(self, p):
        return ("term",expression("LEFT",p.NUMBER))
        

    @_('BACK NUMBER PTOCOMA')
    def term(self, p):
        return ('term',expression("BACK",p.NUMBER)) 
       

    @_('REPEAT NUMBER LPAREN expr RPAREN')
    def term(self, p):
        return ('term',expression("REPEAT",p.NUMBER),p.expr)




class expression():
    
    def __init__(self,exprname, num):
        self.name = exprname
        self.number = num


class interpreter:    

    def __init__(self, tree):
        resultado = self.avanzarArbol(tree)        
        if resultado is not None and isinstance(resultado, int):
            print(resultado)
        if isinstance(resultado, str) and resultado[0] == '"':
            print(resultado)

    def avanzarArbol(self, node):
        
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:            
            return None

        if node[0] == 'next':
            self.avanzarArbol(node[1])
            self.avanzarArbol(node[2])


        if node[0] == 'term':                        
            if(node[1].name == "FORWARD"):
                t.forward(node[1].number)

            if(node[1].name == "LEFT"):                
                if(node[1].number >= 0 and node[1].number <= 360):
                    t.left(node[1].number)
                else:
                    raise ValueError("El angulo sobrepasa los valores")

            if(node[1].name == "RIGHT"):
                if(node[1].number >= 0 and node[1].number <= 360):
                    t.right(node[1].number)
                else:
                    raise ValueError("El angulo sobrepasa los valores")

            if(node[1].name == "BACK"):
                t.back(node[1].number)
            

            if(node[1].name == "REPEAT"):
                for i in range(node[1].number):
                   self.avanzarArbol(node[2])
     


if __name__ == '__main__':
    lexer = lexerLOGO()
    parser = Gramatica()   

    try:        
        text_file = open('code.txt')
        text = text_file.read()
        
        text_file.close()
       
        tree = parser.parse(lexer.tokenize(text))
        interpreter(tree)
        turtle.exitonclick()
        turtle.bye()

    except EOFError:
        print("Failed!")