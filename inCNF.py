# Michael Mullings
# mcm14n
# COT4420 - inCNF.py
from itertools import permutations

def returnNullSet(cfg):
    li=[]
    cn=cfg
    for i in cn:
        if '*' in cn[i]:
            li.append(i)
    else:
        for i in cn:
            if i not in li:
                for j in cn[i]:
                    for k in j:
                        if k not in li:
                            break
                    else:
                        li.append(i)
                            
    return li


def killNullTerminals(pr, nset):
    li=[]
    for i in nset:
        for j in range(len(i)+1):
            temp=pr
            if i[:j] != '':
                for l in [ k for k in i[:j]]:
                    temp=temp.replace(l,"")
                    li.append(temp)
    return ' '.join(li)




def killNullProductions(cfg):
    cnf, cfgkeys, rules= {}, cfg.keys(), ''
    perms = [''.join(p) for p in permutations( ''.join(returnNullSet(cfg)) )]
    for i in cfgkeys:
        cnf[i]=''
        pr=cfg[i].split()
        for j in pr:
            temp=j
            rules+=killNullTerminals(temp, perms)+' '
            cnf[i]+=j+' '+rules
            rules=''
    else:
        for i in cnf:
            cnf[i]=cnf[i].replace('*', '')
            cnf[i]=cnf[i].strip()
        li=[i for i in cnf if cnf[i] == '']
        for i in li:
            for j in cnf:
                if j != i:
                    cnf[j]=' '.join([k for k in cnf[j].split() if i not in k])
                    if cnf[j] == '':
                        li.append(j)
            del cnf[i]
    
    for i in cnf:
        cnf[i]= ' '.join(list(set(cnf[i].split())))
    return cnf


def dfs(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        if state in graph.keys():
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path+[next_state]))

def DepthFS(graph, start):
    fringe=[(start, [])]
    while fringe:
        state, path= fringe.pop()
        if path and state.islower():
            yield path
            continue
        if state in graph.keys():
            for next_state in graph[state]:
                if next_state in path:
                    continue
                fringe.append((next_state, path+[next_state]))

def findCycles(graph):
    cycles = [ [node]+path for node in graph for path in dfs(graph, node, node)]
    for i in cycles:
        for j in cycles:
            if i!=j and (set(i[:-1])==set(j[:-1]) or set(i[:-1]).issuperset(set(j[:-1]))):
                cycles[cycles.index(j)] = []
    return [i for i in cycles if i != []]


def removeCycles(cfg):
    cycles = findCycles(str2ListsProductions(cfg))
    ntoffset, rules, li, chT= 0, '', [],''
    cfg=list2StringProductions(cfg)
    for i in cycles:
        if 'S' in i:
            chT='S'
        else:
            if 'V'+str(ntoffset) in cfg:
                ntoffset+=1
            chT='V'+str(ntoffset)
        for j in i[:-1]:
            rules+=''.join(cfg[j])+' '
            li.append(j)
            del cfg[j]
        for i in li:
            rules=rules.replace(i, chT)
            for o in cfg:
                cfg[o]=cfg[o].replace(i, chT)
        cfg[chT] = rules.strip()
        rules,li ='', []
        ntoffset+=1
    else:
        r=[]
        if len(cycles) > 0:
            for i in cfg:
                rules=cfg[i].split()
                for l in range(len(rules)):
                    if i != rules[l]:
                        r.append(rules[l])
                cfg[i] = (' '.join(r)).strip()
                r=[]
    
    return cfg
     
def findUnitProductions(graph):
    unit=[ [node]+path for node in graph for path in DepthFS(graph, node)]
    for i in unit:
        for j in unit:
            if i!=j and set(j) <= set(i):
                unit[unit.index(j)]=[]
    return [i for i in unit if i != []]

def removeUnitProductions(cfg):
    unitp = findUnitProductions(cfg)
    for i in unitp:
        pr=i[:-1]
        pr.reverse()
        for j in range(len(pr)-1):
            cfg[pr[j+1]].extend(cfg[pr[j]])
            cfg[pr[j+1]]=[k for k in cfg[pr[j+1]] if k not in i[:-1]]
    else:
        for i in cfg:
            cfg[i]=' '.join(list(set(cfg[i])))

    return cfg

class Stack:
    def __init__(self):
        self.li=[]
        self.length=0
    def push(self, x):
        self.li.append(x)
        self.length+=1
    def pop(self):
        term=''
        if self.length != 0:
            term=self.li.pop()
            self.length-=1
        return term


def maskTerminals(cfg):
    mask, offset= 'X', 0
    rep, masks = {}, {}
    for i in cfg:
        for j in range(len(cfg[i])):
            if len(cfg[i][j]) > 1:
                for k in cfg[i][j]:
                    if k.islower():
                        if k not in rep:
                            if mask+str(offset) in cfg:
                                offset+=1
                            rep[k]=mask+str(offset)
                            masks[mask+str(offset)]=[k]
                            cfg[i][j]=cfg[i][j].replace(k, mask+str(offset))
                            offset+=1
                        else:
                            cfg[i][j]=cfg[i][j].replace(k,rep[k])
    else:
        for i in masks:
            cfg[i]=masks[i]
    return cfg


def productionLen(string):
    length=0
    for i in string:
        if i.isalpha():
            length+=1
    return length

def maskNonTerminals(cfg):
    stack=Stack()
    rep, masks, cnf, termlist={},{}, {}, []
    mask, offset, term, alpha='Y',0, '', ''
    for i in cfg:
        for j in range(len(cfg[i])):
            if len(cfg[i][j]) > 2:
                temp = cfg[i][j]
                li=[]
                term=''
                while productionLen(temp) > 2:
                    for v in range(len(temp)):
                        li.append(temp[v])
                    term+=li.pop()
                    if term.isdigit():
                        alpha=li.pop()
                        while alpha.isdigit():
                            alpha+=li.pop()
                        term=alpha[::-1]+term
                    stack.push(term)
                    term=li.pop()
                    if term.isdigit():
                        alpha=li.pop()
                        while alpha.isdigit():
                            alpha+=li.pop()
                        term=alpha[::-1]+term
                    stack.push(term)
                    term=stack.pop()
                    term+=stack.pop()
                    if term not in termlist:
                        if mask+str(offset) in cfg or mask+str(offset) in cnf:
                            offset+=1
                        temp=temp.replace(term, mask+str(offset))
                        cnf[mask+str(offset)]=[term]
                        offset+=1
                        termlist.append(term)
                        term=''
                    else:
                        w=''
                        for l in cnf:
                            if term in cnf[l]:
                                w=l
                                break
                        temp=temp.replace(term, w)
                cfg[i][j]=temp
    for i in cnf:
        cfg[i]=cnf[i]
                        
    return cfg

def str2ListsProductions(cfg):
    grm=cfg
    for i in grm:
        if type(grm[i]) != type('string'):
            return grm
    for i in grm:
        grm[i]=grm[i].split()
    return grm

def list2StringProductions(cfg):
    grm=cfg
    for i in grm:
        if type(grm[i]) != type([]):
            return grm
    for i in grm:
        grm[i]=' '.join(grm[i])
    return grm

def inCNF(cfg_file):
    grammar,keys, cnf={}, [], {}
    with open(cfg_file, 'r') as cfg:
        for line in cfg:
            if line.split()[0] not in grammar.keys():
                grammar[line.split()[0]]=''
                keys.append(line.split()[0])
            grammar[line.split()[0]]+=line.split()[2]+' '
        else:
            cfg.close()

    cnf=killNullProductions(grammar)
    cnf=removeCycles(cnf)
    cnf=removeUnitProductions(str2ListsProductions(cnf))
    cnf=maskTerminals(str2ListsProductions(cnf))
    cnf=maskNonTerminals(str2ListsProductions(cnf))
    
    li=cnf.keys()
    try:
        li.remove('S')
    except:
        pass
    li.sort()
    li=['S']+li
    for i in li:
        try:
            for j in cnf[i]:
                print i, ' -> ', j
        except:
            continue


