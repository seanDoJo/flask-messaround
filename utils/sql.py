from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HostData(Base):
    __tablename__ = "hostdata"

    id = Column(Integer, primary_key=True)
    host = Column(String(64))
    item = Column(String(128))
    category = Column(String(128))
    price = Column(String(32))
    description = Column(String(32))
    photo = Column(String(32))
    options = Column(String(32))
    availability = Column(String(32))

class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True)
    host = Column(String(64), unique=True)
    url = Column(String(128), unique=True)
    address = Column(String(128))
    latitude = Column(String(32))
    longitude = Column(String(32))
    queue = Column(String(32))
    photo = Column(String(32))

    def __repr__(self):
        return "<Host(host={}, url={}, address={}, latitude={}, longitude={}, queue={}".format(self.host, self.url, self.address, self.latitude, self.longitude, self.queue)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    import requests

    mysqlAddr = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_IP").json()['success']
    mysqlUser = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_USR").json()['success']
    mysqlPass = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_PASS").json()['success']

    mysqlUrl = "mysql+pymysql://{}:{}@{}:3306/metadata".format(mysqlUser, mysqlPass, mysqlAddr)

    engine = create_engine(mysqlUrl)
    Base.metadata.create_all(engine)
