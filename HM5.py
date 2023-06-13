import sqlite3

from flask import Flask
from webargs.flaskparser import use_kwargs
from webargs import fields

app = Flask(__name__)


def execute_query(query, args=()):
    with sqlite3.connect('chinook.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        connection.commit()
        records = cursor.fetchall()
    return records


@app.route('/stats_by_city')
@use_kwargs({
    'genre': fields.Str(required=True)
},
    location="query")
def stats_by_city(genre):
    query = """
            SELECT City
            FROM (SELECT *
            FROM (SELECT Name, City, popular,
            row_number() OVER (partition by Name ORDER BY popular desc )
            as row_number
            FROM (SELECT g.Name, cus.City, count() AS popular
            FROM genres g
            LEFT JOIN tracks t ON g.GenreId = t.GenreId
            LEFT JOIN invoice_items invi ON t.TrackId = invi.TrackId
            LEFT JOIN invoices inv ON inv.InvoiceId = invi.InvoiceId
            LEFT JOIN customers cus ON inv.CustomerId = cus.CustomerId
            WHERE City IS NOT NULL
            GROUP BY g.Name, cus.City))
            WHERE row_number = 1)
    """

    fields = {}

    if genre:
        fields['Name'] = genre

    if fields:
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in fields.keys())

    records = execute_query(query=query, args=tuple(fields.values()))

    if records == []:
        return "Don't have any information, try another type of genre"
    return records


if __name__ == '__main__':
    app.run(port=5001, debug=True)
