# Ramanujan_Machine
My very own version of the Ramanujan Machine

original paper
https://arxiv.org/pdf/1907.00205.pdf

My conjecture is that:

    4 / pi = 1 + 1 / ( 4 - 2 / ( 7 - 9 / ( 10 - 20 / ( 13 - 35 / ( 16 - 54 ...)))))

alpha(n) = 1 + 3 n
beta(n) = 1 - n - 2 n^2
gamma(c) = 4
delta(c) = c

Converges with exponential speed

    err(n) = 10**(-0.38 n)
    
execute main.py for a demo
execute plots.py for some plots of the search space
    
