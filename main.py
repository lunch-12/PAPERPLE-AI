from fastapi import FastAPI
import ai_router

app = FastAPI()


@app.get("/health")
async def welcome():
    return {"message": "Hello Lunch!"}


app.include_router(ai_router.ai_router)
