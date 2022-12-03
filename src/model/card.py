class Card:
    def __init__(self, name:str, id:str, amount:int) -> None:
        self.name = name
        self.id = id
        self.amount = amount
        self.cost = 0.0
        self.yuyuteiUrl = ""

    def calculate_cost(self) -> float:
        return self.cost * self.amount
