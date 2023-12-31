import numpy as np
from tqdm import trange

class Board:

  def __init__(self, p1, p2, DIM=3, KEY="0000"):
    self.dim = DIM
    self.board = np.zeros((self.dim, self.dim))
    self.BOARD_SIZE = self.dim * self.dim
    self.key = KEY
    
    # this is a player class
    self.p1 = p1 
    self.p2 = p2
    
    self.isEnd: bool = False
    self.boardHase: str = None
    self.playerSymbol: int = 1
  
  def getHash(self) -> str:
    # creates a unique board hash
    self.boardHash = str(self.board.reshape(self.BOARD_SIZE))
    return self.boardHash
  
  def availablePositions(self) -> list:
    # just iterate over and print free pos
    positions: list = []
    for i in range(self.dim):
        for j in range(self.dim):
            if self.board[i, j] == 0:
                positions.append((i, j))  # need to be tuple
    return positions
  
  def updateState(self, position):
    self.board[position] = self.playerSymbol
    # switch to another player after the current player has made his/her move
    self.playerSymbol = -1 if self.playerSymbol == 1 else 1
  
  def winner(self) -> int:
    # 1 for p1, -1 for p2, 0 for draw,
    # None for not the end of the game
    # consider optimizing this function
    
    # row
    for i in range(self.dim):
        if sum(self.board[i, :]) == self.dim:
            self.isEnd = True
            return 1
        if sum(self.board[i, :]) == -self.dim:
            self.isEnd = True
            return -1
    # col
    for i in range(self.dim):
        if sum(self.board[:, i]) == self.dim:
            self.isEnd = True
            return 1
        if sum(self.board[:, i]) == -self.dim:
            self.isEnd = True
            return -1
    # diagonal
    diag_sum1 = sum([self.board[i, i] for i in range(self.dim)])
    diag_sum2 = sum([self.board[i, self.dim - i - 1] for i in range(self.dim)])
    diag_sum = max(abs(diag_sum1), abs(diag_sum2))
    if diag_sum == self.dim:
        self.isEnd = True
        if diag_sum1 == self.dim or diag_sum2 == self.dim:
            return 1
        else:
            return -1

    # tie
    # no available positions
    if len(self.availablePositions()) == 0:
        self.isEnd = True
        return 0
      
    # not end
    self.isEnd = False
    return None
  
  def reward(self):
    # this reward function is simple
    # it makes assessment based on the
    # results of the game only
    
    result = self.winner()
    # backpropagate reward
    if result == 1: # player 1 winning
        self.p1.feedReward(1)
        self.p2.feedReward(0)
    elif result == -1: # player 2 winning
        self.p1.feedReward(0)
        self.p2.feedReward(1)
    else: # draw
        # punish p1 more harshly since we want it to win
        self.p1.feedReward(0.1)
        self.p2.feedReward(0.5)
    return None
  
  def logBoard(self):
    # p1: x  p2: o
    # 
    #  1|2|3  
    #  -+-+-
    #  4|5|6       
    #  -+-+-     
    #  7|8|9
    
    board = open(f'../policies/{self.dim}/logs_{self.key}/board.txt', 'at')
    prefix = '#   '
    board.write(f"#  {self.p1.name}: x  {self.p2.name}: o\n")
    board.write(f"{prefix}\n")
    out = ""
    div = '-+' * (self.dim - 1)
    for i in range(0, self.dim):
      for j in range(0, self.dim):
        if self.board[i, j] == 1:
            token = 'x'
        if self.board[i, j] == -1:
            token = 'o'
        if self.board[i, j] == 0:
            token = " "
        # detect if it is the last item in a row
        out += token if j == self.dim - 1 else token + '|'
      board.write(f"{prefix}{out}\n")
      out = ""
      
      if i < self.dim - 1: board.write(f'{prefix}{div}-\n') 
    board.write("#\n")

  def showBoard(self):
    # p1: x  p2: o
    # 
    #  1|2|3  
    #  -+-+-
    #  4|5|6       
    #  -+-+-     
    #  7|8|9
    
    prefix = '#   '
    div = '-+' * (self.dim - 1)
    print()
    print(f"#  {self.p1.name}: x  {self.p2.name}: o")
    print(f"{prefix}")
    out = ""
    for i in range(0, self.dim):
      for j in range(0, self.dim):
        if self.board[i, j] == 1:
            token = 'x'
        if self.board[i, j] == -1:
            token = 'o'
        if self.board[i, j] == 0:
            token = " "
        # detect if it is the last item in a row
        out += token if j == self.dim - 1 else token + '|'
      print(f"{prefix}{out}")
      out = ""
      
      if i < self.dim - 1: print(f'{prefix}{div}-') 
    print("#\n")

  def reset(self):
    self.board = np.zeros((self.dim, self.dim))
    self.boardHash = None
    self.isEnd = False
    self.playerSymbol = 1
        
  def play(self, rounds=100):
    #actionFile = open(f'../policies/{self.dim}/logs_{self.key}/action.csv', 'wt')
    #actionFile.write("rounds,player,action\n")
    
    for i in trange(1, rounds + 1):
      while not self.isEnd:
        # Player 1
        positions = self.availablePositions()
        p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol, self.dim)
        # take action and upate board state
        self.updateState(p1_action)
        board_hash = self.getHash()
        self.p1.addState(board_hash)
        
        # log
        #actionFile.write(f"{i},{self.p1.name},{p1_action}\n")
        
        # check board status if it is end
        win = self.winner()
        
        # if it is the end, give rewards and reset
        if win is not None:
          self.logBoard()
          # ended with p1 either win or draw
          self.reward()
          self.p1.reset()
          self.p2.reset()
          self.reset()
          break

        else:
          # Player 2
          positions = self.availablePositions()
          p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol, self.dim)
          self.updateState(p2_action)
          board_hash = self.getHash()
          self.p2.addState(board_hash)
          
          # log
          #actionFile.write(f"{i},{self.p2.name},{p2_action}\n")
          
          # check board status if it is end
          win = self.winner()
          
          # if it is the end, give rewards and reset
          if win is not None:
              self.logBoard()
              # ended with p2 either win or draw
              self.reward()
              self.p1.reset()
              self.p2.reset()
              self.reset()
              break
        
  def playHuman(self):
    """
    # play with human
    """
    
    while not self.isEnd:
      # Player 1
      positions = self.availablePositions()
      
      if self.p1.name == "human":
        self.showBoard() 
        p1_action = self.p1.chooseAction(positions)
      else: 
        p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol, self.dim)
      
      # take action and upate board state
      self.updateState(p1_action)
      self.showBoard()
      # check board status if it is end
      win = self.winner()
      if win is not None:
        if win == 1:
            print(self.p1.name, "wins!")
        else:
            print("tie!")
        self.reset()
        break

      else:
        # Player 2
        positions = self.availablePositions()
        
        if self.p2.name == "human": 
          p2_action = self.p2.chooseAction(positions)
        else: 
          p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol, self.dim)
        
        self.updateState(p2_action)
        self.showBoard()
        win = self.winner()
        if win is not None:
          if win == -1:
              print(self.p2.name, "wins!")
          else:
              print("tie!")
          self.reset()
          break




