from bs4 import BeautifulSoup
from urllib.parse import urlparse

page_url = "http://example.com"
html = '<html><body><img src="http://example.com/1.jpg"><img src="/2.jpg"></body></html>'
soup = BeautifulSoup(html, "html.parser")
all_image_urls = []
for img_tag in soup.find_all("img"):
    img_src = img_tag.get("src")
    if not img_src:
        continue
    if img_src.startswith("/"):
        img_src = urlparse(page_url).scheme + "://" + urlparse(page_url).netloc + img_src
    print("after relative:", img_src)
    if img_src.startswith("data:"):
        continue
    if (not img_src.startswith("http")) and (not img_src.startswith("www")):
        continue
    if not img_src.startswith("http"):
        img_src = "http://" + img_src
    all_image_urls.append(img_src)
print(all_image_urls)
