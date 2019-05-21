import argparse

from pulp import *
from random import random
import numpy as np
import math

def incr(base, number):
    """An increment in [n]^(k). (Ex: [5]^(3) = (012,013,014,023,024,034,123,124,134,234)). Where n = 'base' and k = length('number'). 'number' in the list of the digits of the number to increment. The function will of course not work if 'number' is not in [n]^(k).""" 
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
parser.add_argument('integern', metavar='n', type=int, nargs=1 ,help='n the number of boxes')
parser.add_argument('integerk', metavar='k', type=int, nargs=1 ,help='k the number of booby traps')
parser.add_argument('--rewards', metavar=('r_1','r_2'), type=float, nargs='+', help='the rewards in the n boxes, random in [1,n] if not specified')
parser.add_argument('--same', action='store_true', help='set all the rewards to 1')
parser.add_argument('--random', metavar=('a','b'), type=int, nargs=2, help='choose the rewards randomly in [a,b]')

args = parser.parse_args()
n = args.integern[0]
k = args.integerk[0]
assert k == n-2, "For the moment, we only solve the problem for k=n-2"
if args.same:
    r = [1 for i in range(n)]
elif args.rewards == None:
    r = []
    if args.random == None:
        a = n
        b = 1
    else:
        a = args.random[0]
        b = args.random[1]
    for i in range(n):
        r.append(random()*(b-a)//1+1)
else:
    assert len(args.rewards) == n, "The number of rewards must be the same as the number of boxes"
    r = []
    for i in range(n):
        r.append(args.rewards[i])

r.sort(reverse=True)
print(f"Rewards: {r}")

#Matrix x=S,y=H

hider_strats = []
num = [0 for i in range(k)]
incr(n,num)
for i in range(n*(n-1)//2): # n choose k with k = n-2
    hider_strats.append(num.copy())
    incr(n,num)

print(hider_strats)
size_h = len(hider_strats)

searcher_strats = []
for i in range(1,n-k+1):
    num = [0 for j in range(i)]
    if i != 1: incr(n,num)
    for i in range(nCk(n,i)):
        searcher_strats.append(num.copy())
        incr(n,num)

print(searcher_strats)
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

print("A : \n",A)

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
for i in range(size_s):
    print(f"Prob_{searcher_strats[i]} = {x[i].varValue}")
print(f"\nValue = {v.varValue}\n")

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
for i in range(size_h):
    print(f"Prob_{substraction([j for j in range(n)],hider_strats[i])} = {y[i].varValue}")
print(f"\nValue = {u.varValue}")
if u.varValue==v.varValue:
    print("\n Wow! Strong duality and Minimax theorems are correct!")
else:
    print("\n Mhhhh... You might be wrong Jeremy... Or I'm a dumb computer.")