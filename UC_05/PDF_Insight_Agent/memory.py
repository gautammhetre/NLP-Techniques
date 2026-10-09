"""Keeps recent questions and answers so follow-up questions work."""
from config import MEMORY_TURNS


class ConversationMemory:
    def __init__(self):
        self.turns = []  # list of (question, answer)

    def add(self, question, answer):
        self.turns.append((question, answer))
        self.turns = self.turns[-MEMORY_TURNS:]

    def as_text(self):
        if not self.turns:
            return "(no previous conversation)"
        return "\n".join(f"User: {q}\nAssistant: {a}" for q, a in self.turns)

    def is_empty(self):
        return not self.turns

    def clear(self):
        self.turns = []
