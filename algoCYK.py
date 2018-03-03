# Michael Mullings
# mcm14n
# COT4420 - inCNF.py

def parseWord(word):
    wordString=[]
    for i in word:
        wordString.append(i)
    return wordString

def CYK(word, grm):
    table=[ [ [] for i in range(len(word)+1) ] for j in range(len(word))]
    n=len(word)+1
    deriv=''
    for i in range(1,n):
        if word[i-1] in grm:
            table[i-1][i]=grm[word[i-1]].split()
        else:
            return False

    for j in range(2, n):
        for i in range(j-2,-1,-1):
            for k in range(i+1, j):
                for l in [ b+c for b in table[i][k] for c in table[k][j] ]:
                    if l in grm:
                        deriv=grm[l].split()
                        table[i][j]=list(set(table[i][j])|set(deriv))

    if 'S' in table[0][len(word)]:
        return True
    return False

def algoCYK(f1, f2):
    chomsky, keys, words={}, [], []
    accepted=0
    with open(f1, 'r') as cnf:
        for line in cnf:
            if line.split()[2] not in chomsky:
                chomsky[line.split()[2]]=''
            chomsky[line.split()[2]]+=line.split()[0]+' '
    with open(f2, 'r') as word:
        for line in word:
            words.append(line)

    for i in words:
        w=parseWord(i.strip())
        if CYK(w, chomsky):
            accepted=1
        else:
            accepted=0
        print i.strip()+': '+str(accepted)

            
