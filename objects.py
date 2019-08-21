from continued_fractions import *
from math import sin, pi

phi = (5 ** (1 / 2) + 1) / 2


class Loss:

    def __init__(self, const, name, alpha, beta, gamma, delta, depth=15, k_int=0.):
        """"""
        self.const = const
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.depth = depth
        self.k_int_attraction = k_int

    def __call__(self, v):
        """compute loss given alpha, beta, gamma, delta, const"""
        alpha = self.alpha(v)
        beta = self.beta(v)
        gamma = self.gamma(v)
        delta = self.delta(v)
        out = abs(LHS(gamma, delta, self.const) - RHS(alpha, beta, depth=self.depth))
        if self.k_int_attraction == 0.:
            return out
        else:
            return out + sum([abs(sin((i - round(i)) * pi)) for i in v]) / len(v) * self.k_int_attraction


def loss_phi(depth=15, k_int=0.):
    f = Loss(const=phi,
             name='phi',
             alpha=lambda v: Polynomial([v[0]]),
             beta=lambda v: Polynomial([1]),
             gamma=lambda v: Polynomial([0, 1]),
             delta=lambda v: Polynomial([1]),
             depth=depth,
             k_int=k_int)
    return f


def loss_pi(depth=15, k_int=0.):
    f = Loss(const=pi,
             name='pi',
             alpha=lambda v: Polynomial([1, 2]),
             beta=lambda v: Polynomial([v[0], v[1], 1]),
             gamma=lambda v: Polynomial([4]),
             delta=lambda v: Polynomial([0, 1]),
             depth=depth,
             k_int=k_int)
    return f


def loss_pi_2(depth=15, k_int=0.):
    f = Loss(const=pi,
             name='pi_2',
             alpha=lambda v: Polynomial([v[0], v[1], v[2]]),
             beta=lambda v: Polynomial([v[3], v[4], v[5]]),
             gamma=lambda v: Polynomial([v[6]]),
             delta=lambda v: Polynomial([v[7], 1]),
             depth=depth,
             k_int=k_int)
    return f


def loss_pi_3(depth=15, k_int=0.):
    f = Loss(const=pi,
             name='pi_3',
             alpha=lambda v: Polynomial([v[0], v[1]]),
             beta=lambda v: Polynomial([v[2], v[3], v[4]]),
             gamma=lambda v: Polynomial([v[5]]),
             delta=lambda v: Polynomial([0, 1]),
             depth=depth,
             k_int=k_int)
    return f


def add_integer_attraction(loss, k=1.):
    """add cost to number far from integers"""
    def f(v):
        """new loss"""
        return loss(v) + sum([abs(sin((i - round(i)) * pi)) for i in v]) / len(v) * k
    return f


if __name__ == '__main__':
    # def f_(_):
    #     return 0
    #
    # new_loss = add_integer_attraction(f_)

    loss_ = loss_phi(depth=20)
    print(loss_([1]))
    print(loss_([2]))
    print(loss_([1.5]))

    loss_ = loss_phi(depth=20, k_int=.5)
    print(loss_([1.5]))
