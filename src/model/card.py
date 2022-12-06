class Card:
    def __init__(self, name:str, id:str, amount:int) -> None:
        self.name = name
        self.id = id
        self.amount = amount
        self.cost = 0.0
        self.yuyuteiUrl = ""

    def calculate_cost(self) -> float:
        return self.cost * self.amount

    def print(self) -> None:
        print(self.name + " (" + self.id + ") " + str(self.cost))

    def to_csv_row(self) -> str:
        return self.id + ',"' + self.name.replace('"', '""') + '",' + str(self.cost) + "," + str(self.amount) + "," + str(self.calculate_cost()) + ',"' + self.yuyuteiUrl + '"'
