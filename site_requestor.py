import requests

def get_raw_site_html(url:str) -> str:
    try:
        return requests.get(url).text
    except:
        print("Failed to send request to URL :: " + url)
        return ""

