class Player:

    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def hand_value(self):

        value = 0
        aces = 0

        for card in self.hand:

            if card.rank in ["J", "Q", "K"]:
                value += 10

            elif card.rank == "A":
                value += 11
                aces += 1

            else:
                value += int(card.rank)

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def is_busted(self):
        return self.hand_value() > 21

    def clear_hand(self):
        self.hand = []

    def __str__(self):
        return ", ".join(str(card) for card in self.hand)
