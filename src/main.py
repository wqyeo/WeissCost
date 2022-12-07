import os
from encoredeck_reader import read_deck_file
from encoredeck_scraper import load_deck_profile
from logger import LogSeverity, log
from util import is_null_or_whitespace, print_list
from yuyutei_scraper import scrap_card_price

userInput = input("Enter file name of exported EncoreDeck profile (.txt)\r\nURL to EncoreDeck is supported as well, but not recommend as there might be inaccuracies during webpage parsing.\r\n> ")

while userInput.upper() != "EXIT":
    parsingFileOperation = False
    try:
        deckProfile = None
        # Check if user input a file
        parsingFileOperation =os.path.exists(userInput) or os.path.exists(userInput + ".txt") 
        if parsingFileOperation:
            print("Detected file name input, parsing file...")
            deckProfile = read_deck_file(userInput)
        else:
            print("Did not detect file name, parsing as EncoreDeck URL...")
            log(LogSeverity.WARNING, "Load from EncoreDeck URL", "Loading from EncoreDeck URL instead of an exported file. Results might incomplete/inaccurate, if so, consider exporting the deck profile as '.txt' instead, and passing it to this program.")
            deckProfile = load_deck_profile(userInput)

        if deckProfile != None:
            print("Deck Profile loaded, searching yuyutei for deck prices...")
            for card in deckProfile.cards:
                scrap_card_price(card, not parsingFileOperation)
            deckProfile.export(deckProfile.name.replace("/", "_") + ".csv")
    except Exception as e:
        if parsingFileOperation:
            log(LogSeverity.FATAL, "MAIN LOOP (Parse File)", str(e))
        else:
            print(LogSeverity.FATAL, "MAIN LOOP (Parse URL)", str(e))
    userInput = input("Enter file name of exported EncoreDeck profile (.txt)\r\nURL to EncoreDeck is supported as well, but not recommend as there might be inaccuracies during webpage parsing.\r\n> ")

