import yaml
from sqlmodel import create_engine, SQLModel, Session, select
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


def read_newspaper(link_hash: str) -> SQLMODEL.NewsPaper:
    print("[START]read_newspaper, link_hash:", link_hash)
    with Session(engine, expire_on_commit=False) as session:
        try:
            statement = select(SQLMODEL.NewsPaper).where(
                SQLMODEL.NewsPaper.link_hash == link_hash
            )
            newspaper = session.exec(statement).one()
            return newspaper
        except Exception as e:
            print("[EXCEPTION]", e)
            raise ValueError


# def test():
#     try:
#         newspaper = read_newspaper(
#             link_hash="a2de8839d7f32bb07bd9505612796d7abda66a8bc2a32e0a7ac046f20f279fb2"
#         )
#         print(newspaper.__dir__)
#     except Exception:
#         print("ERROR")


# test()
