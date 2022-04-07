from bs4 import BeautifulSoup
import requests
import random


class Scraper:
    def __init__(self):
        pass
    
    def main(self):
        page = requests.get("https://www.goodreads.com/quotes")
        soup = BeautifulSoup(page.text, 'html.parser')

        quotes = soup.find_all(class_='quoteText')

        randIndex = random.randint(0, len(quotes))

        quote = quotes[randIndex].contents[0].strip()
        if quote[-1] != "”":
            quote += "”"
        return quote

quote = Scraper().main()
