from player import Player
from dealer import Dealer
import json
import os


class Game:

    def __init__(self, deck):

        self.deck = deck
        self.player = Player()
        self.dealer = Dealer()

        self.decision_log = []

    def deal_initial_cards(self):

        self.player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())

        self.player.add_card(self.deck.draw())
        self.dealer.add_card(self.deck.draw())

    def player_hit(self):

        self.player.add_card(self.deck.draw())

    def dealer_turn(self):

        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.draw())

    def determine_winner(self):

        player_total = self.player.hand_value()
        dealer_total = self.dealer.hand_value()

        if player_total > 21:
            return "Player Busts"

        if dealer_total > 21:
            return "Dealer Busts — Player Wins"

        if player_total > dealer_total:
            return "Player Wins"

        if dealer_total > player_total:
            return "Dealer Wins"

        return "Push"

   
    def get_optimal_action(self, player_total, dealer_card):

        if dealer_card in ["J", "Q", "K"]:
            dealer_value = 10
        elif dealer_card == "A":
            dealer_value = 11
        else:
            dealer_value = int(dealer_card)

        if player_total >= 17:
            return "stand"

        if player_total <= 11:
            return "hit"

        if player_total == 12:
            if 4 <= dealer_value <= 6:
                return "stand"
            return "hit"

        if 13 <= player_total <= 16:
            if 2 <= dealer_value <= 6:
                return "stand"
            return "hit"

        return "hit"

    # DECISION LOGGING
    def log_decision(self, action):

        player_total = self.player.hand_value()
        dealer_card = self.dealer.hand[0].rank

        optimal = self.get_optimal_action(player_total, dealer_card)

        self.decision_log.append({
            "player_total": player_total,
            "dealer_upcard": dealer_card,
            "action": action,
            "optimal": optimal
        })

    #  POST-GAME REVIEW
    def review_decisions(self):

        print("\n--- Post-Game Review ---")

        correct = 0
        total = len(self.decision_log)

        for decision in self.decision_log:

            player_total = decision["player_total"]
            dealer_card = decision["dealer_upcard"]
            action = decision["action"]
            optimal = decision["optimal"]

            result = "✅" if action == optimal else "❌"

            if action == optimal:
                correct += 1

            print(
                f"Player: {player_total} vs Dealer: {dealer_card} | "
                f"You: {action.upper()} | Optimal: {optimal.upper()} {result}"
            )

        if total > 0:
            accuracy = (correct / total) * 100
            print(f"\nDecision Accuracy: {accuracy:.2f}% ({correct}/{total})")

    # STATS SYSTEM
    def load_stats(self):

        if os.path.exists("stats.json"):
            with open("stats.json", "r") as file:
                return json.load(file)

        return {
            "games_played": 0,
            "total_decisions": 0,
            "correct_decisions": 0
        }

    def save_stats(self, stats):

        with open("stats.json", "w") as file:
            json.dump(stats, file, indent=4)

    def update_stats(self):

        stats = self.load_stats()

        correct = sum(1 for d in self.decision_log if d["action"] == d["optimal"])
        total = len(self.decision_log)

        stats["games_played"] += 1
        stats["total_decisions"] += total
        stats["correct_decisions"] += correct

        self.save_stats(stats)

        return stats