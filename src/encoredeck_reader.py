from io import TextIOWrapper
import os.path
from re import split
from model.card import Card

from model.deck import Deck

def _is_header(string:str) -> bool:
    return string == "Characters" or string == "Climaxes" or string == "Events"

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

        currentCard = Card(cardName.strip(), splitCurrent[0], int(splitCurrent[1]))
        deckProfile.add_card(currentCard)
    return deckProfile

def read_deck_file(fileName:str) -> Deck:
    if not os.path.exists(fileName):
        # Try adding file extension
        fileName += ".txt"
        if not os.path.exists(fileName):
            print("The EncoreDeck file that you have given does not exists!\r\n(Check if its a .txt file?)")
            return None
    
    encoreDeckFile = open(fileName, 'r')
    try:
        deckProfile = _parse_file_to_deck(encoreDeckFile)
    except:
        print("The file given is invalid! Ensure that it is downloaded off EncoreDecks.")
        return None

    if len(deckProfile.cards) == 0:
        print("The given EncoreDeck file might be invalid. Or there is no cards in there.")
        return None

    

    return deckProfile
