import json
import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://metarankings.ru/'
HOST = 'https://metarankings.ru/best-pc-games/page/'


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    res = requests.get(url, headers=headers)

    return res.text



def parse_all_page_links():
    list_link = []
    has_next_page = True
    counter = 20

    while has_next_page:
        html = get_html(f'{HOST}{counter}')

        soup = BeautifulSoup(html, 'html.parser')
        is_next = soup.find('div', class_='pagination').find('div', class_='navi').find('a', class_='next')

        if is_next:
            link_to_page_game = soup.find_all('div', class_='post clear')
            for link in link_to_page_game:
                link = link.find('a', class_='name')
                list_link.append(link['href'])

            with open(f'data/page_{str(counter)}.html', 'w', encoding="utf-8") as file:
                file.write(html)

            counter += 1
        else:
            has_next_page = False

    with open('data/links.json', mode='w', encoding="utf-8") as file:
        json.dump(list_link, file, indent=4, ensure_ascii=False)

    print('Parse finish')


def parse_all_page_link():
    games = []
    with open('data/links.json', mode='r') as link_json:
        data = json.load(link_json)
        count = 0

        for link in data:
            count += 1
            if count > 6:
                break
            html = get_html(link)
            soup = BeautifulSoup(html, 'html.parser')

            game_platform = soup.find('div', class_='featured-game').find_all('p')[2].find_all('a')
            p = [plat.text for plat in game_platform]

            text = []
            desc = soup.find('div', class_='description').find_all('p')
            text = [p.text.strip() for p in desc]

            game_item = {
                'name': soup.find('div', class_='post-meta').find('span').getText(strip=''),
                'rating': soup.find(class_='rating').find(class_='score').text.strip(),
                'appraisals': soup.find(class_='rating').find('span').text.strip(),
                'platforms': p,
                'desc': ' '.join(text)
            }

            games.append(game_item)

    with open('game.json', mode='w', encoding='utf-8') as file:
        json.dump(games, file, indent=4, ensure_ascii=False)


# main run function
if __name__ == '__main__':
    parse_all_page_links()
# parse_all_page_link()
