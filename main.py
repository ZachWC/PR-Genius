from fastapi import FastAPI, Request, Header

app = FastAPI()

@app.get("/")
def home():
    return {"status": "alive"}

@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(None),
):
    body = await request.body()
    print(f"Got an event of type: {x_github_event}")
    print(f"Raw body was {len(body)} bytes") ## returns num of bytes in payload
    return {"ok": True}
