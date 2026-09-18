from fastapi import FastAPI, HTTPException
import logging

from backend.database import SessionLocal
from backend.models import Artist, Song, Album, Lyrics, ReleaseType
from backend.init_db import init_db

from pydantic import BaseModel

from fastapi.responses import FileResponse

####### для фронта
from fastapi.staticfiles import StaticFiles
#######

class SongResponse(BaseModel):
    id: int
    title: str
    track_number: int
    duration_seconds: int
    album_id: int
    release_type: ReleaseType
    artist_name: str
    album_cover_path: str | None

class AlbumResponse(BaseModel):
    id: int
    title: str
    year: int
    cover_path: str | None
    artist_id: int
    release_type: ReleaseType
    songs: list[SongResponse]


class ReleaseSummary(BaseModel):
    id: int
    title: str
    year: int
    cover_path: str | None
    artist_id: int
    release_type: ReleaseType


class ArtistResponse(BaseModel):
    id: int
    name: str
    biography: str | None
    country: str | None
    image_path: str | None
    website: str | None
    releases: list[ReleaseSummary]


class LyricsLine(BaseModel):
    original: str
    translation: str


class LyricsResponse(BaseModel):
    song_id: int
    lyrics: list[LyricsLine]

app = FastAPI()
app.mount(
    "/frontend", 
    StaticFiles(directory="frontend"), 
    name="frontend"
    )
app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)

@app.on_event("startup")
def on_startup() -> None:
    try:
        init_db()
        logging.info("Database initialized via init_db.init_db()")
    except Exception as exc:
        logging.exception("Failed to initialize database tables: %s", exc)

@app.get("/song")
def song_page():
    return FileResponse("frontend/song.html")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

@app.get("/songs")
def get_songs():
    db = SessionLocal()
    try:
        songs = (
            db.query(Song)
            .order_by(Song.track_number)
            .all()
        )
        return [
            {
                "id": song.id,
                "title": song.title,
                "track_number": song.track_number,
                "duration_seconds": song.duration_seconds,
                "album_id": song.album_id,
                "release_type": song.album.release_type,
                "artist_name": song.album.artist.name,
                "album_cover_path": song.album.cover_path,
            }
            for song in songs
        ]
    finally:
        db.close()

@app.get("/albums")
def get_albums():
    db = SessionLocal()
    try:
        albums = db.query(Album).filter(Album.release_type == ReleaseType.ALBUM).all()
        return [
            {
                "id": album.id,
                "title": album.title,
                "year": album.year,
                "cover_path": album.cover_path,
                "artist_id": album.artist_id,
                "release_type": album.release_type,
            }
            for album in albums
        ]
    finally:
        db.close()


@app.get("/releases", response_model=list[ReleaseSummary])
def get_releases(release_type: ReleaseType | None = None):
    db = SessionLocal()
    try:
        query = db.query(Album)
        if release_type is not None:
            query = query.filter(Album.release_type == release_type)
        return [
            ReleaseSummary(
                id=release.id,
                title=release.title,
                year=release.year,
                cover_path=release.cover_path,
                artist_id=release.artist_id,
                release_type=release.release_type,
            )
            for release in query.order_by(Album.year.desc(), Album.title).all()
        ]
    finally:
        db.close()


@app.get("/releases/{release_id}", response_model=AlbumResponse)
def get_release(release_id: int):
    db = SessionLocal()
    try:
        release = db.query(Album).filter(Album.id == release_id).first()
        if release is None:
            raise HTTPException(status_code=404, detail="Release not found")
        return AlbumResponse(
            id=release.id,
            title=release.title,
            year=release.year,
            artist_id=release.artist_id,
            cover_path=release.cover_path,
            release_type=release.release_type,
            songs=[
                SongResponse(
                    id=song.id,
                    title=song.title,
                    track_number=song.track_number,
                    duration_seconds=song.duration_seconds,
                    album_id=song.album_id,
                    release_type=release.release_type,
                    artist_name=release.artist.name,
                    album_cover_path=release.cover_path,
                )
                for song in release.songs
            ],
        )
    finally:
        db.close()


@app.get("/artists", response_model=list[ArtistResponse])
def get_artists():
    db = SessionLocal()
    try:
        return [
            ArtistResponse(
                id=artist.id,
                name=artist.name,
                biography=artist.biography,
                country=artist.country,
                image_path=artist.image_path,
                website=artist.website,
                releases=[
                    ReleaseSummary(
                        id=release.id,
                        title=release.title,
                        year=release.year,
                        cover_path=release.cover_path,
                        artist_id=release.artist_id,
                        release_type=release.release_type,
                    )
                    for release in artist.albums
                ],
            )
            for artist in db.query(Artist).order_by(Artist.name).all()
        ]
    finally:
        db.close()


@app.get("/artists/{artist_id}", response_model=ArtistResponse)
def get_artist(artist_id: int):
    db = SessionLocal()
    try:
        artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if artist is None:
            raise HTTPException(status_code=404, detail="Artist not found")
        return ArtistResponse(
            id=artist.id,
            name=artist.name,
            biography=artist.biography,
            country=artist.country,
            image_path=artist.image_path,
            website=artist.website,
            releases=[
                ReleaseSummary(
                    id=release.id,
                    title=release.title,
                    year=release.year,
                    cover_path=release.cover_path,
                    artist_id=release.artist_id,
                    release_type=release.release_type,
                )
                for release in artist.albums
            ],
        )
    finally:
        db.close()

@app.get("/albums/{album_id}", response_model=AlbumResponse)
def get_album(album_id: int):
    db = SessionLocal()
    try:
        album = db.query(Album).filter(
            Album.id == album_id,
            Album.release_type == ReleaseType.ALBUM,
        ).first()
        if album is None:
            raise HTTPException(status_code=404, detail="Album not found")
        return AlbumResponse(
            id=album.id,
            title=album.title,
            year=album.year,
            artist_id=album.artist_id,
            cover_path=album.cover_path,
            release_type=album.release_type,
            songs=[
                SongResponse(
                    id=song.id,
                    title=song.title,
                    track_number=song.track_number,
                    duration_seconds=song.duration_seconds,
                    album_id=song.album_id,
                    release_type=album.release_type,
                    artist_name=album.artist.name,
                    album_cover_path=album.cover_path,
                )
                for song in album.songs
            ]
        )
    finally:
        db.close() 

@app.get("/songs/{song_id}/lyrics", response_model=LyricsResponse)
def get_song_lyrics(song_id: int):
    db = SessionLocal()
    try:
        lyrics = db.query(Lyrics).filter(Lyrics.song_id == song_id).first()
        if lyrics is None:
            raise HTTPException(status_code=404, detail="Lyrics not found")

        original_lines = lyrics.original_text.splitlines()
        translated_lines = lyrics.translated_text.splitlines()
        line_count = max(len(original_lines), len(translated_lines))

        return LyricsResponse(
            song_id=lyrics.song_id,
            lyrics=[
                LyricsLine(
                    original=original_lines[index] if index < len(original_lines) else "",
                    translation=(
                        translated_lines[index]
                        if index < len(translated_lines)
                        else ""
                    ),
                )
                for index in range(line_count)
            ],
        )
    finally:
        db.close()

@app.get("/songs/{song_id}", response_model=SongResponse)
def get_song(song_id: int):
    db = SessionLocal()
    try:
        song = db.query(Song).filter(Song.id == song_id).first()
        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")
        return SongResponse(
            id=song.id,
            title=song.title,
            track_number=song.track_number,
            duration_seconds=song.duration_seconds,
            album_id=song.album_id,
            release_type=song.album.release_type,
            artist_name=song.album.artist.name,
            album_cover_path=song.album.cover_path,
        )
    finally:
        db.close()

# передача мп3 файла браузеру
@app.get("/songs/{song_id}/audio")
def get_song_audio(song_id: int):
    db = SessionLocal()
    try:
        song = db.query(Song).filter(Song.id == song_id).first()
        if song is None:
            raise HTTPException(status_code=404, detail="Song not found")
        return FileResponse(
            song.audio_path,
            media_type="audio/mpeg",
            content_disposition_type="inline",
        )
    finally:
        db.close()