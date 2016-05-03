import utils
import itertools
import numpy as np

t1 = np.array([
    [(-3,-1),(-3,-1), (-1,-3), (-1,-3)],
    [(-2,-1),(0,0),(0,0),(-2,-1)]])

# generate a probability distribution from a vector of weights
def generateDistribution(weights):
    total = float(sum(weights))
    distribution = [ i / total for i in weights[:-1]]
    distribution.append(1 - sum(distribution))
    assert(sum(distribution) == 1)
    return distribution

# given weights for each player calculate respective mixed strategies
def weightsToStrategies(weights):
    strats = [generateDistribution(weight) for weight in weights]
    return strats


#RIGHT NOW NOT SURE OF GAME PARAMETER
def no_regrets(game, iters, e):
    """
    function that computes equilibrium profile for a game using multiplicative
    weights algorithm

    
    iters = number of iterations
    epsilon = epsilon parameter
    game = instance of Game class

    returns: mixed strategy profiles for each player
    """
    game_actions = game.numActions()
    num_players = game.numPlayers()
    # initialize strategies so that all actions have equal weights 
    weights = [ [1 for _ in xrange(size) ] for size in game_actions]
    
    for _ in xrange(iters):
        # generate mixed strategies for each player based on weights
        strategies  = weightsToStrategies(weights)      
        # calculate costs for each action
        results = []
        for i in xrange(num_players):
            # for each action of every player
            costs = []
            for a in xrange(game_actions[i]):
                costs.append(utils.expectedValue(i, a, strategies, game,
                                                 True))
            results.append(costs)
        
        # update weights based on costs
        for i in xrange(num_players):
            for j in xrange(game_actions[i]):
                weights[i][j] = weights[i][j] * (1 - e) ** results[i][j]
                                
    return weightsToStrategies(weights)


#TESTS

print generateDistribution([1,1,1])
print generateDistribution([1,2,0])
        
print "RESULTS: "

pd = utils.Game('PrisonersDilemma.game')
print no_regrets(pd, 100, .1)

mp = utils.Game('MatchingPennies.game')
print no_regrets(mp, 100, .1)

bots = utils.Game('BattleOfTheSexes.game')
print no_regrets(bots, 100, .1)

rzs = utils.Game('RandomZeroSum.game')
print no_regrets(rzs, 100, .1)

rps = utils.Game('RockPaperScissors.game')
print no_regrets(rps, 100, .1)

chicken = utils.Game('Chicken.game')
print no_regrets(chicken, 100, .1)

t1 = utils.Game('T1.game')
print no_regrets(t1, 100, .1)
