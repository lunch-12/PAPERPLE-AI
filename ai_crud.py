import yaml
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.dialects.mysql import insert
from ai_model import SQLMODEL

db_config: dict[str:str] = None
with open("aws.yaml", "r") as file:
    db_config = yaml.safe_load(file)["database"]

URL_components: list[str] = [
    db_config["drivername"],
    "://",
    db_config["username"],
    ":",
    db_config["password"],
    "@",
    db_config["host"],
    ":",
    db_config["port"],
    "/",
    db_config["database"],
    "?",
    "charset=utf8",
]

engine = create_engine("".join(URL_components))
SQLModel.metadata.create_all(engine)


def upsert_newspapers(newspapers: list[SQLMODEL.NewsPaper]):
    with Session(engine, expire_on_commit=False) as session:
        try:
            for newspaper in newspapers:
                stmt = insert(SQLMODEL.NewsPaper).values(newspaper.model_dump())
                stmt = stmt.on_duplicate_key_update(link_hash=stmt.inserted.link_hash)
                session.exec(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
