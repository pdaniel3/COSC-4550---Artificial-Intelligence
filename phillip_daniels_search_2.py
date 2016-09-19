# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms and heuristics.
"""

import util
from util import Stack
from util import Queue
from util import PriorityQueue
from game import Directions

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
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    pq = util.PriorityQueue()
    traversed_nodes = dict()
    current_state = problem.getStartState()
    key_value = dict()
    if problem.isGoalState(current_state):
        return list()
    else:
      pq.push((current_state,list(),0),0)
      while not pq.isEmpty():
        current_state = pq.pop()
        key_value[current_state[0]] = current_state[1]
        if problem.isGoalState(current_state[0]):
          return key_value[current_state[0]]
        if current_state[0] in traversed_nodes and problem.getCostOfActions(current_state[1]) > traversed_nodes[current_state[0]]:
          continue
        else:    
          traversed_nodes[current_state[0]] = problem.getCostOfActions(current_state[1])
          for v in problem.getSuccessors(current_state[0]):
            pq.push((v[0],current_state[1]+[v[1]],v[2]+heuristic(v[0],problem)+problem.getCostOfActions(current_state[1])),v[2]+heuristic(v[0],problem)+problem.getCostOfActions(current_state[1]))

#####################################################
#                  Question 2                       #
#####################################################
def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.
      state:   The current search state
               (a data structure you chose in your search problem)
      problem: The CornersProblem instance for this layout.
    This function should always return a number that is a lower bound
    on the shortest path from the state to a goal of the problem; i.e.
    it should be admissible (as well as consistent).
    """
    corners = problem.corners  # These are the corner coordinates
    walls = problem.walls  # These are the walls of the maze, as a Grid (game.py)
	
    util.raiseNotDefined()

#####################################################
#                  Question 3                       #
#####################################################

def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a
    Grid (see game.py) of either True or False. You can call foodGrid.asList()
    to get a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the problem.
    For example, problem.walls gives you a Grid of where the walls are.

    If you want to *store* information to be reused in other calls to the heuristic,
    there is a dictionary called problem.heuristicInfo that you can use. For example,
    if you only want to count the walls once and store that value, try:
      problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access problem.heuristicInfo['wallCount']
    """
    util.raiseNotDefined()
# Abbreviations
astar = aStarSearch
