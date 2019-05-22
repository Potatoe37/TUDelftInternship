# TUDelft Internship

This repository contains the programs I implemented during my Master internship in TU Delft under the supervision of Robbert Fokkink, about *A Search Game with Booby Traps* (see the [report](http://perso.ens-lyon.fr/jeremy.petithomme/pro/Files/Search_Game_with_Bobby_Traps_work.pdf)). These programs helped me to find some conjetures and allowed me to check them on multiple examples.

The first program concerns the case of the game with n=k-2. The second program concerns the variation of the game.

<h2>Case with n=k-2</h2>

The program `LinearOptimization.py` solves the game for n=k-2.

To execute it, type `python3 LinearOptimization.py n k`, n and k being those of the game you want to solve.
This command will solve the game with some random integer rewards, selected in [1,n]. To choose yourself the interval in which the rewards are selected, you can add the option `--random a b` so the rewards will be random integers in [a,b].
To force the rewards to be all the same, you can add the option `--same`, then the rewards will be all set to 1.
Finally, you can choose yourself all the rewards whith the option `--rewards r1 [r2 ...]`, with r1 ... rn the rewards.

Note that there is an assertion to force k to be n-2, but that the program should work with any k. 

<h2>Variation of the game</h2>

...