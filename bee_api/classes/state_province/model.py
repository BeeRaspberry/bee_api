from sqlalchemy import *
from sqlalchemy.orm import (relationship)
from database import Base

__all__ = ['StateProvince']


class StateProvince(Base):
    __tablename__ = 'stateProvince'
    id = Column(Integer, primary_key=True, autoincrement=True)
    countryId = Column(Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='stateProvinces')
    name = Column(String(200))
    abbreviation = Column(String(10))

    def __repr__(self):
        return self.name
