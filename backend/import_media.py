from backend.database import SessionLocal
from backend.models import Artist, Album, ReleaseType

session = SessionLocal()

# artist = Artist(
#     name = "Rammstein"
# )
# session.add(artist)
# session.commit()
# # session.close()
# print(artist.id)

# artist = session.query(Artist).filter_by(name="Rammstein").first()

# album = Album(
#     title = 'Rammstein_2019',
#     year = 2019,
#     cover_path = "media\covers\rammstein\rammstein_2019.jpg",
#     artist = artist
# )
artist = Artist(
    name="Anna-Maria Zimmermann"
)

session.add(artist)
session.commit()

print(artist.id)

album = Album(
    title="Bauchgefühl",
    year=2015,
    cover_path="media/covers/Anna-Maria Zimmermann/Bauchgefühl/Bauchgefühl.jpg",
    release_type=ReleaseType.ALBUM,
    artist=artist
)

session.add(album)
session.commit()

print(album.id)
print(album.artist_id)
print(album.artist.name)
print(artist.albums)
session.close()