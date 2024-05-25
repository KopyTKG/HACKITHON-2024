from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DokumentyModel(BaseModel):
    id: int
    nazev: str
    url: str
    text: str
    oznameni_id: int

    class Config:
        orm_mode = True


class OznameniModel(BaseModel):
    id: int
    nazev: str
    datum_vytvoreni: datetime
    url: str
    urad_id: int
    dokumenty: List[DokumentyModel]

    class Config:
        orm_mode = True


class UradModel(BaseModel):
    id: int
    nazev: str
    url: str
    okres: str
    kraj: str
    oznameni: List[OznameniModel]

    class Config:
        orm_mode = True