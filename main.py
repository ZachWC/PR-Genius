from fastapi import FastAPI, Request, Header
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

app = FastAPI()

REVIEWABLE_ACTIONS = ("opened", "synchronize", "reopened")


@app.get("/")
def home():
    """Return service health status"""
    return {"status": "alive"}


@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(None),
):
    """Accept and acknowledge Github webhook POST requests"""
    body = await request.body()
    payload = json.loads(body)

    action = payload.get("action")
    print(f"Event: {x_github_event}, action: {action}")

    if x_github_event == "pull_request" and action in REVIEWABLE_ACTIONS:
        pr_number = payload.get("number")
        print(f"--> Reviewing PR #{pr_number}")
    else:
        print("--> Ignoring this event")

    return {"ok": True}


async def fetch_pr_diff(
    repo_full_name,
    pr_number
):

    url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
    
    return response.text