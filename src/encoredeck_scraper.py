from bs4 import BeautifulSoup
from encoredeck_reader import remove_english_from_id
from logger import LogSeverity, log
from model.card import Card
from model.deck import Deck
from requests_html import HTMLSession


def test() -> None:
    load_deck_profile("https://www.encoredecks.com/deck/-zJ843rHC")

def _extract_card_id_from_imgUrl(imgUrl: str) -> str:
    imgUrl = imgUrl.replace("/images/EN/", "")
    imgUrl = imgUrl.replace("/images/JP/", "")
    imgUrl = imgUrl.replace(".gif", "")

    # Replace last occurance of '/' to '-',
    # then remove English ID.
    temp = imgUrl[::-1]
    imgUrl = temp.replace("/", "-", 1)
    return remove_english_from_id(imgUrl[::-1])

def _scrap_deck_profile(encoreDeckSoup: BeautifulSoup) -> Deck:
    resultDeck = Deck()
    resultDeck.name = encoreDeckSoup.find("h2", class_="deck-name").text
    log(LogSeverity.LOG, "Deck Name Found", "Found Deck (" + resultDeck.name + ").")

    cardItemsList = encoreDeckSoup.find_all("div", class_="container-carditem clickable")
    for cardItem in cardItemsList:
        # NOTE: These are set first to log for exception.
        # (To know which was failed to scrap)
        cardName = "NOT FOUND"
        cardCount = -1
        cardId = "NOT-FOUND"
        
        try:
            # Scrap fro current card details.
            cardName = cardItem.find("div", class_="card-name").get_text()
            cardCount = int(cardItem.find("p", class_="ant-scroll-number-only-unit current").get_text())
            cardId = cardItem.find("img")['src']
            cardId = _extract_card_id_from_imgUrl(cardId)
            # Create Card object and add to deck.
            currentCard = Card(cardName, cardId, cardCount)
            resultDeck.add_card(currentCard)
            log(LogSeverity.LOG, "Card Found", "Loaded Card '" + cardName + "' (" + cardId + ").")
        except:
            log(LogSeverity.WARNING, "Load Card Failed", "Failed to load one of the cards; " + cardName + "(" + cardId + ")" + str(cardCount))
    return resultDeck

def load_deck_profile(url: str) -> Deck:
    session = HTMLSession()
    r = None
    try:
        r = session.get(url)
        r.html.render()
    except:
        log(LogSeverity.WARNING, "URL Request Failed", "Tried to parse user input as a URL, but failed.")
        return None
    
    log(LogSeverity.LOG, "URL Request Success", "Get request to EncoreDeck URL successful.")
    soup = None
    try:
        soup = BeautifulSoup(r.html.html, "html.parser")
    except:
        log(LogSeverity.ERROR, "URL Parse Failed", "Failed to parse user given URL Website.")
        return None

    log(LogSeverity.LOG, "Parse Website Success", "Managed to parse raw website as HTML.")
    deck = None
    try:
        deck = _scrap_deck_profile(soup)
    except Exception as e:
        log(LogSeverity.WARNING, "Scrap Deck Failed", "Failed to scrap website for deck. Error: (" + str(e) + "); Website might not be encoredeck or network issue.")
        return None

    log(LogSeverity.LOG, "EncoreDeck Loaded", "EncoreDeck profile successfully loaded from URL")
    return deck
