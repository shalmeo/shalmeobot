from sqlalchemy.engine import URL

from tgbot.config import DbConfig


def get_connection_string(db: DbConfig):
    # return f"postgresql+asyncpg://{db.login}:{db.password}@{db.host}:{db.port}/{db.name}"
    return URL.create(
                drivername="postgresql+asyncpg",
                username=db.login,
                password=db.password,
                host=db.host,
                port=db.port,
                database=db.name,
            )