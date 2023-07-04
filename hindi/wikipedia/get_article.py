from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pickle

def get_article(url, fname):
    html_doc = ''
    with urlopen(url) as response:
        for line in response:
            line = line.decode('utf-8')
            html_doc = html_doc + line.replace('\n','')
    soup = BeautifulSoup(html_doc, 'html.parser')
    title = soup.title.string
    print(title)
    paras = soup.find_all('p')
    article = ''
    for para in paras:
        article = article + para.text + '\n'
    article = re.sub(r'\([^)]*\)', r'', article)
    article = re.sub(r'\[[^\]]*\]', r'', article)
    article = re.sub(r'<[^>]*>', r'', article)
    article = re.sub(r'^https?:\/\/.*[\r\n]*', '', article)
    article = article.replace(u'\ufeff','')
    article = article.replace(u'\xa0', u' ')
    article = article.replace('  ', ' ');
    article = article.replace(' , ', ', ');
    devanagari_nums = ('०','१','२','३','४','५','६','७','८','९')
    for c, n in enumerate(devanagari_nums):
        article = re.sub(n, str(c), article)
    with open(fname, 'wb') as f:
        pickle.dump(article,f)
    print("Saved " + fname)
    return title