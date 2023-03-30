from datetime import date

from api.crud import statistic as statistic_crud
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.factories.statistic import StatisticFactory


def test_create_statistic(
    client: TestClient, db: Session
) -> None:
    data = StatisticFactory.create()
    r = client.post(
        f"{settings.API_V1_STR}/statistics/", json=jsonable_encoder(data),
    )
    assert 200 <= r.status_code < 300
    created_statistic = r.json()
    assert created_statistic['views'] == data.views


def test_create_statistic_only_date(
    client: TestClient, db: Session
) -> None:
    data = StatisticFactory.create(views=None, clicks=None, cost=None)
    r = client.post(
        f"{settings.API_V1_STR}/statistics/", json=jsonable_encoder(data),
    )
    assert 200 <= r.status_code < 300
    created_statistic = r.json()
    assert created_statistic['views'] == data.views


def test_get_statistic(
    client: TestClient, db: Session
) -> None:
    statistic_in = StatisticFactory.create()
    statistic = statistic_crud.create(db, obj_in=statistic_in)
    statistic_id = statistic.id
    r = client.get(
        f"{settings.API_V1_STR}/statistics/{statistic_id}",
    )
    assert 200 <= r.status_code < 300
    api_statistic = r.json()
    existing_statistic = statistic_crud.get(db, id=statistic_id)
    assert existing_statistic
    assert existing_statistic.views == api_statistic["views"]


def test_retrieve_statistics(
    client: TestClient, db: Session
) -> None:
    statistics_in = StatisticFactory.create_batch(5)
    statistic_crud.bulk_create(db=db, objs=statistics_in)

    r = client.get(f"{settings.API_V1_STR}/statistics/",
                   )
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "views" in item


def test_delete_all_statistics(
        client: TestClient, db: Session
) -> None:
    statistics_in = StatisticFactory.create_batch(5)
    statistic_crud.bulk_create(db=db, objs=statistics_in)

    r = client.delete(f"{settings.API_V1_STR}/statistics/delete-all",
                      )

    api_statistic = r.json()
    assert api_statistic["success"] == True


def test_read_stats_with_dates(
    client: TestClient, db: Session
) -> None:
    statistics = [
        StatisticFactory.create(date=date(2022, 1, i),
                                views=10 * i, clicks=5 * i, cost=0.5 * i)
        for i in range(1, 6)
    ]
    statistic_crud.bulk_create(db=db, objs=statistics)

    # Test with from_date and to_date parameters only
    response = client.get(
        f"{settings.API_V1_STR}/statistics/read-stats",
        params={
            "from_date": date(2022, 1, 1),
            "to_date": date(2022, 1, 5)
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert response.json()[0]["views"] == 10
    assert response.json()[0]["clicks"] == 5
    assert response.json()[0]["cost"] == 0.5
    assert response.json()[0]["cpc"] == 0.1
    assert response.json()[0]["cpm"] == 50


def test_read_stats_with_params_and_sorting(
    client: TestClient, db: Session
) -> None:
    statistics = [
        StatisticFactory.create(date=date(2022, 1, i),
                                views=10 * i, clicks=5 * i, cost=0.5 * i)
        for i in range(1, 6)
    ]
    statistic_crud.bulk_create(db=db, objs=statistics)

    response = client.get(
        f"{settings.API_V1_STR}/statistics/read-stats",
        params={
            "from_date": date(2022, 1, 1),
            "to_date": date(2022, 1, 5),
            "clicks_sort": True,
            "cost_sort": True,
            "views_sort": True
        }
    )
    assert response.status_code == 200
    assert len(response.json()) == 10
    assert response.json()[0]["clicks"] == 25
    assert response.json()[0]["cost"] == 2.5
    assert response.json()[0]["views"] == 50
    assert response.json()[0]["cpc"] == 0.1
    assert response.json()[0]["cpm"] == 50
    assert response.json()[1]["clicks"] == 25
    assert response.json()[1]["cost"] == 2.5
    assert response.json()[1]["views"] == 50
    assert response.json()[1]["cpc"] == 0.1
    assert response.json()[1]["cpm"] == 50
