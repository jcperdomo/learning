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

def getConstraint(game, player, a1, a2, other_profs, mix_strats):
    """Figures out the constraint needed for the best-response LP.

    :game: The utils.Game object representing the game.
    :player: The index of the player for which we're computing a BR.
    :a1: The action we're considering.
    :a2: The action we're comparing it to.
    :other_profs: The set of opponent action profiles (A_-i).
    :mix_strats: The mixed strategies implied by each player's history.
    :returns: A row to be added to the matrix on the LHS of the LP and the
    value for the RHS.
    """

    def computeCoef(game, player, a, other_profs, mix_strats):
        coef = 0
        for o_prof in other_profs:

            # get full action profile and player's utility
            a_prof = list(o_prof)
            a_prof.insert(player, a)
            util = game.utility(a_prof)[player]

            # find probability of o_prof (a_-i)
            o_prof_prob = np.prod(float(mix_strats[p][act])
                                  for p, act in enumerate(a_prof) if p != player)
            o_prof_prob = list(o_prof_prob)[0]

            coef += util * o_prof_prob
        return coef

    a1coef = computeCoef(game, player, a1, other_profs, mix_strats)
    a2coef = computeCoef(game, player, a2, other_profs, mix_strats)

    row = [0 for _ in xrange(game.numActions()[player])]
    row[a2] = a2coef
    row[a1] = -a1coef

    return row, 0

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

    return [dict(enumerate(getMixedStrat(hist))) for hist in history]

pd = utils.Game('PrisonersDilemma.game')
print fictPlay(pd, 1000)

mp = utils.Game('MatchingPennies.game')
print fictPlay(mp, 1000)

bots = utils.Game('BattleOfTheSexes.game')
print fictPlay(bots, 1000)
