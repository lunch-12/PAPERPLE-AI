from pydantic import BaseModel


class NewsPaper(BaseModel):
    title: str
    body: str
    url: str
    source: str


class Newspapers(BaseModel):
    USER_ID: int
    page: int
    page_count: int
    newspapers: list[NewsPaper]
