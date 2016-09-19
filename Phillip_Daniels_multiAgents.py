# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
from game import Agent
from util import Stack
from util import Queue

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()



class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent and AlphaBetaPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          Directions.STOP:
            The stop direction, which is always legal

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        return self.minimax_prime(gameState,0,0)[0]

    def minimax_prime(self,gameState,j,depth): 
      total_agents = gameState.getNumAgents()
      if j >= total_agents:
        depth = depth+1
	j = 0
      if depth == self.depth:
        return self.evaluationFunction(gameState)
      if j == self.index:
        minimax_prime = ("placeholder", -999999999)
        legal_actions = gameState.getLegalActions(j) 
	if legal_actions:
	  for a in legal_actions:
            if a != "Stop":
              val = self.minimax_prime(gameState.generateSuccessor(j,a),j+1,depth)
              if type(val) is not tuple: 
                new_val = max(minimax_prime[1], val)
                if new_val is not minimax_prime[1]:
                  minimax_prime = (a, new_val)
              else:
                new_val = max(minimax_prime[1], val[1])
                if new_val is not minimax_prime[1]:
                  minimax_prime = (a, new_val)
	else:	
          return self.evaluationFunction(gameState)
        return minimax_prime	
      else:
        minimax_prime = ("placeholder", 999999999)
        legal_actions = gameState.getLegalActions(j) 
	if legal_actions:
	  for a in legal_actions:
            if a != "Stop":
              val = self.minimax_prime(gameState.generateSuccessor(j,a),j+1,depth)
              if type(val) is not tuple: 
                new_val = min(minimax_prime[1], val)
                if new_val is not minimax_prime[1]:
                  minimax_prime = (a, new_val)
              else:
                new_val = min(minimax_prime[1], val[1])
                if new_val is not minimax_prime[1]:
                  minimax_prime = (a, new_val)
	else:	
          return self.evaluationFunction(gameState)
        return minimax_prime

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
      return self.alpha_beta_prime(gameState, 0, 0, -999999999, 999999999)[0]

    def alpha_beta_prime(self, gameState, j, depth, alpha, beta): 
      total_agents = gameState.getNumAgents()
      if j >= total_agents:
        depth = depth+1
	j = 0
      if depth == self.depth:
        return self.evaluationFunction(gameState)
      if j == self.index:
        alpha_beta_prime = ("placeholder", -999999999)
        legal_actions = gameState.getLegalActions(j) 
	if legal_actions:
	  for a in legal_actions:
            if a != "Stop":
              val = self.alpha_beta_prime(gameState.generateSuccessor(j,a),j+1,depth,alpha,beta)
              if type(val) is not tuple:
                new_val = max(alpha_beta_prime[1], val)
                if new_val is not alpha_beta_prime[1]:
                  alpha_beta_prime = (a, new_val) 
                if alpha_beta_prime[1] >= beta:
                  return alpha_beta_prime
                alpha = max(alpha, alpha_beta_prime[1])
              else: 
                new_val = max(alpha_beta_prime[1], val[1])
                if new_val is not alpha_beta_prime[1]:
                  alpha_beta_prime = (a, new_val) 
                if alpha_beta_prime[1] >= beta:
                  return alpha_beta_prime
                alpha = max(alpha, alpha_beta_prime[1])
        else:
          return self.evaluationFunction(gameState)  
        return alpha_beta_prime
      else:
        alpha_beta_prime = ("placeholder", 999999999)
        legal_actions = gameState.getLegalActions(j) 
        if legal_actions:
          for a in legal_actions:
            if a != "Stop":
              val = self.alpha_beta_prime(gameState.generateSuccessor(j,a),j+1,depth,alpha,beta)
              if type(val) is not tuple:
                new_val = min(alpha_beta_prime[1], val)
                if new_val is not alpha_beta_prime[1]:
                  alpha_beta_prime = (a, new_val) 
                if alpha_beta_prime[1] <= alpha:
                  return alpha_beta_prime
                beta = min(beta, alpha_beta_prime[1])
              else: 
                new_val = min(alpha_beta_prime[1], val[1])
                if new_val is not alpha_beta_prime[1]:
                  alpha_beta_prime = (a, new_val) 
                if alpha_beta_prime[1] <= alpha:
                  return alpha_beta_prime
                beta = min(beta, alpha_beta_prime[1])
        else:
          return self.evaluationFunction(gameState)  
        return alpha_beta_prime

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 3).

    You can store some additional information in a game-state using the 
    customData dictionairy. You can store this information in the getAction
    function and retrieve it here. Note that all data will be reset
    the next time getAction is called, so if your data has to be persistent
    between calls to getAction you will have to store the data in your
    search agent and then initialize the dictionairy for every call of
    getAction.

    Also note that a deep copy of the dictionairy is created for every
    call to getSuccessor, meaning that stroring large data structures in
    the dictionairy might make you code really slow. For data that should
    be initialized once and never be altered you might want to consider 
    storing in it a global variable and setting it only the first time
    getAction gets called.

    To store data in the customData dictionairy:
    currentGameState.customData['myData'] = thisIsMyData

    To get data from the customData dictionairy:
    retreivedData = currentGameState.customData['myData']

 q	   Also, do not forget you can set some variables in the __init__ function
    of the MultiAgentSearchAgent and that your agents should still work
    on the problems provided by the autograder.
  """
  "*** YOUR CODE HERE ***"
  capsules = currentGameState.getCapsules()
  food = currentGameState.getFood().asList()
  ghosts = currentGameState.getGhostStates()
  ghosts_afraid = 0
  list_one = list()
  list_two = list()
  list_two.append(0)
  pacman = currentGameState.getPacmanPosition()
  for f in food:
    x_val = pacman[0]-f[0]
    if x_val < 0:
      x_val = -x_val
    y_val = pacman[1]-f[1]
    if y_val < 0:
      y_val = -y_val
    list_one.append(-x_val-y_val)
  if not list_one:
    list_one.append(0)
  for g in ghosts:
    if g.scaredTimer == 0:
      ghosts_afraid = ghosts_afraid+1
    ghost_position = g.getPosition()
    x_val = ghost_position[0] - pacman[0]
    if x_val < 0:
      x_val = -x_val
    y_val = ghost_position[1] - pacman[1]
    if y_val < 0:
      y_val = -y_val
    if y_val-x_val != 0:
      recipricol = 1/(x_val+y_val)
      list_two.append(recipricol)
  evaluation = 2*currentGameState.getScore()+(max(list_one) - max(list_two))-(15*len(ghosts)+15*ghosts_afraid+110*len(capsules)) 
  return evaluation

# Abbreviation
better = betterEvaluationFunction

class UltimateAgent(MultiAgentSearchAgent):
  """
    The best agent you can think of (question 4).
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the excercise is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    
