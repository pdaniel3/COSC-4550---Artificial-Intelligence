# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solution_paths, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""
import util

from game import Directions
from game import Agent
from game import Actions

#####################################################
#                Tiny maze example                  #
#####################################################

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]


#####################################################
#                  Question 1                       #
#####################################################

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's xs:", problem.getSuccessors(problem.getStartState())

    Note that get xs does not just, as its name suggests, returns xs.
    It actuall returns a list of triples (x, action, stepCost).
    So to get, for example, the x of the first x, you can do something like:

    firstSuccessorList = problem.getSuccessors(problem.getStartState())
    firstSuccessor, firstAction, firstCost = firstSuccessorList[0]
    secondSuccessor = problem.getSuccessors(firstSuccessor)

    Note that, for this problem, the x is just a Pacman position (x, y).
    IMPORTANT: this will not be the case once we start introducing heuristics,
    xs might be positions, list or pointers to objects your program
    knows nothing about. Do not assume anything about what a x is!
    """
    stack = util.Stack()
    traversed_nodes = list()
    current_state = problem.getStartState()
    dict = {}
    stack.push((problem.getStartState(),list()))
    
    while not stack.isEmpty():
      current_state = stack.pop()
      dict[current_state[0]] = current_state[1]
      if problem.isGoalState(current_state[0]):
        return dict[current_state[0]]
      if current_state[0] not in traversed_nodes:
        traversed_nodes.append(current_state[0])
        for v in problem.getSuccessors(current_state[0]):
          if v[0] not in traversed_nodes:
            stack.push((v[0],current_state[1]+[v[1]]))

#####################################################
#                  Question 2                       #
#####################################################

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    queue = util.Queue()
    traversed_nodes = list()
    current_state = problem.getStartState()
    dict = {}
    queue.push((problem.getStartState(),list()))
    
    while not queue.isEmpty():
      current_state = queue.pop()
      dict[current_state[0]] = current_state[1]
      if problem.isGoalState(current_state[0]):
        return dict[current_state[0]]
      if current_state[0] not in traversed_nodes:
        traversed_nodes.append(current_state[0])
        for v in problem.getSuccessors(current_state[0]):
          if v[0] not in traversed_nodes:
            queue.push((v[0],current_state[1]+[v[1]]))

#####################################################
#                  Question 3                       #
#####################################################

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    
    pq = util.PriorityQueue()
    traversed_nodes = list()
    current_state = problem.getStartState()
    dict = {}
    pq.push((problem.getStartState(),list(),0),0)
    
    while not pq.isEmpty():
      current_state = pq.pop()
      dict[current_state[0]] = current_state[1]
      if problem.isGoalState(current_state[0]):
        return dict[current_state[0]]
      if current_state[0] not in traversed_nodes:
        traversed_nodes.append(current_state[0])
        for v in problem.getSuccessors(current_state[0]):
          if v[0] not in traversed_nodes:
            pq.push((v[0],current_state[1]+[v[1]],current_state[2]+v[2]),current_state[2]+v[2])

#####################################################
#                  Question 4                       #
#####################################################

class ApproximateSearchAgent(Agent):
    """
    Agent that should collect all food in the fewest number of steps possible,
    while all calculations should remain within the time-limit.
    Change anything but the class name.
     
    It is recommmended that you reuse your search algrotihms implemented above.
    To use one of your search algrotihms you'll need a search problem
    (see searchAgents.py for examples of search problems).
    For example, if you want to use the AnyFoodSearchProblem found in searchProblems.py
    you can do the following:
     
    from searchProblems import AnyFoodSearchProblem
    problem = AnyFoodSearchProblem(current)
    solution_path = breadthFirstSearch(problem)
    """

    def registerInitialState(self, current_state):
        """"
		"This method is called before any moves are made.
         You can do most of your searching here, and simply
         execute the move in getAction"
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
        """
    def getAction(self, current_state):
        """
        From game.py:
        The Agent will receive a GameState and must return an action from
        Directions.{North, South, East, West, Stop}
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
