from sqlalchemy import Column, BigInteger, Boolean, Integer, String, ARRAY

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'Users'
    
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), default=None)
    referal = Column(BigInteger, default=None)
    referals = Column(ARRAY(BigInteger), default=[])
    purchases = Column(Integer, default=0)
    amount = Column(Integer, default=0)
    points = Column(Integer, default=0)
    
    def __str__(self):
        return f'user_id - {self.user_id}\nfull_name - {self.full_name}'


class Items(TimedBaseModel):
    __tablename__ = 'Items'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(50), nullable=False)
    description = Column(String(500))
    price = Column(Integer)
    photo_url = Column(String(350))