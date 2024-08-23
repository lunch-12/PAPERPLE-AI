from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Text
from typing import Optional
from datetime import datetime, timezone


class APIMODEL:
    class NewsPaper(BaseModel):
        title: str
        summary: str
        link: str
        img: Optional[str] = None
        source: str
        published_at: datetime = datetime.now(timezone.utc)

    class Newspapers(BaseModel):
        page: int
        page_count: int
        newspapers: list["APIMODEL.NewsPaper"]


class SQLMODEL:
    class NewsPaper(SQLModel, table=True):
        __tablename__ = "NewsPaper"
        id: int = Field(default=None, primary_key=True)
        title: str = Field(max_length=255)
        body: str = Field(sa_column=Text())
        summary: str = Field(max_length=1000)
        link: str = Field(max_length=2048)
        image: Optional[str] = Field(default=None, max_length=2048)
        source: str = Field(max_length=255)
        created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        published_at: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc)
        )
