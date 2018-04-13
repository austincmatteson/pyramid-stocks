from sqlalchemy import (
    Column,
    Integer,
    String,
)

from .meta import Base
from sqlalchemy.orm import relationship
from .junction import association_table


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    account_id = relationship(
        "Account", secondary=association_table, back_populates="stock_id")
    symbol = Column(String, nullable=False, unique=True)
    companyName = Column(String)
    exchange = Column(String)
    industry = Column(String)
    website = Column(String)
    description = Column(String)
    CEO = Column(String)
    issueType = Column(String)
    sector = Column(String)
