from deck import Deck
from game import Game


def main():

    deck = Deck()
    deck.shuffle()

    game = Game(deck)

    game.deal_initial_cards()

    print("\nDealer shows:", game.dealer.hand[0])
    print("Player hand:", game.player)
    print("Player total:", game.player.hand_value())

    # PLAYER TURN
    while True:

        if game.player.is_busted():
            break

        action = input("\nHit or Stand? ").strip().lower()

        if action == "hit":

            game.log_decision("hit")

            game.player_hit()

            print("Player hand:", game.player)
            print("Player total:", game.player.hand_value())

        elif action == "stand":

            game.log_decision("stand")
            break

        else:
            print("Invalid input (type 'hit' or 'stand')")

    # DEALER TURN
    if not game.player.is_busted():

        print("\nDealer reveals:", game.dealer)

        game.dealer_turn()

    # FINAL RESULTS
    print("\nFinal Hands")
    print("Player:", game.player, game.player.hand_value())
    print("Dealer:", game.dealer, game.dealer.hand_value())

    print("\nResult:", game.determine_winner())

    # POST-GAME ANALYSIS
    game.review_decisions()

    stats = game.update_stats()

    print("\n--- Lifetime Stats ---")
    print("Games Played:", stats["games_played"])
    print("Total Decisions:", stats["total_decisions"])

    if stats["total_decisions"] > 0:
        accuracy = (stats["correct_decisions"] / stats["total_decisions"]) * 100
        print(f"Overall Accuracy: {accuracy:.2f}%")

    print("\n-------------------------\n")


if __name__ == "__main__":
    main()

def build_summary(self, stats):

    result = self.game.determine_winner()

    summary = ""
    summary += f"Result: {result}\n\n"

    summary += "--- Post-Game Review ---\n"

    correct = 0
    total = len(self.game.decision_log)

    for decision in self.game.decision_log:
        player_total = decision["player_total"]
        dealer_card = decision["dealer_upcard"]
        action = decision["action"]
        optimal = decision["optimal"]

        is_correct = action == optimal
        if is_correct:
            correct += 1

        mark = "✅" if is_correct else "❌"

        summary += (
            f"Player: {player_total} vs Dealer: {dealer_card} | "
            f"You: {action.upper()} | Optimal: {optimal.upper()} {mark}\n"
        )

    if total > 0:
        accuracy = (correct / total) * 100
        summary += f"\nDecision Accuracy: {accuracy:.2f}% ({correct}/{total})\n"

    summary += "\n--- Lifetime Stats ---\n"
    summary += f"Games Played: {stats['games_played']}\n"
    summary += f"Total Decisions: {stats['total_decisions']}\n"

    if stats["total_decisions"] > 0:
        overall_accuracy = (
            stats["correct_decisions"] / stats["total_decisions"]
        ) * 100
        summary += f"Overall Accuracy: {overall_accuracy:.2f}%\n"

    summary += "\n-------------------------\n"

    return summary