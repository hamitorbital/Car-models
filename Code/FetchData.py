import re
import requests
import mysql.connector 

from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="user",
    passwd="password",
    database="database",
)

list_items, information, list_years = [], [], []
list_models, list_prices = [], []


def information_regex(item):
    # this use for clear data from html tag
    regex = re.sub(r'\s+', ' ', item.text)
    list_items.append(regex)


def get_information(url):
    """ find cars informations from html """
    response = requests.get(url)
    text = response.text
    homes = BeautifulSoup(text, 'html.parser')
    cars_tag = homes.findAll('div', {"class": "card-details"})
    for item in cars_tag:
        information_regex(item)        


models = ['sedan', 'coupe', 'suv', 'wagon', 'convertible', 'van', 'truck']
for model in models:
    for year in range(2017, 2020):
        UrlName = 'https://www.cars.com/research/{}/{}/?pageNum=0&rpp=110'
        url = UrlName.format(model, year)
        get_information(url)
    for year in range(2015, 2017):
        UrlName = 'https://www.cars.com/research/{}/{}/?pageNum=0&rpp=110'
        url = UrlName.format(model, year)
        get_information(url)

for info in list_items:
    if 'MSRP' in info:
        regex = re.findall(r'\d+ .* STARTING MSRP \$\d+\,\d+', info)
        for item in regex:
            information.append(item.split('STARTING MSRP'))
    if 'CURRENT LISTING PRICE' in info:
        r = r'\d+ .* CURRENT LISTING PRICE \$\d+\,\d+\s\-\s\$\d+\,\d+'
        regex = re.findall(r, info)
        for item in regex:
            information.append(item.split('CURRENT LISTING PRICE'))

for i in information:
    num = i[0].split(maxsplit= 1)
    list_years.append(int(num[0]))
    list_models.append(num[1].strip())

for pri in information:
    item = pri[1].replace('$', '')
    item = item.split('-')
    if len(item) == 1:
        item1 = item[0].split(',')
        list_prices.append(int(''.join(item1)))
    if len(item) == 2:
        item2 = item[1].split(',')
        list_prices.append(int(''.join(item2)))
zip_item = list(zip(list_models, list_years, list_prices))
mycursor = mydb.cursor()

for item in zip_item:
        car_model = item[0]
        car_year = item[1]
        car_price = item[2]
        sql = "INSERT IGNORE INTO tablename (model, year, price)\
               VALUES (%s, %s, %s)"
        val = [(car_model, car_year, car_price)]
        mycursor.executemany(sql, val)
        mydb.commit()
