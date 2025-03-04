from fastapi import FastAPI, HTTPException, Query
from psycopg2.extras import RealDictCursor
from parser import parse_page
from psycopg2 import connect
import uvicorn

app = FastAPI()

# connection to the sql-database:
DATABASE = {
    "dbname" : "cnn_news", # for example
    "user" : "your_username_in_PostgreSQL",
    "password" : "your_sql_database_password",
    "host" : "your_host", # usually, localhost
    "port" : 5432 # default
}

def get_connection():
    return connect(
        dbname = DATABASE["dbname"],
        user = DATABASE["user"],
        password = DATABASE["password"],
        host = DATABASE["host"],
        port = DATABASE["port"]
    )

# sql-database initiallization:
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cnn_news (
            id SERIAL PRIMARY KEY,
            headline TEXT,
            date TEXT,
            author TEXT,
            source TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

# 'parse' endpoint:
@app.get("/parse")
def parse(url: str = Query(..., description = "URL for parsing")):
    try:
        # starting site parsing:
        data = parse_page(url)
        # recording:
        conn = get_connection()
        cur = conn.cursor()
        for item in data:
            cur.execute("""
                INSERT INTO cnn_news (headline, date, author, source)
                VALUES (%s, %s, %s, %s)
            """, (item["headline"], item["date"], item["author"], item["source"]))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "inserted": len(data), "data": data}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

# 'reforming into json view' endpoint: 
@app.get("/news")
def get_news():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT headline, date, author, source FROM cnn_news;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)

'''
Use [uvicorn main:app --reload] to start the API point
Use [curl "http://127.0.0.1:8000/parse?url=https://edition.cnn.com/account/log-in"] to start CNN parsing
Use [curl http://127.0.0.1:8000/news -o news_data.json] to get the json - format parsing data 
'''