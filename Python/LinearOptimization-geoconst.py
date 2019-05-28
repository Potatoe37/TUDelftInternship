import argparse

from pulp import *
from random import random
import numpy as np
import math

def incr(base, number):
    """An increment in [n]^(k). (Ex: [5]^(3) = {012,013,014,023,024,034,123,124,134,234}). Where n = 'base' and k = length('number'). 'number' in the list of the digits of the number to increment. The function will of course not work if 'number' is not in [n]^(k).""" 
    n = base
    k = len(number)
    assert n > k, "As we select k elements in {1,...,n}, 'base' must be larger than length('number')"
    i = k-1
    number[i] +=1
    while number[i] >= i+(n-k+1) and i != 0: #For 'i+(n-k+1)', see page 4 of draft, or try it yourself... 
        number[i] = 0
        number[i-1] += 1
        #if number[i-1] == i+2: number[i-1] = n #See page 4 of draft
        i -= 1
    if number[0] == n-k+1:
        for j in range(k): number[j] = 0
    i=1
    while i<k:
        while number[i] <= number[i-1]:
            number[i] += 1
        i += 1

def incringraph(base,number,edges):
    #Working for n=4 k=2 only
    assert len(number) == 2, "Sorry, my script is a bit shit for the moment"
    incr(base, number)
    while number not in edges: 
        incr(base, number)

def intersection(lst1, lst2): 
    """Returns the intersection of two lists"""
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3 

def substraction(lst1, lst2):
    """Returns the substraction of the sets lst1 and lst2""" 
    lst3 = [value for value in lst1 if value not in lst2] 
    return lst3 

def nCk(n,k):
    """computes n choose k"""
    f = math.factorial
    return f(n) // (f(k) * f(n-k))

parser = argparse.ArgumentParser(description="Parses the arguments of the search game with booby traps")
parser.add_argument('n_boxes', metavar='n', type=int, nargs=1 ,help='n the number of boxes')
parser.add_argument('k_traps', metavar='k', type=int, nargs=1 ,help='k the number of booby traps')
parser.add_argument('--rewards', metavar=('r_1','r_2'), type=float, nargs='+', help='the rewards in the n boxes, random in [1,n] if not specified')
parser.add_argument('--same','-s', action='store_true', help='set all the rewards to 1')
parser.add_argument('--random', metavar=('a','b'), type=int, nargs=2, help='choose the rewards randomly in [a,b]')
parser.add_argument('--hider','-H',action='store_true', help='Display only the probabilities for the Hider (compatible with -S)')
parser.add_argument('--searcher','-S', action='store_true', help='Display only the probabilities for the Searcher (compatible with -H)')
parser.add_argument('--test', action='store_true', help='Prints only some output to check a conjecture for example')

args = parser.parse_args()
n = args.n_boxes[0]
k = args.k_traps[0]
assert k < n, "The number of traps must be lower than the number of boxes"
assert k >= 0 and int(n) == n and int(k) == k, "The number of traps and boxes must be positive integers"
assert k == n-2 and n==4, "We only defined the problem for n=4 and k=2"
if args.same:
    r = [1 for i in range(n)]
elif args.rewards == None:
    r = []
    if args.random == None:
        a = 1
        b = 20*n
    else:
        a = args.random[0]
        b = args.random[1]
    for i in range(n):
        r.append(random()*(b-a)//1+a)
else:
    assert len(args.rewards) == n, "The number of rewards must be the same as the number of boxes"
    r = []
    for i in range(n):
        r.append(args.rewards[i])

assert 0 not in r, "The rewards must be strictly positive numbers"

verb = True
if args.searcher or args.hider:
    verb = False

if args.test:
    verb = False
    args.searcher = False
    args.hider = False

r.sort(reverse=True)
print(f"n={n} and k={k}")
print("Game with geographical constraints")
print(f"Rewards: {r}")

edges = [[0,1],[1,2],[2,3],[3,0]]
#Matrix x=S,y=H

hider_strats = []
num = [0 for i in range(k)]
incr(n,num)
for i in range(len(edges)): #TODO The strategies of the hider are the edges if k=2
    num = edges[i]
    hider_strats.append(num.copy())

if verb: print(hider_strats)
size_h = len(hider_strats)

searcher_strats = []
for i in range(1,n-k+1):
    num = [0 for j in range(i)]
    if i != 1: incr(n,num) #We must take in account Strategy {0}, but not {0,...,0}
    for j in range(4): #TODO 4 edges and 4 vertices
        if i == 2: num = edges[j]
        searcher_strats.append(num.copy())
        if i == 1: incr(n,num)

if verb: print(searcher_strats)
size_s = len(searcher_strats)

#Rewards
a = []
for s in searcher_strats:
    l = []
    for h in hider_strats:
        if intersection(s,h) == []:
            tot_r = 0
            for i in s:
                tot_r+=r[i]
            l.append(tot_r)
        else:
            l.append(0)
    a.append(l)

A = np.array(a)

if verb: print("A : \n",A)

At = A.transpose()

#For the Searcher
problem = LpProblem("BoobyTraps-Searcher", LpMaximize)

x = LpVariable.dicts("Prob", list(range(size_s)), 0, None, cat="Continuous")
v = LpVariable("Value", None, None, cat="Continuous")

#Adding the constraints
for i in range(size_h):
    s = 0
    for j in range(size_s):
        s += -At[i][j]*x[j]
    c = s + v <= 0
    problem += c

s = 0
for j in range(size_s):
    s += x[j]
c1 = s <= 1
c2 = s >= 1
problem += c1
problem += c2

#Objective
problem += v

problem.solve()
if verb or args.searcher:
    print("\nSearcher:")
    for i in range(size_s):
        print(f"Prob_{searcher_strats[i]} = {x[i].varValue}")
    
if verb: print(f"\nValue = {v.varValue}\n")

#For the Hider
problem = LpProblem("BoobyTraps-Hider", LpMinimize)

y = LpVariable.dicts("Prob", list(range(size_h)), 0, None, cat="Continuous")
u = LpVariable("Value", None, None, cat="Continuous")

#Adding the constraints
for i in range(size_s):
    s = 0
    for j in range(size_h):
        s += -A[i][j]*y[j]
    c = s + u >= 0
    problem += c

s = 0
for j in range(size_h):
    s += y[j]
c1 = s <= 1
c2 = s >= 1
problem += c1
problem += c2

#Objective
problem += u

problem.solve()
if verb or args.hider:
    print("\nHider:")
    for i in range(size_h):
        print(f"Prob_{substraction([j for j in range(n)],hider_strats[i])} = {y[i].varValue}")
if verb:
    print(f"\nValue = {u.varValue}")
    if u.varValue==v.varValue:
        print("\n Wow! Strong duality and Minimax theorems are correct!")
    else:
        print("\n Mhhhh... You might be wrong Jeremy... Or I'm a dumb computer.")


def conjecture1(n,k,r):
    """Set all the probabilities according to the conjecture for the Searcher for the case n=k-2"""
    vavb = sum([1/r[i] for i in range(n-2)]) >= 1/r[n-1]+1/r[n-2]-2/(r[n-1]+r[n-2])
    vavc = sum([1/(r[i]+r[n-1]) for i in range(n-1)]) >= 1/r[n-1]
    vbvc = sum([1/(r[i]+r[n-1]) for i in range(n-2)])+1/r[n-2] >= sum([1/r[i] for i in range(n-2)])+1/(r[n-2]+r[n-1])
    vbva = sum([1/r[i] for i in range(n-2)]) <= 1/r[n-1]+1/r[n-2]-2/(r[n-1]+r[n-2])
    vcva = sum([1/(r[i]+r[n-1]) for i in range(n-1)]) <= 1/r[n-1]
    vcvb = sum([1/(r[i]+r[n-1]) for i in range(n-2)])+1/r[n-2] <= sum([1/r[i] for i in range(n-2)])+1/(r[n-2]+r[n-1])
    if vavb and vavc:
        #Strategy A
        game_value = 2/sum([1/r[i] for i in range(n)])
        if game_value*10000//1 != v.varValue*10000//1:
            #*10000//1 to avoid rounding errors
            print(f"Ouch... Value A: {game_value} != {v.varValue}")
        for i in range(size_s):
            if len(searcher_strats[i]) == 1:
                pi = game_value/(2*r[i])
                if (x[i].varValue*10000//1)!=(pi*10000//1):
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue*10000//1} != {pi*10000//1}\n")
                    return False
            else:
                if int(x[i].varValue*10000)!=0:
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue} != 0\n")
                    return False
        print("Checked !\n")
        return True
    elif vbva and vbvc:
        #Strategy B
        game_value = 1/(sum([1/r[i] for i in range(n-2)])+1/(r[n-2]+r[n-1]))
        if game_value*10000//1 != v.varValue*10000//1:
            #*10000//1 to avoid rounding errors
            print(f"Ouch... Value B: {game_value} != {v.varValue}")
        for i in range(size_s):
            if len(searcher_strats[i]) == 1 and i<n-2:
                pi = game_value/r[i]
                if (x[i].varValue*10000//1)!=(pi*10000//1):
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue*10000//1} != {pi*10000//1}\n")
                    return False
            elif searcher_strats[i]==[n-2,n-1]:
                pi = game_value/(r[n-2]+r[n-1])
                if (x[i].varValue*10000//1)!=(pi*10000//1):
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue*10000//1} != {pi*10000//1}\n")
                    return False
            else:
                if int(x[i].varValue*10000)!=0:
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue} != 0\n")
                    return False
        print("Checked !\n")
        return True
    elif vcva and vcvb:
        #Strategy C
        game_value = 2/(sum([1/r[i] for i in range(n-1)])+sum([1/(r[i]+r[n-1]) for i in range(n-1)]))
        if game_value*10000//1 != v.varValue*10000//1:
            #*10000//1 to avoid rounding errors
            print(f"Ouch... Value C: {game_value} != {v.varValue}")
        for i in range(size_s):
            if len(searcher_strats[i]) == 1 and i!=n-1:
                pi = game_value/(2*r[i])
                if (x[i].varValue*10000//1)!=(pi*10000//1):
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue*10000//1} != {pi*10000//1}\n")
                    return False
            elif len(searcher_strats[i]) == 2 and searcher_strats[i][1]==n-1:
                pi = game_value/(2*(r[searcher_strats[i][0]]+r[searcher_strats[i][1]])) 
                if (x[i].varValue*10000//1)!=(pi*10000//1):
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue*10000//1} != {pi*10000//1}\n")
                    return False
            else:
                if int(x[i].varValue*10000)!=0:
                    print("Ouch...")
                    print(f"{searcher_strats[i]} : {x[i].varValue} != 0\n")
                    return False
        print("Checked !\n")
        return True

if args.test:
    conjecture1(n,k,r)
