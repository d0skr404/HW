from flask import Flask
import random
import string
import secrets
import pandas as pd

app = Flask(__name__)


@app.route("/generate_password")
def generate_password():
    letter_upper = string.ascii_letters.upper()
    letter_lower = string.ascii_letters.lower()
    digits = string.digits
    special_chars = string.punctuation
    set_of_symbol = digits + special_chars + letter_upper + letter_lower
    password = ''

    for symbol in range(random.randint(10, 20)):
        password += ''.join(secrets.choice(set_of_symbol))

    return password


@app.route("/average")
def calculate_average():
    file = '/Users/denisoskorib/Documents/hw.csv'
    df = pd.read_csv(file)
    mean_weight = round(df.agg({' Weight(Pounds)': 'mean'})[0], 2)
    mean_height = round(df.agg({' Height(Inches)': 'mean'})[0], 2)
    return f'Average height for student: {mean_height} ' \
           f'Average weight for student: {mean_weight}'
