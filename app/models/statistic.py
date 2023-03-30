from db.base_class import Base
from sqlalchemy import Column, Date, DateTime, Float, Integer
from sqlalchemy.sql import func


class Statistic(Base):
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    views = Column(Integer)
    clicks = Column(Integer)
    cost = Column(Float(precision=3, asdecimal=True))

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
