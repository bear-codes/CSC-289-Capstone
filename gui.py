import tkinter as tk
from deck import Deck
from game import Game

class BlackjackGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Demo")

        # Fullscreen (press ESC to exit)
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # =========================
        # COLOR THEME
        # =========================
        self.bg_color = "#1e1e2f"
        self.panel_color = "#2a2a40"
        self.text_color = "#e6e6e6"
        self.accent_color = "#4fa3ff"
        self.button_color = "#3a7bd5"

        self.root.configure(bg=self.bg_color)

        # =========================
        # GRID LAYOUT
        # =========================
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        # =========================
        # LEFT SIDE (GAME AREA)
        # =========================
        self.game_frame = tk.Frame(root, bg=self.panel_color, padx=20, pady=20)
        self.game_frame.grid(row=0, column=0, sticky="nsew")

        self.game_frame.columnconfigure(0, weight=1)

        font_large = ("Arial", 28)
        font_medium = ("Arial", 20, "bold")

        self.dealer_label = tk.Label(
            self.game_frame, text="Dealer:",
            font=font_large, bg=self.panel_color, fg=self.text_color
        )
        self.dealer_label.grid(row=0, column=0, pady=20)

        self.player_label = tk.Label(
            self.game_frame, text="Player:",
            font=font_large, bg=self.panel_color, fg=self.text_color
        )
        self.player_label.grid(row=1, column=0, pady=20)

        self.total_label = tk.Label(
            self.game_frame, text="Total:",
            font=font_large, bg=self.panel_color, fg=self.text_color
        )
        self.total_label.grid(row=2, column=0, pady=20)

        self.result_label = tk.Label(
            self.game_frame, text="",
            font=("Arial", 30, "bold"),
            bg=self.panel_color,
            fg=self.accent_color
        )
        self.result_label.grid(row=3, column=0, pady=30)

        # =========================
        # BUTTONS
        # =========================
        self.button_frame = tk.Frame(self.game_frame, bg=self.panel_color)
        self.button_frame.grid(row=4, column=0, pady=40)

        def styled_button(parent, text, command):
            return tk.Button(
                parent,
                text=text,
                font=font_medium,
                width=10,
                bg=self.button_color,
                fg="white",
                activebackground="#2f5fa5",
                activeforeground="white",
                bd=0,
                relief="flat",
                command=command
            )

        self.hit_button = styled_button(self.button_frame, "Hit", self.hit)
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = styled_button(self.button_frame, "Stand", self.stand)
        self.stand_button.grid(row=0, column=1, padx=10)

        self.deal_button = styled_button(self.button_frame, "Deal", self.deal)
        self.deal_button.grid(row=0, column=2, padx=10)

        # =========================
        # RIGHT SIDE (SUMMARY)
        # =========================
        self.summary_frame = tk.Frame(root, bg=self.panel_color, padx=20, pady=20)
        self.summary_frame.grid(row=0, column=1, sticky="nsew")

        self.summary_label = tk.Label(
            self.summary_frame,
            text="Game Summary",
            font=("Arial", 24, "bold"),
            bg=self.panel_color,
            fg=self.accent_color
        )
        self.summary_label.pack(pady=10)

        self.summary_text = tk.Text(
            self.summary_frame,
            font=("Courier", 14),
            bg="#1a1a2e",
            fg=self.text_color,
            insertbackground="white",
            bd=0
        )
        self.summary_text.pack(fill="both", expand=True)

        self.deal()

    # =========================
    # GAME LOGIC
    # =========================
    def new_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.game = Game(self.deck)
        self.game_over = False

    def format_hand(self, hand):
        return " ".join(str(card) for card in hand)

    def update_display(self):
        self.player_label.config(
            text=f"Player: {self.format_hand(self.game.player.hand)}"
        )
        self.dealer_label.config(
            text=f"Dealer: {self.format_hand(self.game.dealer.hand)}"
        )
        self.total_label.config(
            text=f"Total: {self.game.player.hand_value()}"
        )

    def deal(self):
        self.new_game()
        self.game.deal_initial_cards()

        self.result_label.config(text="")
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

        self.update_display()

    def build_summary(self, stats):
        result = self.game.determine_winner()

        summary = f"Result: {result}\n\n"
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
                f"{player_total} vs {dealer_card} | "
                f"You: {action.upper()} | Optimal: {optimal.upper()} {mark}\n"
            )

        if total > 0:
            accuracy = (correct / total) * 100
            summary += f"\nAccuracy: {accuracy:.2f}% ({correct}/{total})\n"

        summary += "\n--- Lifetime Stats ---\n"
        summary += f"Games Played: {stats['games_played']}\n"
        summary += f"Total Decisions: {stats['total_decisions']}\n"

        if stats["total_decisions"] > 0:
            overall_accuracy = (
                stats["correct_decisions"] / stats["total_decisions"]
            ) * 100
            summary += f"Overall Accuracy: {overall_accuracy:.2f}%\n"

        return summary

    def end_game(self):
        result = self.game.determine_winner()
        stats = self.game.update_stats()
        summary = self.build_summary(stats)

        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

        # Color result dynamically
        if "win" in result.lower():
            self.result_label.config(text=result, fg="#00d084")
        elif "lose" in result.lower():
            self.result_label.config(text=result, fg="#ff4d4d")
        else:
            self.result_label.config(text=result, fg="#ffd166")

        self.game_over = True
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

    def hit(self):
        if self.game_over:
            return

        self.game.player_hit()
        self.game.log_decision("hit")

        self.update_display()

        if self.game.player.hand_value() > 21:
            self.end_game()

    def stand(self):
        if self.game_over:
            return

        self.game.log_decision("stand")

        self.game.dealer_turn()
        self.update_display()

        self.end_game()


# =========================
# RUN APP
# =========================
root = tk.Tk()
app = BlackjackGUI(root)
root.mainloop()