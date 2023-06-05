from flask import Flask
import random
import string
import secrets
import pandas as pd

app = Flask(__name__)

@app.route("/")
def generate_password():
    '''Password generator with the following parameters:
       Length from 10 to 20 chars
       String in upper and lower cases[A-Z][a-z]
       Digits[0-9]
       Special symbols[!-~]
    '''
    __letter_upper = string.ascii_letters.upper() #generate set of string in uppercase [A-Z]
    __letter_lower = string.ascii_letters.lower() #generate set of string in lowerrcase [a-z]
    __digits = string.digits #generate set of digits [0-9]
    __special_chars = string.punctuation #generate set of special characters [!-~]
    __set_of_symbol = __digits + __special_chars + __letter_upper + __letter_lower #сollecting all symbols
    __password = '' #variable to which the character will be written after each loop


    for symbol in range(random.randint(10, 21)):
        #length_password - allows us to specify the length of our password, we can specify a range
        __password += ''.join(secrets.choice(__set_of_symbol))

    return __password

generate_password()

@app.route("/average")
def calculate_average(file):
    df = pd.read_csv(file)
    height = [col for col in df.columns if 'Height' in col]
    weight = [col for col in df.columns if 'Weight' in col]
    mean_height = round(df[height].mean().values[0], 2)
    mean_weight = round(df[weight].mean().values[0], 2)
    return f'Average height for student: {mean_height}\nAverage weight for student: {mean_weight}'

path = '/Users/denisoskorib/Documents/hw.csv'
calculate_average(path)