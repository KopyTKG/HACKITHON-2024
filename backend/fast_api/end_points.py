from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pydantic
import requests
import psycopg2

class Item(pydantic.BaseModel):
    filter: str

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

filtry = ["oznámení", "rozhodnutí", "stanovení", "vyhláška", "dražba", "rozpočet", "prodej", "nálezy", "stavební nálezy", "přerušení dodávek"]
string = "postgres://postgres:postgres@172.28.5.4:5432/postgres"

def get_connection():
    try:
        conn = psycopg2.connect(string)
        return conn
    except:
        raise HTTPException(status_code=500, detail="Database connection error")


@app.get("/urad/{urad_id}")
def read_urad(urad_id: int):
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM urad WHERE id = %s LIMIT 1;"
    cur.exeute(sql)
    results = cur.fetchall()
    if results is None:
        raise HTTPException(status_code=404, detail="Urad not found")

    conn.close()
    return results

@app.get("/map/")
async def read_item():
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT nazev, url, lat, lon FROM urad"
    cur.execute(sql)
    results = cur.fetchall()
    export = []
    for row in results:
        if row[2] is not None and row[3] is not None:
            export.append({"name": row[0], "url": row[1], "coordinates": [row[3], row[2]]})

    conn.close()
    return export

@app.post("/search")
async def search(item: Item):
    conn = get_connection()
    cur = conn.cursor()
    if item.filter in filtry:
        sql = "SELECT o.id, o.nazev, o.url, o.datum_vyveseni FROM oznameni o JOIN kategorie_oznameni ko ON o.id = ko.id_oznameni JOIN kategorie k ON ko.id_kategorie = k.id WHERE k.nazev ILIKE %s"
        cur.execute(sql, (item.filter,))
        results = cur.fetchall()
        export = []
        for row in results:
            if row[0] is not None and row[1] is not None:
                export.append({"doc_id": row[0], "nazev": row[1], "url": row[2], "datum": row[3].strftime("%Y-%m-%d")})

        conn.close()
        return export 
    else: 
        sql = "SELECT o.id, o.nazev, o.url, o.datum_vyveseni FROM oznameni o WHERE o.nazev ILIKE %s"
        cur.execute(sql, (item.filter,))
        results = cur.fetchall()
        export = []
        for row in results:
            if row[0] is not None and row[1] is not None:
                export.append({"doc_id": row[0], "nazev": row[1], "url": row[2], "datum": row[3].strftime("%Y-%m-%d")})

        conn.close()
        return export

if __name__ == "__main__":
    import uvicorn

    # Start the server with Uvicorn
    uvicorn.run("end_points:app", host="0.0.0.0", port=9999, reload=True)
