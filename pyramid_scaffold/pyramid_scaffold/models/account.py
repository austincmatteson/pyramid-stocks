from sqlalchemy import (
    Column,
    Integer,
    String,
)


from .meta import Base


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String)
    password = Column(String)
