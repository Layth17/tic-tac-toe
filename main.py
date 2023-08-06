from board import Board
from player import Player
from human import HumanPlayer
import os
from datetime import datetime

TIMESTAMP = f'{datetime.now().day}{datetime.now().month}{datetime.now().year}_{datetime.now().hour}{datetime.now().minute}{datetime.now().second}'
ITER = 50000
TRAIN_MODE = True
PLAYER="p1"
  
def createDirectories():
  directory_path = f'./policies/logs_{TIMESTAMP}'
  os.makedirs(directory_path)
  print(f"Directory '{directory_path}' created.")
  return None

def train(iter=1000):
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

def main():
  policy = "policy_default_50000"
  if TRAIN_MODE:
    createDirectories()
    train(ITER)
    policy = f"./policies/logs_{TIMESTAMP}/policy_{PLAYER}"
  
  # play computer vs human
  p1 = Player("computer", exp_rate=0)
  print(f"Loaded policy: {policy}")
  p1.loadPolicy(policy)

  p2 = HumanPlayer("human")

  st = Board(p1, p2)
  st.playHuman()

if __name__ == "__main__":
  main()