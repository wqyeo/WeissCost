from site_requestor import get_raw_site_html
from util import is_null_or_whitespace

userInput = input("Enter EncoreDeck URL:")

while userInput.upper() != "EXIT":
    rawHtml = get_raw_site_html(userInput)
    if not is_null_or_whitespace(rawHtml):
        print(rawHtml)
        userInput = input("\r\nEnter EncoreDeck URL:")
