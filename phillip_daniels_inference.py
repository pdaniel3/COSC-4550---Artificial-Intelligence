# inference.py
# ------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import itertools
import util
import random
import busters
import game
from game import Actions
from game import Directions
from baseInference import InferenceModule
from bustersAgents import BustersAgent
from distanceCalculator import Distancer


#####################################################
#             Questions 1a and 1b                   #
#####################################################

class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward-algorithm
    updates to compute the exact belief function at each time step.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        """
        Updates beliefs based on the distance observation and Pacman's position.

        The noisyDistance is the estimated manhattan distance to the ghost you are tracking.

        The observationDistribution below stores the probability of the noisyDistance for any true
        distance you supply.  That is, it stores P(noisyDistance | TrueDistance).

        self.legalPositions is a list of the possible ghost positions (you
        should only consider positions that are in self.legalPositions).

        A correct implementation will handle the following special case:
          *  When a ghost is captured by Pacman, all beliefs should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition()

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

        """


        "xxxx*** YOUR CODE HERE ***"
        # Replace parts of this code with a correct observation update
        # You should find many (but not all) af the statements below useful in your solution.
        # Be sure to handle the "jail" edge case where the ghost is eaten
        # and noisyDistance is None
        
	noisyDistance = observation
	observationDistribution = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        newBeliefs = util.Counter()
	if noisyDistance != None:
	  for p in self.legalPositions:
            trueDistance = util.manhattanDistance(p, pacmanPosition)
            if observationDistribution[trueDistance] > 0: 
              newBelief = self.beliefs[p] * observationDistribution[trueDistance] 
              newBeliefs[p] = newBelief 
        else:
          for p in self.legalPositions:
            newBeliefs[p] = 0.0
          newBeliefs[self.getJailPosition()] = 1.0  
        newBeliefs.normalize()
        self.beliefs = newBeliefs
        "*** END YOUR CODE HERE ***"

    def elapseTime(self, gameState):
        """
        Update self.beliefs in response to a time step passing from the current state.

        The transition model is not entirely stationary: it may depend on Pacman's
        current position (e.g., for DirectionalGhost).  However, this is not a problem,
        as Pacman's current position is known.

        In order to obtain the distribution over new positions for the
        ghost, given its previous position (oldPos) as well as Pacman's
        current position, use this line of code:

          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

        Note that you may need to replace "oldPos" with the correct name
        of the variable that you have used to refer to the previous ghost
        position for which you are computing this distribution. You will need to compute
        multiple position distributions for a single update.

        newPosDist is a util.Counter object, where for each position p in self.legalPositions,

        newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )

        (and also given Pacman's current position).  You may also find it useful to loop over key, value pairs
        in newPosDist, like:

          for newPos, prob in newPosDist.items():
            ...

        *** GORY DETAIL AHEAD ***

        As an implementation detail (with which you need not concern
        yourself), the line of code at the top of this comment block for obtaining newPosDist makes
        use of two helper methods provided in InferenceModule above:

          1) self.setGhostPosition(gameState, ghostPosition)
              This method alters the gameState by placing the ghost we're tracking
              in a particular position.  This altered gameState can be used to query
              what the ghost would do in this position.

          2) self.getPositionDistribution(gameState)
              This method uses the ghost agent to determine what positions the ghost
              will move to from the provided gameState.  The ghost must be placed
              in the gameState with a call to self.setGhostPosition above.

        It is worthwhile, however, to understand why these two helper methods are used and how they
        combine to give us a belief distribution over new positions after a time update from a particular position
        """

        "xxxx*** YOUR CODE HERE ***"
        newBeliefs = util.Counter()
        for p in self.legalPositions:
          for q in self.getPositionDistribution(self.setGhostPosition(gameState, p)):
            newBeliefs[q] = self.beliefs[p] * self.getPositionDistribution(self.setGhostPosition(gameState, p))[q] + newBeliefs[q]
        newBeliefs.normalize()
        self.beliefs = newBeliefs
 
    def getBeliefDistribution(self):
        return self.beliefs


#####################################################
#                  Question 1c                      #
#####################################################

class GreedyBustersAgent(BustersAgent):
    "An agent that charges the closest ghost."

    def registerInitialState(self, gameState):
        "Pre-computes the distance between every two points."
        BustersAgent.registerInitialState(self, gameState)
        self.distancer = Distancer(gameState.data.layout, False)

    def chooseAction(self, gameState):
        """
        First computes the most likely position of each ghost that
        has not yet been captured, then chooses an action that brings
        Pacman closer to the closest ghost (in maze distance!).

        To find the maze distance between any two positions, use:
        self.distancer.getDistance(pos1, pos2)

        To find the successor position of a position after an action:
        successorPosition = Actions.getSuccessor(position, action)

        livingGhostPositionDistributions, defined below, is a list of
        util.Counter objects equal to the position belief distributions
        for each of the ghosts that are still alive.  It is defined based
        on (these are implementation details about which you need not be
        concerned):

          1) gameState.getLivingGhosts(), a list of booleans, one for each
             agent, indicating whether or not the agent is alive.  Note
             that pacman is always agent 0, so the ghosts are agents 1,
             onwards (just as before).

          2) self.ghostBeliefs, the list of belief distributions for each
             of the ghosts (including ghosts that are not alive).  The
             indices into this list should be 1 less than indices into the
             gameState.getLivingGhosts() list.

        """
        pacmanPosition = gameState.getPacmanPosition()
        legal = [a for a in gameState.getLegalPacmanActions()]
        livingGhosts = gameState.getLivingGhosts()
        livingGhostPositionDistributions = [beliefs for i,beliefs
                                            in enumerate(self.ghostBeliefs)
                                            if livingGhosts[i+1]]
        "xxxx*** YOUR CODE HERE ***"
        gList = list()
        for p in livingGhostPositionDistributions:
          largestLGPD = p.argMax()
          gList.append(largestLGPD)
        g = pacmanPosition
        smallest = 999999999
        for q in gList:
          distancerF = self.distancer.getDistance(pacmanPosition, q)
          if distancerF < smallest:
            smallest = distancerF
            g = q                
        nextA = legal[0]
        dist = 999999999
        for a in legal:
          successorPosition =  Actions.getSuccessor(pacmanPosition, a)
          nextDist = self.distancer.getDistance(successorPosition, g)
          if nextDist < dist:
            nextA = a
            dist = nextDist
        return nextA

#####################################################
#             Questions 2a and 2b                   #
#####################################################

class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.

    Useful helper functions will include random.choice, which chooses
    an element from a list uniformly at random, and util.sample, which
    samples a key from a Counter by treating its values as probabilities.
    """


    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent);
        self.setNumParticles(numParticles)
        self.particles = []

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles


    def initializeUniformly(self, gameState):
        """
          Initializes a list of particles. Use self.numParticles for the number of particles.
          Use self.legalPositions for the legal board positions where a particle could be located.
          Particles should be evenly (not randomly) distributed across positions in order to
          ensure a uniform prior.

          ** NOTE **
          The only thing you should store are the particles. The particles can be stored as a list
          (as suggested by the __init__ function) where each element is a single particle 
          or they can be stored in a dictionary that keeps track of the number of partciles at each position.

          What should NOT be stored are the weights or probabilities. Recalculate the probabilities
          from your current set of partciles in the getBeliefDistribution function. Storing the weights
          can lead to some very odd errors.
        """
        "xxxx*** YOUR CODE HERE ***"
	def function(x, y):
	  if x > len(y) or x < 0: 
	    return list(y)
          s = int((len(y) - 1.0)/(x - 1.0))
          epsilon = list()
          for z in range(x):
            product = s*z 
            epsilon.append(y[product])
          return epsilon
        self.particles = list()
        u = self.numParticles
        self.particles.extend(function(u, self.legalPositions))
        while u > 0:
          eS = function(u, self.legalPositions)
          self.particles.extend(eS)
          u = u-len(eS)

    def observe(self, observation, gameState):
        """
        Update beliefs based on the given distance observation. Make
        sure to handle the special case where all particles have weight
        0 after reweighting based on observation. If this happens,
        resample particles uniformly at random from the set of legal
        positions (self.legalPositions).

        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, **all** particles should be updated so
             that the ghost appears in its prison cell, self.getJailPosition()

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

          2) When all particles receive 0 weight, they should be recreated from the
             prior distribution by calling initializeUniformly. The total weight
             for a belief distribution can be found by calling totalCount on
             a Counter object

        util.sample(Counter object) is a helper method to generate a sample from
        a belief distribution

        You may also want to use util.manhattanDistance to calculate the distance
        between a particle and pacman's position.
        """

        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        "xxxx*** YOUR CODE HERE ***"
        if noisyDistance is not None:
          beliefDist = self.getBeliefDistribution()
	  new = util.Counter()
          for p in self.legalPositions:
            distance = util.manhattanDistance(p, pacmanPosition)
            new[p] = beliefDist[p] * emissionModel[distance] + new[p]
          if new.totalCount() != 0:
            self.particles = list()
            for x in range(self.numParticles):
              self.particles.append(util.sample(new))		  
          else:
            self.initializeUniformly(gameState)		
        else:	
          self.particles = self.numParticles * [self.getJailPosition()] 
        
    def elapseTime(self, gameState):
        """
        Update beliefs for a time step elapsing.

        As in the elapseTime method of ExactInference, you should use:

          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

        to obtain the distribution over new positions for the ghost, given
        its previous position (oldPos) as well as Pacman's current
        position.

        util.sample(Counter object) is a helper method to generate a sample from a
        belief distribution
        """
        "xxxx*** YOUR CODE HERE ***"
        list1 = list()
        for p in self.particles:
          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, p))
          list1.append(util.sample(newPosDist))
        self.particles = list1

    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "xxxx*** YOUR CODE HERE ***"
        bDist = util.Counter()
        for p in self.particles:
          bDist[p] = bDist[p] + 1.0
        bDist.normalize()
        return bDist


#####################################################
#             Questions 3a and 3b                   #
#####################################################

class MarginalInference(InferenceModule):
    "A wrapper around the JointInference module that returns marginal beliefs about ghosts."

    def initializeUniformly(self, gameState):
        "Set the belief state to an initial, prior value."
        if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observeState(self, gameState):
        "Update beliefs based on the given distance observation and gameState."
        if self.index == 1: jointInference.observeState(gameState)

    def elapseTime(self, gameState):
        "Update beliefs for a time step elapsing from a gameState."
        if self.index == 1: jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        "Returns the marginal belief over a particular ghost by summing out the others."
        jointDistribution = jointInference.getBeliefDistribution()
        dist = util.Counter()
        for t, prob in jointDistribution.items():
          dist[t[self.index - 1]] += prob
        return dist

class JointParticleFilter:
    "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."

    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)
        self.particles = []

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initialize(self, gameState, legalPositions):
        "Stores information about the game, then initializes particles."
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeParticles()

    def initializeParticles(self):
        """
        Initialize particles to be consistent with a uniform prior.  

        Each particle is a tuple of ghost positions. Use self.numParticles for
        the number of particles. You may find the python package 'itertools' helpful.  
        Specifically, you will need to think about permutations of legal ghost
        positions, with the additional understanding that ghosts may occupy the
        same space. Look at the 'product' function in itertools to get an
        implementation of the catesian product. Note: If you use
        itertools, keep in mind that permutations are not returned in a random order;
        you must shuffle the list of permutations in order to ensure even placement
        of particles across the board. Use self.legalPositions to obtain a list of
        positions a ghost may occupy.

          ** NOTE **
          The only thing you should store are the particles. The particles can be stored as a list
          (as suggested by the __init__ function) where each element is a single particle 
          or they can be stored in a dictionary that keeps track of the number of partciles at each position.

          What should NOT be stored are the weights or probabilities. Recalculate the probabilities
          from your current set of partciles in the getBeliefDistribution function. Storing the weights
          can lead to some very odd errors.

        """
        "*** YOUR CODE HERE ***"

    def addGhostAgent(self, agent):
        "Each ghost agent is registered separately and stored (in case they are different)."
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1);

    def observeState(self, gameState):
        """
        Resamples the set of particles using the likelihood of the noisy observations.

        To loop over the ghosts, use:

          for i in range(self.numGhosts):
            ...

        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, all particles should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition(i)
             where "i" is the index of the ghost.

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

          2) When all particles receive 0 weight, they should be recreated from the
              prior distribution by calling initializeParticles. After all particles
              are generated randomly, any ghosts that are eaten (have noisyDistance of 0)
              must be changed to the jail Position. This will involve changing each
              particle if a ghost has been eaten.

        ** Remember ** We store particles as tuples, but to edit a specific particle,
        it must be converted to a list, edited, and then converted back to a tuple. Since
        this is a common operation when placing a ghost in the jail for a particle, we have
        provided a helper method named self.getParticleWithGhostInJail(particle, ghostIndex)
        that performs these three operations for you.

        """
        pacmanPosition = gameState.getPacmanPosition()
        noisyDistances = gameState.getNoisyGhostDistances()
        if len(noisyDistances) < self.numGhosts: return
        emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]

        "*** YOUR CODE HERE ***"

    def getParticleWithGhostInJail(self, particle, ghostIndex):
        particle = list(particle)
        particle[ghostIndex] = self.getJailPosition(ghostIndex)
        return tuple(particle)

    def elapseTime(self, gameState):
        """
        Samples each particle's next state based on its current state and the gameState.

        To loop over the ghosts, use:

          for i in range(self.numGhosts):
            ...

        Then, assuming that "i" refers to the index of the
        ghost, to obtain the distributions over new positions for that
        single ghost, given the list (prevGhostPositions) of previous
        positions of ALL of the ghosts, use this line of code:

          newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, prevGhostPositions),
                                                       i, self.ghostAgents[i])

        **Note** that you may need to replace "prevGhostPositions" with the
        correct name of the variable that you have used to refer to the
        list of the previous positions of all of the ghosts, and you may
        need to replace "i" with the variable you have used to refer to
        the index of the ghost for which you are computing the new
        position distribution.

        As an implementation detail (with which you need not concern
        yourself), the line of code above for obtaining newPosDist makes
        use of two helper functions defined below in this file:

          1) setGhostPositions(gameState, ghostPositions)
              This method alters the gameState by placing the ghosts in the supplied positions.

          2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
              This method uses the supplied ghost agent to determine what positions
              a ghost (ghostIndex) controlled by a particular agent (ghostAgent)
              will move to in the supplied gameState.  All ghosts
              must first be placed in the gameState using setGhostPositions above.

              The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],
              but in this project all ghost agents are always the same.
        """
        newParticles = []
        for oldParticle in self.particles:
            newParticle = list(oldParticle) # A list of ghost positions

            # now loop through and update each entry in newParticle...

            "*** YOUR CODE HERE ***"

            "*** END YOUR CODE HERE ***"
            newParticles.append(tuple(newParticle))
        self.particles = newParticles

    def getBeliefDistribution(self):
        "*** YOUR CODE HERE ***"
	
# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
    """
    Returns the distribution over positions for a ghost, using the supplied gameState.
    """

    # index 0 is pacman, but the students think that index 0 is the first ghost.
    ghostPosition = gameState.getGhostPosition(ghostIndex+1)
    actionDist = agent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
        successorPosition = game.Actions.getSuccessor(ghostPosition, action)
        dist[successorPosition] = prob
    return dist

def setGhostPositions(gameState, ghostPositions):
    "Sets the position of all ghosts to the values in ghostPositionTuple."
    for index, pos in enumerate(ghostPositions):
        conf = game.Configuration(pos, game.Directions.STOP)
        gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
    return gameState

