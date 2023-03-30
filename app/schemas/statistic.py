from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class StatisticBase(BaseModel):
    """ Shared properties """
    date: date
    views: Optional[int] = None
    clicks: Optional[int] = None
    cost: Optional[float] = None


class StatisticCreate(StatisticBase):
    """ Properties to receive on сomment creation """
    pass


class StatisticInDBBase(StatisticBase):
    """ Properties shared by models stored in DB """
    id: int
    time_created: datetime
    time_updated: Optional[datetime] = None

    class Config:
        orm_mode = True


class Statistic(StatisticInDBBase):
    """ Properties to return to client """
    pass


class StatisticInDB(StatisticInDBBase):
    """ Properties properties stored in DB """
    pass


class StatisticForSee(StatisticInDBBase):
    """ Properties for the special method of requesting statistics """
    cpc: float
    cpm: float
