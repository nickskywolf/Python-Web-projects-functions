import configparser
import pathlib
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker


file_config = pathlib.Path(__file__).parent.joinpath('config.ini')  # ../config.ini
print(file_config)
config = configparser.ConfigParser()
config.read(file_config)


user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
db = config.get('DEV_DB', 'DB_NAME')
URI = f'postgresql+psycopg2://{user}:{password}@{domain}:{port}/{db}'

engine = create_engine(URI)
Session = sessionmaker(bind=engine)
session = Session()