import requests
import telegram_send

SearchDict = requests.get('https://www.reddit.com/r/hardwareswap/search.json?q=laptop&source=recent&restrict_sr=1&sort=new', headers = {'User-agent': 'your bot 0.1'}).json()
LatestItemTitle1 = SearchDict.get('data').get('children')[0].get('data').get('title')

while True:
    SearchDict = requests.get('https://www.reddit.com/r/hardwareswap/search.json?q=laptop&source=recent&restrict_sr=1&sort=new', headers = {'User-agent': 'your bot 0.1'}).json()
    LatestItemTitle2 = SearchDict.get('data').get('children')[0].get('data').get('title')
    LatestItemText2 = SearchDict.get('data').get('children')[0].get('data').get('selftext')
    if LatestItemTitle2 != LatestItemTitle1:
        telegram_send.send(messages=['New Listing Detected \n'+ LatestItemTitle2 + '\n'+ LatestItemText2])
        LatestItemTitle1 = LatestItemTitle2
        print(LatestItemTitle2 + '\n' + LatestItemText2)
