from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Message": "Meu hub de Games está vivo!"}


class GameResponse(BaseModel):
    id: str
    title: str
    usd_price: float | None
    image: str | None


@app.get("/api/games", response_model=list[GameResponse])
def read_games(name: str):
    url = f"https://www.cheapshark.com/api/1.0/games?title={name}"
    response = requests.get(url)

    game_data = response.json()

    if not game_data:
        raise HTTPException(status_code=404, detail="Game not found.")

    data = []

    for g in game_data:
        if not g.get("gameID") or not g.get("external"):
            continue
        data.append({
            "id": g.get("gameID"),
            "title": g.get("external"),
            "usd_price": float(g["cheapest"]) if g.get("cheapest") else None,
            "image": g.get("thumb"),
        })

    return data