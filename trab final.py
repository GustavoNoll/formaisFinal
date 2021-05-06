
import copy

def processString(afd, string):
    """
    Verifies if w is accepted by afd
    """
    count = 0
    w_new = [initial]
    tam=len(string)

    while w_new:
        value = w_new.pop(0)
        state = afd[value]
        if count >= tam:
            if value in final:
                return True
            return False
        for transition in afd[value]:
            if string[count] == transition:
                print("from ", value, " to ", afd[value][transition], " with ", transition)
                w_new.append(afd[value][transition])
        count += 1
    return False

def renameState(afd, state, new_state):
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
    #Initialize del_list list, the minimized DFA and changed flag
    del_list = []
    min_afd = copy.deepcopy(afd)
    changed = True
    # compare two states,if they have the same transitions, they have not been del_list
    # and they are both final or non final, delete them from min_afd then
    # add them to the del_list list and rename any transitions with the del_list state to the new state
    while(changed):
        changed = False
        for state1 in afd:
            for state2 in afd:
                if state1 != state2:
                    if state1 in min_afd and state2 in min_afd:
                        if min_afd[state1] == min_afd[state2]:
                            if state2 in min_afd and state2 not in del_list:
                                if (state2 in final and state1 in final) or (state2 not in final and state1 not in final):


                                    del_list.append(state2)
                                    del_list.append(state1)
                                    changed = True
                                    #Check if one of the states is initial, in order to avoid its deletion
                                    if state1 in initial:
                                        print("state to delete: ", state2)
                                        del min_afd[state2]
                                        renameState(min_afd, state2, state1)
                                        if state2 in final:
                                            final.remove(state2)
                                    elif state2 in initial:
                                        print("state to delete: ", state1)
                                        if state1 in final:
                                            final.remove(state1)
                                        del min_afd[state1]
                                        renameState(min_afd, state1, state2)
                                    else:
                                        print("state to delete: ", state2)
                                        if state2 in final:
                                            final.remove(state2)
                                        del min_afd[state2]
                                        renameState(min_afd, state2, state1)

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