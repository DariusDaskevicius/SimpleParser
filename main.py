import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'  # The file in which we will store the collected data
HOST = 'https://minfin.com.ua'  # Site name what you need to parse
URL = 'https://minfin.com.ua/cards/'  # Page name in site what you need to parse
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
}  # Headers should always be there to impersonate the user (to find them go to Inspect element -> Network -> Headers)

def get_html(url, params=''):  # url == URL from top, params its name of site after https://minfin.com.ua/cards/*****   /   Gets global HTML code
    request = requests.get(url, headers=HEADERS, params=params)
    return request

def get_content(html):  # Collects content on only one page. Logic for switching between pages in a method parser()
    soup = BeautifulSoup(html, 'html.parser')  #  This variable will disassemble the elements
    items = soup.find_all('div', class_='product-item')  # Blocks from which we will pull information
    cards = []

    for item in items:  # This loop is needed to go through all the blocks(variable items) from which we pull information
        cards.append({
            'title': item.find('div', class_='title').get_text(strip=True),                    # Find title text element in variable items(block)
            'link': HOST + item.find('div', class_='title').find('a').get('href'),             # Find link to element in variable items(block).
                                                                                               # Good example to find element in element. Because
                                                                                               # now we search 'a' tag in 'Title' and get 'href'
                                                                                               # information what we need
            'brand': item.find('div', class_='brand').get_text(strip=True),                    # Find brand text element in variable items(block)
            'image': HOST + item.find('div', class_='image').find('img').get('src')            # Find image. Find element in element like in
                                                                                               # 'Link to product' and find path to picture we
                                                                                               # need. 'src' == (path to picture)
        })
    return cards

def save_doc(items, path):  # Function will collect to file collected data
    with open(path, 'w', newline='') as file:  # Show path to file, 'w' == write to file and 'newline=' ' means space between lines
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title name', 'Link to product', 'Brand of product', 'Image link'])  # Column names in csv files
        for item in items:
            writer.writerow([item['title'], item['link'], item['brand'], item['image']])  # Takes a package of elements from each item

def parser():
    PAGENATION = input('Specify the number of pages to parse: ')
    PAGENATION = int(PAGENATION.strip())  # Transform to int and remove spaces if needed
    html = get_html(URL)  # Check if is a page
    if html.status_code == 200:
        cards = []
        for page in range(1, PAGENATION + 1):
            print(f'Parsing page number: {page}')
            ############################################## Switches between pages
            html = get_html(URL, params={'page': page})  # Number of page we need is taken from URL.
                                                         # https://minfin.com.ua/cards/catalog?page=3&per-page=10
                                                         # example ...?page=3&per...
            ##############################################
            cards.extend(get_content(html.text))  # Collects data from all pages into one array
            save_doc(cards, CSV)  # Saves data to file!
    else:
        print('Error')

parser()