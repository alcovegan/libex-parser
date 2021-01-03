from bs4 import BeautifulSoup
import requests
import json
import sys
import re
import csv
import os
from telegram import telegram_bot_sendtext

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"

# filenames
csv_output = "./books.csv"

csvOpen = open(csv_output, "w", encoding="utf-8", newline="\n")
c = csv.writer(csvOpen, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)

def parseBooks(tg_short_message = False):

	books_and_prices = []
	books_and_prices_minmax = []

	with open("books.json", encoding="utf-8") as json_file:
		books = json.load(json_file)

		for book in books:
			headers = { "User-Agent": user_agent, "Referer": book["url"] }
			r = requests.get(book["url"], headers=headers)

			soup = BeautifulSoup(r.text, "html.parser")
			not_in_sale = soup.findAll(text = re.compile("сейчас этого издания книги в продаже нет"))

			template = """<b>{bookname}</b>"""
			book_name = template.format(bookname=book["name"])
			clean_bookname = book["name"]

			if(not_in_sale):
				books_and_prices.append(book_name + ": отсутствует в продаже")
				c.writerow([book["name"], "отсутствует в продаже"])
			else:
				prices = soup.findAll("big")

				book_prices = {}

				for price in prices:
					book_prices[book["name"]] = []

				for price in prices:
					clean_price = int(price.getText())

					if(len(book_prices[clean_bookname]) > 0):
						book_prices[clean_bookname].append(clean_price)
					else:
						book_prices[clean_bookname] = [clean_price]

					books_and_prices.append(book_name + ": " + price.getText() + " руб.")
					c.writerow([book["name"], price.getText()])

				book_names = book_prices.keys()
				tmplt = """<b>{bookname}</b>: {minprice} - {maxprice} руб."""

				for key in book_names:
					minprice=min(book_prices[key])
					maxprice=max(book_prices[key])
					fmt = tmplt.format(bookname=key, minprice=minprice, maxprice=maxprice)
					books_and_prices_minmax.append(fmt)

		sep = "\n"
		formatted_text = sep.join(books_and_prices)
		formatted_text_minmax = sep.join(books_and_prices_minmax)

		if(len(sys.argv) > 1 and sys.argv[1] or tg_short_message):
			telegram_bot_sendtext(formatted_text_minmax)
		else:
			telegram_bot_sendtext(formatted_text)

parseBooks()