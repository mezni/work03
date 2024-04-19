import uuid
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class Period:
    """Definition of the Period entity"""

    period_code: uuid.UUID
    period_name: str
    period_date: datetime
    period_day: int
    period_month: int
    period_year: int
    period_quarter: int
    period_day_of_week: int
    period_day_of_year: int
    period_week_of_year: int
    period_is_holiday: bool

    @classmethod
    def from_dict(cls, data):
        """Convert data from a dictionary"""
        return cls(**data)

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class PeriodInputDto:
    period_name: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class PeriodOutputDto:
    """Output Dto for create profession"""

    period: Period


class PeriodPresenter:
    @staticmethod
    def dto_to_entity(period_dto):
        period_code = uuid.uuid4()
        period_name = period_dto.period_name
        period_date = datetime.strptime(period_dto.period_name, "%Y-%m-%d")
        period_day = period_date.day
        period_month = period_date.month
        period_year = period_date.year
        period_quarter = period_date.month // 3 + 1
        period_day_of_week = period_date.weekday() + 1
        period_day_of_year = period_date.timetuple().tm_yday
        period_week_of_year = period_date.isocalendar()[1]
        period_is_holiday = False
        period = Period(
            period_code,
            period_name,
            period_date,
            period_day,
            period_month,
            period_year,
            period_quarter,
            period_day_of_week,
            period_day_of_year,
            period_week_of_year,
            period_is_holiday,
        )
        return period


class PeriodRepository:
    def __init__(self):
        self.periods = []

    def add(self, period):
        self.periods.append(period)

    def generate_dates(self, start_date, end_date):
        current_date = start_date
        while current_date <= end_date:
            yield current_date
            current_date += timedelta(days=1)

    def get_interval_gap(self, period_name):
        period_interval_gap = []

        period_min_max = self.get_period_min_max()
        if not period_min_max["period_min"] and not period_min_max["period_max"]:
            period_interval_gap.append(period_name)
        else:
            period_date = datetime.strptime(period_name, "%Y-%m-%d")
            period_min_date = datetime.strptime(
                period_min_max["period_min"], "%Y-%m-%d"
            )
            period_max_date = datetime.strptime(
                period_min_max["period_max"], "%Y-%m-%d"
            )

            if period_date > period_max_date:
                start_date = period_max_date + timedelta(days=1)
                end_date = period_date
                for curr_date in self.generate_dates(start_date, end_date):
                    period_interval_gap.append(curr_date.strftime("%Y-%m-%d"))

            if period_date < period_min_date:
                start_date = period_date
                end_date = period_min_date - timedelta(days=1)
                for curr_date in self.generate_dates(start_date, end_date):
                    period_interval_gap.append(curr_date.strftime("%Y-%m-%d"))

        return period_interval_gap

    def get_period_by_name(self, period_name):
        l = [p for p in self.periods if p.period_name == period_name]
        if l:
            return l[0]
        else:
            return None

    def get_period_min_max(self):
        period_min = None
        period_max = None

        for p in self.periods:
            if not period_max or p.period_name > period_max:
                period_max = p.period_name
            if not period_min or p.period_name < period_min:
                period_min = p.period_name
        return {"period_min": period_min, "period_max": period_max}

    def list(self):
        return self.periods


def main():
    data = [
        {"period_name": "2024-04-03"},
        {"period_name": "2024-04-06"},
        {"period_name": "2024-04-06"},
        {"period_name": "2024-04-01"},
    ]
    period_repo = PeriodRepository()

    for d in data:
        print(d)
        period_saved = period_repo.get_period_by_name(d["period_name"])
        if period_saved:
            period = period_saved
        else:
            period_gap = period_repo.get_interval_gap(d["period_name"])
            for p in period_gap:
                period_dto = PeriodInputDto(p)
                period = PeriodPresenter.dto_to_entity(period_dto)
                print(f"    = {period.period_name}")
                period_repo.add(period)

    period_list = period_repo.list()
    for p in period_list:
        print(f"period= {p.period_code} - {p.period_name} - {p.period_date}")


main()
