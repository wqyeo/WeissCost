#from requests_html import HTMLSession
import requests
from bs4 import BeautifulSoup
from model.card import Card
import re

from util import is_null_or_whitespace

def debug_call() -> None:
    scrap_card_price(Card("Test", "BD/W54-007", 2))
    scrap_card_price(Card("Test", "LSS/W45-024", 2))

def _create_link_from_id(id:str) -> str:
    return "https://yuyu-tei.jp/game_ws/sell/sell_price.php?name=" + id + "&rare=&type=&kizu=0"

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
    
    # TODO: Filter/Loop through and find cheapest, append to card.
    return True
