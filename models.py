from copy import deepcopy
# Warning: dx can affect precision


def sign(x):
    """sign of x"""
    if x > 0:
        return +1
    elif x < 0:
        return -1
    else:
        return 0


def gradient(f, v, dx=10**-10, cost0=None):
    """gradient of f in v (dx = tiny step to compute derivatives)"""
    if cost0 is None:   # in case cost in v has already been computed (more efficient)
        cost0 = f(v)
    return [(f([v[j] + dx * (i == j) for j in range(len(v))]) - cost0) / dx for i in range(len(v))]


class GradientDescent:
    """GD"""
    def __init__(self, loss):
        self.loss = loss
        self.sol = None
        self.record = []

    def fit(self, initial_point, n_steps=40, min_cost=10**-4, eta=.4, do_record=False, dx=10**-10, show=False):
        """training"""
        v = deepcopy(initial_point)
        if do_record:
            self.record.append(v)

        cost = self.loss(v)

        for steps in range(n_steps):

            if show:
                for i in v:
                    print('%.2f' % i, end='\t')
                print('\t', cost)

            grad = gradient(self.loss, v, cost0=cost, dx=dx)

            v = [v[i] - eta * grad[i] for i in range(len(v))]

            if do_record:
                self.record.append(deepcopy(v))

            if steps >= n_steps-1:
                # print('model did not converge')
                break

            cost = self.loss(v)
            if cost <= min_cost:
                break

        self.sol = v
        return self.sol


class RProp:
    """RProp"""
    def __init__(self, loss):
        self.loss = loss
        self.sol = None
        self.record = []

    def fit(self, initial_point, s0=.01, n_steps=80, min_cost=10**-5, k_plus=1.2, k_minus=.5, do_record=False):
        """training"""
        w = deepcopy(initial_point)
        if do_record:
            self.record.append(deepcopy(w))

        n = len(w)
        cost = self.loss(w)

        # init speed & gradient
        grad = gradient(self.loss, w, cost0=cost)

        # speed = [s0 for _ in range(n)]
        speed = [s0 for _ in range(n)]

        for steps in range(1, 1 + n_steps):

            # compute gradient
            new_grad = gradient(self.loss, w, cost0=cost, dx=min_cost/10)
            new_speed = [i for i in speed]

            for i in range(n):
                if new_grad[i] * grad[i] > 0:   # keep going
                    new_speed[i] *= k_plus
                    w[i] -= sign(new_grad[i]) * new_speed[i]
                elif new_grad[i] * grad[i] < 0:     # step back
                    new_speed[i] *= k_minus
                    new_grad[i] = 0
                else:
                    w[i] -= sign(new_grad[i]) * new_speed[i]

            grad = new_grad
            speed = new_speed

            cost = self.loss(w)

            if do_record:
                self.record.append(deepcopy(w))

            if steps >= n_steps:
                break

            if cost <= min_cost:
                break

        self.sol = w
        return self.sol


class RPropPlus:
    """RProp"""
    def __init__(self, loss):
        self.loss = loss
        self.sol = None
        self.record = []
        self.steps = None
        self.cost = None

    def fit(self, initial_point, s0=1/2, n_steps=50, min_cost=10**-5,
            k_plus=1.2, k_minus=.5, dx=10**-10, do_record=False, show=False):
        """training"""
        w = deepcopy(initial_point)
        if do_record:
            self.record.append(deepcopy(w))

        n = len(w)
        cost = self.loss(w)

        # init speed & gradient
        grad = gradient(self.loss, w, cost0=cost, dx=dx)

        # speed = [s0 for _ in range(n)]
        speed = [max(abs(i*s0), s0/10) for i in grad]

        for steps in range(1, 1 + n_steps):

            if show:
                for i in w:
                    print(round(i, 2), end='\t')
                print('\t', cost)

            if steps >= n_steps:
                # print('\n', 'model did not converge\t', cost, '\n')
                break

            # compute gradient
            new_grad = gradient(self.loss, w, cost0=cost, dx=dx)
            new_speed = [i for i in speed]
            delta = [0. for _ in speed]

            for i in range(n):
                if new_grad[i] * grad[i] > 0:   # keep going
                    new_speed[i] *= k_plus
                    delta[i] = -sign(new_grad[i]) * new_speed[i]
                    w[i] += delta[i]
                elif new_grad[i] * grad[i] < 0:     # slow down
                    new_speed[i] *= k_minus
                    new_grad[i] = 0
                else:
                    delta[i] = -sign(new_grad[i]) * new_speed[i]
                    w[i] += delta[i]

            new_cost = self.loss(w)

            if new_cost <= cost:
                grad = new_grad
                speed = new_speed
                cost = new_cost
            else:
                w = [w[i] - delta[i] for i in range(n)]
                speed = [i * k_minus for i in speed]

            if do_record:
                self.record.append(deepcopy(w))
                self.steps = steps
                self.cost = cost

            if steps >= n_steps:
                break

            if cost <= min_cost:
                break
        # print(steps)
        self.sol = w
        return self.sol
