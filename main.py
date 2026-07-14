from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

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
    title: str
    usd_price: float | None
    image: str | None


@app.get("/api/games", response_model=GameResponse)
def read_games(name: str):
    url = f"https://www.cheapshark.com/api/1.0/games?title={name}"
    response = requests.get(url)

    game_data = response.json()
    if not game_data:
       raise HTTPException(status_code=404, detail="Game not found.")
    
    first_game = game_data[0] 

    if not first_game["external"]:
        raise HTTPException(status_code=502, detail="Title is Missing.")

    cleaned_data = {
        "title": first_game.get("external"),
        "usd_price": first_game.get("cheapest", None),
        "image": first_game.get("thumb", None)

    }
    return cleaned_data