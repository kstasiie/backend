from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from music_catalog import (
    add_song,
    update_song,
    delete_song,
    delete_artist,
    delete_album,
    search_tracks,
    get_album_details,
    get_artist_albums
)

app = FastAPI(
    title="Музыкальный каталог API",
    description="API для управления музыкальной коллекцией",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # или ["http://localhost:3000"] для конкретного фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=PlainTextResponse)  # Явно указываем тип ответа
async def root():
    return "Добро пожаловать в API музыкального каталога"

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return ""  # Пустой ответ с кодом 204 (автоматически)

# Основные эндпоинты API

@app.post("/songs", status_code=201)
async def create_song(artist: str, title: str, genre: str = None, album: str = None, year: int = None):
    """Добавление новой песни в каталог"""
    try:
        add_song(artist, title, genre, album, year)
        return {"message": "Песня успешно добавлена"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при добавлении песни: {str(e)}")

@app.get("/search")
async def search(query: str):
    """Поиск песен по запросу"""
    results = search_tracks(query)
    if not results:
        return {"message": "Ничего не найдено", "results": []}
    return {"results": results}

@app.put("/songs/{song_title}")
async def update_song_route(
    song_title: str,
    new_title: str = None,
    new_artist: str = None,
    new_genre: str = None,
    new_album: str = None,
    new_year: int = None
):
    """Обновление информации о песне"""
    success = update_song(song_title, new_title, new_artist, new_genre, new_album, new_year)
    if not success:
        raise HTTPException(status_code=404, detail="Песня не найдена или не удалось обновить")
    return {"message": "Песня успешно обновлена"}

@app.delete("/songs/{song_title}")
async def delete_song_route(song_title: str):
    """Удаление песни из каталога"""
    delete_song(song_title)
    return {"message": "Песня успешно удалена"}

@app.get("/albums/{album_name}")
async def get_album(album_name: str):
    """Получение информации об альбоме"""
    album_details = get_album_details(album_name)
    if not album_details:
        raise HTTPException(status_code=404, detail="Альбом не найден")
    return album_details

@app.get("/artists/{artist_name}/albums")
async def get_albums_by_artist(artist_name: str):
    """Получение альбомов исполнителя"""
    albums = get_artist_albums(artist_name)
    if not albums:
        raise HTTPException(status_code=404, detail="Исполнитель не найден или нет альбомов")
    return {"albums": albums}

@app.delete("/artists/{artist_name}")
async def delete_artist_route(artist_name: str):
    """Удаление исполнителя и всех связанных данных"""
    delete_artist(artist_name)
    return {"message": "Исполнитель и все связанные данные успешно удалены"}

@app.delete("/albums/{album_name}")
async def delete_album_route(album_name: str):
    """Удаление альбома"""
    delete_album(album_name)
    return {"message": "Альбом успешно удален"}