import ai_model


def crawl_and_save_newspaper(url: str) -> ai_model.NewsPaper:
    """
    1. 해당 URL의 뉴스를 크롤링하고, 요약합니다
    2. 요약한 정보를 RDS에 저장합니다
    3. 뉴스 정보를 리턴합니다

    Args:
        url (str): 크롤링 하고자 하는 뉴스의 URL
    """

    # 1 기능
    # 2 기능
    # 3 기능

    dummy_newspaper = ai_model.NewsPaper(
        title="TEMP TITLE", body="TEMP BODY", url=url, source="TEMP SOURCE"
    )

    return dummy_newspaper


def get_newspapers_for_user(userID: int) -> ai_model.Newspapers:
    """
    ### Summary:
    사용자에게 게시할 Newspaper 리스트를 반환합니다

    ### Args:
    - id (str): 사용자의 id

    ### Returns:
    - page (int): 현재 페이지
    - page_count (int): 총 페이지 수
    - newspapers (list[Newspapaer]): 뉴스페이퍼 리스트를 반환(최대20개)
    """

    temp_newspapers = [
        ai_model.NewsPaper(
            title="TEMP NEWSPAPER TITLE",
            body="TEMP NEWSPAPER BODY",
            url="TEMP NEWSPAPER URL",
            source="TEMP NEWSPAPER SOURCE",
        ),
        ai_model.NewsPaper(
            title="TEMP NEWSPAPER TITLE2",
            body="TEMP NEWSPAPER BODY2",
            url="TEMP NEWSPAPER URL2",
            source="TEMP NEWSPAPER SOURCE2",
        ),
    ]

    dummy_newspapers = ai_model.Newspapers(
        USER_ID=userID, page=1, page_count=1, newspapers=temp_newspapers
    )

    return dummy_newspapers
