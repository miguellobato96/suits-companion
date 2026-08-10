from sqlalchemy import text

from app.core.database import engine


def main() -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar_one()

    print(f"Database connection OK: {value}")


if __name__ == "__main__":
    main()
