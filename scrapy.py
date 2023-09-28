import bs4
from decouple import config
import requests
import csv

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                  'rv:109.0) Gecko/20100101 Firefox/117.0',
    'accept': '*/*',

}
URL = config('URL')
CSV_FILE = 'softech'


def content(html_doc):
    soup = bs4.BeautifulSoup(html_doc, 'lxml')
    all_info = soup.find_all('div', class_='list-item list-label')
    content_result_list = []
    for i in all_info:
        content_result_list.append(
            {
                'dollars': i.find('div', class_='block price').find('p').find('strong').get_text().strip(),
                'som': i.find('div', class_='block price').find('p').find('br').next_sibling.get_text().strip(),
                'name': i.find('h2', class_='name').contents[0].strip(),
                'photo': i.find('img').get('src'),
                'info':  ''.join([res for res in i.find('div', class_='block info-wrapper item-info-wrapper').stripped_strings]).replace('.,',''),
                'views': i.find('span', class_='listing-icons views').get_text().strip(),

            }
         )
    return content_result_list



res = []
def execute():
    for i in range(1, 15):
        html_content = requests.get(URL + f'/?page={i}', HEADERS)
        if html_content.status_code == 200:
            laptops = content(html_content.text)
            res.append(laptops)

execute()

def save(page):
    with open(CSV_FILE, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Цена в долларах', 'Цена в соaмах', 'Название', 'картинка', 'описание', 'количество просмотров',] )
        for a in page:
            for i in a:
                writer.writerow([i['dollars'], i['som'], i['name'], i['photo'], i['info'], i['views']])

save(res)