import ai_model
import ai_crud


def crawl_and_write_newspaper(url: str) -> ai_model.APIMODEL.NewsPaper:
    """
    1. 해당 URL의 뉴스를 크롤링하고, 요약합니다
    2. 요약한 정보를 RDS에 저장합니다
    3. 뉴스 정보를 리턴합니다

    Args:
        url (str): 크롤링 하고자 하는 뉴스의 URL
    """

    # 1.
    title = "CREATE TEMP TITLE"
    body = "CREATE TEMP BODY"
    summary = "CREATE TEMP SUMMARY"
    source = "CREATE TEMP SOURCE"

    # 2.
    sql_newspaper = ai_model.SQLMODEL.NewsPaper(
        title=title + url,
        body=body + url,
        summary=summary + url,
        link=url,
        source=source,
    )

    ai_crud.create_newspaper(sql_newspaper)

    # 3.
    return ai_model.APIMODEL.NewsPaper(
        title=title, summary=summary, link=url, source=source
    )


def get_newspapers_for_user(user_id: int) -> ai_model.APIMODEL.Newspapers:
    # 1. User ID로 페이지 리스트 받아오기
    page = 0
    page_count = 10
    newspapers = []

    return ai_model.APIMODEL.Newspapers(
        page=page, page_count=page_count, newspapers=newspapers
    )
