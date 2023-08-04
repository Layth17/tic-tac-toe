from board import Board
from player import Player
from human import HumanPlayer

def train(iter=5000):
  # training
  p1 = Player("p1")
  p2 = Player("p2")
  st = Board(p1, p2)
  
  print("training...")
  st.play(iter)
  p1.savePolicy(suffix=f"{iter}")
  print("done training!\n")
  return None

def main():
  ITER = 50000
  TRAIN_MODE = False
  if TRAIN_MODE: train(ITER)
  
  # play computer vs human
  p1 = Player("computer", exp_rate=0)
  p1.loadPolicy(f"policy_p1_50000")

  p2 = HumanPlayer("human")

  st = Board(p1, p2)
  st.playHuman()

if __name__ == "__main__":
  main()