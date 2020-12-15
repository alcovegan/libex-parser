import schedule
import time
from checker import parseBooks

def job():
	print("Started books parsing...")
	parseBooks()
	print("Finished books parsing...")

schedule.every(1).minute.do(job)

while True:
	schedule.run_pending()
	time.sleep(1)