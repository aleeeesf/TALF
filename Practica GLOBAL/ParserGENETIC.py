# Realizado por: Alejandro Serrano Fernández & Pedro Antonio Navas Luque. 
# Universidad de Cádiz, Mayo 2021.
# Proyecto: Lenguaje de programación para la configuración de algoritmos genéticos
# Este código incluye Parser e Intérprete del código introducido en 
# el fichero "code.txt". La sintáxis y características del leguaje
# queda definida en el manual de usuario que se ofrece.

from sly import Parser
from LexerGENETIC import lexerGENETIC
import numpy as np


class Gramatica(Parser):
    # Get the token list from the lexer (required)
    debugfile = 'parser.out'
    tokens = lexerGENETIC.tokens
    start = 'total'

# Aquí se definen las reglas. Cuando una regla llega a su final, se devuelven n-nodos
# Cuando se acabe de parsear, se obtendremos un árbol, que incluye todos 
# los nodos por los que hemos pasado a través de las reglas.
# return (nodo_izq, nodo_drcho,...) 

    #   ***     TOTAL       ***    
    @_('BEGIN typebegin')
    def total(self, p):
        return p.typebegin        
    

    @_('END')
    def typebegin(self, p):
        print("FINALIZADO")  
    

    @_('expr END POLICY_BEGIN LPAREN rules RPAREN POLICY_END')
    def typebegin(self, p):
        return ("nextconfig",p.expr,p.rules)




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




    #   ***     RULES       ***
    @_('rules polytypes')
    def rules(self, p):
        return ("next",p.rules,p.polytypes)
   
    
    @_('polytypes')
    def rules(self, p):
        return p.polytypes



    #   ***     CARACTERISTICAS       ***
    @_('caracteristicas sentence')
    def caracteristicas(self,p):
        return ("next",p.caracteristicas,p.sentence)


    @_('sentence')
    def caracteristicas(self,p): 
        return p.sentence




    #   ***     POLYTYPES       ***
    @_('GENERATIONS NUMBER PTOCOMA')
    def polytypes(self,p):
        return ("polysentence",expression("GENERATIONS",p.NUMBER,None,None))


    @_('INTERCHANGE NUMBER PTOCOMA')
    def polytypes(self,p):
        return ("polysentence",expression("INTERCHANGE",p.NUMBER,None,None))


    @_('SEND typesend PTOCOMA')
    def polytypes(self,p):
        return p.typesend


    @_('RECEIVE typereceive PTOCOMA')
    def polytypes(self,p):
        return p.typereceive




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



    #Tipos de send        
    @_('BEST')
    def typesend(self,p):
        return ("polysentence",expression("SEND","BEST",None,None))


    @_('RANDOM')
    def typesend(self,p):
        return ("polysentence",expression("SEND","RANDOM",None,None))



    #Tipos de receive
    @_('WORST')
    def typereceive(self,p):
        return ("polysentence",expression("RECEIVE","WORST",None,None))


    @_('RANDOM')
    def typereceive(self,p):
        return ("polysentence",expression("RECEIVE","RANDOM",None,None))




  

# Clase expresion: Almacena los elementos que se devuelven en una regla. 
# Almacena el nombre de la regla, y almacena hasta 3 elementos (Números, otra regla...)
class expression():

    def __init__(self,exprname, element, element2, element3):
        self.name = exprname
        self.fElement = element
        self.sElement = element2
        self.tElement = element3


# Interpreta las reglas por las que pasa el Parser. Hace uso de un 
# árbol binario para interpretarlas
class interpreter:    

    def __init__(self, tree):
        self.sentenceCounter = np.zeros(6)      # Cuenta cuántas configuraciones tiene la variable (del código) por la que pasamos
        self.policyCounter = np.zeros(4)        # Cuenta cuántas políticas tenemos definida en el código

        # Nombres de configuraciones: para determinar que configuración falta en una variable.
        self.sentenceNames = ["MUTATION","POBLATION","SELECTION","CROSSOVER","REPLACEMENT","FITNESS"]  
        # Nombres de políticas: para determinar que política falta en en el código.
        self.policyNames = ["INTERCHANGE","GENERATIONS","SEND","RECEIVE"]
        
        resultado = self.avanzarArbol(tree)        
        if resultado is not None and isinstance(resultado, int):
            print(resultado)
        if isinstance(resultado, str) and resultado[0] == '"':
            print(resultado)


    #Función recursiva que interpreta el árbol binario recibido por el parser
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


        if node[0] == 'nextconfig':            
            print("\n     *****   VARIABLES DEFINIDAS   *****")  
            self.avanzarArbol(node[1]) 
            
            print("\n\n     *****   POLITICAS DE INTERCAMBIOS   *****\n")           
            self.avanzarArbol(node[2])
            
            # Comprobamos si falta una política por definir
            findError = np.where(self.policyCounter == 0)[0]               
            # Si falta una, lanzar el error e indicar dónde se encuentra
            if findError.size != 0:                             
                raise ValueError("ERROR: Falta caracteristica %s en la politica "%(self.policyNames[findError[0]]))


        if node[0] == 'term': 
            if(node[1].name == "VARIABLE"):
                self.sentenceCounter = np.zeros(6)                              
                print("\n>Variable ",node[1].fElement," con las siguientes caracteristicas:")
                self.avanzarArbol(node[1].sElement)
                
                # Comprobamos si falta una configuración en la variable en la que nos encontramos
                findError = np.where(self.sentenceCounter == 0)[0]   
                # Si falta una, lanzar el error e indicar dónde se encuentra             
                if findError.size != 0:
                    raise ValueError("ERROR: Falta caracteristica %s en variable %s "%(self.sentenceNames[findError[0]],node[1].fElement))
                
            
        if node[0] == 'sentence':
            if node[1].name == "MUTATION":
                self.sentenceCounter[0] = 1
                if node[1].fElement == "BITFLIP":
                    print("  * Mutacion bitflip con %s elementos"%node[1].sElement)
                
                elif node[1].fElement == "POLYNOMIAL":
                    print("  * Mutacion polinomica con %s elementos"%node[1].sElement)

                else:
                    raise ValueError("ERROR: Error configuracion en MUTATION")


            if node[1].name == "POBLATION":
                self.sentenceCounter[1] = 1
                if node[1].fElement != None:
                    print("  * Población con %s elementos"%node[1].fElement)

                else:
                    print("ERROR: Error sintactico en POBLATION")


            if node[1].name == "SELECTION":
                self.sentenceCounter[2] = 1
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
                self.sentenceCounter[3] = 1
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
                self.sentenceCounter[4] = 1
                if node[1].fElement == "WORST":
                    print("  * Reemplazo (peor)")
               
                elif node[1].fElement == "RANDOM":
                    print("  * Reemplazo (mejor)")
            
                else:
                    raise ValueError("ERROR: Error sintactico en REPLACEMENT")            


            if node[1].name == "FITNESS":
                self.sentenceCounter[5] = 1
                print("  * Funcion FITNESS: %s"%node[1].fElement)


        if node[0] == 'polysentence':
            if node[1].name == "INTERCHANGE":
                self.policyCounter[0] = 1
                if node[1].fElement != None:
                    print("  * Intercambios de %s elementos"%node[1].fElement)

                else:
                    print("ERROR: Error sintactico en INTERCHANGES")
            

            if node[1].name == "GENERATIONS":
                self.policyCounter[1] = 1
                if node[1].fElement != None:
                    print("  * Intercambios cada %s generaciones"%node[1].fElement)

                else:
                    print("ERROR: Error sintactico en GENERATIONS")


            if node[1].name == "SEND":
                self.policyCounter[2] = 1
                if node[1].fElement == "BEST":
                    print("  * Enviando mejores individuos")
               
                elif node[1].fElement == "RANDOM":
                        print("  * Enviando individuos aleatoriamente")   
                    
                else:
                    raise ValueError("ERROR: Error configuracion en SEND")

            
            if node[1].name == "RECEIVE":
                self.policyCounter[3] = 1
                if node[1].fElement == "WORST":
                    print("  * Reeemplaza recibidos por sus peores individuos")
               
                elif node[1].fElement == "RANDOM":
                        print("  * Reeemplaza recibidos por alguno de sus individuos aleatoriamente")   
                    
                else:
                    raise ValueError("ERROR: Error configuracion en RECEIVE")




if __name__ == '__main__':
    lexer = lexerGENETIC()
    parser = Gramatica()   

    try:        
        text_file = open('code.txt')
        text = text_file.read()
        
        text_file.close()
       
        # Parseamos el código introducido
        tree = parser.parse(lexer.tokenize(text))
        # Interpretamos el árbol recibido por el parser
        interpreter(tree)

    except EOFError:
        print("Failed!")