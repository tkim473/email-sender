import requests
from config import *
from get_bible import get_verses

def get_display_verse(verse):

    bible_url = f"https://rest.api.bible/v1/bibles/78a9f6124f344018-01/search?query={verse}&sort=relevance"

    headers = {
        "api-key": bible_api_key,
    }

    response = requests.get(bible_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
    else:
        data = "no verse selected"
        print("Error:", response.status_code, response.text)
    
    try:
        display_verse_html = data['data']['passages'][0]['content']
    except:
        print('a verse was not selected')
        display_verse_html = ""

    return display_verse_html
