from board import Board
from player import Player
from human import HumanPlayer
import os
from datetime import datetime

TIMESTAMP = f'{datetime.now().day}{datetime.now().month}{datetime.now().year}_{datetime.now().hour}{datetime.now().minute}{datetime.now().second}'
ITER = 100_000
TRAIN_MODE = False
PLAYER="p1"
DIM=4 

def createDirectories():
  directory_path = f'../policies/{DIM}/logs_{TIMESTAMP}'
  os.makedirs(directory_path)
  print(f"Directory '{directory_path}' created.")
  return None

def logIter():
  with open(f'../policies/{DIM}/logs_{TIMESTAMP}/log_p1', 'at') as file:
    file.write(f"Iter: {ITER}\n")
  with open(f'../policies/{DIM}/logs_{TIMESTAMP}/log_p2', 'at') as file:
    file.write(f"Iter: {ITER}\n")

def train(iter):
  # training
  p1 = Player("p1", file="../policies/4/logs_1482023_134039/policy_p1")
  p2 = Player("p2", exp_rate=.6, file="../policies/4/logs_1482023_134039/policy_p2")
  st = Board(p1, p2, DIM, TIMESTAMP)
  
  print("training...")
  p1.logDetails(TIMESTAMP, DIM)
  p2.logDetails(TIMESTAMP, DIM)
  
  logIter()
    
  st.play(iter)
  
  p1.savePolicy(TIMESTAMP, DIM)
  p2.savePolicy(TIMESTAMP, DIM)
  print("done training!\n")
  return None

def computerVersusHuman(policy_p1, policy_p2):
  # play computer vs human
  whoStarts = input("Who should start [c]omputer/[h]uman: ")
  try:
    if whoStarts == 'h':
      p1 = HumanPlayer("human", DIM)
      # TODO: I can increase the exp_rate in order to create hard/medium/easy modes
      p2 = Player("computer", exp_rate=0)
      p2.loadPolicy(policy_p2)
      print(f"Loaded policy: {policy_p2}")
    elif whoStarts == 'c':
      p1 = Player("computer", exp_rate=0)
      p1.loadPolicy(policy_p1)
      print(f"Loaded policy: {policy_p1}")

      p2 = HumanPlayer("human", DIM)
    else:
      raise Exception("Sorry, input must be 'h' or 'c' (case sensitive)") 
  except Exception as e:
    print(e)
    exit()
    
  st = Board(p1, p2, DIM=DIM)
  st.playHuman()
  return None

def main():
  # hardcoded policies for gamin'
  # TODO: this needs to be cleaned up
  if DIM == 3:
    policy_p1 = f"../policies/3/logs_582023_19237/policy_p1"
    policy_p2 = f"../policies/3/logs_582023_19237/policy_p2"
  if DIM == 4:
    policy_p1 = f"../policies/4/logs_1482023_174833/policy_p1"
    policy_p2 = f"../policies/4/logs_1482023_174833/policy_p2"
    
  # overwrite with the most recently-trained policy
  if TRAIN_MODE:
    createDirectories()
    train(ITER)
    policy_p1 = f"../policies/{DIM}/logs_{TIMESTAMP}/policy_p1"
    policy_p2 = f"../policies/{DIM}/logs_{TIMESTAMP}/policy_p2"
  
  computerVersusHuman(policy_p1, policy_p2)
  return None

if __name__ == "__main__":
  main()