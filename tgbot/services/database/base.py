from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, TIMESTAMP, func

Base = declarative_base()

class TimedBaseModel(Base):
    __abstract__ = True

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True),
                        default=func.now(),
                        onupdate=func.now(),
                        server_default=func.now())