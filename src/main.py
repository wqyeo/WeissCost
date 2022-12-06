from encoredeck_reader import read_deck_file
from util import is_null_or_whitespace, print_list
from yuyutei_scraper import debug_call, scrap_card_price

userInput = input("Enter file name of exported EncoreDeck (.txt):")

while userInput.upper() != "EXIT":
    try:
        deckProfile = read_deck_file(userInput)
        if deckProfile != None:
            for card in deckProfile.cards:
                scrap_card_price(card)
            deckProfile.export(deckProfile.name + ".csv")        
    except Exception as e:
        print("Failed to parse given file, check if the file is valid.\r\nHINT: Should be an exported EncoreDeck file (.txt)")
    userInput = input("\r\nEnter EncoreDeck File Name (.txt):")
