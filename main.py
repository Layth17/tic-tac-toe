from board import Board
from player import Player
from human import HumanPlayer

def main():
  # training
  p1 = Player("p1")
  p2 = Player("p2")

  st = Board(p1, p2)
  print("training...")
  st.play(5000)
  p1.savePolicy()
  print("done training!")
  print()
  
  # play with human
  p1 = Player("computer", exp_rate=0)
  p1.loadPolicy(f"policy_p1")

  p2 = HumanPlayer("human")

  st = Board(p1, p2)
  st.play2()

if __name__ == "__main__":
  main()