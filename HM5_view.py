from flask import Flask
from webargs.flaskparser import use_kwargs
from webargs import fields

from database_handler import execute_query

app = Flask(__name__)


@app.route('/stats_by_city')
@use_kwargs({
    'genre': fields.Str(required=True)
},
    location="query")
def stats_by_city(genre):
    query = """
            SELECT * FROM(SELECT Name, City
            FROM (
                SELECT g.Name, cus.City, COUNT(*) AS popular
                FROM genres g
                LEFT JOIN tracks t ON g.GenreId = t.GenreId
                LEFT JOIN invoice_items invi ON t.TrackId = invi.TrackId
                LEFT JOIN invoices inv ON inv.InvoiceId = invi.InvoiceId
                LEFT JOIN customers cus ON inv.CustomerId = cus.CustomerId
                WHERE City IS NOT NULL
                GROUP BY g.Name, cus.City
            ) AS subquery
            GROUP BY Name
            HAVING popular = MAX(popular))
    """

    if genre:
        query += f" WHERE Name = '{genre}'"

    records = execute_query(query=query)

    # if records == []:
    #     return "Don't have any information, try another type of genre"
    # return records

    if records:
        return records
    else:
        return "Don't have any information, try another type of genre"


if __name__ == '__main__':
    app.run(port=5001, debug=True)
