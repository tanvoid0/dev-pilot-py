from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase

from py_helper.processor.db_processor import get_session


class BaseModel(DeclarativeBase):
    def __repr__(self):
        columns = inspect(self.__class__).c
        column_values = ", ".join([f"{column.key}={getattr(self, column.key)}" for column in columns])
        return f"{self.__class__.__name__}({column_values})"

    def get_session(self):
        return get_session()