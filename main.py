"""
        The Ramanujan Machine


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

"""
from search import *


# MY SOLUTION

Alpha = Polynomial([1, 3])
Beta = Polynomial([1, -1, -2])
Gamma = Polynomial([4])
Delta = Polynomial([0, 1])

Depth = 20


print('\n my solution \n')
print('4 / pi = ', end='')
print(ContinuedFraction(a=[Alpha(n) for n in range(Depth)],
                        b=[Beta(n) for n in range(Depth-1)]))
print()
print(RHS(Alpha, Beta, depth=Depth))
print(LHS(Gamma, Delta, const=pi))


# RUN THE CODE!

# define loss
Loss = loss_pi_3(depth=30)

# define search space
Range = [-4, +4]
Domain = [Range for _ in range(5)] + [[1, 4]]

# search
print('\n\n', 'searching... (solutions are stored in file data_' + Loss.name + '.pi)', '\n')
search_engine(loss=Loss,
              optimizer=RPropPlus,
              domain=Domain,
              size=1000,
              walk=20)

# print results
show_data(Loss.name)
