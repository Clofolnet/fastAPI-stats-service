from api.crud import statistic as statistic_crud
from sqlalchemy.orm import Session

from app.tests.factories.statistic import StatisticFactory


def test_create_statistic(db: Session) -> None:
    statistic_in = StatisticFactory.create()
    statistic = statistic_crud.create(db=db, obj_in=statistic_in)
    assert statistic.date == statistic_in.date


def test_get_statistic(db: Session) -> None:
    statistic_in = StatisticFactory.create()
    statistic = statistic_crud.create(db=db, obj_in=statistic_in)
    stored_statistic = statistic_crud.get(db=db, id=statistic.id)
    assert stored_statistic
    assert statistic.id == stored_statistic.id
    assert statistic.date == stored_statistic.date


def test_delete_statistic(db: Session) -> None:
    statistic_in = StatisticFactory.create()
    statistic = statistic_crud.create(db=db, obj_in=statistic_in)
    statistic2 = statistic_crud.remove(db=db, id=statistic.id)
    statistic3 = statistic_crud.get(db=db, id=statistic.id)
    assert statistic3 is None
    assert statistic2.id == statistic.id
    assert statistic2.date == statistic_in.date


def test_delete_all_statistic(db: Session) -> None:
    statistics_in = StatisticFactory.create_batch(5)
    statistics = statistic_crud.bulk_create(db=db, objs=statistics_in)
    statistic_crud.delete_all(db=db)
    statistic = statistic_crud.get(db=db, id=statistics[0].id)
    assert statistic is None
