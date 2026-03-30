import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

OLLAMA_URL = "http://localhost:11434"
MODEL = "mistral:7b-instruct-q4_0"


class GenerateRequest(BaseModel):
    prompt: str


class ChatRequest(BaseModel):
    messages: list[dict]


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL}


@app.post("/generate")
async def generate(request: GenerateRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": request.prompt, "stream": False},
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    data = response.json()
    return {"response": data.get("response")}


@app.post("/chat")
async def chat(request: ChatRequest):
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": request.messages, "stream": False},
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    data = response.json()
    return {"response": data.get("message", {}).get("content")}
