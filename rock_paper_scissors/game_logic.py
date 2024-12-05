import random

class GameLogic:
    def __init__(self):
        self.rules = {
            "rock": {"scissors": "win", "paper": "lose", "rock": "draw"},
            "scissors": {"paper": "win", "rock": "lose", "scissors": "draw"},
            "paper": {"rock": "win", "scissors": "lose", "paper": "draw"}
        }

    def judge(self, player1, player2):
        """判断两只手势的胜负"""
        if player1 not in self.rules or player2 not in self.rules:
            return "invalid"
        return self.rules[player1][player2]

    def computer_always_win(self, player_hand):
        """电脑永远赢"""
        winning_choices = {
            "rock": "paper",
            "scissors": "rock",
            "paper": "scissors"
        }
        return winning_choices.get(player_hand, "rock")

    def computer_always_lose(self, player_hand):
        """电脑永远输"""
        losing_choices = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }
        return losing_choices.get(player_hand, "scissors")