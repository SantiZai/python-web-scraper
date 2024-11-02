import requests
from bs4 import BeautifulSoup

url = 'https://www.hectortenis.com/categoria/raquetas'

response = requests.get(url)

if response.status_code == 200:    
    soup = BeautifulSoup(response.text, 'html.parser')

    pagination_list = soup.find('ul', class_='page-numbers')

    last_page = pagination_list.find_all('a', class_='page-numbers')[-2].text if pagination_list.find_all('a', class_='page-numbers') else 'None'

    urls = []

    for i in range(1, int(last_page) + 1):
        urls.append(f'https://www.hectortenis.com/categoria/raquetas/page/{i}')

    products_list = []

    for url in urls:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find('ul', class_='products')

            if products:
                items = products.find_all('li', class_='product')

                for item in items:
                    product_name = item.find('h2', class_='woocommerce-loop-product__title').text if item.find('h2') else 'No name'
                    product_price = item.find('span', class_='woocommerce-Price-amount').text if item.find('span', class_='price') else 'No price'

                    print(f'Nombre: {product_name}, Precio: {product_price}')
                    products_list.append({"nombre": product_name, "precio": product_price})
            else:
                print("No se encontró la lista de productos")
        else:
            print(f'Ocurrió un error con la url:{url}')
    print(products_list)
else:
    print(f"Error al cargar la página. Código de estado: {response.status_code}")
