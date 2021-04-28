
class Grafo:
    def __init__(self):
        self.lista_vizinhos = {}
        self.lista_vertices = {}
    
    def add_vertice(self, vertice):
        self.lista_vertices[vertice] = True
    
    def add_aresta(self, qa, qb, palavra):
    	#se nao existe estado qa nao add
        if not qa in self.lista_vizinhos:
            self.lista_vizinhos[qa] = []
        #add qb e w como uma transicao de qa
        self.lista_vizinhos[qa].append([palavra,qb])
    
    def transicoes(self, qa):
        if qa in self.lista_vizinhos:
        	#retorna as transicoes de um estado qa
            return self.lista_vizinhos[qa]
        else:
            return []
    
    def estados(self):
        return self.lista_vertices.keys()

    def deleta_aresta(self, vertice, outro_vertice):
        self.vizinhos(vertice).remove(outro_vertice)
    
    def deleta_vertice(self, vertice):
        for outro_vertice in self.lista_vizinhos[vertice]:
            self.deleta_aresta(vertice, outro_vertice)
        del self.lista_vizinhos[vertice]
        del self.lista_vertices[vertice]
        


def aceita_W(w,Grafo):

    w = w.split(",")#entrada da palavra separada por virgula
    invalido=False
    estadoAtual = estadoI
    resp = True
    caminho=[('Inicio',estadoAtual)]
    for i in w:
        proximo_estado = False
        t = Grafo.transicoes(estadoAtual)
        for j in Grafo.transicoes(estadoAtual):
            if i == j[0]:
                proximo_estado = True
                estadoAtual = j[1]
                caminho.append((i,estadoAtual))
        if proximo_estado == False:
            resp = False
            invalido=True
            break


    for e in estadoF:
        if e == estadoAtual:
            resp = True 

    if resp == False or invalido:
        return False,caminho
    else:
        return True,caminho


# ============Leitura do arquivo================
file = open("arquivodeentrada.txt", "r")
words = []
transitions = []
#Leitura do arquivo
for i in file:
    for word in i.split():
        words.append(word)

#Organização do arquivo
AFD = words[0]
AFD_aux = AFD.split("{")
estados = AFD_aux[1].split(',')
estados.pop()
estados[len(estados)-1]=estados[len(estados)-1].replace("}","")


palavras = AFD_aux[2].split('}')
palavras= palavras[0].split(',')



estadoI = AFD_aux[2].split('}')[1]
estadoI = estadoI.replace(",","")

estadoF = AFD_aux[3].split(',')
estadoF[len(estadoF)-1]= estadoF[len(estadoF)-1].replace("})","")

for i in range (2, len(words)):
    transitions.append(words [i])

Grafo = Grafo()
#============Criando AFD=======================

#adiciona os estados no Grafo_M
for i in range (0, len(estados)):
	Grafo.add_vertice(estados[i])

#add transicoes no Grafo_M (qa -> qb)
for i in range (0, len(transitions)):
	#quebra a string -> aux[0] = (qa,w) e aux[1] = qb
	aux = transitions[i].split("=")
	#retira parenteses
	aux[0] = aux[0][1:]
	aux[0] = aux[0][:-1]
	#quebra a string em qa e w
	aux[0] = aux[0].split(",")
	#add transicao
	Grafo.add_aresta(aux[0][0],aux[1],aux[0][1])
	
#AFD
print ("AFD: ",AFD)
print ("Estados: ",estados)
print ("Palvras: ",palavras)
print ("Estado inicial: ",estadoI)
print ("Estados finais: ",estadoF)
print ("Transicoes:",transitions)
print ("")
print ("")


# ==========Criando AFD Minimo============================










print ("Digite 0 para verificar se uma palavra é aceita")
menu=input("Digite 1 para verificar se um par de palavras sao ambos aceitos: ")
cont='s'
if int(menu)==0:
    while(cont == 's' or cont == 'S'):
        a = input("Digite a palavra : ")
        resp=aceita_W(a,Grafo)
        if resp[0]:
            print(resp[1])
            print('palavra aceita')
        else:
            print('palavra rejeitada')
        cont = input("\nDeseja inserir uma nova palavra(S/N): ")
        print("\n")
    cont='s'
elif int(menu)==1:
    while(cont == 's' or cont == 'S'):
        pares_aceitos=[]
        a = input("Digite a primeira palavra: ")
        a1 = input("Digite a segunda palavra: ")
        if(aceita_W(a,Grafo)[0] and aceita_W(a1,Grafo)[0]):
            pares_aceitos.append((a,a1))
        cont = input("\nDeseja inserir uma nova palavra(S/N): ")
        print("\n")
    print('pares aceitos: ', pares_aceitos) 