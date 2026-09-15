"""Code to implement the tennis Markov chain model"""

import numpy as np
from matplotlib import pyplot as plt


def index(a, b):
    """Compute the index of a state (a, b).

    This makes it easier to enumerate the states.
    a: Points of player A
    b: Points of player B
    Points are counted as 0, 1, 2, 3 instead of 0, 15, 30, 40.
    """
    return a * 4 + b


def transition_matrix(p):
    """Fill the transition matrix for the tennis Markov chain and return it."""

    P = xxx ### COMPLETE HERE
    # A wins a point
    for a in [0, 1, 2]:
        for b in [0, 1, 2]:
            P[index(a, b), index(a+1, b)] = xxx ### COMPLETE HERE
    # B wins a point
    for a in [0, 1, 2]:
        for b in [0, 1, 2]:
            P[index(a, b), index(a, b+1)] = xxx ### COMPLETE HERE

    # If A already has 3 points, this is final. Stay in this state.
    for b in [0, 1, 2]:
        P[index(3, b), index(3, b)] = xxx ### COMPLETE HERE
    # If B already has 3 points, this is final. Stay in this state.
    for a in [0, 1, 2]:
        P[index(a, 3), index(a, 3)] = xxx ### COMPLETE HERE

    return P


def limiting_distributions(P, n):
    """Compute the limiting distributions of the transition matrix P, for n steps."""

    pi = xxx ### COMPLETE HERE
    return pi


def winning_probability(p):
    """Compute the probability of A to win a game.
    
    p is the probability that A wins a point.
    """

    # Compute the limiting distributions of the Markov chain.
    P = transition_matrix(p)
    pi = xxx ### COMPLETE HERE

    # The probability that A wins is the sum of the probabilities of all states where A has 3 points
    # Remember that this limiting distribution is not unique but depends on the initial state.
    initial = xxx ### COMPLETE HERE
    win_prob = xxx ### COMPLETE HERE

    return win_prob


def main():
    """Compute the winning probabilities for a range of point-winning probabilities
       and plot the result"""
    all_p = np.arange(0.0, 1.0, 0.01)
    win_prob = np.zeros(len(all_p))
    for i, p in enumerate(all_p):
        win_prob[i] = winning_probability(p)

    plt.plot(all_p, win_prob, label='P(A wins)')
    plt.xticks(np.arange(0, 1.1, 0.1))
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.xlabel('P(A wins a point)')
    plt.ylabel('P(A wins the game)')
    plt.title('Winning Probability of Player A')
    plt.grid(True, alpha=0.3)
    plt.savefig('tennis_win_probability.png')


if __name__ == "__main__":
    main()
