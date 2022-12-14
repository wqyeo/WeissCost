import requests
from bs4 import BeautifulSoup
from logger import LogSeverity, log
from model.card import Card
import re
import sys

from util import filter_non_digits_for, is_null_or_whitespace

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

Read NOTE below for 'looseFinding' variable
"""
def scrap_card_price(card: Card, looseFinding = False) -> bool:
    if is_null_or_whitespace(card.id):
        return False

    yuyuteiUrl = _create_link_from_id(card.id)
    rawHtml = ""
    try:
        log(LogSeverity.LOG, "Get Request Yuyutei", "Sending request to Yuyutei for card price (" + yuyuteiUrl + ").")
        rawHtml = requests.get(yuyuteiUrl).text
    except Exception as e:
        log(LogSeverity.WARNING, "Yuyutei URL Request Failed", str(e))
        return False
    
    soup = None
    try:
        soup = BeautifulSoup(rawHtml, "html.parser")
    except Exception as e:
        log(LogSeverity.ERROR, "Yuyutei Website Parsing Failed", str(e)) 
        return False

    cardUnitRegex = re.compile('.*card_unit.*')
    allCardUnit = soup.find_all("li", {"class": cardUnitRegex})

    price = sys.float_info.max
    # Go through each card and get lowest price
    for cardUnit in allCardUnit:
        try:
            # Check if the ID matches first. (Rarity doesn't matter)
            # NOTE: If looseFinding = True, it matches with 'contains' operation rather than 'equals'
            currentId = cardUnit.find("p", class_="id").get_text()
            if not (_id_matches(card.id, currentId.strip()) or (looseFinding and card.id in currentId)):
                # Card ID doesn't match, ignore.
                continue

            # Search for price tag, and compare to see if its lower.
            priceTag = cardUnit.find("p", class_="price").get_text()
            priceTag = filter_non_digits_for(priceTag)
            if float(priceTag) < price:
                # Found a lower price
                price = float(priceTag)
        except Exception as e:
            log(LogSeverity.WARNING, "Failed get CardUnit Price", str(e))
            continue

    if price >= sys.float_info.max:
        log(LogSeverity.WARNING, "No Price Found", "No price found for card (" + card.id + ").") 
        # Could not find price
        return False
    
    card.cost = price
    card.yuyuteiUrl = yuyuteiUrl
    log(LogSeverity.LOG, "Price Found", "Price found for card (" + card.id + "), " + str(card.cost)  +".\r\n")
    return True
