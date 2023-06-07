import random

import json
import requests

from faker import Faker
from flask import Flask, request, jsonify, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)


@app.route("/<int:length>")
def generate_students(length):
    data = []
    for i in range(length):
        faker_instance = Faker("DE")
        dict_student_bio = {
            'first_name': faker_instance.first_name(),
            'last_name': faker_instance.last_name(),
            'email': faker_instance.email(),
            'password': faker_instance.password(),
            'age': random.randrange(18, 61)
        }
        data.append(dict_student_bio)

    json_data = json.dumps(data)
    with open('generate_students.json', 'w') as file:
        file.write(json_data)
    return json_data





@app.route("/currency=<currency>")
@app.route("/currency=<currency>&convert=<int:convert>")
@use_kwargs(
    {
        "currency": fields.Str(missing='USD'),
    },
    location="query")
def get_bitcoin_currency(currency, convert=None):
    __symbol = {}
    resource_url = 'https://test.bitpay.com/currencies'
    try:
        result_resource_url = requests.get(resource_url)
        result_resource_url: dict = result_resource_url.json()
    except Exception as e:
        return f"An error occurred: {e}"
    for i in result_resource_url.get("data", {}):
        __symbol[i['code']] = i['symbol']
    symbol = __symbol.get(currency, None)
    url = f"https://bitpay.com/api/rates/{currency}"
    try:
        url_requests = requests.get(url)
        bitpay = url_requests.json()
    except Exception as e:
        return f"An error occurred: {e}"
    rate = bitpay['rate']

    if rate is None:
        return f"Rate for currency {currency} not found."

    if convert is not None:
        return f'The cost of {convert} bitcoins is {round(float(rate) * convert)} {symbol}, at an exchange rate of {rate}'
    if convert is None:
        return f'The cost of Bitcoin in {currency} is {rate} {symbol}'




