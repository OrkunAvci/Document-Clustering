import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json


def get_blog_urls(tag_url_list):

    tags_and_urls_json={}
    for tag_url in tag_url_list:
        driver = webdriver.Chrome()
        driver.get('https://hashnode.com'+tag_url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(25):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(1)

        post_links = [i.find('a')['href'] for i in BeautifulSoup(driver.page_source, 'html.parser').find_all(class_='mb-1 text-3xl font-semibold leading-tight tracking-tight text-brand-black dark:text-brand-grey-100')]
        absolute_urls=["https://hashnode.com"+i if i.startswith("/post/") else i for i in post_links]
        tags_and_urls_json[str(tag_url)]=absolute_urls

        print(f"{len(post_links)} post link crawled for the tag {tag_url} \n")


    with open('data.json', 'w') as fp:
        json.dump(tags_and_urls_json, fp,indent=0)



# Parse tags page of hashnode.com to get tag names
tags_page = requests.get('https://hashnode.com/tags')
soup = BeautifulSoup(tags_page.text, 'html.parser')

# Get tag group divs
tag_group_divs = soup.find_all(class_='w-full mb-5 md:pr-2 md:w-1/2')
tag_group_divs.extend(soup.find_all(class_='w-full mb-5 md:pl-2 md:w-1/2'))

# Get tag divs with tag urls
tag_divs=[]
for i in tag_group_divs:
    tag_divs.extend((i.find(class_='px-4 py-5 leading-snug',recursive=True)).find_all('a'))

# Pick tag urls from tag divs
tag_name_set= set()
for i in tag_divs:
    tag_name_set.add(i['href'])

print(len(tag_name_set))

for i in tag_name_set:
    print(i)



get_blog_urls(list(tag_name_set))
 