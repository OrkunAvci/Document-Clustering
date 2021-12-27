from datetime import date
from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests as req
import re
import time
from tqdm import tqdm
import json
import os
import file_manager as fm

def get_url_list(url: str, downs = 1600) -> list:
	ser = Service()
	# options.add_argument('--headless')
	# options.add_argument('--disable-gpu') 
	browser = Chrome(service = ser)
	browser.get(url)
	time.sleep(1)
	body = browser.find_element(By.TAG_NAME, "body")

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

def get_text_from_url(url: str) -> str:
	page = req.get(url).text
	soup = bs(page, "html.parser")

	text = ""
	for elem in soup.find_all("p", text=True):
		text = text + " " + elem.getText()

	return text

def get_tags_for_urls(urls: list) -> dict:
	ser = Service()

	options = ChromeOptions()
	# options.add_argument('--headless')
	# options.add_argument('--disable-gpu')

	browser = Chrome(service = ser,chrome_options=options)

	pattern = re.compile("https://hashnode\.com/n/.*")

	urls_with_tags_dict={}
	bad_urls=[]

	if os.path.isfile('data/data_with_tags'):
		urls_with_tags_dict=fm.get('data_with_tags')
		urls = urls - urls_with_tags_dict.keys()

	for url in tqdm(urls):

		browser.set_page_load_timeout(8)
		try:
			browser.get(url)

			body = browser.find_element(By.TAG_NAME, "body")

			for i in range(50):
				body.send_keys(Keys.PAGE_DOWN)
				time.sleep(0.1)
				
			tags_of_url = []
			soup = bs(browser.page_source, "html.parser")
					
			for item in soup.find_all("a", href = True,class_="css-h6a8j6"):
				if pattern.match(item["href"]) :
					tags_of_url.append(item["href"].split('/')[-1])
			tags_of_url = list(set(tags_of_url))

			if(len(tags_of_url) == 0):
				print(f"tags couldn't be fetched for the url {url} ")
				bad_urls.append(url)
				continue
			urls_with_tags_dict[url] = tags_of_url
		except Exception:
			print("timeout")
			pass

	browser.close()
	with open("bad_urls.json","w") as fp:
		json.dump(bad_urls, fp,indent=0)
	return urls_with_tags_dict


	
