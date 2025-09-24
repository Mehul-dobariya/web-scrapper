import requests
import csv
import os
from bs4 import BeautifulSoup

# Get Session With Headers
def get_session():
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.amazon.in/'
    }
    session = requests.Session()
    session.headers.update(HEADERS)
    return session

def get_url(page = 1):
    return f"https://www.amazon.in/s?i=computers&rh=n%3A976392031%2Cn%3A1375344031&s=popularity-rank&dc&fs=true&ds=v1%3Ag9nPP%2BOfn2sBn%2FN8A3kxTCmMc7QeHXFzfMi3NK63POg&qid=1758707447&rnid=976392031&xpid=fGnXesH6KyESU&ref=sr_nr_n_2&page={page}"

#Append Data To CSV File
def write_csv(csv_file, products):
    file_exists = os.path.isfile(csv_file)

    # Write to CSV
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        if not file_exists:
            writer.writerow(["Product Name", "Image", "Price Symbol", "Price", "Product Link"])
        
        # Write data rows
        writer.writerows(products)

#Scrap Item Details
def scrap_item_details(item):
    product_details = []
    image_container = item.find("div", class_='s-product-image-container')

    #Get Product Name
    product_title = item.find("h2")
    product_details.append(product_title.get_text(strip=True) if product_title else "N/A")

    #Get Product Image
    img_tag = image_container.find('img') if image_container else None
    
    #Get Product Image
    product_details.append(img_tag['src'] if img_tag and img_tag.has_attr('src') else "N/A")

    #Get Price Details: Price Symbol And Price 
    price_tag = item.find('span', class_='a-price')
    if price_tag:
        price = price_tag.find("span", class_="a-price-whole")
        price_symbol = price_tag.find("span", class_="a-price-symbol")

        product_details.append(price_symbol.get_text(strip=True) if price_symbol else "N/A")
        product_details.append(price.get_text(strip=True) if price else "N/A")
    else:
        product_details.append("N/A")
        product_details.append("N/A")

    #Product Link
    product_link = item.find("a", class_="a-link-normal")
    product_details.append(product_link['href'] if product_link and product_link.has_attr('href') else "N/A")

    return product_details

#Scrap Last Page
def get_last_page(url, session):
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        page_items = soup.find_all('span', class_='s-pagination-item')
        if page_items:
            return int(page_items[-1].get_text())
    return 1