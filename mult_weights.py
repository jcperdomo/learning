import utils
import itertools
import numpy as np

matchingPennies = np.array([[(1,-1),(-1,1)], [(-1,1), (1,-1)]])
t1 = np.array([[(-3,-1),(-3,-1), (-1,-3), (-1,-3)],[(-2,-1),(0,0),(0,0),(-2,-1)]])
sexes = np.array([[(-2,-1),(0,0)],[(0,0),(-1,-2)]])

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

def expectedValue(i, a, S, game_actions, game):
    """
    calculates expected value of action a according to other players
    playing strategies s_{-i}
    
    i = id of player under consideration
    a = action played by player i
    S = list of strategy profiles for every player
    game =  game object with utilities method
    
    returns: utility value   
    
    """
    action_lists = [xrange(el) for el in game_actions]
    action_lists[i] = [a]
    terms = itertools.product(*action_lists)
    num_players = len(game_actions)
    val = 0
    #print "Player ID ", i
    #print "Action ", a
    #print "Strategies ", S
    #print "Terms ", [el for el in terms]

    for prof in terms:
	# calculate probability of an action profile
	p = 1
	for player in xrange(num_players):
	    if player == i:
		prob = 1
	    else:
		prob = S[player][prof[player]]
	    p *= prob      
	val += game[prof][i] * p
    return val


#RIGHT NOW NOT SURE OF GAME PARAMETER
def no_regrets(iters, e, game_actions, game):
    """
    function that computes equilibrium profile for a game using multiplicative
    weights algorithm

    
    iters = number of iterations
    epsilon = epsilon parameter
    game_actions = list of ints of length equal to the number of players
		   each entry corresponds to the number of actions for the player

    returns: mixed strategy profiles for each player
    """
    num_players = len(game_actions)
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
		costs.append(expectedValue(i, a, strategies, game_actions, game))
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
print no_regrets(100, .1, [2,2], matchingPennies)

print no_regrets(100,.1, [2,4], t1)

print no_regrets(100, .1, [2,2], sexes)

