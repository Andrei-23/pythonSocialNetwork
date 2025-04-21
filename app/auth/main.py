from fastapi import FastAPI
from app.auth.users.router import router as router_users
import uvicorn

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Добро пожаловать!"}


app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)