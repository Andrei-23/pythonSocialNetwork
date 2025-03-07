from fastapi import FastAPI
from app.users.router import router as router_students
import uvicorn

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}


app.include_router(router_students)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)