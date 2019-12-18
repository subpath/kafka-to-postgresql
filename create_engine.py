# import pymysql
# pymysql.install_as_MySQLdb()

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import toml

CONFIG = toml.load('config.toml')

PSQL_URI = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(CONFIG['psql_connector']['user'],
                                           CONFIG['psql_connector']['password'],
                                           CONFIG['psql_connector']['host'],
                                           CONFIG['psql_connector']['port'],
                                           CONFIG['psql_connector']['database'])

engine = create_engine(PSQL_URI, echo=False, pool_size=20, max_overflow=100, pool_recycle=3600 )
session_factory = sessionmaker(autocommit=True, autoflush=False, bind=engine)
session = scoped_session(session_factory)
