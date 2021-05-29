from sly import Parser
from LexerGENETIC import lexerGENETIC
import numpy as np

class Gramatica(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = lexerGENETIC.tokens
    start = 'total'

    #   ***     TOTAL       ***    
    @_('BEGIN expr END')
    def total(self, p):
        return p.expr 
        
    
    @_('BEGIN  END')
    def total(self, p):
        print("FINALIZADO")  
    



    #   ***     TERM       ***
    @_('expr term')
    def expr(self, p):
        return ("next",p.expr,p.term)
   
    
    @_('term')
    def expr(self, p):
        return p.term


    @_('ID LPAREN caracteristicas RPAREN')
    def term(self,p):
        return ("term",expression("VARIABLE",p.ID,p.caracteristicas,None))




#   ***     CARACTERISTICAS       ***
    @_('caracteristicas sentence')
    def caracteristicas(self,p):
        return ("next",p.caracteristicas,p.sentence)


    @_('sentence')
    def caracteristicas(self,p): 
        return p.sentence




    #   ***     SENTENCE       ***
    @_('POBLATION NUMBER PTOCOMA')
    def sentence(self,p):
        return ("sentence",expression("POBLATION",p.NUMBER,None,None))


    @_('MUTATION typemutation PTOCOMA')
    def sentence(self,p):
        return p.typemutation
        

    @_('REPLACEMENT typereplace PTOCOMA')
    def sentence(self,p):
        return p.typereplace
        

    @_('CROSSOVER NUMBER typecross')
    def sentence(self,p):
        return ("sentence",expression("CROSSOVER",p.NUMBER,p.typecross,None))


    @_('SELECTION typeselection PTOCOMA')
    def sentence(self,p):
        return p.typeselection
        

    @_('FITNESS typefitness PTOCOMA')
    def sentence(self,p):
        return p.typefitness
        



    #   ***     TYPES       ***

    #Tipos de mutación
    @_('BITFLIP NUMBER')
    def typemutation(self,p):        
        return ("sentence",expression("MUTATION","BITFLIP",p.NUMBER,None))

    @_('POLYNOMIAL NUMBER')
    def typemutation(self,p):        
        return ("sentence",expression("MUTATION","POLYNOMIAL",p.NUMBER,None))



    #Tipos de selección
    @_('TOURNAMENT NUMBER')
    def typeselection(self,p):
        return ("sentence",expression("SELECTION","TOURNAMENT",p.NUMBER,None))

    @_('ROULETTE')
    def typeselection(self,p):
        return ("sentence",expression("SELECTION","roulette",None,None))

    @_('RANKING')
    def typeselection(self,p):
        return ("sentence",expression("SELECTION","RANKING",None,None))



    #Tipos de Reemplazo
    @_('WORST')
    def typereplace(self,p):
        return ("sentence",expression("REPLACEMENT","WORST",None,None))

    @_('RANDOM')
    def typereplace(self,p):
        return ("sentence",expression("REPLACEMENT","RANDOM",None,None))



    #Tipos de Crossover
    @_('PTOCOMA')
    def typecross(self,p):
        return None

    @_('AND NUMBER PTOCOMA')
    def typecross(self,p):
        return p.NUMBER



    #Tipos de Fitness
    @_('PTOCOMA')
    def typefitness(self,p):
        print('1 NUMERO')

    @_('AND NUMBER PTOCOMA')
    def typefitness(self,p):
        print('2 NUMEROS')


class expression():

    def __init__(self,exprname, element, element2, element3):
        self.name = exprname
        self.fElement = element
        self.sElement = element2
        self.tElement = element3


class interpreter:    

    def __init__(self, tree):
        self.charCounter = np.zeros(5)
        self.charNames = ["MUTATION","POBLATION","SELECTION","CROSSOVER","REPLACEMENT","FITNESS"]
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
            if(node[1].name == "VARIABLE"):
                self.charCounter = np.zeros(5)
                print("\n>Variable ",node[1].fElement," con las siguientes caracteristicas:")
                self.avanzarArbol(node[1].sElement)
                
                findError = np.where(self.charCounter == 0)[0]
                print(findError)
                if findError.size != 0:
                    raise ValueError("ERROR: Falta configuracion en ",node[1].fElement, " caracteristica: ",self.charCounter[findError])
               
            
        if node[0] == 'sentence':            
            if node[1].name == "MUTATION":
                self.charCounter[0] = 1
                if node[1].fElement == "BITFLIP":
                    print("  * Mutacion bitflip con ",node[1].sElement," elementos")
                
                elif node[1].fElement == "POLYNOMIAL":
                    print("  * Mutacion polinomica con ",node[1].sElement," elementos")

                else:
                    raise ValueError("ERROR CONFIGURACION EN MUTACION")

            if node[1].name == "POBLATION":
                self.charCounter[1] = 1
                if node[1].fElement != None:
                    print("  * Población con ",node[1].fElement," elementos")

                else:
                    print("ERROR SINTÁCTICO EN POBLACION")



            if node[1].name == "SELECTION":
                self.charCounter[2] = 1
                if node[1].fElement == "TOURNAMENT":
                    print("  * Seleccion por torneo con ",node[1].sElement," elementos")
               
                else:
                    if node[1].fElement == "ROULETTE":
                        print("  * Seleccion por ruleta")
                    
                    elif node[1].fElement == "RANKING":
                        print("  * Seleccion por ranking")
                    
                    else:
                        raise ValueError("ERROR CONFIGURACION EN SELECCION")


            if node[1].name == "CROSSOVER":
                self.charCounter[3] = 1
                if node[1].sElement != None:
                    if node[1].fElement < node[1].sElement:
                        print("  * Crossover con punto de corte en ",node[1].fElement," y en ",node[1].sElement)
                    
                    else:
                        raise ValueError("ERROR: PRIMER PUNTO MENOR QUE EL SEGUNDO")
               
                elif node[1].sElement == None:
                    print("  * Crossover con punto de corte en ",node[1].fElement)
                
                else:
                    raise ValueError("ERROR SINTACTICO EN CROSSOVER")


            if node[1].name == "REPLACEMENT":
                self.charCounter[4] = 1
                if node[1].fElement == "WORST":
                    print("  * Reemplazo (peor)")
               
                elif node[1].fElement == "RANDOM":
                    print("  * Reemplazo (mejor)")
            
                else:
                    raise ValueError("ERROR SINTACTICO EN REEMPLAZO")


            if node[1].name == "FITNESS":
                self.charCounter[5] = 1
                print("FALTA PONER")

if __name__ == '__main__':
    lexer = lexerGENETIC()
    parser = Gramatica()   

    try:        
        text_file = open('code.txt')
        text = text_file.read()
        
        text_file.close()
       
        tree = parser.parse(lexer.tokenize(text))
        interpreter(tree)

    except EOFError:
        print("Failed!")