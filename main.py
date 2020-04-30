import sqlite3
from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

app = FastAPI()
app.secret_key = "99d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8aa34"


@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('data/chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
    

@app.get("/tracks")
async def get_tracks(page:int=0, per_page:int=10):
    app.db_connection.row_factory = sqlite3.Row
    cursor = app.db_connection.cursor()
    tracks = cursor.execute("SELECT * FROM tracks LIMIT (?) OFFSET (?)", (per_page, page*per_page)).fetchall()
    return tracks

@app.get("/tracks/composers")
async def get_tracks(composer_name:str):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = app.db_connection.cursor()
    track_names = cursor.execute("SELECT name FROM tracks WHERE Composer = (?) ORDER BY name ASC", (composer_name, )).fetchall()
    if len(track_names) == 0:
        raise HTTPException(status_code=404, detail={'error': "Not found such composer"})
    return track_names

class Album(BaseModel):
    title: str
    artist_id: int

@app.post("/albums", status_code=201)
async def add_album(album: Album):
    cursor = app.db_connection.execute("SELECT * FROM artists WHERE ArtistId = (?)", (album.artist_id, ))
    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail={'error': "Not found such artist id"})
    
    cursor = app.db_connection.execute("INSERT INTO albums (Title, ArtistId) VALUES ((?), (?))", (album.title, album.artist_id))
    app.db_connection.commit()
    new_album_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute(
        """SELECT AlbumId, Title, ArtistId
         FROM albums WHERE AlbumId = ?""",
        (new_album_id, )).fetchone()
    return album

@app.get("/albums/{album_id}")
async def get_single_album(album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute(
        "SELECT * FROM albums WHERE AlbumId = ?", (album_id, )).fetchone()
    return data

class Customer(BaseModel):
    company: str = None
    address: str = None
    city: str = None
    state: str = None
    country: str = None
    postalcode: str = None 
    fax: str = None

@app.put("/customers/{customer_id}")
async def update_customer(customer_id: int, customer: Customer):
    cursor = app.db_connection.execute(
        """SELECT customerid 
        FROM customers WHERE customerid = (?)""", (customer_id, ))

    if cursor.fetchone() is None:
        raise HTTPException(status_code=404, detail={'error': "Not found such customer id"})
    
    update_data = customer.dict(exclude_unset=True)
    update_data_set = ' '.join([f'{key} = ?,' for key in update_data])[:-1]
    query = f"UPDATE customers SET {update_data_set} WHERE customerid = (?)"
    cursor = app.db_connection.execute(query, (*update_data.values(), customer_id))
    app.db_connection.commit()

    app.db_connection.row_factory = sqlite3.Row
    customer = app.db_connection.execute(
        """SELECT * FROM customers WHERE customerid = ?""", (customer_id, )).fetchone()
    return customer

@app.get("/sales")
async def get_sales_for_category(category: str):
    print(category)
    if category not in ('customers', 'genres'):
        raise HTTPException(status_code=404, detail={'error': "Not found such category"})
    app.db_connection.row_factory = sqlite3.Row
    if category == 'customers':
        data = app.db_connection.execute('''
        SELECT i.CustomerId, c.Email, c.Phone, ROUND(SUM(total), 2) Sum FROM invoices i 
        JOIN customers c ON i.CustomerId = c.CustomerId
        GROUP BY i.CustomerId
        ORDER BY Sum DESC, i.CustomerId;
        ''').fetchall()
    elif category == 'genres':
        data = app.db_connection.execute('''
        SELECT gen.Name, COUNT(*) Sum FROM invoice_items ii 
        JOIN tracks tr on tr.TrackId = ii.TrackId
        JOIN genres gen ON gen.GenreId = tr.GenreId
        GROUP BY gen.Name
        ORDER BY Sum DESC, gen.Name;
        ''').fetchall()
    return data