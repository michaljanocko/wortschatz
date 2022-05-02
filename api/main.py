import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx


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
            auth=(
                "fce9c87e-3860-47c6-b9a6-65ffc789a2b8",
                os.getenv("NOTION_SECRET"),
            ),
        )

        return response.json()


@app.get("/")
async def index() -> FileResponse:
    return FileResponse("/dist/index.html")


app.mount("/", StaticFiles(directory="/dist"))
