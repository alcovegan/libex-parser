import schedule
import time
import sys
from checker import parseBooks

def job():
	print("Started books parsing...")
	if("--minmax" in sys.argv):
		parseBooks(True)
	else:
		parseBooks()
	print("Finished books parsing...")

schedule.every(1).minute.do(job)

while True:
	schedule.run_pending()
	time.sleep(1)