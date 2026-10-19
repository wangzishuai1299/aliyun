from  app.settings import settings
from sqlalchemy import String, Integer, DateTime, create_engine, func, select,ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker,Session,relationship,selectinload
from datetime import datetime

engine = create_engine(settings.DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    sort : Mapped[str] = mapped_column(String(255), index=True)
    star: Mapped[str] = mapped_column(String(255), index=True)
    start_time : Mapped[str] = mapped_column(String(255), index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




    

    