import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import MetaData, Table

DB_PATH = "sqlite:///database/shop.db"
Base = declarative_base()

# создаем соединение к базе данных
engine = sa.create_engine(DB_PATH, echo = False)
# создаем фабрику сессию
Sessions = sessionmaker(engine)
# cоздаем сессию
session = Sessions()

metadata = MetaData(engine)

class Clients(Base):
    __table__ = Table('clients', metadata, autoload=True)

# class Orders(Base):
#     __table__ = Table('orders', metadata, autoload=True)

def getClientInfo(id):
    data = session.query(Clients).filter(Clients.client_id == id)
    data_result = []
    for values in data:
        data_result.append(values.username)
        data_result.append(values.first_name)
        data_result.append(values.last_name)
        data_result.append(values.location)
        data_result.append(values.phone)
    return data_result

def addClient(id, user, fname, lname):
    check_client = getClientInfo(id)
    if len(check_client) == 0:
        print("Новы клиент. Надо добавить")
        new_client = Clients(client_id = id, username = user, first_name = fname, last_name = lname)
        print(new_client)
        session.add(new_client)
        session.commit()
        session.close()
    else:
        print(f'INFO: Такой пользователь: {user} c ID: {id} уже есть в Базе Данных.')

def addClientInfo(data, id, status):
    if status == 'phone':
        client = session.query(Clients).filter(Clients.client_id == id).first()
        client.phone = data
        session.commit()
        session.close()
    elif status == 'location':
        client = session.query(Clients).filter(Clients.client_id == id).first()
        client.location = data
        session.commit()
        session.close()
    else:
        pass