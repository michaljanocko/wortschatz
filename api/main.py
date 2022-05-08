import os
from fastapi import BackgroundTasks, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.exceptions import HTTPException
import httpx

DIST_FOLDER = os.getenv("DIST_FOLDER")
NOTION_SECRET = os.getenv("NOTION_SECRET")

app = FastAPI()
client = httpx.AsyncClient()


@app.get("/api/token")
async def token(code: str) -> str:
    response = await client.get(
        "https://api.notion.com/v1/oauth/token",
        json={
            "grant_type": "authorization_code",
            "redirect_uri": "https://wortschatz.cz/notion/callback",
            "code": code,
        },
        auth=("fce9c87e-3860-47c6-b9a6-65ffc789a2b8", NOTION_SECRET),
    )

    return response.json()


@app.post("/notion")
async def notion_api(url: str) -> StreamingResponse:
    request = client.build_request(
        "POST", url, headers={"Notion-Version": "2022-02-22"}
    )
    response = await client.send(request, stream=True)
    return StreamingResponse(response.aiter_text(), background=response.aclose)


@app.exception_handler(404)
async def index(_, __) -> FileResponse:
    return FileResponse(f"{DIST_FOLDER}/index.html")


app.mount("/", StaticFiles(directory=DIST_FOLDER))
