from pydantic import BaseModel

# todo
# 관련종목 ERD 논의필요

# class StockInfo(BaseModel):
#     related_stock_name: str  # 관련 종목명
#     stock_code: str  # 종목 코드
#     current_price: str  # 현재 가격
#     price_change: str  # 전일대비 등락가격

class NewsPaper(BaseModel):
    title: str
    body: str
    url: str
    source: str
    # stock_info: StockInfo  # 종목 정보


class Newspapers(BaseModel):
    USER_ID: int
    page: int
    page_count: int
    newspapers: list[NewsPaper]
