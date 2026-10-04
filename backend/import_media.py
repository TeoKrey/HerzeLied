from backend.database import SessionLocal
from backend.models import Album, Artist, ReleaseType


ALBUMS = [
    ("Rammstein", "Rammstein", 2019, "media/covers/rammstein/rammstein_2019.jpg"),
    (
        "Anna-Maria Zimmermann",
        "Bauchgefühl",
        2015,
        "media/covers/Anna-Maria Zimmermann/Bauchgefühl/Bauchgefühl.jpg",
    ),
    ("Sturmmann", "Taiga", 2026, "media/covers/Sturmmann/Taiga/Taiga.png"),
    (
        "Reinhard Mey",
        "Flaschenpost",
        1991,
        "media/covers/Reinhard Mey/Flaschenpost/Flaschenpost.png",
    ),
    ("Nnd", "Dachlatte", 2026, "media/covers/Nnd/Dachlatte/Dachlatte.jpg"),
    (
        "Rammstein",
        "Herzeleid",
        1995,
        "media/covers/rammstein/Herzeleid/Herzeleid.jpg",
    ),
    (
        "Rammstein",
        "Liebe ist für alle da",
        2009,
        "media/covers/rammstein/Liebe ist für alle da.jpg",
    ),
]


def main() -> None:
    session = SessionLocal()
    try:
        for artist_name, title, year, cover_path in ALBUMS:
            artist = session.query(Artist).filter_by(name=artist_name).first()
            if artist is None:
                artist = Artist(name=artist_name)
                session.add(artist)
                session.flush()

            album = (
                session.query(Album)
                .filter_by(artist_id=artist.id, title=title)
                .first()
            )
            if album is None:
                album = Album(
                    artist_id=artist.id,
                    title=title,
                    year=year,
                    cover_path=cover_path,
                    release_type=ReleaseType.ALBUM,
                )
                session.add(album)
            else:
                album.year = year
                album.cover_path = cover_path
                album.release_type = ReleaseType.ALBUM

        session.commit()
        print(f"Imported or updated {len(ALBUMS)} historical albums.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()