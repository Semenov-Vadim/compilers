# -*- coding: utf-8 -*-


print('''Напишить функцію, яка отримує на вхід специфікацію граматикиі повертає
специфікацію граматики без стронніх нетерміналів\n''')
##print("start\n")

##contextually free grammar
##Контекстно-вiльна граматика
class CFG:
    def __init__(self, sigma: list, N: list, S: str, P: dict):
        '''
        sigma- множество терминалов (обязательно маленькие буквы)
        N- множество нетерминалов (состоят из одной буквы, большой)
        S- начальный нетерминал
        P- правила
        '''
        
        ##проверка, есть ли начальный нетерминал в списке нетерминалов
        for temp in N:
            if S == temp:
                ##print("found it")
                break
        else:
            raise Exception("S is not in N")
        
        ##проверка, есть ли нетерсиналы из ключей в P в списке нетерминалов
        for temp in P:
            for temp2 in N:
                if temp == temp2:
                    ##print("found it-", temp)
                    break
            else:
                raise Exception("the key from P is not in N-", temp)
        
        ##удаляем нетерминалы, которые ничего не выводят
        for n in N:
            if n not in P:
                raise Exception(n, "is not in P")
        
        for key in P:
            ##print(P[key])
            for val in P[key]:
                ##print(val)
                for val2 in val:
                    ##print(val2)
                    if val2.istitle() and val2 not in N:
                        raise Exception(val2, "from the key", key, " is not in N")
                    if val2.istitle() == False and val2 not in sigma:
                        raise Exception(val2, "from the key", key, " is not in sigma")
            
        self.sigma = sigma
        self.N = N
        self.S = S
        self.P = P
        
    ##Видалення сторонніх нетерміналів
    def delWasteN(self):
        ##знайти непродуктивнi нетермiнали, видалити їх i правила, що їх мiстять;
        self.delWasteN2(self.findAliveN())
        
        ##для нової граматики знайти всi недосяжнi нетермiнали, видалити їх i правила, що їх мiстять.
        self.delWasteN2(self.findReachablN())
        return(self.P)
        

    ##удаляем нетерминалы и правила с этими нетерминалами, которых нет в списке l
    def delWasteN2(self, l:list):
        for temp in self.N:
            if temp not in l:
                self.N.remove(temp)
                ##print("removing ", temp)
                self.P.pop(temp)
                for val in self.P:
                    for val2 in self.P[val]:
                        for val3 in val2:
                            if val3 == temp:
                                self.P[val].remove(val2)
    
    ##поиск продуктивных нетерминалов
    def findAliveN(self):
        ##список продуктивных нетерминалов
        alives = []
        ##если список alives изменился за последний цикл, то contin= 1
        contin = 1
        
        ##останавливаемся, если проход не расширил список alives
        while contin == 1:
            contin = 0
            ##розширяємо alives нетермiналами, що стоять у лiвих частинах тих правил, правi частини яких мiстять тiльки нетермiнали з alives;
            for val in self.P:
                ##делаем дополнительную проверку, чтобы сократить время работы программы
                if val not in alives: 
                    for val2 in self.P[val]:
                        for val3 in val2:
                            ##если в правой части нашли нетерминал, который не содержится в alives, то нетерминал из левой части добавлять не будем
                            if val in alives or (val3.istitle() and val3 not in alives):
                                ##print("not adding ", val)
                                break
                        else:
                            ##print("adding ", val)
                            alives.append(val)
                            contin = 1
            ##print(contin)
        return alives
    
    ##поиск достижимых нетерминалов
    def findReachablN(self):
        ##список достижимых нетерминалов
        reachables = [self.S]
        ##если список reachables изменился за последний цикл, то contin= 1
        contin = 1
        
        ##останавливаемся, если проход не расширил список reachables
        while contin == 1:
            contin = 0
            ##розширяємо reachables нетермiналами, що стоять у правих частинах тих правил, лiвi частини яких мiстяться в reachables;
            for key in reachables:
                for val in self.P[key]:
                    for val2 in val:
                        if val2.istitle() and val2 not in reachables:
                            reachables.append(val2)
                            contin = 1
        return reachables    




'''Примеры '''
c1= CFG(["cat", "alt"],["A","F","E","D","K","B"],"A",{"K":[["A"]],
                                                      "A":[["cat", "alt"],['F'],["alt"]],
                                                      "F":[["alt"],["K", "alt"],["K"]], 
                                                      "E":[["D","alt"],["F"],],
                                                      "D":[["B"]],
                                                      "B":[["D"]]})
##print(c1.findAliveN())
##print(c1.findReachablN())
print(c1.delWasteN())

'''
c2= CFG(["alt"],["A","B"],"A",{"A":[["B"],["alt"]],
                               "B":[["alt"]]})
print(c2.delWasteN())
'''


