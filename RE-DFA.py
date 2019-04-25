#179 libro dragon morado
from pythonds.basic.stack import Stack
from collections import defaultdict
import os
import sys
def infixToPostfix(infixexpr): 
    '''convierte expresion regular de forma infija a postfija'''
    prec = {}
    prec["*"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []

    for token in infixexpr:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvwyz" or token in "0123456789#":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)


def ponPuntos(re):
	'''Metodo de preprocesamiento para agregar puntos en las concatenaciones'''
	op = ["(","|",".",")"]
	aux = ""
	i = 0
	n = 0
	#print(len(re))
	while (i + 1) < len(re):
		
		if re[i] in op:
			if re[i] == ")" and re[i+1] == "+" or re[i+1] == "*":
				aux += re[i]
				aux += re[i+1]
			elif re[i] == ")" and re[i+1] not in op and re[i+1] != "+" and re[i+1] != "*":
				aux += re[i]
				aux+= "."
				#aux += re[i+1]
			else:
				aux += re[i]

		elif re[i] == "+" or re[i] == "*":
			if(re[i+1] not in op) or re[i+1] == "(":
				aux+= "."
			
			
		elif re[i] not in op and re[i + 1] not in op and re[i + 1] != "*" and re[i + 1] != "+":
			aux += re[i]
			aux += "."
					
		elif re[i] not in op and re[i + 1] == "*" or re[i + 1] == "+":
			aux += re[i]
			aux += re[i+1]
				
		elif (re[i] not in op and re[i+1] in op):
			aux += re[i]
		else:
			print("NO C")
			print(aux)
			break
		i+=1
		n = i
		if re[i] not in op and re[i] != "*" and re[i] != "+" and n + 1 == len(re):
			#print("entra")
			aux += re[i]
	return aux




def postorden(arbol):
	if not arbol.leaf:
		if arbol.one:
			postorden(arbol.left_child)
			if arbol.value == "*":
				arbol.nullable = True
			else:
				arbol.nullable = arbol.left_child.nullable 
		else:
			postorden(arbol.left_child)
			postorden(arbol.right_child)
			if arbol.value == "|":
				arbol.nullable = arbol.left_child.nullable or arbol.right_child.nullable
			elif arbol.value == ".":
				arbol.nullable = arbol.left_child.nullable and arbol.right_child.nullable
		#print(arbol.value)
	else:
		#print(arbol.value)
		arbol.nullable = False

def postorden_followpos(arbol):
	''' recorrido en preorden para crear tabla de siguientes'''
	if not arbol.leaf:
		if arbol.one:
			postorden_followpos(arbol.left_child)
			for i in range(len(arbol.lastpos)):
				for j in range(len(arbol.firstpos)):
					#print("---->" + str(arbol.lastpos[i]))
					Node.followpos[arbol.lastpos[i]].append(arbol.firstpos[j])
		else:
			postorden_followpos(arbol.left_child)
			postorden_followpos(arbol.right_child)
			if arbol.value == ".":
				for i in range(len(arbol.left_child.lastpos)):
					for j in range(len(arbol.right_child.firstpos)):
						Node.followpos[arbol.left_child.lastpos[i]].append(arbol.right_child.firstpos[j])
	
		

def postorden_firstpos(arbol):
	''' recorrido en preorden para  agregar firspos y lastpos'''
	if not arbol.leaf:
		if arbol.one:
			postorden_firstpos(arbol.left_child)
			arbol.firstpos = arbol.left_child.firstpos
			arbol.lastpos = arbol.left_child.lastpos
		else:
			postorden_firstpos(arbol.left_child)
			postorden_firstpos(arbol.right_child)
			if arbol.value == "|":
				arbol.firstpos = arbol.left_child.firstpos + arbol.right_child.firstpos
				arbol.lastpos = arbol.left_child.lastpos + arbol.right_child.lastpos
			else:
				if arbol.left_child.nullable == True:
					arbol.firstpos = arbol.left_child.firstpos + arbol.right_child.firstpos
				else:
					arbol.firstpos = arbol.left_child.firstpos
				if arbol.right_child.nullable == True:
					arbol.lastpos = arbol.left_child.lastpos + arbol.right_child.lastpos
				else:
					arbol.lastpos = arbol.right_child.lastpos

def createDictionary(arbol):
	''' recorrido en preorden para crear diccionario {nombre: 'caracter'}'''
	if not arbol.leaf:
		if arbol.one:
			createDictionary(arbol.left_child)
		else:
			createDictionary(arbol.left_child)
			createDictionary(arbol.right_child)
	else:
		Node.dictionaryofpos[arbol.name] = arbol.value
			
class Node(object):
	'''clase NODO para arbol'''
	aux = "" #auxiliar para declarar .gv
	aux2 = "" #auxiliar parara declarar conexiones .gv
	total_of_nodes = 0 #atributo auxiliar para nombrar nodo
	nameaux = 1
	followpos = defaultdict(list)
	dictionaryofpos = {}
	def __init__(self,value,leaf = False,one=True,center_child=False,right_child=False,left_child=False,nullable=False,name = 0):
		#print(firstpos)
		self.firstpos = [] 
		self.lastpos  = []
		self.value = value
		self.leaf = leaf
		self.one = one
		self.nullable = nullable
		self.number = Node.total_of_nodes
		self.name = name
		Node.total_of_nodes += 1
		if leaf == False:
			if one:
				self.left_child = center_child
			else:
				self.left_child = left_child  
				self.right_child = right_child



	def preordenConection(self):
		''' recorrido en preorden para  declarar conexiones en archivo .gv'''
		#s = "	node" + str(self.number) + "[label =\""+ "" +str(self.firstpos)+"\t "+self.value+ " \t" + str(self.lastpos) + "\"];\n"
		s = "node" +str(self.number) + "[label=<<TABLE BORDER=\"0\" CELLBORDER=\"1\" CELLSPACING=\"0\"> \
			<TR><TD>"+str(self.firstpos)+"</TD><TD>  "+self.value+"  </TD><TD>"+str(self.lastpos)+"</TD></TR> \
			</TABLE>>];"
		Node.aux += s
		#print("valor: " + self.value + " nullable: " + str(self.nullable) + " Name: " + str(self.name) + "\n")
		#print("firstpos: " + str(self.firstpos))
		#print("lastpos: " + str(self.lastpos))
		#print("\n")
		if not self.leaf:
			if not self.one:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.aux2 += s
					self.left_child.preordenConection()
				if self.right_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.right_child.number) + "[dir=none]" +  "\n"
					Node.aux2 += s
					self.right_child.preordenConection()
			else:
				if self.left_child:
					
					s = "	node" + str(self.number) + " -> " + "node" + str(self.left_child.number) + "[dir=none]" + "\n"
					Node.aux2 += s
					self.left_child.preordenConection()
	

class RegularExpresion(object):
	"""docstring for RegularExpresion"""
	def __init__(self, regexp):
		self.infix = ponPuntos("(" + regexp + ")#") #agrega hashtag y pone puntos en las concatenaciones
		self.postfix = infixToPostfix(self.infix) #convierte de infijo a postfijo

	

	def re_to_syntaxTree(self):
		'''convierte expresion regular a syntax tree'''
		stack = []
		postfix = infixToPostfix(self.infix)
		for s in postfix:
			'''itera la expresion postfija '''
			if s == '*':
				t = stack.pop() #saca el ultimo dato de la lista 
				stack.append(Node(s,center_child=t)) #crea nodo con valor s y agrega t como único hijo 
			elif s == '+':
				t = stack.pop() #saca el ultimo dato de la lista
				stack.append(Node(s,center_child=t)) #crea nodo con valor s y agrega t como único hijo
			elif s == '|':
				right = stack.pop() #saca ultimo dato de la lista
				left = stack.pop() #saca penultimo dato de la lista
				stack.append(Node(s,one=False,right_child = right,left_child=left)) #crea nodo con valor s y agrega right como hijo derecho y left como hijo izquierdo
			elif s == '.':
				right = stack.pop() #saca ultimo dato de la lista
				left = stack.pop() #saca penultimo dato de la lista
				stack.append(Node(s,one=False,right_child = right,left_child=left)) #crea nodo con valor s y agrega right como hijo derecho y left como hijo izquierdo
			else:
				new_leaf = Node(s,leaf=True) #crea hoja, no agrega hijos al nodo 
				new_leaf.name = Node.nameaux
				new_leaf.firstpos.append(new_leaf.name)
				new_leaf.lastpos.append(new_leaf.name)
				Node.nameaux+=1
				stack.append(new_leaf) #inserta al final de la lista
		return stack.pop() #regresa el ultimo valor de la lista, que es el arbol final

	def write_graphviz(self,syntax_tree):
		'''crea archivo .gv para dibujar arbol sintactico'''
		f= open("syntax_tree.gv","w+")
		f.write("digraph AFN{\n")
		f.write("rankdir=TB;\n    node[shape = plaintext] ;\n")
		f.write(Node.aux) 
		f.write(Node.aux2)
		f.write("\n}")
		f.close()
		os.system("dot -Tgif syntax_tree.gv > st.gif") #ejecuta comando para compilar gv y la salida es redirigida a una imagen .gif

class State(object):
	'''Clase State para cada estado del DFN'''
	def __init__(self,values):
		self.marked = False #marked para saber si ya reviso 
		self.values = values #lista de valores del estado
		self.transitions = defaultdict(list) #diccionario de transisiones

	def __str__(self):
		return "values: " + str(self.values) + "\ntransitions: " + str(list(self.transitions.items())) + "\n"

class DFA(object):
	'''Clase DFA (automata finito determinisata) '''
	def __init__(self,tree,dictionaryofpos,followpos):
		self.states = [] #lista de estados objetos tipo State
		self.tree = tree #arbol sintactico
		self.dictionaryofpos = dictionaryofpos #diccionario {nombre = 'caracter'}
		self.followpos = followpos #tabla de siguientes
		self.initialState = State(tree.firstpos) #estado inicial firstpos de la raiz del arbol
		self.states.append(self.initialState) #agrega estado inicial a lista de estados
		self.final_state = max(list(dictionaryofpos.keys())) #estado final nombre del hashtag

	def printTransitions(self):
		'''Imprime las transiciones del DFA'''
		for s in self.states:
			print(str(s))

	def write_dfa_graphviz(self):
		'''Escribe archivo .gv para dibujar DFA'''
		dic = {}
		i = 1
		f= open("DFA.gv","w+")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR;\n    node[shape = circle] ;\n")
		f.write("nodeI [shape=point];\n")
		for s in self.states:
			n = "node"+str(i)
			dic[str(s.values)] = n
			if self.final_state not in s.values: 
				#si no es final
				f.write(n + "[label=\""+str(s.values)+"\"];\n")
			else:
				#si es final
				f.write(n + "[label=\""+str(s.values)+"\" shape=\"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label=I];\n")
		for s in self.states:
			for label, state in s.transitions.items():
				f.write(dic[str(s.values)]+"->"+dic[str(state)] + "[label = "+label+"];\n")
		f.write("\n}")
		f.close()
		os.system("dot -Tgif DFA.gv > DFA.gif") #ejecuta comando para compilar gv y la salida es redirigida a una imagen .gif

	def list_of_states(self):
		#escribe lista de estados
		state_aux = []
		for s in self.states:
			state_aux.append(s.values)
		return state_aux

	def check_mark(self):
		#verifica si el estado ya fue revisado
		r = True
		for s in self.states:
			if not s.marked:
				r = False
				break
			else:
				continue
		return r

	def get_unmarked_state(self):
		'''Regresa estado sin revisar '''
		for s in self.states:
			if not s.marked:
				return s,self.states.index(s)

	def createDFA(self):
		#crea automata y sus transiciones
		while(self.check_mark() != True):
			print(self.check_mark())
			current_states = self.list_of_states()
			#print(current_states)
			state, i = self.get_unmarked_state()
			self.states[i].marked = True
			for v in state.values:
				if v == self.final_state:
					continue
				else:
					state.transitions[self.dictionaryofpos[v]] += self.followpos[v]
					state.transitions[self.dictionaryofpos[v]] = list(set(state.transitions[self.dictionaryofpos[v]]))
			print("termina")
			for ns in list(state.transitions.values()):
				if ns not in current_states:
					self.states.append(State(ns))


if __name__ == '__main__':
	#re = RegularExpresion("((ab+|a+b)*|(bc|ab|a*))+")
	re = RegularExpresion(str(sys.argv[1]))
	#re = RegularExpresion("(abc*|cb*)+")
	tree = re.re_to_syntaxTree()
	postorden(tree)
	postorden_firstpos(tree)
	postorden_followpos(tree)
	tree.preordenConection()
	re.write_graphviz(tree)
	print("name")
	createDictionary(tree)
	print(Node.dictionaryofpos)
	print('Position followpos')
	for name, followpos in sorted(Node.followpos.items()):
		print('{}\t{}'.format(name, set(followpos)))
	print("\nDFA\n")
	dfa = DFA(tree,Node.dictionaryofpos,Node.followpos)

	dfa.createDFA()

	dfa.printTransitions()
	dfa.write_dfa_graphviz()
