import requests
from bs4 import BeautifulSoup
import json

base_url = "http://quotes.toscrape.com"
quotes_data = []
authors_data = []


def scrape_quotes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')

    for quote, author in zip(quotes, authors):
        quote_text = quote.get_text()
        author_name = author.get_text()

        quotes_data.append({'quote': quote_text, 'author': author_name})
        if author_name not in authors_data:
            authors_data.append(author_name)

    next_page = soup.find('li', class_='next')
    if next_page:
        next_page_url = base_url + next_page.find('a')['href']
        scrape_quotes(next_page_url)


if __name__ == "__main__":
    scrape_quotes(base_url)

    with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)
