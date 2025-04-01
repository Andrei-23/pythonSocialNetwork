from fastapi import FastAPI
from app.content.posts.router import router as router_posts
import uvicorn

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Постики"}


app.include_router(router_posts)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)