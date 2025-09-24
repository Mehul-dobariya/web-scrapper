from bs4 import BeautifulSoup
from utils import get_session, get_url, write_csv, scrap_item_details, get_last_page

session = get_session()
page = 1
csv_file = 'products.csv'
url = get_url(page)
products = []
last_page = get_last_page(url, session)


while page <= last_page:
    url = get_url(page)
    response = session.get(url)
    if response.status_code != 200:
        continue
    
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all('div', role='listitem')

    if items:
        for item in items:
            products.append(scrap_item_details(item))

    # Write to CSV
    write_csv(csv_file, products)

    print("Page %d scrapped!!!" % (page))
    page = page + 1

print(f"Data exported successfully to {csv_file}")