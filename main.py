from src.database.connection import init_db, seed_db
from src.interface.app import init_app


if __name__ == "__main__":
    init_db()
    seed_db()
    init_app()