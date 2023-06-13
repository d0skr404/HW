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


@app.route('/get_all_info_about_track')
@use_kwargs({
    "track_id": fields.Int(missing=None)
},
    location="query")
def get_all_info_about_track(track_id):
    query = """SELECT * FROM
                (SELECT * FROM playlist_track pt LEFT JOIN playlists p
                ON pt.PlaylistId = p.PlaylistId LEFT JOIN tracks t
                ON pt.TrackId = t.TrackId LEFT JOIN media_types mt
                ON t.MediaTypeId = mt.MediaTypeId LEFT JOIN genres g
                ON t.GenreId = g.GenreId LEFT JOIN albums alb
                ON t.AlbumId = alb.AlbumId LEFT JOIN artists art
                ON art.ArtistId = alb.ArtistId LEFT JOIN invoice_items invi
                ON t.TrackId = invi.TrackId LEFT JOIN invoices inv
                ON invi.InvoiceId = inv.InvoiceId LEFT JOIN customers cus
                ON inv.CustomerId = cus.CustomerId LEFT JOIN employees emp
                ON cus.CustomerId = emp.EmployeeId)"""

    track_fields = {}

    if track_id:
        track_fields['TrackId'] = str(track_id)

    if track_fields:
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in track_fields.keys()
        )

    records = execute_query(query=query, args=tuple(track_fields.values()))
    return records


@app.route("/order_price")
@use_kwargs(
    {
        "country": fields.Str(
            required=False,
            missing=None
            # validate=[validate.Regexp("^[0-9]*")]
        )
    },
    location="query"
)
def order_price(country):
    query = """SELECT * FROM
            (SELECT BillingCountry, round(SUM(UnitPrice * Quantity),
            2) AS sales FROM (SELECT InvoiceId, UnitPrice, Quantity
            FROM invoice_items) inv_i LEFT JOIN
            (SELECT InvoiceId, BillingCountry FROM invoices) i
            ON inv_i.InvoiceId = i.InvoiceId
            GROUP BY i.BillingCountry)"""

    fields = {}

    if country:
        fields["BillingCountry"] = country

    if fields:
        query += " WHERE " + " AND ".join(
            f"{key}=?" for key in fields.keys()
        )

    records = execute_query(query=query, args=tuple(fields.values()))

    return records


@app.route("/time_all_track")
def time_all_track():
    query = """SELECT round(SUM(Milliseconds) /
    (1000.0 * 60.0 * 60.0),2) AS Hours
    FROM tracks"""
    records = execute_query(query=query)
    return f"Time all track in hours: {records[0][0]} h"


if __name__ == '__main__':
    app.run(port=5002, debug=True)
