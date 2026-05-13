from app import character_models
from app.database import Base, engine


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


if __name__ == "__main__":
    main()