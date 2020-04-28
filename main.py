import sqlite3
from fastapi import FastAPI


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
    print((type(per_page), type(page)))
    tracks = cursor.execute("SELECT * FROM tracks LIMIT ? OFFSET ?", (per_page, page*per_page)).fetchall()
    return tracks
