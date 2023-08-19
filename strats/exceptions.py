

class InsufficientFunds(Exception):
    def __init__(self, message = "Insufficient funds"):
        self.message = message
    pass

class MaxBetsReached(Exception):
    def __init__(self, message = "Max bets reached"):
        self.message = message
    pass
