from fastapi import Request, FastAPI
import httpx
import uvicorn

app = FastAPI()
user_service_url = "http://localhost:8001"

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(request: Request, path: str):
    async with httpx.AsyncClient() as client:
        url = f"{user_service_url}/{path}"
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            content=request.stream(),
        )
        return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)