import requests
from bs4 import BeautifulSoup

"""
def get_blog_urls(tag_url_list):
    for tag_url in tag_url_list:
        tag_page = requests.get('https://hashnode.com'+tag_url)
        soup = BeautifulSoup(tag_page.text, 'html.parser')

"""

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





    
