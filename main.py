print(r"    _________              __  .__  _____               __________                             __          ___________                _________________  .____    .__  __          ")
print(r"   /   _____/_____   _____/  |_|__|/ ____\__.__.        \______   \ ____ ______   ____________/  |_        \__    ___/___            /   _____/\_____  \ |    |   |__|/  |_  ____  ")
print(r"   \_____  \\____ \ /  _ \   __\  \   __<   |  |  ______ |       _// __ \\____ \ /  _ \_  __ \   __\  ______ |    | /  _ \   ______  \_____  \  /  / \  \|    |   |  \   __\/ __ \ ")
print(r"   /        \  |_> >  <_> )  | |  ||  |  \___  | /_____/ |    |   \  ___/|  |_> >  <_> )  | \/|  |   /_____/ |    |(  <_> ) /_____/  /        \/   \_/.  \    |___|  ||  | \  ___/ ")
print(r"  /_______  /   __/ \____/|__| |__||__|  / ____|         |____|_  /\___  >   __/ \____/|__|   |__|           |____| \____/          /_______  /\_____\ \_/_______ \__||__|  \___  >")
print(r"          \/|__|                         \/                     \/     \/|__|                                                               \/        \__>       \/             \/ ")
print("  Copyright (c) 2025 Cromatin")
print()
print("  Source: https://github.com/official-Cromatin/spotify-report-to-sqlite")
print("\n")

# Import dependencies
import sqlite3
import pathlib
import json
from datetime import datetime, timedelta

def get_or_create_artist(cursor:sqlite3.Cursor, artist_name:str) -> int:
    cursor.execute("SELECT id FROM artist WHERE name = ?", (artist_name,))
    artist = cursor.fetchone()

    if artist:
        return artist[0]
    else:
        cursor.execute("INSERT INTO artist (name) VALUES (?)", (artist_name,))
        return cursor.lastrowid
    
def get_or_create_song(cursor:sqlite3.Cursor, song_name:str, artist_id:int) -> int:
    cursor.execute("SELECT id FROM song WHERE title = ?", (song_name,))
    artist = cursor.fetchone()

    if artist:
        return artist[0]
    else:
        cursor.execute("INSERT INTO song (title, artist_id) VALUES (?, ?)", (song_name, artist_id))
        return cursor.lastrowid

# Get the path to this folder
source_path = pathlib.Path(__file__).resolve()
base_path = source_path.parents[0]
print(f"Using the following path as entrypoint: '{base_path}'")

# Open the database connection
db_connection = sqlite3.connect(base_path / "export.db")
db_cursor = db_connection.cursor()

# Create the tables
db_cursor.execute("DROP TABLE IF EXISTS artist")
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS artist (
        id INTEGER PRIMARY KEY, 
        name TEXT)""")

db_cursor.execute("DROP TABLE IF EXISTS song")
db_cursor.execute("""    
    CREATE TABLE IF NOT EXISTS song (
        id INTEGER PRIMARY KEY, 
        title TEXT, 
        artist_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artist (id))""")

db_cursor.execute("DROP TABLE IF EXISTS stream")
db_cursor.execute("""
    CREATE TABLE IF NOT EXISTS stream (
        id INTEGER PRIMARY KEY,
        start TIMESTAMP,
        end TIMESTAMP,
        duration INTEGER,
        song_id INTEGER,
        FOREIGN KEY (song_id) REFERENCES song (id))""")
print("Database ready")

# Load each file into memory
listening_history:list[dict] = []
for file_path in base_path.joinpath("streaming_history").iterdir():
    if file_path.suffix == ".txt":
        continue

    if file_path.suffix != ".json":
        print(f"Skipped the file {file_path.name}, since its not json")
    
    with open(file_path, encoding = "utf-8") as file:
        listening_history.extend(json.load(file))

# Go over each streamed song
for streamed_song in listening_history:
    artist_id = get_or_create_artist(db_cursor, streamed_song["artistName"])
    song_id = get_or_create_song(db_cursor, streamed_song["trackName"], artist_id)

    end_time = datetime.strptime(streamed_song["endTime"], "%Y-%m-%d %H:%M")
    start_time = end_time - timedelta(milliseconds = streamed_song["msPlayed"])

    db_cursor.execute("INSERT INTO stream (start, end, duration, song_id) VALUES (?, ?, ?, ?)", (start_time, end_time, streamed_song["msPlayed"], song_id))
db_connection.commit()
db_cursor.close()
db_connection.close()