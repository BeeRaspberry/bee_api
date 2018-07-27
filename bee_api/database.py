from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from bee_api.app import app


engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       convert_unicode=True)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    metadata.create_all(bind=engine)
