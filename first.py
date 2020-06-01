from urllib.request import urlopen as uReq

from bs4 import BeautifulSoup as soup

my_url = "https://www.newegg.com/p/pl?d=video&N=100007709&name=Desktop%20Graphics%20Cards"
uClient = uReq(my_url)

page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grab each product
containers = page_soup.find_all("div", {"class": "item-container"})

# grab each product
title_containers = page_soup.find_all("div", {"class": "item-title"})
print(title_containers)

# try:
#     for container in containers:
#         brand = container.a.img['title']
#         # print (container)
#         print (brand ,"\n")
# except Exception as e:
#     print(e)
