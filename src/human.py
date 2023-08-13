class HumanPlayer:
    def __init__(self, name, dim=3):
        self.name = name
        self.dim = dim

    def chooseAction(self, positions):
        while True:
            row = int(input(f"Input your action row (1-{self.dim}):"))
            col = int(input(f"Input your action col (1-{self.dim}):"))
            action = (row - 1, col - 1)
            if action in positions:
                return action

    # append a hash state
    def addState(self, state):
        pass

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        pass

    def reset(self):
        pass