# Phillip_Daniels_Agents.py
# ---------
# Phillip Daniels

# COSC4550/COSC5550
# Artificial Intelligence
# University of Wyoming
# ---------
# Most code was part of the Pacman AI projects by John DeNero and Dan Klein
# Code has been modified for the Cleaning Agents AI Challenge by Joost Huizinga
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
This file contains all of the agents that can be selected to 
control our cleaner robot.  To select an agent, use the '-p' option
when running cleaner.py. 

Please only change the parts of the file you are asked to.
Look for the lines that say

# YOUR CODE HERE #

Good luck!
"""
from game import Directions
from game import Agent
from game import RobotActions
from game import Grid
from sets import Set
import util
import time
import random

class BasicAgent(Agent):
  "An agent that goes Forward until it can't, and then turns in a random direction."
  def getAction(self, state):
    "The agent receives an AgentState (defined in game.py)."
    if state.frontWallSensor == 1:
      if random.random() < 0.5:
        action = RobotActions.TURN_AND_MOVE_LEFT
      else:
        action = RobotActions.TURN_AND_MOVE_RIGHT
    else:
      action = RobotActions.FORWARD

    return action

class SimpleReflexAgent(Agent):
  "A reflex agent you have to implement"
  def getAction(self, state):
    "The agent receives an AgentState (defined in game.py)."
    
    action = RobotActions.FORWARD
	
    if state.leftDustSensor == 0 and state.rightDustSensor == 0 and state.frontDustSensor == 0:
      if state.frontWallSensor == 1 and state.leftWallSensor == 1 and state.rightWallSensor == 1:
        action = RobotActions.TURN_RIGHT
      elif state.frontWallSensor == 1 and state.leftWallSensor == 1 and state.backWallSensor == 1:
        action = RobotActions.TURN_AND_MOVE_RIGHT
      elif state.frontWallSensor == 1 and state.rightWallSensor == 1 and state.backWallSensor == 1:
	    action = RobotActions.TURN_AND_MOVE_LEFT
      elif random.random() < 0.03:
        action = RobotActions.TURN_AND_MOVE_LEFT
      elif random.random() > 0.97:
        action = RobotActions.TURN_AND_MOVE_RIGHT
      elif state.frontWallSensor == 1:
        if state.rightWallSensor == 1 and state.leftWallSensor > 1:
          action = RobotActions.TURN_AND_MOVE_LEFT
        elif state.leftWallSensor == 1 and state.rightWallSensor > 1:
          action = RobotActions.TURN_AND_MOVE_RIGHT
        else:
          if random.random() < 0.49:
            action = RobotActions.TURN_AND_MOVE_LEFT
          else:
	        action = RobotActions.TURN_AND_MOVE_RIGHT
      else:
        action = RobotActions.FORWARD
    else:		
      if state.rightDustSensor >= state.leftDustSensor and state.rightDustSensor > state.frontDustSensor:
        action = RobotActions.TURN_AND_MOVE_RIGHT
      elif state.leftDustSensor >= state.rightDustSensor and state.leftDustSensor > state.frontDustSensor:
        action = RobotActions.TURN_AND_MOVE_LEFT
      else:
        action = RobotActions.FORWARD
		
    return action

class ModelBasedReflexAgent(Agent):
  "A reflex agent you have to implement"
  def __init__(self):
    self.board = [[0 for i in range(20)] for j in range(20)]
	
    self.left = 0
    self.right = 0
    self.front = 0
	
    at_a_wall = False
    no_dust = True
	
    self.left_valid = True
    self.right_valid = True
    self.forward_valid = True
	
    self.step_one = False
    self.step_two = False

  def getAction(self, state):
    "The agent receives an AgentState (defined in game.py)."
    position = state.getPosition()
    x = position[0]
    y = position[1]
    if self.board[x][y] != 1000:
      self.board[x][y] = 1 + self.board[x][y]
	
    if state.leftDustSensor == 0 and state.rightDustSensor == 0 and state.frontDustSensor == 0:
      self.no_dust = True
    else:
      self.no_dust = False
    if state.frontWallSensor == 1 or state.rightWallSensor == 1 or state.leftWallSensor == 1:
      self.at_a_wall = True
      if self.no_dust == True:
        self.board[x][y] = 2 + self.board[x][y]
    else:
      self.at_a_wall = False	
	
    self.left_valid = True
    self.right_valid = True
    self.forward_valid = True
	
    if state.leftWallSensor == 1 and state.getDirection() == 'North':
      self.left_valid = False
	  
    if state.leftWallSensor == 1 and state.getDirection() == 'South':
      self.right_valid = False
	  
    if state.rightWallSensor == 1 and state.getDirection() == 'North':
      self.right_valid = False
	  
    if state.rightWallSensor == 1 and state.getDirection() == 'South':
      self.left_valid = False

    adjacent_matrix =[0]*9

    if self.left_valid == True and self.right_valid == True:
      adjacent_matrix[0] = self.board[x-1][y-1]
      adjacent_matrix[1] = self.board[x][y-1]
      adjacent_matrix[2] = self.board[x+1][y-1]
      adjacent_matrix[3] = self.board[x-1][y]
      adjacent_matrix[4] = self.board[x][y]
      adjacent_matrix[5] = self.board[x+1][y]
      adjacent_matrix[6] = self.board[x-1][y+1]
      adjacent_matrix[7] = self.board[x][y+1]
      adjacent_matrix[8] = self.board[x+1][y+1]
	
    elif self.left_valid == True and self.right_valid == False:
      adjacent_matrix[0] = self.board[x-1][y-1]
      adjacent_matrix[1] = self.board[x][y-1]
      adjacent_matrix[2] = 1000
      adjacent_matrix[3] = self.board[x-1][y]
      adjacent_matrix[4] = self.board[x][y]
      adjacent_matrix[5] = 1000
      adjacent_matrix[6] = self.board[x-1][y+1]
      adjacent_matrix[7] = self.board[x][y+1]
      adjacent_matrix[8] = 1000
	  
    elif self.left_valid == False and self.right_valid == True:
      adjacent_matrix[0] = 1000
      adjacent_matrix[1] = self.board[x][y-1]
      adjacent_matrix[2] = self.board[x+1][y-1]
      adjacent_matrix[3] = 1000
      adjacent_matrix[4] = self.board[x][y]
      adjacent_matrix[5] = self.board[x+1][y]
      adjacent_matrix[6] = 1000
      adjacent_matrix[7] = self.board[x][y+1]
      adjacent_matrix[8] = self.board[x+1][y+1]
	  
    else:
      adjacent_matrix[0] = 1000
      adjacent_matrix[1] = self.board[x][y-1]
      adjacent_matrix[2] = 1000
      adjacent_matrix[3] = 1000
      adjacent_matrix[4] = self.board[x][y]
      adjacent_matrix[5] = 1000
      adjacent_matrix[6] = 1000
      adjacent_matrix[7] = self.board[x][y+1]
      adjacent_matrix[8] = 1000
	
    action = RobotActions.FORWARD
	#       N
	#     6 7 8
	#  W  3 A 5  E
	#     0 1 2
	#       S
	
    if state.getDirection() == 'North':
      self.left = adjacent_matrix[3]
      self.right = adjacent_matrix[5]
      self.front = adjacent_matrix[7]
    elif state.getDirection() == 'South':
      self.left = adjacent_matrix[5]
      self.right = adjacent_matrix[3]
      self.front = adjacent_matrix[1]
    elif state.getDirection() == 'East':
      self.left = adjacent_matrix[7]
      self.right = adjacent_matrix[1]
      self.front = adjacent_matrix[5]
    else:
      self.left = adjacent_matrix[1]
      self.right = adjacent_matrix[7]
      self.front = adjacent_matrix[3]
	  
    temp = random.random()
	
    if (state.leftWallSensor == 1 and state.rightWallSensor == 1 and state.frontWallSensor == 1) or (self.left == 1000 and self.right == 1000 and self.front == 1000):
      self.step_one = True
      action = RobotActions.TURN_RIGHT
    elif self.step_one == True:
      self.step_one = False
      self.board[x][y] = 1000
      action = RobotActions.TURN_AND_MOVE_RIGHT	
    elif state.leftDustSensor == 0 and state.rightDustSensor == 0 and state.frontDustSensor == 0 and state.frontWallSensor > 1:
      if temp < 0.02:
        action = RobotActions.TURN_AND_MOVE_LEFT
      elif temp > 0.97:
        action = RobotActions.TURN_AND_MOVE_RIGHT	
      elif temp < 0.09 and temp > 0.06:
       action = RobotActions.FORWARD
      elif self.left < self.right and self.left != 1000:
        if self.left < self.front:
          action = RobotActions.TURN_AND_MOVE_LEFT
      elif self.right < self.left and self.right != 1000:
        if self.right < self.front:
          action = RobotActions.TURN_AND_MOVE_RIGHT
      else:
	    action = RobotActions.FORWARD	  
    elif state.frontWallSensor == 1 and state.leftDustSensor == 0 and state.rightDustSensor == 0 and state.frontDustSensor == 0:
      if state.rightWallSensor == 1 and state.leftWallSensor > 1:
        action = RobotActions.TURN_AND_MOVE_LEFT
      elif state.leftWallSensor == 1 and state.rightWallSensor > 1:
        action = RobotActions.TURN_AND_MOVE_RIGHT
      else:
        if random.random() < 0.49:
          action = RobotActions.TURN_AND_MOVE_LEFT
        else:
          action = RobotActions.TURN_AND_MOVE_RIGHT
    else:		
      if state.rightDustSensor >= state.leftDustSensor and state.rightDustSensor > state.frontDustSensor:
        action = RobotActions.TURN_AND_MOVE_RIGHT
      elif state.leftDustSensor >= state.rightDustSensor and state.leftDustSensor > state.frontDustSensor:
        action = RobotActions.TURN_AND_MOVE_LEFT
      else:
        action = RobotActions.FORWARD
    return action

class UtilityBasedAgent(Agent):
  "A utility-based agent you have to implement"
  def __init__(self):
    # YOUR CODE HERE #
    util.raiseNotDefined()
  
  def getAction(self, state):
    "The agent receives an AgentState (defined in game.py)."
    # YOUR CODE HERE #
    util.raiseNotDefined()
    return action