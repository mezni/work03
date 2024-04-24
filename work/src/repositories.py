import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.models import PeriodModel


@dataclass
class CreatePeriodDTO:
    period_name: str

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return asdict(self)


@dataclass
class PeriodDTO:
    period_name: str
    period_is_holiday: bool = False

    def __post_init__(self):
        self.period_code = uuid.uuid4()
        self.period_date = datetime.strptime(self.period_name, "%Y-%m-%d")
        self.period_day = self.period_date.day
        self.period_month = self.period_date.month
        self.period_year = self.period_date.year

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        return {
            "period_code": self.period_code,
            "period_name": self.period_name,
            "period_date": self.period_date,
            "period_day": self.period_day,
            "period_month": self.period_month,
            "period_year": self.period_year,
            "period_is_holiday": self.period_is_holiday,
        }


class SQLitePeriodRepository:
    def __init__(self, async_session: async_sessionmaker[AsyncSession]):
        self.async_session = async_session()

    async def create_period(self, period_dto: CreatePeriodDTO):
        async with self.async_session as session:
            new_period_dto = PeriodDTO(**period_dto.to_dict())
            new_period_item = PeriodModel(**new_period_dto.to_dict())
            session.add(new_period_item)
            await session.commit()
