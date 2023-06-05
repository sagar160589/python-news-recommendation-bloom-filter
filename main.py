import requests as requests
import sqlite3
import redis
from bs4 import BeautifulSoup
from bloom import BloomFilter

NEWS_URL = "https://news.ycombinator.com/"
"""
Initializing variables START
count_fp-- Counting False positives
total_titles-- Holds total titles at the end to calculate false positives
news_list-- to hold news title added to bloom filter
page_count-- global variable to hold the page count to be scraped which gets incremented in code
"""
count_fp = 0
total_titles = []
news_list = []
page_count = 1

"""
Initialize Redis on local host
Initialize BloomFilter and populate with size 1000, number of hash functions set to 3, and redis client
Create database connection and create table if not exists to store the scraped news data
"""
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
bloom = BloomFilter(700, 5, redis_client)
#Optional - delete key news_bloom from Redis for Testing each time
redis_client.delete('news_bloom')
conn = sqlite3.connect("newsdata.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS news
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT,
                   title_links TEXT)''')

"""
Get news function that takes page count and scrapes data from news URL
Also this function calls add_element_redis_bloom_filter() to add title text to bloom filter
"""


def get_news(page_count):
    news_content = requests.get(f"{NEWS_URL}?p={page_count}")
    soup = BeautifulSoup(news_content.text, 'html.parser')

    titles = soup.findAll('span', class_='titleline')
    title_text = [title.get_text() for title in titles]
    title_links = [title.find(name='a').get('href') for title in titles]

    for t in title_text:
        news_data = (t, title_links[title_text.index(t)])
        cursor.execute("INSERT into news (title, title_links) VALUES(?,?)", news_data)
        conn.commit()
    total_titles.extend(title_text)
    add_element_redis_bloom_filter(title_text)
    page_count += 1
    if page_count < 10:
        get_news(page_count)


"""
Adds titles to bloom filter depending on the business logic conditions
Also checks for title existence in bloom filter
"""


def add_element_redis_bloom_filter(title_text):
    global count_fp
    for t in title_text:
        if t in news_list:
            print("News exists. Not be recommended again to the user")
        elif bloom.exists(t) and t not in news_list:
            print("Result is False positive as News doesn't exists in the bloom filter but still it returns true. "
                  "Hence not recommended to show to user")
            count_fp += 1
        else:
            print("News not exists. Add it to Redis bloom filter and recommended to show to the user")
            bloom.add(t)
            news_list.append(t)


# Calculate false positivity rate
def check_false_positivity_rate():
    global count_fp
    print(len(total_titles))
    fp_rate = float(100 * (count_fp / len(total_titles)))
    print(fp_rate)

"""
Call get_news()
Call check_false_positivity_rate()
"""
get_news(page_count)
check_false_positivity_rate()
conn.close()
