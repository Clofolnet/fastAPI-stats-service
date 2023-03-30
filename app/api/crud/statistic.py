from datetime import date
from typing import List, Optional

from api.crud.base import CRUDBase
from models.statistic import Statistic
from schemas.statistic import StatisticCreate, StatisticForSee
from sqlalchemy import desc, func
from sqlalchemy.orm import Session, aliased


class CRUDStatistic(CRUDBase[Statistic, StatisticCreate]):

    def read_stats(self,
                   db: Session,
                   *,
                   from_date: date,
                   to_date: date,
                   views_sort: Optional[bool] = False,
                   clicks_sort: Optional[bool] = False,
                   cost_sort: Optional[bool] = False) -> List[StatisticForSee]:
        # Create aliases for Statistic to use in the subquery and main query
        StatisticSubquery = aliased(Statistic)
        StatisticMainQuery = aliased(Statistic)

        # Define the subquery to calculate cpc and cpm grouped by date
        subquery = db.query(
            StatisticSubquery.date.label('date'),
            (func.sum(StatisticSubquery.cost) /
             func.sum(StatisticSubquery.clicks)).label('cpc'),
            ((func.sum(StatisticSubquery.cost) /
             func.sum(StatisticSubquery.views)) * 1000).label('cpm')
        ).filter(
            StatisticSubquery.date.between(from_date, to_date)
        ).group_by(
            StatisticSubquery.date
        ).subquery()

        # Define the main query to join the Statistic table with the subquery and select the desired fields
        query = db.query(
            StatisticMainQuery,
            subquery.c.cpc,
            subquery.c.cpm
        ).outerjoin(
            subquery,
            StatisticMainQuery.date == subquery.c.date
        ).filter(
            StatisticMainQuery.date.between(from_date, to_date)
        )

        # Order the query by the desired sort order(s)
        if views_sort:
            query = query.order_by(desc(StatisticMainQuery.views))
        if clicks_sort:
            query = query.order_by(desc(StatisticMainQuery.clicks))
        if cost_sort:
            query = query.order_by(desc(StatisticMainQuery.cost))

        # Transform the query result into a list of StatisticForSee objects
        result = []
        for row in query.all():
            # Create a dictionary to store the data for the StatisticForSee object
            statistic_dict = row[0].__dict__
            # Remove SQLAlchemy internal state
            del statistic_dict['_sa_instance_state']
            statistic_dict['cpc'] = row[1]
            statistic_dict['cpm'] = row[2]
            result.append(StatisticForSee(**statistic_dict))

        print('read_stats', result)
        return result


statistic = CRUDStatistic(Statistic)
