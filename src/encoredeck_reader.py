from io import TextIOWrapper
import os.path
from re import split
from logger import LogSeverity, log
from model.card import Card
from model.deck import Deck
from util import get_last_index_of

def _is_header(string:str) -> bool:
    return string == "Characters" or string == "Climaxes" or string == "Events"

def remove_english_from_id(id:str) -> str:
    # Get last index of '-', and remove all letter 'E' after that.
    lastIndexHyphen = get_last_index_of(id, "-")
    cardId = id[lastIndexHyphen:len(id)]
    cardId = cardId.replace("E", "")
    return id[0:lastIndexHyphen] + cardId

def _parse_file_to_deck(file:TextIOWrapper) -> Deck:
    fileLines = file.readlines()
    
    firstLine = False
    deckProfile = Deck()
    # Foreach line, attempt to parse it as a card and add to deck profile. 
    for line in fileLines:
        if not firstLine:
            # First Line is always the deck name.
            deckProfile.name = line.strip()
            firstLine = True
            continue

        current = line.strip()
        if _is_header(current):
            # ignore headers
            continue

        # First index should be ID, 2nd is amount; Everything after is Card Name.
        splitCurrent = current.split()
        
        # Everything after 2nd element is the card name.
        cardName = ""
        for i in range(2, len(splitCurrent)):
            cardName += splitCurrent[i] + " "

        currentCard = Card(cardName.strip(), remove_english_from_id(splitCurrent[0]), int(splitCurrent[1]))
        deckProfile.add_card(currentCard)
    return deckProfile

def read_deck_file(fileName:str) -> Deck:
    if not os.path.exists(fileName):
        # Try adding file extension
        fileName += ".txt"
        if not os.path.exists(fileName):
            print("this")
            log(LogSeverity.WARNING, "EncoreDeck file not found", "The file you have given is not found. Check if it exists")
            return None
    
    encoreDeckFile = open(fileName, 'r')
    try:
        deckProfile = _parse_file_to_deck(encoreDeckFile)
        deckProfile.name = fileName.replace(".txt", "")
    except:
        log(LogSeverity.WARNING, "Invalid EncoreDeck File Format", "The file you have given might be invalid. Check if it downloaded off EncoreDecks (.txt).")
        return None
    encoreDeckFile.close()

    if len(deckProfile.cards) == 0:
        log(LogSeverity.WARNING, "Invalid Deck Profile" , "The EncoreDeck file you have given might be invalid, or have no cards.")
        return None
    return deckProfile
