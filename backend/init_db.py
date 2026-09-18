from sqlalchemy import inspect, text

from backend.database import engine, Base


def _add_column_if_missing(table_name: str, column_name: str, definition: str) -> None:
    inspector = inspect(engine)
    columns = {column["name"] for column in inspector.get_columns(table_name)}
    if column_name not in columns:
        with engine.begin() as connection:
            connection.execute(
                text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")
            )

def init_db() -> None:
    # Import models to ensure they are registered with Base.metadata
    import backend.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    for column_name, definition in (
        ("biography", "TEXT"),
        ("country", "VARCHAR(100)"),
        ("image_path", "VARCHAR(255)"),
        ("website", "VARCHAR(255)"),
    ):
        _add_column_if_missing("artists", column_name, definition)
    _add_column_if_missing(
        "albums",
        "release_type",
        "VARCHAR(20) NOT NULL DEFAULT 'album'",
    )
