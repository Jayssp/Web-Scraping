import requests
from bs4 import BeautifulSoup
import pandas as pd

current_page = 1
data = []

while True:  # Infinite loop until broken
    print("Currently scraping page:", current_page)
    
    url = f"https://books.toscrape.com/catalogue/page-{current_page}.html"
    page = requests.get(url)

    # Check if the page exists
    if page.status_code == 404:
        break

    soup = BeautifulSoup(page.text, "html.parser")
    all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in all_books:
        item = {}
        item['Title'] = book.find("img").attrs["alt"]
        item['Link'] = book.find("a").attrs["href"]
        item['Price'] = book.find("p", class_="price_color").text[2:]
        item['Stock'] = book.find("p", class_="instock availability").text.strip()

        data.append(item)

    current_page += 1  

df = pd.DataFrame(data)
df.to_excel("books.xlsx", index=False)
df.to_csv("books.csv", index=False)