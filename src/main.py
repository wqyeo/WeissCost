from encoredeck_reader import read_deck_file
from logger import log, LogSeverity
from util import is_null_or_whitespace, print_list
from yuyutei_scraper import debug_call, scrap_card_price

userInput = input("Enter file name of exported EncoreDeck (.txt):")

while userInput.upper() != "EXIT":
    try:
        deckProfile = read_deck_file(userInput)
        if deckProfile != None:
            log(LogSeverity.LOG, "Deck Profile Loaded", "Loaded deck profile, scraping yuyutei for prices...")
            for card in deckProfile.cards:
                scrap_card_price(card)
            log(LogSeverity.LOG, "Exporting Deck Cost CSV", "Exporting Deck Profile costs to CSV...")
            deckProfile.export(deckProfile.name + ".csv")        
    except Exception as e:
        log(LogSeverity.FATAL, "Exception occured at Main Loop", str(e))
    userInput = input("\r\nEnter EncoreDeck File Name (.txt):")
