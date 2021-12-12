from bs4 import BeautifulSoup, SoupStrainer 
import requests

main_url = 'https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html'
base_url = 'https://docs.aws.amazon.com/service-authorization/latest/reference/'


html_document = requests.get(url=main_url).content
strainer = SoupStrainer(id="main-col-body")
soup = BeautifulSoup(html_document, "html.parser", parse_only=strainer)
all_li = soup.find_all("li")

all_a = []
for li in all_li:
    all_a.append(li.find_all("a"))

all_pages = []

for a_list in all_a:
    if len(a_list) > 0:
        a=a_list[0]
        if a.has_attr("href"):
            if './' in a['href']:
                all_pages.append(a['href'].replace("./",""))

strainer_page = SoupStrainer(class_="table-container")
for page_suffix in all_pages:
    print(page_suffix)
    full_url = base_url + page_suffix
    page_content = requests.get(url=full_url).content
    soup_page = BeautifulSoup(page_content, "html.parser", parse_only=strainer_page)
    with open(f'html\\{page_suffix}','w') as file:
        file.write(soup_page.prettify())


