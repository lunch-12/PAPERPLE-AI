import yaml
from sqlmodel import create_engine, SQLModel, Session
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


def create_newspaper(newspaper: SQLMODEL.NewsPaper):
    with Session(engine, expire_on_commit=False) as session:
        session.add(newspaper)
        session.commit()


def create_newspapers(newspapers: list[SQLMODEL.NewsPaper]):
    with Session(engine, expire_on_commit=False) as session:
        for newspaper in newspapers:
            session.add(newspaper)
        session.commit()
