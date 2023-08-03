import numpy as np
import pickle

class Player:
  
  def __init__(self, name, exp_rate=0.3):
    self.name = name
    self.states = []  # record all positions taken
    self.lr = 0.2 # learning rate
    
    # ϵ-greedy method to balance between exploration and exploitation
    # exp_rate = .3 
    # ==> 70% of the time our agent will take greedy action
    # ==> 30% random action
    self.exp_rate = exp_rate
    
    self.decay_gamma = 0.9
    self.states_value = {}  # state -> value
    
  def getHash(self, board, dim=3):
    boardHash = str(board.reshape(dim * dim))
    return boardHash
      
  def chooseAction(self, positions, current_board, symbol):
      # generate a random percentage and check if
      # it meets our random move threshold
      if np.random.uniform(0, 1) <= self.exp_rate:
        idx = np.random.choice(len(positions))
        action = positions[idx]
      else:
        value_max = -999
        for p in positions:
          # housekeeping
          next_board = current_board.copy()
          next_board[p] = symbol
          next_boardHash = self.getHash(next_board)
          
          # if hash for next state does not exist, then return 0 otherwise get that value
          value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
          # print("value", value)
          if value >= value_max:
            value_max = value
            action = p
      # print(f"{self.name} takes action {action}")
      return action
  
  def feedReward(self, reward) -> None:
    # at the end of game, backpropagate and update states value
    for st in reversed(self.states):
      # init value
      if self.states_value.get(st) is None:
        self.states_value[st] = 0
      
      # update value
      self.states_value[st] += self.lr * (self.decay_gamma * reward - self.states_value[st])
      reward = self.states_value[st]
    return None

  def addState(self, state) -> None:
    self.states.append(state)
    return None

  def reset(self):
    self.states = []

  def savePolicy(self):
    fw = open('policy_' + str(self.name), 'wb')
    pickle.dump(self.states_value, fw)
    fw.close()

  def loadPolicy(self, file):
    fr = open(file, 'rb')
    self.states_value = pickle.load(fr)
    fr.close()

