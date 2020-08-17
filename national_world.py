import re
import requests

from bs4 import BeautifulSoup
from gensim.summarization import summarize

def n_w_news():
    urls = {'https://www.reuters.com/news/us': 'National News', 'https://www.reuters.com/news/world': 'World News'}

    for link in urls:
        print('------------------------------------------------- ' + urls[link] + ' --------------------------------------------------')

        req = requests.get(link).text
        soup = BeautifulSoup(req, 'html.parser')
        links = soup.findAll('div', {'class': 'story-content'})

        news = []
        for link in links:
            news.append('https://www.reuters.com' + link.a.get('href'))

        for article in news:
            page = requests.get(article).text
            soup = BeautifulSoup(page, 'html.parser')
            headline = soup.find('h1').getText()
            paragraph = soup.findAll('p')

            paragraph_text = [tag.getText().strip() for tag in paragraph]
            sentence_list = [sentence for sentence in paragraph_text if not '\n' in sentence]
            sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

            combined = ' '.join(sentence_list)
            summary = summarize(combined, word_count = 100)
            new_summary = summary[summary.find('-') + 2:] #removes eveything up to and including the hyphen
            exclude = ['© 2020 Reuters.', 'All Rights Reserved.', 'All quotes delayed a minimum of 15 minutes.', 'See here for a complete list of exchanges and delays.']
            final = re.sub('|'.join(exclude), '', new_summary.strip()) #uses regular expression to join the sentences

            print(headline.strip())
            print(article.strip())
            print(final.strip())
            print()