from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import db

try:
    from babel.dates import format_timedelta
except ImportError:
    def format_timedelta(timed):
        ret = []
        if timed.days == 1:
            ret.append("einem Tag")
        elif timed.days > 1:
            ret.append("%i Tagen" % timed.days)

        if timed.seconds:
            hours = timed.seconds / 3600
            if hours == 1:
                ret.append("einer Stunde")
            elif hours > 1:
                ret.append("%i Stunden" % hours)

            minutes = (timed.seconds % 3600) / 60
            if minutes == 1:
                ret.append("einer Minute")
            elif minutes > 1:
                ret.append("%i Minuten" % minutes)

        if not ret:
            ret = ["gerade eben"]

        try:
            return " und ".join(ret[0:2])
        except IndexError:
            return ret[0]


Base = declarative_base()


class Node(Base):
    __tablename__ = 'nodes'

    id = Column(String, primary_key=True)
    name = Column(String)
    lastseen = Column(Integer)
    contact = Column(String)
    lastcontact = Column(Integer)
    ignore = Column(Integer)

    def __repr__(self):
        return "<Node(id='%s', name='%s')>" % (self.id, self.name)

    def format_infotext(self, text):
        return text.format(
            id=self.id,
            name=self.name,
            contact=self.contact,
            since=format_timedelta(
                datetime.now() - datetime.fromtimestamp(self.lastseen)
            ),
        )

engine = create_engine(db)
Session = sessionmaker(bind=engine)
session = Session()
