from process_pages import get_link_list

urls = get_link_list("https://hashnode.com/n/javascript")

print(len(urls))
print(urls)
