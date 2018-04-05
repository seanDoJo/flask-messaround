from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    url = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    queue = Column(String)

    def __repr__(self):
        return "<Host(host={}, url={}, address={}, latitude={}, longitude={}, queue={}".format(self.host, self.url, self.address, self.latitude, self.longitude, self.queue)

if __name__ == '__main__':
    from sqlalchemy import create_engine
    import requests

    mysqlAddr = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_IP").json()['success']
    mysqlUser = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_USR").json()['success']
    mysqlPass = requests.get("http://172.31.36.195:8000/get_preauth/MYSQL_PASS").json()['success']

    mysqlUrl = "mysql:/{}:{}@{}:3306/".format(mysqlUser, mysqlPass, mysqlUrl)

    print(mysqlUrl)

    engine = create_engine(mysqlUrl)
    Base.metadata.create_all(engine)
