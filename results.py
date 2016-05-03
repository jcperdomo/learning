from utils import Game
from fict_play import fictPlay
from mult_weights import no_regrets

print 'RESULTS:'
print '===================='

print
print ('Outputs are lists where the index is the agent and the value is a'
       ' mixed strategy represented by a mapping from actions to'
       ' probabilities.')
print

print "Prisoner's Dilemma:"
print '--------------------'
pd = Game('PrisonersDilemma.game')
print 'Fictitious Play:\t', fictPlay(pd, 2000)
print 'Multpilicative Weights:\t', no_regrets(pd, 100, .1)
print

print "Matching Pennies:"
print '--------------------'
mp = Game('MatchingPennies.game')
print 'Fictitious Play:\t', fictPlay(mp, 2000)
print 'Multpilicative Weights:\t', no_regrets(mp, 100, .1)
print

print "Rock, Paper, Scissors:"
print '--------------------'
rps = Game('RockPaperScissors.game')
print 'Fictitious Play:\t', fictPlay(rps, 2000)
print 'Multpilicative Weights:\t', no_regrets(rps, 100, .1)
print

print "Battle of the Sexes:"
print '--------------------'
bots = Game('BattleOfTheSexes.game')
print 'Fictitious Play:\t', fictPlay(bots, 2000)
print 'Multpilicative Weights:\t', no_regrets(bots, 100, .1)
print

print "A Simple Sequential Game:"
print '--------------------'
t1 = Game('T1.game')
print 'Fictitious Play:\t', fictPlay(t1, 2000)
print 'Multpilicative Weights:\t', no_regrets(t1, 100, .1)
print

print "Chicken:"
print '--------------------'
chicken = Game('Chicken.game')
print 'Fictitious Play:\t', fictPlay(chicken, 2000)
print 'Multpilicative Weights:\t', no_regrets(chicken, 100, .1)
print

print "Multiplication Gadget:"
print '--------------------'
gadget = Game('Gadget.game')
print 'Fictitious Play:\t', fictPlay(gadget, 2000)
print 'Multpilicative Weights:\t', no_regrets(gadget, 100, .1)
print

print "A Public Goods Game:"
print '--------------------'
pgg = Game('PublicGoods.game')
print 'Fictitious Play:\t', fictPlay(pgg, 2000)
print 'Multpilicative Weights:\t', no_regrets(pgg, 100, .1)
print
