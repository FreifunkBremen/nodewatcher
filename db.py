from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'

    mac = Column(String, primary_key=True)
    name = Column(String)
    vpn = Column(Integer)
    lastseen = Column(Integer)
    contact = Column(String)
    lastcontact = Column(Integer)
    ignore = Column(Integer)

    def __repr__(self):
        return "<Node(mac='%s', name='%s')>" % (self.mac, self.name)

engine = create_engine(db)
Session = sessionmaker(bind=engine)
session = Session()
