from pathlib import Path

from backend.database import SessionLocal
from backend.models import Artist, Lyrics, Song


def parse_lyrics(text: str) -> tuple[str, str]:
    if "[TRANSLATION]" in text:
        original_text, translated_text = text.split("[TRANSLATION]", 1)
    else:
        original_text, translated_text = text, ""
    return original_text.replace("[ORIGINAL]", "").strip(), translated_text.strip()


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    lyrics_root = project_root / "media" / "lyrics"
    session = SessionLocal()
    try:
        imported = 0
        skipped = []
        seen_song_ids = set()

        for file_path in sorted(lyrics_root.rglob("*.txt")):
            relative_path = file_path.relative_to(lyrics_root)
            if len(relative_path.parts) >= 2 and relative_path.parts[:2] == ("Rammstein", "Mutter"):
                continue

            title = file_path.stem
            prefix, separator, remainder = title.partition("_")
            if separator and prefix.isdigit():
                title = remainder
            title = title.replace("_", " ").casefold()
            artist_name = relative_path.parts[0]

            song = (
                session.query(Song)
                .join(Song.album)
                .join(Song.album.property.mapper.class_.artist)
                .filter(Artist.name == artist_name)
                .all()
            )
            song = next((item for item in song if item.title.casefold() == title), None)
            if song is None:
                skipped.append(str(relative_path))
                continue
            if song.id in seen_song_ids:
                continue
            seen_song_ids.add(song.id)

            original_text, translated_text = parse_lyrics(
                file_path.read_text(encoding="utf-8")
            )
            lyrics = session.query(Lyrics).filter_by(song_id=song.id).first()
            if lyrics is None:
                lyrics = Lyrics(song_id=song.id)
                session.add(lyrics)
            lyrics.original_text = original_text
            lyrics.translated_text = translated_text
            imported += 1

        session.commit()
        print(f"Imported or updated lyrics for {imported} historical songs.")
        if skipped:
            print(f"Skipped {len(skipped)} lyric files without a matching song.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
