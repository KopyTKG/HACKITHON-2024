from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, select 
from sqlalchemy.orm import sessionmaker
from models import Urad, Base
from schema import UradModel
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

filtry = ["Oznámení", "Rozhodnutí", "Stanovení", "vyhláška", "dražva", "rozpočet", "prodej", "nálezy", "stavební práce", "přerušení dodávek"]

conn = psycopg2.connect('dbname=postgres user=postgres password=postgres host=hackithon_db port=51943')
cur = conn.cursor()

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@hackithon_db:51943/postgres"
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
async def search(item: Item):
    print(item)
    if item in filtry:
        sql = "SELECT o.id, o.nazev, o.url, o.datum_vyveseni FROM oznameni o JOIN kategorie_oznameni ko ON o.id = ko.oznameni_id JOIN kategorie k ON ko.kategorie_id = k.id WHERE k.nazev Like %s"
        cur.execute(sql, (item.filter,))
        results = cur.fetchall()
        export = []
        for row in results:
            if row[0] is not None and row[1] is not None:
                export.append({"doc_id": row[0], "nazev": row[1], "url": row[2], "datum": row[3]})
        return export 
    else: 
        sql = "SELECT o.id, o.nazev, o.url, o.datum_vyveseni FROM oznameni o WHERE o.nazev LIKE %s"
        cur.execute(sql, (item.filter,))
        results = cur.fetchall()
        export = []
        for row in results:
            if row[0] is not None and row[1] is not None:
                export.append({"doc_id": row[0], "nazev": row[1], "url": row[2], "datum": row[3]})
        return export

if __name__ == "__main__":
    import uvicorn

    # Start the server with Uvicorn
    uvicorn.run("end_points:app", host="0.0.0.0", port=9999, reload=True)
