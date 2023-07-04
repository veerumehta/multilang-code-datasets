import pickle
from get_article import *

PATH = '/var/data/wikipedia/articles/'
mapping_dict = {}

with open('./content/hindi_wiki_links_jun_2023.pkl', 'rb') as f:
    all_urls = pickle.load(f)

start_url = 0
end_url = 220692

for counter, url in enumerate(all_urls[start_url:end_url]):
    try:
        counter = counter + start_url
        filename = PATH + str(counter) + '.pkl'
        print('counter is ' + str(counter) + ' file name is ' + filename)
        mapping_dict[filename] = get_article(url, filename)
    except:
        continue
