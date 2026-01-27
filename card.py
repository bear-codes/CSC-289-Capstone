class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def value(self):
        if self.rank in ['J', 'Q', 'K']: #10 for JQK
            return 10
        if self.rank == 'A': #11 for Ace, have to add change to 1 if player bust when ace = 11
            return 11
        return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}" #accounts for displaying 2-10 for cards 2-10
    
    
