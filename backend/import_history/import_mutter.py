from pathlib import Path

from backend.database import SessionLocal
from backend.models import Album, Artist, Lyrics, ReleaseType, Song


TRACKS = [
    ("Mein Herz brennt", 1, 279, "01_Mein_Herz_brennt"),
    ("Links 2 3 4", 2, 216, "02_Links_2_3_4"),
    ("Sonne", 3, 272, "03_Sonne"),
    ("Ich will", 4, 217, "04_Ich_will"),
    ("Feuer frei", 5, 188, "05_Feuer_frei"),
    ("Mutter", 6, 268, "06_Mutter"),
    ("Spieluhr", 7, 286, "07_Spieluhr"),
    ("Zwitter", 8, 257, "08_Zwitter"),
    ("Rein raus", 9, 189, "09_Rein_raus"),
    ("Adios", 10, 228, "10_Adios"),
    ("Nebel", 11, 294, "11_Nebel"),
]


def parse_lyrics(text: str) -> tuple[str, str]:
    if "[TRANSLATION]" in text:
        original_text, translated_text = text.split("[TRANSLATION]", 1)
    else:
        original_text, translated_text = text, ""
    return original_text.replace("[ORIGINAL]", "").strip(), translated_text.strip()


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    songs_dir = project_root / "media" / "songs" / "Rammstein" / "Mutter"
    lyrics_dir = project_root / "media" / "lyrics" / "Rammstein" / "Mutter"
    cover_path = "media/covers/rammstein/Mutter.png"
    cover_file = project_root / cover_path

    if not cover_file.is_file():
        raise FileNotFoundError(cover_file)

    session = SessionLocal()
    try:
        with session.begin():
            artist = session.query(Artist).filter_by(name="Rammstein").first()
            if artist is None:
                artist = Artist(name="Rammstein")
                session.add(artist)
                session.flush()

            album = (
                session.query(Album)
                .filter_by(artist_id=artist.id, title="Mutter")
                .first()
            )
            if album is None:
                album = Album(
                    title="Mutter",
                    year=2001,
                    cover_path=cover_path,
                    release_type=ReleaseType.ALBUM,
                    artist_id=artist.id,
                )
                session.add(album)
                session.flush()
            else:
                album.year = 2001
                album.cover_path = cover_path
                album.release_type = ReleaseType.ALBUM

            for title, track_number, duration, filename in TRACKS:
                audio_path = f"media/songs/Rammstein/Mutter/{filename}.mp3"
                lyrics_path = lyrics_dir / f"{filename}.txt"
                audio_file = project_root / audio_path
                if not audio_file.is_file():
                    raise FileNotFoundError(audio_file)
                if not lyrics_path.is_file():
                    raise FileNotFoundError(lyrics_path)

                song = (
                    session.query(Song)
                    .filter_by(album_id=album.id, track_number=track_number)
                    .first()
                )
                if song is None:
                    song = Song(
                        title=title,
                        track_number=track_number,
                        duration_seconds=duration,
                        audio_path=audio_path,
                        album_id=album.id,
                    )
                    session.add(song)

                song.title = title
                song.duration_seconds = duration
                song.audio_path = audio_path
                session.flush()

                original_text, translated_text = parse_lyrics(
                    lyrics_path.read_text(encoding="utf-8")
                )
                lyrics = session.query(Lyrics).filter_by(song_id=song.id).first()
                if lyrics is None:
                    lyrics = Lyrics(song_id=song.id)
                    session.add(lyrics)
                lyrics.original_text = original_text
                lyrics.translated_text = translated_text

        print(f"Imported album Mutter with {len(TRACKS)} songs and lyrics.")
    finally:
        session.close()


if __name__ == "__main__":
    main()