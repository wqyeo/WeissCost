import requests

def scrap_yuyutei(url:str) -> None:
    try:
        print(requests.get(url).text)
    except:
        print("Failed to send request to site :: " + url)
        return None
