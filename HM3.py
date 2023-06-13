import pandas as pd
import requests

from http import HTTPStatus

from faker import Faker
from flask import Flask, Response
from webargs import validate, fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)

@app.route("/generate_students")
@use_kwargs(
    {
        "length": fields.Int(
            validate=[validate.Range(min=1, max=999)])
    },
    location="query")
def generate_students(length):
    data = []
    for i in range(length):
        faker_instance = Faker("DE")
        dict_student_bio = {
            'first_name': faker_instance.first_name(),
            'last_name': faker_instance.last_name(),
            'email': faker_instance.email(),
            'password': faker_instance.password(),
            'age': faker_instance
            .date_of_birth(minimum_age=18, maximum_age=59).strftime('%Y-%m-%d')
        }
        data.append(dict_student_bio)

    pd.DataFrame(data).to_csv('generate_students.csv')
    return data


@app.route("/get_bitcoin_currency")
@use_kwargs(
    {
        "currency": fields.Str(missing='USD'),
        "convert": fields.Int()
    },
    location="query")
def get_bitcoin_currency(currency, convert=None):
    __symbol = {}

    currencies_url = 'https://bitpay.com/currencies'
    currencies_url = requests.get(currencies_url)

    if currencies_url.status_code not in (HTTPStatus.OK,):
        return Response("ERROR: Something went wrong",
                        status=currencies_url.status_code)

    currencies_url: dict = currencies_url.json()

    for i in currencies_url.get("data", {}):
        __symbol[i['code']] = i['symbol']
    symbol = __symbol.get(currency, None)

    rates_url = f"https://bitpay.com/api/rates/{currency}"
    rates_url = requests.get(rates_url)

    if rates_url.status_code not in (HTTPStatus.OK,):
        return Response("ERROR: Something went wrong",
                        status=rates_url.status_code)

    bitpay_rates = rates_url.json()

    rate = bitpay_rates['rate']

    if rate is None:
        return f"Rate for currency {currency} not found."

    if convert is not None:
        return f'The cost of {convert} bitcoins is ' \
               f'{round(float(rate) * convert)} {symbol}, ' \
               f'at an exchange rate of {rate}'
    if convert is None:
        return f'The cost of Bitcoin in {currency} is {rate} {symbol}'
