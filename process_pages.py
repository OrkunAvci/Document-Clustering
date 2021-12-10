from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests as req
import nltk
import re
import time

def get_link_list(url: str):
	ser = Service("D:/chromedriver_win32/chromedriver.exe")
	browser = Chrome(service = ser)
	browser.get(url)
	time.sleep(1)
	body = browser.find_element(By.TAG_NAME, "body")

	downs = 600     #   1 min
	while downs :
		body.send_keys(Keys.PAGE_DOWN)
		time.sleep(0.1)
		downs = downs - 1

	soup = bs(browser.page_source, "html.parser")

	pattern = re.compile("https://[a-z]*\.hashnode\.dev/.*")
	urls = []
	for item in soup.find_all("a", href = True, class_ = "block") :
		if pattern.match(item["href"]) :
			urls.append(item["href"])

	urls = list(set(urls))

	browser.close()
	return  urls

def get_text_from_url(url: str):
	page = req.get(url).text
	soup = bs(page, "html.parser")

	text = ""
	for elem in soup.find_all("p", text=True):
		text = text + " " + elem.getText()

	tokens = nltk.word_tokenize(text)
	print(tokens)
