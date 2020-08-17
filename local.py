import re
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient
from gensim.summarization import summarize

client = MongoClient('mongodb://localhost:27017')
db = client['news']

def l_news():
    duplicates = db.duplicates

    urls = {'https://www.eastbaytimes.com/location/california/bay-area/east-bay/contra-costa-county/central-contra-costa/walnut-creek/': 'Walnut Creek News',
            'https://www.mercurynews.com/location/california/bay-area/south-bay/santa-clara-county/downtown-san-jose/': 'San Jose State News'}

    for i in urls:
        print('------------------------------------------------- ' + urls[i] + ' --------------------------------------------------')

        req = requests.get(i).text
        soup = BeautifulSoup(req, 'html.parser')
        links = soup.findAll('a', {'class': 'article-title'})

        news = []
        for link in links:
            news.append(link.get('href'))

        search = ['walnut creek', 'wc', 'san jose state', 'sjsu', 'coronavirus', 'covid']
        for article in news:
            page = requests.get(article).text
            soup = BeautifulSoup(page, 'html.parser')
            headline = soup.find('h1').getText()

            if any(word in headline.lower() for word in search): #checks if any headlines contain a word from the list
                paragraph = soup.findAll('p')

                paragraph_text = [tag.getText().strip() for tag in paragraph]
                sentence_list = [sentence for sentence in paragraph_text if not '\n' in sentence]
                sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

                combined = ' '.join(sentence_list)
                summary = summarize(combined, word_count = 100)
                exclude = ['GET BREAKING NEWS IN YOUR BROWSER.', 'CLICK HERE TO TURN ON NOTIFICATIONS.']
                final = re.sub('|'.join(exclude), '', summary)

                print(headline.strip())
                print(article.strip())
                print(final.strip())
                print()

                duplicates.insert_one({headline: str(article)}) #storage in the event of duplicates