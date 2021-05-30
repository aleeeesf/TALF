from sly import Parser
from LexerGENETIC import lexerGENETIC
import numpy as np

class Gramatica(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = lexerGENETIC.tokens
    start = 'total'

    #   ***     TOTAL       ***    
    @_('BEGIN typebegin')
    def total(self, p):
        return p.typebegin        
    
    @_('END')
    def typebegin(self, p):
        print("FINALIZADO")  
    
    @_('expr END')
    def typebegin(self, p):
        return p.expr   


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
        

    @_('FITNESS EQUATION PTOCOMA')
    def sentence(self,p):
        return ("sentence",expression("FITNESS",p.EQUATION,None,None))


    @_('INTERCHANGE NUMBER PTOCOMA')
    def sentence(self,p):
        return ("sentence",expression("INTERCHANGE",p.NUMBER,None,None))
        



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


class expression():

    def __init__(self,exprname, element, element2, element3):
        self.name = exprname
        self.fElement = element
        self.sElement = element2
        self.tElement = element3


class interpreter:    

    def __init__(self, tree):
        self.charCounter = np.zeros(7)
        self.charNames = ["MUTATION","POBLATION","SELECTION","CROSSOVER","REPLACEMENT","INTERCHANGES","FITNESS"]
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
                self.charCounter = np.zeros(7)
                print("\n>Variable ",node[1].fElement," con las siguientes caracteristicas:")
                self.avanzarArbol(node[1].sElement)
                
                findError = np.where(self.charCounter == 0)[0]                
                if findError.size != 0:
                    raise ValueError("ERROR: Falta caracteristica %s en variable %s "%(self.charNames[findError[0]],node[1].fElement))
               
            
        if node[0] == 'sentence':            
            if node[1].name == "MUTATION":
                self.charCounter[0] = 1
                if node[1].fElement == "BITFLIP":
                    print("  * Mutacion bitflip con %s elementos"%node[1].sElement)
                
                elif node[1].fElement == "POLYNOMIAL":
                    print("  * Mutacion polinomica con %s elementos"%node[1].sElement)

                else:
                    raise ValueError("ERROR: Error configuracion en MUTATION")


            if node[1].name == "POBLATION":
                self.charCounter[1] = 1
                if node[1].fElement != None:
                    print("  * Población con %s elementos"%node[1].fElement)

                else:
                    print("ERROR: Error sintactico en POBLATION")



            if node[1].name == "SELECTION":
                self.charCounter[2] = 1
                if node[1].fElement == "TOURNAMENT":
                    print("  * Seleccion por torneo con %s elementos"%node[1].sElement)
               
                else:
                    if node[1].fElement == "ROULETTE":
                        print("  * Seleccion por ruleta")
                    
                    elif node[1].fElement == "RANKING":
                        print("  * Seleccion por ranking")
                    
                    else:
                        raise ValueError("ERROR: Error configuracion en SELECTION")


            if node[1].name == "CROSSOVER":
                self.charCounter[3] = 1
                if node[1].sElement != None:
                    if node[1].fElement < node[1].sElement:
                        print("  * Crossover con punto de corte en %s y en %s"%(node[1].fElement,node[1].sElement))
                    
                    else:
                        raise ValueError("ERROR: El primer punto es mayor que el segundo")
               
                elif node[1].sElement == None:
                    print("  * Crossover con punto de corte en %s"%node[1].fElement)
                
                else:
                    raise ValueError("ERROR: Error sintactico en CROSSOVER")


            if node[1].name == "REPLACEMENT":
                self.charCounter[4] = 1
                if node[1].fElement == "WORST":
                    print("  * Reemplazo (peor)")
               
                elif node[1].fElement == "RANDOM":
                    print("  * Reemplazo (mejor)")
            
                else:
                    raise ValueError("ERROR: Error sintactico en REPLACEMENT")


            if node[1].name == "INTERCHANGE":
                self.charCounter[5] = 1
                if node[1].fElement != None:
                    print("  * Intercambios de %s elementos"%node[1].fElement)

                else:
                    print("ERROR: Error sintactico en INTERCHANGES")

            if node[1].name == "FITNESS":
                self.charCounter[6] = 1
                print("  * Funcion FITNESS: %s"%node[1].fElement)

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