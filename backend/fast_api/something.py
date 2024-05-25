from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, select 
from sqlalchemy.orm import sessionmaker
from models import Urad, Base
from schema import UradModel



DATABASE_URL = "postgresql://postgres:BeicfkeCYmrolGsYgFOXkUawuesjkcYt@viaduct.proxy.rlwy.net:51943/railway"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
with SessionLocal() as session:
    uredni_desky = session.query(Urad.nazev).limit(10).all() 
    results = [nazev for nazev, in uredni_desky]
    if results:
        print(results)
    else:
        print('it aint working')