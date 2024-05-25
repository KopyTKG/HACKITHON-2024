from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select 
from sqlalchemy.orm import sessionmaker
from models import Urad, Base
from schema import UradModel
import requests
# Create FastAPI instance
app = FastAPI()

# Database connection
DATABASE_URL = "postgresql://postgres:BeicfkeCYmrolGsYgFOXkUawuesjkcYt@viaduct.proxy.rlwy.net:51943/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

@app.get("/map/")
async def read_item():
    with SessionLocal() as session:
        uredni_desky = session.query(Urad.nazev).limit(10).all() 
        results = [nazev for nazev, in uredni_desky] 
        return {"name": "uredni_desky", "results": results}

@app.get("/urad/{urad_id}", response_model=UradModel)
def read_urad(urad_id: int):
    db = SessionLocal()
    urad = db.query(Urad).filter(Urad.id == urad_id).first()
    if urad is None:
        raise HTTPException(status_code=404, detail="Urad not found")
    return urad

@app.get("/mapy/")
async def read_item():
    with SessionLocal() as session:
        # Získání názvů úřadů z databáze
        uredni_desky = session.query(Urad.nazev).limit(10).all()
        # Extrahování druhého slova z každého názvu
        modified_names = [nazev.split()[1] for nazev, in uredni_desky]

    # Procházení získaných názvů a získání informací o jejich umístění
    locations = []
    for name in modified_names:
        # Vytvoření URL s názvem z druhého slova
        url = f"https://api.mapy.cz/v1/geocode?query={name}&lang=cs&limit=5&type=regional&type=poi"
        # Získání dat z externího API
        response = requests.get(url)
        # Získání informací o umístění z odpovědi API
        data = response.json()
        # Přidání informací o umístění do seznamu
        locations.append(data)

    return {"name": "uredni_desky", "results": locations}

@app.post("/search/")
async def search(item_name: str):
    # Open a new session
    with SessionLocal() as session:
        uredni_desky = select(Urad).limit(10)
        result = session.execute(uredni_desky)
        results = [dict(row) for row in result]
        return {"item_name": item_name, "results": results}

if __name__ == "__main__":
    import uvicorn

    # Start the server with Uvicorn
    uvicorn.run("end_points:app", host="0.0.0.0", port=9999, reload=True)