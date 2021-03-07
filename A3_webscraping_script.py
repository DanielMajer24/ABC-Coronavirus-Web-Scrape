# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os


# %%
start_time = time.time()
url = "https://www.abc.net.au/news/story-streams/coronavirus/"
page = urlopen(url)
page = page.read()
soup = BeautifulSoup(page, 'lxml')
articles = soup.findAll("li", class_="doctype-article")

news_list = []

for article in articles:
    try:
        title  = article.find('h3')
        date = article.get('data-first-published')[:10]
        time_str = article.get('data-first-published')[10:]
        link = article.find('a').get('href')
        link = "https://www.abc.net.au" + link
        description = article.find('p').get_text().strip()
        title = title.text.strip()
        print("\nHeadline: ", title)
        print('--------------------------------------')
        print('Date:', date)
        print('Time:', time_str)
        print('Description:\n', description)
        # print('Article:\n', cleaned_text[1:5], "...")
        image_id1 = article.get('data-image-cmid')
        image_url = "https://www.abc.net.au/cm/rimage/{image_id}-{image_size}.jpg?v=2"
         
        image_size = ["4x3-xlarge", "16x9-xlarge"]
        for size in image_size:
            url = image_url.format(image_id=image_id1, image_size=size)

            try:
                pages = urlopen(url)
                # pages = pages.read()
                # print(pages)
                print(url)
                url_ = url
                break

            except:
                continue
        if not description:
            description = ""
        if not link:
            link = ""
        if not date:
            date = ""
        if not time_str:
            time_str = ""
        if not url_:
            url_ = ""
        new_row = {'title': title, 'description': description,'link': link,'date': date,'time_str': time_str,'url_': url_}
        #print(new_row)
        news_list.append(new_row)
    except:
        continue

news_items = pd.DataFrame(news_list)

article_text = []
for i in range(len(news_items['link'])):
    individual_page = urlopen(news_items['link'][i])
    individual_page = individual_page.read()
    individual_page_soup = BeautifulSoup(individual_page, 'lxml')
    #print(soup.prettify())
    raw_text = individual_page_soup.findAll("p", class_="_1SzQc")
    cleaned_text = []
    for paragraph in raw_text:
        text = paragraph.get_text().strip()
        cleaned_text.append("".join(text))
    article_text.append(cleaned_text)

news_items['articles'] = article_text

if os.path.exists('news_items.csv'):
    news_items_file =  pd.read_csv('news_items.csv')
    news_items_file = news_items_file.drop("Unnamed: 0", axis = 1)
    news_items_file = news_items_file.append(news_items, ignore_index=True)
    new_items_file = news_items_file.reset_index()
    title = news_items_file['title'].drop_duplicates(keep = 'first')
    values  = list(title.index)
    filtered_news_items = news_items_file.loc[values]
    filtered_news_items.to_csv('news_items.csv')
else:
    news_items.to_csv("news_items.csv")
    


