import requests
from bs4 import BeautifulSoup
from model.card import Card
import re
import sys

from util import filter_non_digits_for, is_null_or_whitespace

def debug_call() -> None:
    scrap_card_price(Card("Test", "BD/W54-007", 2))
    scrap_card_price(Card("Test", "LSS/W45-024", 2))

def _create_link_from_id(id:str) -> str:
    return "https://yuyu-tei.jp/game_ws/sell/sell_price.php?name=" + id + "&rare=&type=&kizu=0"

"""
Checks if the givenID matches the targetID by seeing through all possible rarity
which the givenID could be.
"""
def _id_matches(targetID:str, givenID:str) -> bool:
    possible = ["SPb", "SPa", "S", "R", "SSP", "SPm", "SP", "SPMb", "SPMa"]
    if targetID == givenID:
        return True

    # Match against all possible rarity:
    for possibleRarity in possible:
        if (targetID + possibleRarity) == givenID:
            return True
    return False

"""
Scrap for a card's price.

Return True if successful.
Price will be set on the given card parameter.
"""
def scrap_card_price(card: Card) -> bool:
    if is_null_or_whitespace(card.id):
        return False

    yuyuteiUrl = _create_link_from_id(card.id)
    rawHtml = ""
    try:
        rawHtml = requests.get(yuyuteiUrl).text
    except:
        print("Failed to send request to site :: " + yuyuteiUrl)
        return False
    
    soup = None
    try:
        soup = BeautifulSoup(rawHtml, "html.parser")
    except:
        print("Failed to parse website :: " + yuyuteiUrl)
        return False

    cardUnitRegex = re.compile('.*card_unit.*')
    allCardUnit = soup.find_all("li", {"class": cardUnitRegex})

    price = sys.float_info.max
    # Go through each card and get lowest price
    for cardUnit in allCardUnit:
        try:
            # Check if the ID matches first. (Rarity doesn't matter)
            currentId = cardUnit.find("p", class_="id").get_text()
            if not _id_matches(card.id, currentId.strip()):
                # Card ID doesn't match, ignore.
                continue

            # Search for price tag, and compare to see if its lower.
            priceTag = cardUnit.find("p", class_="price").get_text()
            priceTag = filter_non_digits_for(priceTag)
            if float(priceTag) < price:
                # Found a lower price
                price = float(priceTag)
        except Exception as e:
            continue

    if price >= sys.float_info.max:
        # Could not find price
        return False
    
    card.cost = price
    card.yuyuteiUrl = yuyuteiUrl
    return True
