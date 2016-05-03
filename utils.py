import re
import numpy as np

class Game:
    def __init__(self, filename):
        # read in file
        with open(filename) as f:
            lines = f.readlines()

        # parse file
        self.utilities = {}
        for line in lines:

            # look for number of players
            playersRE = r'.*?Players:\s*?(\d+)'
            m = re.match(playersRE, line)
            if m:
                self.nplayers = int(m.group(1))

            # look for # actions per player
            actionsRE = r'.*?Actions:\s*?(.*)'
            m = re.match(actionsRE, line)
            if m:
                self.nactions = map(int, m.group(1).split())

            # look for utilities
            utilRE = (
                r'\[(?P<profile>.*?)\].*?'
                r'\[\s*(?P<payoffs>.*?)\s*\]'
            )
            m = re.match(utilRE, line)
            if m:
                prof = m.group('profile')
                prof = map(int, prof.split())
                prof = tuple(map(lambda x: x-1, prof)) # make 0-indexed
                payoffs = m.group('payoffs')
                payoffs = tuple(map(float, payoffs.split()))
                self.utilities[prof] = payoffs

    def numPlayers(self):
        """Returns the number of players in the game."""
        return self.nplayers

    def numActions(self):
        """Returns a list where the ith entry is the number of actions for
        agent i."""
        return self.nactions

    def utility(self, actions):
        """Returns utilities given an action profile.

        :actions: List of actions with length equal to number of players
        :returns: List of floats that are payoffs for each player
        """
        return self.utilities[tuple(actions)]


def sampleMixedStrat(mixed):
    """Samples a pure strategy from a mixed strategy.

    :mixed: list of tuples (a, p) where the player plays action a with
    probability p. Probabilities must sum to 1.
    :returns: One of the actions a sampled from the mixed strategy argument.
    """
    actions, probs = zip(*mixed)
    return np.random.choice(actions, size=1, p=probs)[0]
