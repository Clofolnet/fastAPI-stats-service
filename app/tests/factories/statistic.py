from datetime import datetime

from factory import Factory, LazyFunction
from factory.fuzzy import FuzzyFloat, FuzzyInteger
from schemas import StatisticCreate


class StatisticFactory(Factory):
    class Meta:
        model = StatisticCreate

    date = LazyFunction(datetime.now)
    views = FuzzyInteger(low=0)
    clicks = FuzzyInteger(low=0)
    cost = FuzzyFloat(low=0, precision=2)
