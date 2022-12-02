from model.card import Card

class Deck:
    def __init__(self) -> None:
        self.name = ""
        self.cards = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def calculate_total_cost(self) -> float:
        totalCost = 0.0
        for card in self.cards:
            totalCost += card.calculate_cost()
        return totalCost

    """
    For Debug
    """
    def print_deck(self):
        for card in self.cards:
            print(card.name + "(" + card.id + ") :: " + str(card.amount))
