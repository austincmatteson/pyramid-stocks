from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Table,
)

from .meta import Base

association_table = Table(
    'association', Base.metadata,
    Column('account_id', Integer, ForeignKey('accounts.id')),
    Column('stock_id', Integer, ForeignKey('stocks.id'))
)
