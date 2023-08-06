from board import Board
from player import Player
from human import HumanPlayer
import os
from datetime import datetime

TIMESTAMP = f'{datetime.now().day}{datetime.now().month}{datetime.now().year}_{datetime.now().hour}{datetime.now().minute}{datetime.now().second}'
ITER = 50_000
TRAIN_MODE = False
PLAYER="p1"
  
def createDirectories():
  directory_path = f'../policies/logs_{TIMESTAMP}'
  os.makedirs(directory_path)
  print(f"Directory '{directory_path}' created.")
  return None

def train(iter):
  # training
  p1 = Player("p1")
  p2 = Player("p2")
  st = Board(p1, p2)
  
  print("training...")
  p1.logDetails(key=TIMESTAMP)
  p2.logDetails(key=TIMESTAMP)
  
  st.play(iter, key=TIMESTAMP)
  
  p1.savePolicy(key=TIMESTAMP)
  p2.savePolicy(key=TIMESTAMP)
  print("done training!\n")
  return None

def computerVersusHuman(policy_p1, policy_p2):
  # play computer vs human
  whoStarts = input("Who should start [c]omputer/[h]uman: ")
  try:
    if whoStarts == 'h':
      p1 = HumanPlayer("human")

      p2 = Player("computer", exp_rate=0)
      p2.loadPolicy(policy_p2)
      print(f"Loaded policy: {policy_p2}")
    elif whoStarts == 'c':
      p1 = Player("computer", exp_rate=0)
      p1.loadPolicy(policy_p1)
      print(f"Loaded policy: {policy_p1}")

      p2 = HumanPlayer("human")
    else:
      raise Exception("Sorry, input must be 'h' or 'c' (case sensitive)") 
  except Exception as e:
    print(e)
    exit()
    
  st = Board(p1, p2)
  st.playHuman()
  return None

def main():
  # hardcoded policies for gamin'
  policy_p1 = "../policies/logs_582023_19237/policy_p1"
  policy_p2 = "../policies/logs_582023_19237/policy_p2"
  
  if TRAIN_MODE:
    createDirectories()
    train(ITER)
    policy_p1 = f"../policies/logs_{TIMESTAMP}/policy_p1"
    policy_p2 = f"../policies/logs_{TIMESTAMP}/policy_p2"
  
  computerVersusHuman(policy_p1, policy_p2)
  return None

if __name__ == "__main__":
  main()