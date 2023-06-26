from urllib.request import urlopen
import pickle

# @contextmanager
def opened_w_error(filename, mode="r"):
    try:
        f = open(filename, mode)
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


html_doc = ''
with urlopen('https://hi.wikipedia.org/wiki/%E0%A4%AE%E0%A5%81%E0%A4%96%E0%A4%AA%E0%A5%83%E0%A4%B7%E0%A5%8D%E0%A4%A0') as response:
    for line in response:
            line = line.decode('utf-8')
            html_doc = html_doc + line.replace('\n', '')

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')

print(soup.h1.string)

tab = soup.find("table",{"style":"border:2px solid #e1eaee; border-collapse:separate;font-size:120%"})

anchors = tab.find_all('a')

home_url = 'https://hi.wikipedia.org' 
links = [home_url + anchor['href'] for anchor in anchors]

print(len(links))

# Main code
all_links = []
prev_len = 0
for link in links:    
    while link:
        html_doc = ''
        with urlopen(link) as response:
            for line in response:
                line = line.decode('utf-8')
                html_doc = html_doc + line.replace('\n','')
            soup = BeautifulSoup(html_doc, 'html.parser')
            div = soup.find('div',{'class':'mw-allpages-body'})
            if div:
                anchors = div.find_all('a');
                all_links = all_links + [home_url + anchor['href'] for anchor in anchors]
                print(len(set(all_links)))
            if prev_len == len(set(all_links)):
                break
            nav_div = soup.find('div',{'class':'mw-allpages-nav'})
            if nav_div and len(nav_div.find_all('a')) == 2:
                link = home_url + nav_div.find_all('a')[1]['href']
            prev_len = len(set(all_links))



print('The total is ')
print(len(set(all_links)))


all_links = list(set(all_links)); len(all_links)

filename = "all_hindi_wikipedia_links.pkl"
try:
    f = open(filename, "wb")
except IOError as err:
    print("IOError:" + err)
else:
    pickle.dump(all_links, f)
    print('dumped')
finally:
        f.close()


print('160th link is ')
print(all_links[160])