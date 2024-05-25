from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select 
from sqlalchemy.orm import sessionmaker
from models import Urad, Base
from schema import UradModel
import requests
import psycopg2
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
filtry = ["Oznámení", "Rozhodnutí", "Stanovení", "vyhláška", "dražva", "rozpočet", "prodej", "nálezy", "stavební_práce", "přerušení dodávek"]

conn = psycopg2.connect('dbname=postgres user=postgres password=BeicfkeCYmrolGsYgFOXkUawuesjkcYt host=viaduct.proxy.rlwy.net port=51943')
cur = conn.cursor()

# Database connection
DATABASE_URL = "postgresql://postgres:BeicfkeCYmrolGsYgFOXkUawuesjkcYt@viaduct.proxy.rlwy.net:51943/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@app.get("/urad/{urad_id}", response_model=UradModel)
def read_urad(urad_id: int):
    db = SessionLocal()
    urad = db.query(Urad).filter(Urad.id == urad_id).first()
    if urad is None:
        raise HTTPException(status_code=404, detail="Urad not found")
    return urad

@app.get("/map/")
async def read_item():
    sql = "SELECT nazev, url, lat, lon FROM urad"
    cur.execute(sql)
    results = cur.fetchall()
    export = []
    for row in results:
        if row[2] is not None and row[3] is not None:
            export.append({"name": row[0], "url": row[1], "coordinates": [row[3], row[2]]})
    return export

@app.post("/search/")
async def search(item_name: str):
    if item_name is in filtry:
        sql = "SELECT urad.nazev, urad.url FROM urad JOIN filter_table ON urad.filter_id = filter_table.id WHERE filter_table.name = %s "
        cur.execute(sql)
        results = cur.fetchall()
        export = []
        for row in results:
        if row[0] is not None and row[1] is not None:
            export.append({"name": row[0], "url": row[1]})
         return export 
    else: 
        query = "SELECT urad.nazev, urad.url FROM urad JOIN filter_table ON urad.filter_id = filter_table.id WHERE urad.nazev = %s"
        cur.execute(sql)
        results = cur.fetchall()
        export = []
        for row in results:
        if row[0] is not None and row[1] is not None:
            export.append({"name": row[0], "url": row[1],})
         return export
if __name__ == "__main__":
    import uvicorn

    # Start the server with Uvicorn
    uvicorn.run("end_points:app", host="0.0.0.0", port=9999, reload=True)
