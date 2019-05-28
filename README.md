# TUDelft Internship

This repository contains the programs I implemented during my Master internship in TU Delft under the supervision of Robbert Fokkink, about *A Search Game with Booby Traps* (see the [report](http://perso.ens-lyon.fr/jeremy.petithomme/pro/Files/Search_Game_with_Bobby_Traps_work.pdf)). These programs helped me to find some conjetures and allowed me to check them on multiple examples.

The first program concerns the case of the game with n=k-2. The second program concerns the variation of the game.

<h2>Case with n=k-2</h2>

The program `LinearOptimization.py` solves the game for n=k-2.

To execute it, type `python3 LinearOptimization.py n k`, n and k being those of the game you want to solve.
This command will solve the game with some random integer rewards, selected in [1,20*n]. To choose yourself the interval in which the rewards are selected, you can add the option `--random a b` so the rewards will be random integers in [a,b].
To force the rewards to be all the same, you can add the option `--same`, then the rewards will be all set to 1.
Finally, you can choose yourself all the rewards whith the option `--rewards r1 [r2 ...]`, with r1 ... rn the rewards.

By default, the program prints many information. To print only the strategy of the Searcher or the one of the Hider, use respectively options `-S` and `-H`. 

Use option `--help` for more information.

Note that the algorithm can solve the game for any k and n.

The program `Tests.py` tests the conjecture from the [report](http://perso.ens-lyon.fr/jeremy.petithomme/pro/Files/Search_Game_with_Bobby_Traps_work.pdf). To execute it, type `python3 Tests.py n_min n_max n_tests`. The program will test the conjecture on `n_tests` random cases, with n selected in [`n_min`,`n_max`]. The output will be written in a corresponding file. Some output file are already available in this repository. Note that there may be some errors detected, due to some rounding errors...

<h2>Variation of the game</h2>

...