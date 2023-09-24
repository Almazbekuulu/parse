from decouple import config
import requests
from bs4 import BeautifulSoup
import csv




HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "accept": "*/*",
}

URL = config("URL")
CSV_FILE = "softech.csv"


def get_response_data(headers, url):

        response = requests.get(url, headers=headers)
        return response


def content(html_text):
    soup = BeautifulSoup(html_text, "html.parser")

    all_data = soup.find_all("div", class_="list-item list-label")
    laptop_content = []
    for i in all_data:
        laptop_content.append(
            {
                "description": i.find("div", class_="block info-wrapper item-info-wrapper").get_text(),
                "block price": i.find("div", class_="block price").get_text(),
                "title": i.find("div", class_="title").get_text().strip(),
                "image": i.find("img", class_="lazy-image").get("data-src"),

                "views": i.find("div",class_="counters").get_text(),
            }
        )
    return laptop_content


def save_csv(laptops: list) -> None:
    with open(CSV_FILE, "w") as f:
        writer = csv.writer(f, delimiter=",")
        #writer.writerow(["Название", "Цена", "Картина","Характеристика"])
        for i in laptops:
            writer.writerow(["Название",i["title"],'\n',"Цена",(i["block price"]),'\n',"Просмотры" ,i["views" ],'\n',"Картины",'\n',i["image"],'\n',"Описание",'\n',i["description"],])

    print("уусе!!!")


def execute():
    html_content = get_response_data(HEADERS, URL)
    if html_content.status_code == 200:
        laptops = content(html_content.text)
        save_csv(laptops)


execute()