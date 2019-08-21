"""
        The Ramanujan Machine: Automatically Generated
        Conjectures on Fundamental Constants


original paper
https://arxiv.org/pdf/1907.00205.pdf

"""
from math import pi
import hashlib


class Polynomial:
    """polynomial given the coefficients"""
    def __init__(self, coeff: list):
        self.c = coeff

    def __call__(self, x):
        # c0 + c1 * x + c2 * x**2 + ...
        return sum([self.c[i] * x**i for i in range(len(self.c))])

    def __repr__(self):
        out = str(self.c[0])
        if len(self.c) >= 1:
            if self.c[1] != 0:
                out += ' + ' + str(self.c[1]) + 'c'
        for i in range(2, len(self.c)):
            if self.c[i] != 0:
                out += ' + ' + str(self.c[i]) + 'c^' + str(i)
        return out


def LHS(gamma, delta, const):
    """
    Left-Hand Side fraction
    :param const: constant
    :param gamma: function
    :param delta: function
    :return: float
    """
    return gamma(const) / delta(const)


def RHS(alpha, beta, depth=15):
    """
    Right-Hand Side continued fraction
    :param alpha: function
    :param beta: function
    :param depth: depth of the continued fraction
    :return: float
    """
    return ContinuedFraction(a=[alpha(n) for n in range(depth)],
                             b=[beta(n) for n in range(depth-1)]).value()


class ContinuedFraction:
    """ a0 + b1/(a1 + b2/(a2 + b3/(...))) """

    def __init__(self, a=None, b=None):
        # [a_0, a_1, ..., a_n]
        self.a = a if a else [0]
        #      [b_1, ..., b_n]
        self.b = b if b is not None else [1 for _ in range(len(a))]

    def value(self):
        """convert continued fraction to number"""
        # a0 + b1/(a1 + b2/(a2 + b3/(...)))
        if len(self.a) == 1:
            return self.a[0]
        else:
            den = ContinuedFraction(self.a[1:], self.b[1:]).value()
            if den == 0:
                return 10**10   # todo how to deal with infinity? =0?
            else:
                return self.a[0] + self.b[0] / den

    def __eq__(self, other, precision=10**-15):
        """equal if difference is below precision"""
        if type(other) == float or type(other) == int:
            # number
            return abs(self.value() - other) <= precision
        elif type(other) == ContinuedFraction:
            # continued fraction
            return abs(self.value() - other.value()) <= precision

    def __hash__(self):
        return int.from_bytes(hashlib.sha256(self.__repr__().encode('utf-8')).digest(), 'big')

    def __repr__(self):
        out = str(self.a[0])
        if len(self.a) > 1 and len(self.b) > 0:
            out += ' - ' if self.b[0] < 0 else ' + '
            out += str(abs(self.b[0])) + ' / ( ' + ContinuedFraction(self.a[1:], self.b[1:]).__repr__() + ' )'
        return out

    def data(self):
        """ display a abd b coefficients """
        return '(%s, %s)' % (str(self.a), str(self.b))


if __name__ == '__main__':

    assert ContinuedFraction([2 for _ in range(30)]) == 2**(1/2)+1
    assert ContinuedFraction([i for i in range(30)],
                             [i + 1 for i in range(30)]) == 1/(e - 1)
    assert ContinuedFraction([i for i in range(30)],
                             [i + 2 for i in range(30)]) == 1
    N = ContinuedFraction([1, 2], [3])
    print(N)
    print(N.value())
    print(hash(N))

    assert abs(Polynomial([1/fact(i) for i in range(30)])(1)-e) < 10**-15

    try:
        v_ = [randrange(5) + 1 for _ in range(15)]
        print(log(abs(ContinuedFraction(v_).value() - ContinuedFraction(v_[:-1]).value()), 10))
    except ValueError:
        pass

    print(ContinuedFraction([-1, -1, -1, -1]))

    print((RHS(Polynomial([0, 3]), Polynomial([1, -4]), depth=30)+1)**2)

    print(LHS(Polynomial([1, 0]), Polynomial([-1, 1]), e))
    print(RHS(Polynomial([0, 3]), Polynomial([1, -4]), depth=30))

    print()
    print(RHS(Polynomial([-1, 3, 3]), Polynomial([-3, -3, 4]), depth=40))
    print(LHS(Polynomial([3, 0]), Polynomial([-5, 1]), pi))
