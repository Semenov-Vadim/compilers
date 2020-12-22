# -*- coding: utf-8 -*-
import copy
import time
##from collections import deque
##from builtins import True


print('''Обов'язково (20 балів). Побудуйте python-тулкіт для парсингу ліво-рекурсивним спуском, який забезпечить
1) пошук і видалення сторонніх нетерміналів (на основі попередніх завдань)
2) пошук зникаючих нетерміналів (на основі попередніх завдань)
3) діагностування лівої рекурсії (на основі попередніх завдань)
4) приведення граматики до нормальної форми Грейбах
5) позбавдення від лівої рекурсії
6) ліву факторизацію граматики
7) універсальний ліво-рекурсивний парсер 
''')

# #print('''1) Напишіть функцію, яка приймає специфікацію граматики і повертає список зникаючих нетерміналів
# #2) Напишіть функцію, яка приймає специфікацію граматики і повертає список нетерміналів, для які визначаються ліворекурсивно.\n''')

# #print('''Напишить функцію, яка отримує на вхід специфікацію граматикиі повертає
# #специфікацію граматики без стронніх нетерміналів\n''')
# #print("start\n")


# #contextually free grammar
# #Контекстно-вiльна граматика
class CFG:

    def __init__(self, sigma: list, N: list, S: str, P: dict):
        '''
        sigma- множество терминалов (обязательно маленькие буквы)
        N- множество нетерминалов (состоят из одной буквы, большой)
        S- начальный нетерминал
        P- правила
        '''
        
        # #проверка, есть ли начальный нетерминал в списке нетерминалов
        for temp in N:
            if S == temp:
                # #print("found it")
                break
        else:
            raise Exception("S is not in N")
        
        # #проверка, есть ли нетерсиналы из ключей в P в списке нетерминалов
        for temp in P:
            for temp2 in N:
                if temp == temp2:
                    # #print("found it-", temp)
                    break
            else:
                raise Exception("the key from P is not in N-", temp)
        
        # #поиск нетерминалов, которые ничего не выводят
        for n in N:
            if n not in P:
                raise Exception(n, "is not in P")
        
        # #проверка символов в правилах. Выбрасываем Exception, если символа нет в списке N либо sigma
        for key in P:
            for val in P[key]:
                for val2 in val:
                    if val2.istitle() and val2 not in N:
                        raise Exception(val2, "from the key", key, " is not in N")
                    if val2.istitle() == False and val2 not in sigma:
                        raise Exception(val2, "from the key", key, " is not in sigma")
            
        self.sigma = sigma
        self.N = N
        self.S = S
        self.P = P
        
    # #Видалення сторонніх нетерміналів
    def delWasteN(self):
        ##print(self.P)
        # #знайти непродуктивнi нетермiнали, видалити їх i правила, що їх мiстять;
        self.delWasteN2(self.findAliveN())
        #print(self.P)
        # #для нової граматики знайти всi недосяжнi нетермiнали, видалити їх i правила, що їх мiстять.
        self.delWasteN2(self.findReachablN(self.S))
        
        self.delEmpty()
        return(self.P)

    # #удаляем нетерминалы и правила с этими нетерминалами, которых нет в списке l
    def delWasteN2(self, l:list):
        ##newN = copy.deepcopy(self.N)
        newP = copy.deepcopy(self.P)
        contin = True
        
        for key in self.P:
            if key not in l:
                self.N.remove(key)
                newP.pop(key)
        self.P = copy.deepcopy(newP)
        
        while contin == True:
            contin = False
            for key in self.P:
                for val in self.P[key]:
                    ##newV = copy.deepcopy(self.P[key])
                    for val2 in val:
                        if val2.istitle() and val2 not in l:
                            val.remove(val2)
                            contin = True
                        ##print("deleting ", val2)
                        ##print(newP.get(key))
                        ##newV.remove(val2)
                ##print("newP[key] ", newP[key])
                ##print("newV ", newV)
                ##newP[key] = copy.deepcopy(newV)
        ##self.P = copy.deepcopy(newP)
        ##print(self.P)
        '''for temp in self.N:
            if temp not in l:
                self.N.remove(temp)
                # #print("removing ", temp)
                self.P.pop(temp)
                for val in self.P:
                    for val2 in self.P[val]:
                        for val3 in val2:
                            if val3 == temp:
                                self.P[val].remove(val2)'''
    
    # #поиск продуктивных нетерминалов
    def findAliveN(self):
        # #список продуктивных нетерминалов
        alives = []
        # #если список alives изменился за последний цикл, то contin= 1
        contin = 1
        
        # #останавливаемся, если проход не расширил список alives
        while contin == 1:
            contin = 0
            
            # #розширяємо alives нетермiналами, що стоять у лiвих частинах тих правил, правi частини яких мiстять тiльки нетермiнали з alives;
            for key in self.P:
                # #делаем дополнительную проверку, чтобы сократить время работы программы
                if key not in alives: 
                    for val2 in self.P[key]:
                        for val3 in val2:
                            # #если в правой части нашли нетерминал, который не содержится в alives, то нетерминал из левой части добавлять не будем
                            if key in alives or (val3.istitle() and val3 not in alives):
                            ##if key in alives or (val3.istitle() and val3 not in alives):
                                # #print("not adding ", key)
                                break
                        else:
                            # #print("adding ", key)
                            alives.append(key)
                            contin = 1
        
        return alives
    
    # #поиск достижимых нетерминалов, если начинать путь из переданного нетерминала
    def findReachablN(self, S: str):
        # #список достижимых нетерминалов
        # #начальный нетерминал всегда является достижимым по определению
        reachables = [S]
        # #если список reachables изменился за последний цикл, то contin= 1
        contin = 1
        
        # #останавливаемся, если проход не расширил список reachables
        while contin == 1:
            contin = 0
            # #розширяємо reachables нетермiналами, що стоять у правих частинах тих правил, лiвi частини яких мiстяться в reachables;
            for key in reachables:
                for val in self.P[key]:
                    for val2 in val:
                        if val2.istitle() and val2 not in reachables:
                            ##print("reachables ", reachables)
                            reachables.append(val2)
                            contin = 1
        return reachables    
    
    # #возвращает список нетерминалов, которые исчезнут после очистки с помощью метода delWasteN

    '''def findVanishN(self):
        ##список нетерминалов, которые исчезнут после очистки
        vanish= []
        for t in self.P:
            vanish.append(t)
        
        ##находим список нетерминалов, которые останутся после очистки
        tempCFG= CFG(self.sigma, self.N, self.S, self.P).delWasteN()
        for t in tempCFG:
            vanish.remove(t)
        
        return vanish'''
    
    ##возвращает список исчезающих нетерминалов
    def findVanishN(self):
        vanish = []
        # #если список alives изменился за последний цикл, то contin= 1
        contin = 1
                
        for key in self.P:
            for val in self.P[key]:
                if len(val) == 1 and val[0] == 'e' and key not in vanish:
                    vanish.append(key)
            
        # #розширяємо vanishings нетермiналами, що стоять у лiвих частинах тих правил, правi частини яких мiстять тiльки нетермiнали з vanishings i не мiстять термiнальних символiв;
        # #останавливаемся, если проход не расширил список vanish
        while contin == 1:
            contin = 0
            for key in self.P:
                if key not in vanish:
                    for val in self.P[key]:
                        for val2 in val:
                            if val2 not in vanish:
                                break
                        else:
                            vanish.append(key)
                            contin = 1
                            break
        return vanish
    
    # #повертає список нетерміналів, які визначаються ліворекурсивно
    def findLR(self):
        lRNonterm = []
        
        for nonterm in self.N:
            # #список достижимых нетерминалов из этого нетерминала
            reachables = self.findReachablN(nonterm)
            for n in reachables:
                for val in self.P[n]:
                    # #if нужен, чтобы избежать лишних проверок и ускорить работу программы
                    if nonterm not in lRNonterm:
                        for val2 in val:
                            # #если нашли зацикливание
                            if val2 == nonterm:
                                if nonterm not in lRNonterm:
                                    lRNonterm.append(nonterm)
                                break
        return lRNonterm
    
    # #удаляет нетерминанты, которые ничего не выводят
    def delEmpty(self):
        contin = 1
        deleted = []
        
        # #заканчиваем, если ничего не удалидли
        while contin == 1:
            contin = 0
            emptyN = []
            
            # #поиск нетерминалов, которые ничего не выводят
            for key in self.P:
                if len(self.P[key]) == 0:
                    emptyN.append(key)
                    contin = 1
            # #print("empty", emptyN)
                    
            # #удаление нетерминала и связей с ним
            for key in self.P:
                for val in self.P[key]:
                    for val2 in val:
                        if val2 in emptyN:
                            val.remove(val2)
            # #удаляем пустые списки внутри списка в P
            for key in self.P:
                for val in self.P[key]:
                    # #print(val)
                    if len(val) == 0:
                        self.P[key].remove(val)
                        contin = 1
            for val in emptyN:
                deleted.append(val)
                self.N.remove(val)
                self.P.pop(val)
            # #emptyN.clear()
            # #print()
        return deleted
    
    # #приведення граматики до нормальної форми Грейбах 
    def getGreibach(self):
        self.delWasteN()
        vanish = self.findVanishN()
        ##print(vanish)
        newP = copy.deepcopy(self.P)
        
        # #удаляем правила вида А-> e
        for key in self.P:
            if key in vanish:
                for val in self.P[key]:
                    # #print(val)
                    if len(val) == 1 and val[0] == 'e':
                        ##self.P[key].remove(val)
                        newP[key].remove(val)
        
        self.P = newP
        
        deleted = self.delEmpty()
        for n in deleted:
            vanish.remove(n)
        
        greibach = copy.deepcopy(self.P)
        
        # #ищем исчезающие нетерминалы и обрабатываем их с getGreibVal()
        for key in self.P:
            for val in self.P[key]:
                vanishTemp = []
                for val2 in val:
                    if val2 in vanish:
                        vanishTemp.append(val2)
                if len(vanishTemp) != 0:
                    self.getGreibVal(greibach[key], vanishTemp, val)
                    vanishTemp.clear()
        
        ##print("before", greibach)
        self.delChain(greibach)
        ##print("after", greibach)
        return greibach

    # #рекурсивно добавляем в список greib все комбинации (с и без) элементов из списка vanishTemp
    def getGreibVal(self, greib: list, vanishTemp: list, val: list):
        for v in vanishTemp:
            # #копии списка с элементом v
            vanishTemp2 = copy.deepcopy(vanishTemp)
            vanishTemp2.remove(v)
            if val not in greib and len(val) != 0:
                ##print("adding ", val)
                greib.append(val)
            self.getGreibVal(greib, vanishTemp2, val)
            
            # #копии списка без элемента v
            valCopy = copy.deepcopy(val)
            valCopy.remove(v)
            vanishTempCopy = copy.deepcopy(vanishTemp)
            vanishTempCopy.remove(v)
            if valCopy not in greib and len(valCopy) != 0:
                ##print("adding ", valCopy)
                greib.append(valCopy)
            self.getGreibVal(greib, vanishTempCopy, valCopy)
    
    ##удаляем цепи в правилах (т.е. правила типа A->B)
    def delChain(self, greibach):
        contin = 1
        
        while contin == 1:
            contin = 0
            for key in greibach:
                for val in greibach[key]:
                    if len(val) == 1 and val[0] == key:
                        greibach[key].remove(val)
                        contin = 1 
                    elif len(val) == 1 and val[0].istitle() and val[0] != key:
                        for val2 in self.P[val[0]]:
                            if val2 not in greibach[key]:
                                contin = 1
                                greibach[key].append(val2)
                            if val in greibach[key]:
                                greibach[key].remove(val)
    
    ##избавляемся от непосредственной левой рекурсии
    def deleteLRDirect(self):
        ##print("f ", self.P)
        foundRec = False
        newP = copy.deepcopy(self.P)
        
        for key in self.P:
            for val in self.P[key]:
                if val[0] == key:
                    ##нашли рекурсию
                    foundRec = True
            
            if foundRec == True:
                if key + str(3) not in newP:
                    self.N.append(key + str(3))
                    ##print("1newP ", newP)
                    newP.update({key + str(3) : []})
                    ##print("2newP ", newP)
                    ##time.sleep(1.0)
                for val in self.P[key]:
                    ##добавляем key + 3 к элементам без рекурсии
                    if val[0] != key:
                        newVal = copy.deepcopy(val)
                        newVal.append(key + str(3))
                        if newVal not in newP[key]:
                            newP[key].append(newVal)
                    ##добавляем новые правила в новый нетерминальный символ
                    else:
                        ##добавляем слово без символа key + str(3)
                        newP[key].remove(val)
                        newVal = copy.deepcopy(val)
                        newVal.remove(newVal[0])
                        if newVal not in newP[key + str(3)]:
                            newP[key + str(3)].append(newVal)
                        ##добавляем слово с символом key + str(3) в конце
                        newVal = copy.deepcopy(newVal)
                        newVal.append(key + str(3))
                        if newVal not in newP[key + str(3)]:
                            newP[key + str(3)].append(newVal)
            foundRec = False
        self.P = newP
        ##print("s ", self.P)
        ##self.delEmpty()
        '''contin = True
        
        while contin == True:
            contin = False
            for key in self.P:
                newP = copy.deepcopy(self.P)
                for i in range(len(self.P[key])):
                    val = self.P[key][i]
                    for val2 in val:
                        ##убираем прямую левую рекурсию
                        if val2 == key:
                            contin = True
                            valNew = copy.deepcopy(val)
                            valNew.remove(val2)
                            ##проверяем наличие дубликатов
                            if valNew in newP[key]:
                                newP[key].remove(val)
                                ##time.sleep(1.0)
                            else:
                                newP[key].remove(val)
                                newP[key].append(valNew)
                self.P = newP
        ##time.sleep(1.0)
        self.delEmpty()'''
    
    ##убираем левую рекурсию (прямую и непрямую)
    def deleteLR(self):
        self.deleteLRDirect()
        ##print("1 ", self.P)
        newP = copy.deepcopy(self.P)
        contin = False
        
        for i in range(len(self.N)):
            key = self.N[i]
            for i2 in range(len(self.N)):
                if i2 >= 1 and i2 < i:
                    key2 = self.N[i2]
                    ##print("self.P ", self.P)
                    for val in self.P[key2]:
                        if val[0] == key:
                            newP[key2].remove(val)
                            for val3 in self.P[key]:
                                ##print("val3 ", val3)
                                #print("self.P ", self.P)
                                newVal = copy.deepcopy(val)
                                newVal.remove(val[0])
                                for val4 in val3:
                                    if val4 not in newVal:
                                        newVal.append(val4)
                                        ##print("newVal ", newVal)
                                        ##print("val4 ", val4)
                                        if newVal not in newP[key2]:
                                            newP[key2].append(newVal)
                                            contin = True
                        '''for val2 in val:
                            if val2 == key:
                                ##print("1 newP[key2] ", newP[key2])
                                newP[key2].remove(val)
                                for val3 in self.P[key]:
                                    ##print("val3 ", val3)
                                    #print("self.P ", self.P)
                                    newVal = copy.deepcopy(val)
                                    newVal.remove(val2)
                                    for val4 in val3:
                                        if val4 not in newVal:
                                            newVal.append(val4)
                                            ##print("newVal ", newVal)
                                            ##print("val4 ", val4)
                                            if newVal not in newP[key2]:
                                                newP[key2].append(newVal)'''
                                ##print("2 newP[key2] ", newP[key2])
            ##for i in len(range(self.P[key])):
        self.P = newP
        ##self.deleteLRDirect()
        self.delEmpty()
        ##print("2 ", self.P)
        ##self.deleteLRDirect()
        ##print("3 ", self.P)
        ##print("self.P ", self.P)
        if contin == True:
            self.deleteLR()
        
        '''checked = []
        newP = copy.deepcopy(self.P)
        contin = False
        
        ##проверяем непрямую левую рекурсию
        for key in self.P:
            checked.append(key)
            for key2 in self.P:
                ##исключаем уже проверенные элементы
                if key2 not in checked:
                    for i in range(len(self.P[key2])):
                        val = self.P[key2][i]
                        if val[0] == key and key in newP[key2][i]:
                            ##print("newP ", newP)
                            ##print("newP[key2] ", newP[key2])
                            newP.update({key+str(1):self.P[key]})
                            newVal= copy.deepcopy(val)
                            newVal[0] += str(1)
                            temp = newVal[0]
                            newVal[0] = newVal[-1]
                            newVal[-1] = temp
                            newP[key2].append(newVal)
                            newP[key2].remove(val)
                            contin = True
                            ##time.sleep(0.5)
        
        self.P = newP
        if contin == True:
            self.deleteLR()'''
    
    ##левая факторизация
    def lFactorization(self):
        ##print(self.P)
        newP = copy.deepcopy(self.P)
        
        for key in self.P:
            ##for val in self.P[key]:
            for i in range(len(self.P[key])):
                val = self.P[key][i]
                if val[0].istitle():
                    ##for val2 in self.P[key]:
                    for i2 in range(len(self.P[key])):
                        val2 = self.P[key][i2]
                        if val2[0] == val[0] and i2 != i:
                            ##print(newP)
                            ##print("val[0] ", val[0])
                            ##newPKey.update({key+str(1):self.P[key]})
                            l = [val[0],val[0]+str(2)]
                            if l not in newP[key]:
                                newP[key].append(l)
                            if val in newP[key]:
                                newP[key].remove(val)
                            l = copy.deepcopy(val)
                            l.remove(val[0])
                            
                            ##print("l ", l)
                            
                            if val[0]+str(2) not in newP:
                                newP.update({val[0]+str(2) : []})
                            ##print("newP[val[0]+str(2)] ", newP[val[0]+str(2)])
                            if l not in newP[val[0]+str(2)]:
                                ##newP.update({val[0]+str(2) : newP[val[0]+str(2)].append(l)})
                                newP[val[0]+str(2)].append(l)
                            ##print("2 newP[val[0]+str(2)] ", newP[val[0]+str(2)])
            
        self.P = newP
        self.delEmpty()
        
    ##подготовка к лево-рекурсивному парсингу
    def prepareLRParsing(self):
        ##self.delWasteN()
        self.P = self.getGreibach()
        ##print(len(self.findLR()))
        if len(self.findLR()) != 0:
            self.deleteLR()
        self.lFactorization()
    
    '''##этот метод нужен так как неходясь в рекурсии невозможно узнать если мы вернемся на шаг назад не закончится ли список myStack либо expectRes
    ##т.е. LRParsing2 может возвращать либо True, если найдет заданую последовательность, либо None, если не найдет
    ##этот дополнительный метод нужен только для красивого вывода и не более
    def LRParsing(self, myStack: list, expectRes):
        ##print(self.LRParsing2(myStack, expectRes))
        if self.LRParsing2(myStack, expectRes) == True:
            return True
        else:
            return False'''
    
    
    def LRParsing(self, myStack: list, expectRes):
        if len(myStack) == 0 and len(expectRes) == 0:
            ##print("TRUE")
            return True
        if len(myStack) == 0 or len(expectRes) == 0:
            ##print("FALSE")
            return False
        ##заменяем нетерминант на последовательность, которую он выводит
        if myStack[0].istitle():
            for val in self.P[myStack[0]]:
                newMyStack = []
                for val2 in val:
                    newMyStack.append(val2)
                
                newMyStack2 = copy.deepcopy(myStack)
                newMyStack2.remove(myStack[0])
                
                for valStack in newMyStack2:
                    newMyStack.append(valStack)
                '''newMyStack = copy.deepcopy(myStack)
                newMyStack.remove(myStack[0])
                for val2 in val:
                    newMyStack.append(val2)'''
                ##print("newMyStack ",newMyStack)
                if self.LRParsing(newMyStack,expectRes) == True:
                    return True
                    break
                ##если вызов вернул не True, проверяем достигли ли мы конца 
                elif val == self.P[myStack[0]][-1]:
                    return False
                    
        else:
            ##если нашли терминальный символ -> убираем его и продолжаем рекурсию
            if myStack[0] == expectRes[0]:
                ##print("found it ", myStack, " ", expectRes)
                newMyStack = copy.deepcopy(myStack)
                newMyStack.remove(myStack[0])
                newExpectRes = copy.deepcopy(expectRes)
                newExpectRes.remove(expectRes[0])
                if self.LRParsing(newMyStack, newExpectRes) == True:
                    return True
            
            ##найденый терминальный символ нам не подходит -> возвращаемся 
            else:
                ##print("ELSE ", myStack)
                return False


##-------------------------------------------------------------------------------

'''Примеры '''
'''c = CFG(["|",",","*","chr","nil"],["S","A","P"],"S",{"S":[["S","|","S"],["A"]],
                                                     "A":[["A",",","A"],["P"]],
                                                     "P":[["P","*"],["chr"],["nil"]]})
   
c.prepareLRParsing()
print(c.P)

print(c.LRParsing([c.S],["chr"]))                           ##True
print(c.LRParsing([c.S],["chr","|","nil"]))                 ##True
print(c.LRParsing([c.S],["chr","|","nil","|","nil","*"]))   ##True
print(c.LRParsing([c.S],["chr","chr","chr"]))               ##False'''


'''c1= CFG(["cat", "alt"],["A","F","E","D","K","B","W"],"A",{"K":[["A"]],
                                                          "A":[["cat", "alt"],['F'],["alt"]],
                                                          "F":[["alt"],["K", "alt"],["K"]], 
                                                          "E":[["D","alt"],["F"],],
                                                          "D":[["B"]],
                                                          "B":[["D"]],
                                                          "W":[["W"]]})
##print(c1.findAliveN())
##print(c1.findReachablN(c1.S))
##print(c1.delWasteN())
##print(c1.findVanishN())
print(c1.findLR())


##Пример №2

c2= CFG(["alt"],["A","B"],"A",{"A":[["B"],["alt"]],
                               "B":[["alt"]]})
##print(c2.delWasteN())
print(c2.findVanishN())
print(c2.findLR())'''

'''c3 = CFG(["alt", "e","com"], ["A", "B", "C", "D", "E", "F"], "A", {"A":[["B"], ["alt", "B","F"],["B","C"]],
                                                                   "B":[["e"]],
                                                                   "C":[["A", "B", "alt", "C", "D"], ["A", "B"],["alt"]],
                                                                   "D":[["A", "B", "alt"],["E"]],
                                                                   "E":[["alt"], ["E","A"],["E","A","com"]],
                                                                   "F":[["E"], ["alt", "E"]]})


##print(c3.P)
##print(c3.P)
##c3.deleteLR()
##print(c3.P)
##c3.lFactorization()
##c3.prepareLRParsing()
##print(c3.P)
##c3.deleteLRDirect()
##c3.P = c3.getGreibach() 
##c3.deleteLR()
##c3.prepareLRParsing()
##print(c3.P)'''


'''c4 = CFG(["alt"],["S","A","B","C"],"S",{"S":[["S"],["alt"],["A"],["B","C"]],
                                        "A":[["A"],["A","alt"]],
                                        "B":[["alt","S"],["S"]],
                                        "C":[["alt"]]})

print(c4.P)
c4.P = c4.getGreibach()
print(c4.P)
c4.delWasteN()
print(c4.P)'''

c5= CFG(["c","a","b","d"],["S","A"],"S",{"S":[["c","A","d"]],
                                        "A":[["a","b"],["a"]]})

c5.prepareLRParsing()
print(c5.P)
print(c5.LRParsing([c5.S],["c","a","d"]))
print(c5.LRParsing([c5.S],["c","a","b","d"]))
print(c5.LRParsing([c5.S],["c","a","b"]))






