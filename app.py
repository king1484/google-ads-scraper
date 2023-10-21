from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def scrape(keyword):
    url = f'https://www.google.com/search?q={keyword}&tbm=shop'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_name = soup.find('h3', class_='sh-np__product-title')
        if product_name:
            product_name = product_name.get_text()
        else:
            return {
                'product_name': ""
            }
        price = soup.find('span', class_='T14wmb').get_text()
        img = soup.find('img').get('src')
        return {
            'product_name': product_name,
            'price': price,
            'image_url': img
        }
    else:
        return {
            'product_name': ""
        }


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        keyword = request.form['keyword']
        result = scrape(keyword)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run()
