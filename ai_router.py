from fastapi import APIRouter
import ai_model
import ai_service

ai_router = APIRouter()


@ai_router.post("/newspaper/{url}")
def post_newspaper(url: str) -> ai_model.NewsPaper:
    return ai_service.crawl_and_save_newspaper(url)


@ai_router.get("/newspapaers/{id}")
def get_newspapers(id: int) -> ai_model.Newspapers:
    return ai_service.get_newspapers_for_user(id)
