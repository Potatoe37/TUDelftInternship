import os
import sys
import signal
import time
from random import randint

import argparse

def stop_test(sig, frame):
        print('You are lucky! Your CTRL+C has been detected!')
        sys.exit(0)

t0 = time.time()

parser = argparse.ArgumentParser(description="Parses the arguments for the tests")
parser.add_argument('n_min', metavar='n_min', type=int, nargs=1 ,help='n the number of boxes')
parser.add_argument('n_max', metavar='n_max', type=int, nargs=1 ,help='k the number of booby traps')
parser.add_argument('n_tests', metavar='n_tests', type=int, nargs=1 ,help='n the number of tests')

args = parser.parse_args()

n_tests = int(args.n_tests[0])
n_min = int(args.n_min[0])
n_max = int(args.n_max[0])
fileout = f'out_{n_min}-{n_max}.txt'
#os.system(f"echo '' > {fileout}") #Uncomment if you want to reset the output file before starting the test
for i in range(n_tests):
    signal.signal(signal.SIGINT, stop_test)
    os.system('clear')
    print(f"Tests for n selected randomly in [{n_min},{n_max}], output written in {fileout}\n")
    print(f"Running {n_tests} tests...")
    print("Hold down CTRL+C to interrupt Keybord... Not very clean I know...\nIn fact you should better close your console ;)")
    print('[',end='')
    for k in range(100):
        if k<(i*100)//n_tests:
            print('#',end='')
        else:
            print(' ',end='')
    print(f'] {10000*i//(n_tests)/100}%')
    n = randint(n_min,n_max)
    k = n-2
    t = time.time()
    dt = t - t0
    exec_h = dt//3600
    exec_m = (dt-3600*exec_h)//60
    exec_s = dt-3600*exec_h-60*exec_m
    print(f"\nExectution time: {int(exec_h)} hours, {int(exec_m)} min, {int(exec_s)} sec.")
    if i!=0: 
        timepertest = (dt / i)
        remaining = timepertest*(n_tests-i)
        h_remain = remaining//3600
        m_remian = (remaining-h_remain*3600)//60
        s_remain = remaining-h_remain*3600-m_remian*60
        print(f"\nEstimated time remaining: {int(h_remain)} hours, {int(m_remian)} min, {int(s_remain)} sec.")

    #Trying some things to interrupt the script properly...
    try: os.system(f"python3 LinearOptimization.py {n} {k} --test >> {fileout}")
    except KeyboardInterrupt: sys.exit(0)
os.system('clear')
print(f"Tests for n selected randomly in [{n_min},{n_max}], output written in {fileout}\n")
print("Hold down CTRL+C to interrupt Keybord... Not very clean I know...\nIn fact you should better close your console ;)")
print('[####################################################################################################] 100%')
print(f"\nExectution time: {int(exec_h)} hours, {int(exec_m)} min, {int(exec_s)} sec.")
print(f"\nEstimated time remaining: 0 hours, 0 min, 0 sec.")