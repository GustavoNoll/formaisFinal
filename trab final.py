
import copy

def processString(afd, string):
    """
    Verifies if w is accepted by afd
    """
    count = 0
    w_new = [initial]

    while w_new:
        value = w_new.pop(0)
        state = afd[value]
        if count >= len(string):
            if value in final:
                return True
            return False
        for transition in afd[value]:
            if string[count] == transition:
                print("from ", value, " to ", afd[value][transition], " with ", transition)
                w_new.append(afd[value][transition])
            elif string[count] not in afd[value]:
                print("from ", value, " to sink state with ", string[count])
        count += 1
    return False

def changeName(afd, state, new_state):
    """
       Function to rename afd states while minimizing
         """
    #For every state in DFA
    for element in afd:
        #For every transition
        for letter in afd[element]:
            #If the state we are renaming is a result from any transition, change its name to the new state
            if state == afd[element][letter]:
                afd[element].update({letter : new_state})


def minimize(afd):
    """
           Function to minimize a DFA

             """
    #Initialize deleted list, the minimized DFA and changed flag
    deleted = []
    min_afd = copy.deepcopy(afd)
    changed = True
    # compare two states,if they have the same transitions, they have not been deleted
    # and they are both final or non final, delete them from min_afd then
    # add them to the deleted list and rename any transitions with the deleted state to the new state
    while(changed):
        changed = False
        for one_state in afd:
            for another_state in afd:
                if one_state != another_state:
                    if one_state in min_afd and another_state in min_afd:
                        if min_afd[one_state] == min_afd[another_state]:
                            if another_state in min_afd and another_state not in deleted:
                                if (another_state in final and one_state in final) or (another_state not in final and one_state not in final):


                                    deleted.append(another_state)
                                    deleted.append(one_state)
                                    changed = True
                                    #Check if one of the states is initial, in order to avoid its deletion
                                    if one_state in initial:
                                        print("state to delete: ", another_state)
                                        del min_afd[another_state]
                                        changeName(min_afd, another_state, one_state)
                                        if another_state in final:
                                            final.remove(another_state)
                                    elif another_state in initial:
                                        print("state to delete: ", one_state)
                                        if one_state in final:
                                            final.remove(one_state)
                                        del min_afd[one_state]
                                        changeName(min_afd, one_state, another_state)
                                    else:
                                        print("state to delete: ", another_state)
                                        if another_state in final:
                                            final.remove(another_state)
                                        del min_afd[another_state]
                                        changeName(min_afd, another_state, one_state)

    return min_afd






if __name__ == "__main__":
    #Extract all of the states, alphabet, initial states and final states from the file
    file = open("arquivodeentrada.txt", "r")
    words = []
    transitions = []
    #Leitura do arquivo
    for i in file:
        for word in i.split():
            words.append(word)

    #Process Arquive
    afd_string = words[0]
    afd_aux = afd_string.split("{")
    states = afd_aux[1].split(',')
    states.pop()
    states[len(states)-1]=states[len(states)-1].replace("}","")
    alphabet_sym = afd_aux[2].split('}')
    alphabet_sym= alphabet_sym[0].split(',')

    initial = afd_aux[2].split('}')[1]
    initial = initial.replace(",","")

    final = afd_aux[3].split(',')
    final[len(final)-1]= final[len(final)-1].replace("})","")

    for i in range (2, len(words)):
        transitions.append(words [i])

    #============afd creation======================

    #For each remaining line in the file, get the transition, and the states involved in the transition
    afd = dict(dict())
    for i in range (0, len(transitions)):


        aux = transitions[i].split("=")
        aux[0] = aux[0][1:]
        aux[0] = aux[0][:-1]
        aux[0] = aux[0].split(",")

        state0 = aux[0][0]
        letter = aux[0][1]
        for_state = aux[1]

        #If the original state already has a transition in the afd, add the new transition to it,
        # otherwise create the new state and its first transition
        if state0 in afd:
            afd[state0].update({letter: for_state})
        else:
            afd[state0] = {letter: for_state}
        

    #original afd
    print()
    print("Original afd")
    for i in afd.keys():
        print(i,'=',afd[i])
    min_afd = minimize(afd)
    #minimized afd
    print("Minimized afd")
    for i in min_afd.keys():
        print(i,'=',min_afd[i])

    print("Final states ", final)
    print("Initial state ", initial)

    menu=input("Digite 0 para verificar se uma palavra é aceita e 1 para verificar se um par de palavras sao ambos aceitos: ")
    cont='s'
    if int(menu)==0:
        while(cont == 's' or cont == 'S'):
            string = input("Digite a palavra : ")
            if processString(min_afd, string):
                print('palavra aceita')
            else:
                print('palavra rejeitada')
            cont = input("\nDeseja inserir uma nova palavra(S/N): ")
            print("\n")
        cont='s'
    elif int(menu)==1:
        while(cont == 's' or cont == 'S'):
            pares_aceitos=[]
            string = input("Digite a primeira palavra: ")
            string2= input("Digite a segunda palavra: ")
            if(processString(min_afd, string) and processString(min_afd, string2)):
                pares_aceitos.append((string,string2))
            cont = input("\nDeseja inserir uma nova palavra(S/N): ")
            print("\n")
        print('pares aceitos: ', pares_aceitos) 