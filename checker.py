from bs4 import BeautifulSoup
import requests
import json
import re
import csv
import os
from telegram import telegram_bot_sendtext

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

# filenames
csv_output = "./books.csv"

csvOpen = open(csv_output, "w", encoding="utf-8", newline="\n")
c = csv.writer(csvOpen, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

def parseBooks():

	books_and_prices = []

	with open("books.json", encoding="utf-8") as json_file:
		books = json.load(json_file)

		for book in books:
			headers = { "User-Agent": user_agent, "Referer": book["url"] }
			r = requests.get(book["url"], headers=headers)

			soup = BeautifulSoup(r.text, "html.parser")
			not_in_sale = soup.findAll(text = re.compile("сейчас этого издания книги в продаже нет"))

			template = """<b>{bookname}</b>"""
			book_name = template.format(bookname=book["name"])

			if(not_in_sale):
				books_and_prices.append(book_name + ": отсутствует в продаже")
				c.writerow([book["name"], "отсутствует в продаже"])
			else:
				prices = soup.findAll("big")

				for price in prices:
					books_and_prices.append(book_name + ": " + price.getText() + " руб.")
					c.writerow([book["name"], price.getText()])

		sep = "\n"
		formatted_text = sep.join(books_and_prices)

		telegram_bot_sendtext(formatted_text)

parseBooks()