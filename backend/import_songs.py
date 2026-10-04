from pathlib import Path

from backend.database import SessionLocal
from backend.models import Album, Artist, Song


SONGS = [
    ("Rammstein", "Rammstein", "Deutschland", 1, 322, "media/songs/Rammstein/Rammstein_2019/01_Deutschland.mp3"),
    ("Rammstein", "Rammstein", "Radio", 2, 277, "media/songs/Rammstein/Rammstein_2019/02_Radio.mp3"),
    ("Rammstein", "Rammstein", "Zeig dich", 3, 256, "media/songs/Rammstein/Rammstein_2019/03_Zeig_Dich.mp3"),
    ("Rammstein", "Rammstein", "Ausländer", 4, 230, "media/songs/Rammstein/Rammstein_2019/04_Ausländer.mp3"),
    ("Rammstein", "Rammstein", "Sex", 5, 237, "media/songs/Rammstein/Rammstein_2019/05_Sex.mp3"),
    ("Rammstein", "Rammstein", "Puppe", 6, 274, "media/songs/Rammstein/Rammstein_2019/06_Puppe.mp3"),
    ("Rammstein", "Rammstein", "Was ich liebe", 7, 269, "media/songs/Rammstein/Rammstein_2019/07_Was_ich_liebe.mp3"),
    ("Rammstein", "Rammstein", "Diamant", 8, 154, "media/songs/Rammstein/Rammstein_2019/08_Diamant.mp3"),
    ("Rammstein", "Rammstein", "Weit weg", 9, 261, "media/songs/Rammstein/Rammstein_2019/09_Weit_weg.mp3"),
    ("Rammstein", "Rammstein", "Tattoo", 10, 252, "media/songs/Rammstein/Rammstein_2019/10_Tattoo.mp3"),
    ("Rammstein", "Rammstein", "Hallomann", 11, 252, "media/songs/Rammstein/Rammstein_2019/11_Hallomann.mp3"),
    ("Rammstein", "Herzeleid", "Wollt Ihr Das Bett In Flammen Sehen", 1, 320, "media/songs/Rammstein/Herzeleid/01_Wollt_Ihr_Das_Bett_In_Flammen_Sehen.mp3"),
    ("Rammstein", "Herzeleid", "Der Meister", 2, 249, "media/songs/Rammstein/Herzeleid/02_Der_Meister.mp3"),
    ("Rammstein", "Herzeleid", "Weisses Fleisch", 3, 216, "media/songs/Rammstein/Herzeleid/03_Weisses_Fleisch.mp3"),
    ("Rammstein", "Herzeleid", "Asche zu Asche", 4, 231, "media/songs/Rammstein/Herzeleid/04_Asche_zu_Asche.mp3"),
    ("Rammstein", "Herzeleid", "Seemann", 5, 288, "media/songs/Rammstein/Herzeleid/05_Seemann.mp3"),
    ("Rammstein", "Herzeleid", "Du Riechst So Gut", 6, 290, "media/songs/Rammstein/Herzeleid/06_Du_Riechst_So_Gut.mp3"),
    ("Rammstein", "Herzeleid", "Das Alte Leid", 7, 344, "media/songs/Rammstein/Herzeleid/07_Das_Alte_Leid.mp3"),
    ("Rammstein", "Herzeleid", "Heirate Mich", 8, 285, "media/songs/Rammstein/Herzeleid/08_Heirate_Mich.mp3"),
    ("Rammstein", "Herzeleid", "Herzeleid", 9, 225, "media/songs/Rammstein/Herzeleid/09_Herzeleid.mp3"),
    ("Rammstein", "Herzeleid", "Laichzeit", 10, 263, "media/songs/Rammstein/Herzeleid/10_Laichzeit.mp3"),
    ("Rammstein", "Herzeleid", "Rammstein", 11, 266, "media/songs/Rammstein/Herzeleid/11_Rammstein.mp3"),
    ("Rammstein", "Liebe ist für alle da", "FÜHRE MICH", 12, 273, "media/songs/Rammstein/Liebe ist für alle da/12_FÜHRE_MICH.mp3"),
    ("Rammstein", "Liebe ist für alle da", "DONAUKINDER", 13, 318, "media/songs/Rammstein/Liebe ist für alle da/13_DONAUKINDER.mp3"),
    ("Rammstein", "Liebe ist für alle da", "HALT", 14, 261, "media/songs/Rammstein/Liebe ist für alle da/14_HALT.mp3"),
    ("Rammstein", "Liebe ist für alle da", "ROTER SAND ORCHESTER VERSION", 15, 245, "media/songs/Rammstein/Liebe ist für alle da/15_ROTER_SAND_ORCHESTER_VERSION.mp3"),
    ("Rammstein", "Liebe ist für alle da", "LIESE", 16, 236, "media/songs/Rammstein/Liebe ist für alle da/16_LIESE.mp3"),
    ("Anna-Maria Zimmermann", "Bauchgefühl", "Nur noch einmal schlafen", 14, 179, "media/songs/Anna-Maria Zimmermann/Bauchgefühl/14_Nur noch einmal schlafen.mp3"),
    ("Sturmmann", "Taiga", "Taiga", 1, 221, "media/songs/Sturmmann/Taiga.mp3"),
    ("Reinhard Mey", "Flaschenpost", "Das Narrenschiff", 1, 416, "media/songs/Reinhard Mey/Flaschenpost/Das Narrenschiff.mp3"),
    ("Nnd", "Dachlatte", "Dachlatte", 1, 200, "media/songs/Nnd/Dachlatte/Dachlatte.mp3"),
]


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    session = SessionLocal()
    try:
        imported = 0
        missing_albums = set()
        for artist_name, album_title, title, track_number, duration, audio_path in SONGS:
            album = (
                session.query(Album)
                .join(Artist)
                .filter(Artist.name == artist_name, Album.title == album_title)
                .first()
            )
            if album is None:
                missing_albums.add((artist_name, album_title))
                continue

            song = (
                session.query(Song)
                .filter_by(album_id=album.id, track_number=track_number)
                .first()
            )
            if song is None:
                song = Song(album_id=album.id, track_number=track_number)
                session.add(song)

            song.title = title
            song.duration_seconds = duration
            song.audio_path = audio_path
            imported += 1

        if missing_albums:
            names = ", ".join(f"{artist}: {title}" for artist, title in sorted(missing_albums))
            raise RuntimeError(f"Run import_media.py first; missing albums: {names}")

        missing_files = [
            audio_path
            for *_, audio_path in SONGS
            if not (project_root / audio_path).is_file()
        ]
        if missing_files:
            print(f"Warning: {len(missing_files)} historical audio files are missing locally.")

        session.commit()
        print(f"Imported or updated {imported} historical songs.")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()