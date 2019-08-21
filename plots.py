from search import *
import matplotlib.pyplot as plt
import numpy as np
from models import *


def plot_loss(loss, x_range, y_range, dx=.1, title=None):
    """plot loss space"""
    x_ = np.arange(x_range[0], x_range[1] + dx, dx)
    y_ = np.arange(y_range[1], y_range[0] + dx, -dx)
    data_ = np.array([[loss([x, y]) ** (1 / 5) for x in x_] for y in y_])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(data_,
              interpolation='bicubic',
              cmap='Blues',
              extent=[min(x_), max(x_), min(y_), max(y_)],
              vmin=0,
              vmax=2)
    period = 1
    ax.set_xticks([x for x in x_ if round(x/period, 8) == round(x/period)])
    ax.set_yticks([y for y in y_ if round(y/period, 8) == round(y/period)])
    plt.title(title)


def plot_path(points, color='blue'):
    """plot the path traced by 1 point in the parameter space"""

    x = [points[i][0] for i in range(len(points))]
    y = [points[i][1] for i in range(len(points))]

    plt.plot(x, y, c=color, linewidth=.3)
    for i in points:
        plt.plot(i[0], i[1], '+', color='blue', markersize=2)
    plt.plot(points[-1][0], points[-1][1], 'o', color='blue', markersize=2)


def plot_loss_and_path(loss, optimizer, init_points, x_range, y_range, dx, **fit_kwargs):
    """"""
    plot_loss(loss, x_range=x_range, y_range=y_range, dx=dx)

    for p in init_points:
        model_ = optimizer(loss)
        model_.fit(p, do_record=True, **fit_kwargs)
        print(model_.steps)
        print(model_.cost)
        data_ = model_.record
        plot_path(data_)
    plt.show()


if __name__ == '__main__':

    def ran():
        return random() * 2 - 1

    def test_loss(v):
        return loss_pi(depth=10)(v)

    X = [-8, +8]
    Y = [-10, +8]

    plot_loss(test_loss, x_range=X, y_range=Y, dx=1/3)

    for _ in range(20):
        model = RPropPlus(test_loss)
        model.fit([ran()*4, ran()*4], do_record=True, n_steps=50)
        data = model.record
        print(model.steps)
        print(model.cost)
        plot_path(data)
    plt.show()
