from objects import *
from models import *
from datahandling import *
from random import random, randrange


def ran():
    a = random() * 2 - 1
    return a + sign(a)


def search_routine(loss, optimizer, initial_point, domain=None, kwargs1=None, kwargs2=None):
    """search, validate and save a solution"""

    # find candidate
    model = optimizer(loss)
    solution = model.fit(initial_point, **kwargs1)  # fine-tune

    # add non-integer cost
    k = 1.
    model = optimizer(add_integer_attraction(loss, k=k))
    solution = model.fit(solution, **kwargs2)  # fine-tune

    # validity check    # todo validate domain
    round_sol = [round(i) for i in solution]
    valid = loss(round_sol) < 10 ** -8  # fine-tune
    if domain is not None:
        for i in range(len(round_sol)):
            if round_sol[i] < domain[i][0] or round_sol[i] > domain[i][1]:
                valid = False

    # if good then print SAVE and return results
    if valid:
        print('\n', round_sol, '\n')

        # save
        new_entry(name=loss.name,
                  hash_=hash_list(round_sol),
                  alpha=loss.alpha(round_sol).c,
                  beta=loss.beta(round_sol).c,
                  gamma=loss.gamma(round_sol).c,
                  delta=loss.delta(round_sol).c)

    # return results
    return solution


def search_engine(loss, optimizer, domain, size=50, walk=20, kwargs1=None, kwargs2=None):
    """search solutions"""
    if not kwargs1:
        kwargs1 = {'min_cost': 10 ** -3, 's0': 1, 'n_steps': 30}
    if not kwargs2:
        kwargs2 = {'min_cost': 10 ** -3, 's0': 1 / 10, 'n_steps': 30}

    for epoch in range(1, 1 + size):

        print(round(100 * epoch / size, 1), '%')

        point = [randrange(i[0], i[1] + 1) for i in domain]

        point = search_routine(loss=loss,
                               optimizer=optimizer,
                               initial_point=point,
                               domain=domain,
                               kwargs1=kwargs1,
                               kwargs2=kwargs2)

        # point move nearby the local minimum
        for j in range(walk):
            point = [i + ran() for i in point]

            point = search_routine(loss=loss,
                                   optimizer=optimizer,
                                   initial_point=point,
                                   domain=domain,
                                   kwargs1=kwargs1,
                                   kwargs2=kwargs2)


if __name__ == '__main__':

    Loss = loss_pi_3(depth=30)
    Range = [1, +2]
    search_engine(loss=Loss,
                  optimizer=RPropPlus,
                  domain=[Range for _ in range(5)] + [[1, 4]],
                  size=20,
                  walk=20)
    show_data(Loss.name)
