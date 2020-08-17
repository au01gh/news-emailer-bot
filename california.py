import requests

from bs4 import BeautifulSoup
from gensim.summarization import summarize

def c_news():
    print('-------------------------------------------------- Calfornia News --------------------------------------------------')

    req = requests.get('https://apnews.com/California').text
    soup = BeautifulSoup(req, 'html.parser')
    links = soup.find_all('a')

    news = []
    for link in links[::3][2:12]: #every third element of all the links / the first ten of all the links
        news.append('https://apnews.com' + link.get('href'))

    for article in news:
        page = requests.get(article).text
        soup = BeautifulSoup(page, 'html.parser')
        headline = soup.find('h1').getText()
        paragraph = soup.findAll('p')

        paragraph_text = [tag.getText().strip() for tag in paragraph]
        sentence_list = [sentence for sentence in paragraph_text if not '\n' in sentence]
        sentence_list = [sentence for sentence in sentence_list if '.' in sentence]

        combined = ' '.join(sentence_list) #combines parsed sentences together
        final = summarize(combined, word_count = 100)
        print(headline.strip())
        print(article.strip())
        print(final.strip())
        print()