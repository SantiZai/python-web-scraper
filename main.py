import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.hectortenis.com/categoria/raquetas'

response = requests.get(url)

if response.status_code == 200:    
    soup = BeautifulSoup(response.text, 'html.parser')

    pagination_list = soup.find('ul', class_='page-numbers')

    last_page = pagination_list.find_all('a', class_='page-numbers')[-2].text if pagination_list.find_all('a', class_='page-numbers') else 'None'

    urls = ['https://www.digitalsport.com.ar/search/?search=raqueta&discipline=13']

    for i in range(1, int(last_page) + 1):
        urls.append(f'https://www.hectortenis.com/categoria/raquetas/page/{i}')

    products_list = []

    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            container_products1 = soup.find('ul', class_='products')

            if container_products1:
                items1 = container_products1.find_all('li', class_='product')
                for item in items1:
                    product_name = item.find('h2', class_='woocommerce-loop-product__title').text if item.find('h2') else 'No name'
                    product_price = item.find('span', class_='woocommerce-Price-amount').text if item.find('span', class_='price') else 'No price'
                    products_list.append({"raqueta": product_name, "precio": product_price})
            else:
                container_products2 = soup.find('div', class_='products_wraper')
                items2 = container_products2.find_all('a', class_='product')
                for item in items2:
                    product_name = item.find('h3').text if item.find('h3') else 'No name'
                    product_price = item.find('div', class_='precio').text if item.find('div', class_='precio') else 'No price'
                    if product_name.split(" ")[0].lower() == "raqueta":
                        products_list.append({"raqueta": product_name, "precio": product_price})

        else:
            print(f'Ocurrió un error con la url:{url}')
    with open('nuevo_archivo.csv', 'w', newline='') as archivo:
        columnas = ['raqueta', 'precio']
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(products_list)
    print(products_list)
else:
    print(f"Error al cargar la página. Código de estado: {response.status_code}")
