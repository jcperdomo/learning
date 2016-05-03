from collections import deque
import itertools

import numpy as np
from scipy.optimize import linprog

import utils

def getMixedStrat(hist):
    """Gets the mixed strategy implied by a single player's history.

    :hist: List representing history.
    :returns: List of probabilities, where the index is the action.
    """
    ret = list(hist)
    tot = sum(ret)
    ret = [x/float(tot) for x in ret]
    return ret

def findBestResponse(game, player, mix_strats):
    """Finds a best response to a profile of opponent mixed strategies.

    :player: Player for which we're finding a best response, represented as an
    index from 0 to numPlayers - 1.
    :mix_strats: List of lists representing each player's implied mixed
    strategy.
    :returns: The best response action, which maximizes expected utility.
    """
    numPlayers = game.numPlayers()
    numActs = game.numActions()
    playerActs = numActs[player]

    exp_values = [utils.expectedValue(player, a, mix_strats, game)
                  for a in xrange(playerActs)]

    smallVal = float('-inf')
    smallAct = []
    for a, ev in enumerate(exp_values):
        if ev > smallVal:
            smallVal = ev
            smallAct = [a]
        elif ev == smallVal:
            smallAct.append(a)

    return np.random.choice(smallAct)


def fictPlay(game, iters):
    """Runs fictitious play on a given game for a given number of iterations.

    :game: A Game object as defined in utils.Game.
    :iters: The number of iterations for which to run ficitious play.
    :returns: The final strategy profile as a list of (a, p) pairs.
    """
    nactions = game.numActions()
    history = [[0 for a in xrange(nactions[p])]
               for p in xrange(game.numPlayers())]

    actions = [np.random.randint(0, na) for na in nactions]

    for i in xrange(iters):

        # update history
        for player, act in enumerate(actions):
            history[player][act] += 1

        # compute mixed strategies based on history
        mix_strats = [getMixedStrat(hist) for hist in history]

        # decide on next actions based on best responses
        actions = [findBestResponse(game, player, mix_strats)
                   for player in xrange(game.numPlayers())]

    return [getMixedStrat(hist) for hist in history]
