import process_pages as pp
import process_text as pt
import file_manager as fm
import os

tags = [
	"https://hashnode.com/n/javascript",
	"https://hashnode.com/n/web-development",
	"https://hashnode.com/n/reactjs",
	"https://hashnode.com/n/python",
	"https://hashnode.com/n/nodejs",
	"https://hashnode.com/n/github",
	"https://hashnode.com/n/java",
	"https://hashnode.com/n/programming",
	"https://hashnode.com/n/javascript/recent",
	"https://hashnode.com/n/web-development/recent",
	"https://hashnode.com/n/reactjs/recent",
	"https://hashnode.com/n/python/recent",
	"https://hashnode.com/n/nodejs/recent",
	"https://hashnode.com/n/github/recent",
	"https://hashnode.com/n/java/recent",
	"https://hashnode.com/n/programming/recent"
]

all_links = []
for tag in tags:
	urls = pp.get_url_list(tag)
	fm.save("tag_" + tag, urls)
	all_links = all_links + urls

guide = {}
for link in all_links:
	raw = pp.get_text_from_url(link)
	#   fm.save("raw_" + link, raw)     #   Optional.
	tokens = pt.tokenize(raw)
	table = pt.frequency_table(tokens)
	if len(table) > 5:
		fm.save("ft_" + link, table)
		for key in table.keys():
			guide[key] = 0

fm.save("_all_links", all_links)
fm.save("_guide", guide)
