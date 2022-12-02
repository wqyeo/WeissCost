from encoredeck_reader import read_deck_file
from util import is_null_or_whitespace, print_list

userInput = input("Enter file name of exported EncoreDeck (.txt):")

while userInput.upper() != "EXIT":
    try:
        deckProfile = read_deck_file(userInput)
        if deckProfile != None:
            deckProfile.print_deck()
            # TODO: Parse and scrap through yuyutei for pricing.
    except Exception as e:
        print("Failed to parse given file, check if the file is valid.\r\nHINT: Should be an exported EncoreDeck file (.txt)")
    userInput = input("\r\nEnter EncoreDeck File Name (.txt):")
