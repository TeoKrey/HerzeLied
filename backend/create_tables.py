from backend.init_db import init_db

def main() -> None:
    init_db()
    print("Database tables created (or already existed).")


if __name__ == "__main__":
    main()
