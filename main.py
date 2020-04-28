import sqlite3
from fastapi import FastAPI, HTTPException


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
    tracks = cursor.execute("SELECT * FROM tracks LIMIT ? OFFSET ?", (per_page, page*per_page)).fetchall()
    return tracks

@app.get("/tracks/composers")
async def get_tracks(composer_name:str):
    # app.db_connection.row_factory = sqlite3.Row
    app.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = app.db_connection.cursor()
    track_names = cursor.execute("SELECT name FROM tracks WHERE Composer = ? ORDER BY name ASC", (composer_name, )).fetchall()
    if len(track_names) == 0:
        raise HTTPException(status_code=404, detail="Not found such composer")
    return track_names
