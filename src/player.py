import numpy as np
import datetime as dt
import pickle
import json

class Player:
  
  def __init__(self, name, exp_rate=0.3, lr=0.2, decay_gamma=0.9, file=""):
    self.name = name
    self.states = []  # record all positions taken
    self.lr = lr # learning rate
    
    # ϵ-greedy method to balance between exploration and exploitation
    # exp_rate = .3 
    # ==> 70% of the time our agent will take greedy action
    # ==> 30% random action
    self.exp_rate = exp_rate
    
    self.decay_gamma = decay_gamma
    
    # a dict in which the key is a board position
    # and the value is the winning chances broadly speaking (??)
    if file == "": self.states_value = {}  # state -> value
    else: self.loadPolicy(file)
      
  def getHash(self, board, dim=3):
    boardHash = str(board.reshape(dim * dim))
    return boardHash
      
  def chooseAction(self, positions, current_board, symbol, dim):
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
        next_boardHash = self.getHash(next_board, dim)
        
        # if hash for next state does not exist, then return 0 otherwise get that value
        value = 0 if self.states_value.get(next_boardHash) is None else self.states_value.get(next_boardHash)
        # print("value", value)
        if value >= value_max:
          value_max = value
          action = p
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

  def logDetails(self, key="", dim=3):
    with open(f'../policies/{dim}/logs_{key}/log_{self.name}', 'wt') as file:
      file.write(f"Learning rate: {self.lr}\n")
      file.write(f"Decay gamma: {self.decay_gamma}\n")
      file.write(f"Exploration Rate: {self.exp_rate}\n")
      file.write(f"Dim: {dim}x{dim}\n")
    return None
  
  def savePolicy(self, key="", dim=3):
    fw = open(f'../policies/{dim}/logs_{key}/policy_{self.name}', 'wb')
    pickle.dump(self.states_value, fw)
    fw.close()
    self.saveReadablePolicy(key, dim)
    
  def saveReadablePolicy(self, key="", dim=3):
      with open(f'../policies/{dim}/logs_{key}/readable_policy_{self.name}.txt', 'wt') as f:
        json.dump(pickle.load(open(f'../policies/{dim}/logs_{key}/policy_{self.name}', 'rb')),
                  f,
                  indent=2)

  def loadPolicy(self, file):
    fr = open(file, 'rb')
    self.states_value = pickle.load(fr)
    fr.close()

