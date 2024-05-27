from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class Urad(Base):
    __tablename__ = "urad"

    id = Column(Integer, primary_key=True, index=True)
    nazev = Column(String(80))
    url = Column(String(120))
    okres = Column(String(120))
    kraj = Column(String(120))

    oznameni = relationship("Oznameni", backref="urad")


class Oznameni(Base):
    __tablename__ = "oznameni"

    id = Column(Integer, primary_key=True, index=True)
    nazev = Column(String(80))
    datum_vytvoreni = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    url = Column(String(120))

    urad_id = Column(Integer, ForeignKey("urad.id"))
    dokumenty = relationship("Dokumenty", backref="oznameni")


class Dokumenty(Base):
    __tablename__ = "dokumenty"

    id = Column(Integer, primary_key=True, index=True)
    nazev = Column(String(80))
    url = Column(String(120))
    text = Column(Text)

    oznameni_id = Column(Integer, ForeignKey("oznameni.id"))
