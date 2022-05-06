import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
import httpx

DIST_FOLDER = os.getenv("DIST_FOLDER")
NOTION_SECRET = os.getenv("NOTION_SECRET")

app = FastAPI()


@app.get("/api/token")
async def token(code: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.notion.com/v1/oauth/token",
            json={
                "grant_type": "authorization_code",
                "redirect_uri": "https://wortschatz.cz/notion/callback",
                "code": code,
            },
            auth=("fce9c87e-3860-47c6-b9a6-65ffc789a2b8", NOTION_SECRET),
        )

        return response.json()


@app.exception_handler(404)
async def index(_, __) -> FileResponse:
    return FileResponse(f"{DIST_FOLDER}/index.html")


app.mount("/", StaticFiles(directory=DIST_FOLDER))
