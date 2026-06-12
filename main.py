from fastapi import FastAPI, Request, Header
import json

app = FastAPI()

# PR actions we want to review
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
    payload = json.loads(body) # parses body

    action = payload.get("action") # None if absent
    print(f"Event: {x_github_event}, action: {action}")

    if x_github_event == "pull_request" and action in REVIEWABLE_ACTIONS:
        pr_number = payload.get("number")
        print(f"--> Reviewing PR #{pr_number}")
    else:
        print("--> Ignoring this event")
   
    return {"ok": True}
