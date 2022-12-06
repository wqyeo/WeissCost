from logger import LogSeverity, log
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

    def export(self, filePath:str) -> None:
        try:
            csvFile = open(filePath, "w")
            # Append header
            csvFile.write("Card_ID,Card_Title,Card_Price,Card_Amount,Total_Price,Yuyutei_URL\n")
            # Write all cards
            for card in self.cards:
                csvFile.write(card.to_csv_row() + "\n")
            # Final, total price
            csvFile.write(',,,,"' + str(self.calculate_total_cost()) + '",')
            csvFile.close()
            print("Cost of Deck Profile has been written to " + filePath + ".")
        except Exception as e:
            log(LogSeverity.ERROR, "Failed to write CSV", str(e))
