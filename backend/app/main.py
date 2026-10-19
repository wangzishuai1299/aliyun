from typing import Annotated,Optional
from datetime import datetime
from fastapi import Depends, FastAPI, Query, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker,Session,selectinload
from sqlalchemy import String, Integer, DateTime, create_engine, func, select
from app.database import get_db, Movie
from app.settings import settings
from fastapi.responses import JSONResponse

def get_settings():
    return settings.TITLE

def pagation(page: int = 1, page_size: int = 10):
    return {"page": page, "page_size": page_size}

class MovieCreate(BaseModel):
    title: str
    sort: str
    star: str
    start_time:str

class MovieUpdate(BaseModel):
    title:str | None=None
    sort:str | None=None
    star:str | None=None
    start_time:str | None=None

class  MovieRead(BaseModel):
    id: int
    title: str
    sort: str
    star: str
    start_time: str
    model_config = ConfigDict(from_attributes=True)

class MoviePage(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[MovieRead]

class  MovieService:
    @staticmethod
    def create_movie(movie: MovieCreate,db: Session):
        db_movie = Movie(**movie.dict())
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    @staticmethod
    def get_movies(db: Session, page,page_size,keywords:str=None):
        stmt=select(Movie)
        if keywords:
            stmt=stmt.where(Movie.title.contains(keywords))
        total=db.scalar(select(func.count(Movie.id)).select_from(stmt.subquery()))
        offset=(page-1)*page_size
        stmt=stmt.limit(page_size).offset(offset)
        items=db.scalars(stmt).all()
        return total,items
    @staticmethod
    def get_movie(id:int,db:Session):
        return db.scalars(select(Movie).where(Movie.id==id)).first()
    @staticmethod
    def update_movie(id:int,movie:MovieUpdate,db:Session):
        db_movie=db.get(Movie,id)
        if db_movie:
            for key,value in movie.dict(exclude_unset=True).items():
                setattr(db_movie,key,value)
            db.commit()
            db.refresh(db_movie)
            return db_movie
        else:
            raise HTTPException(status_code=404,detail="Movie not found")
        
    @staticmethod
    def delete_movie(id:int,db:Session):
        db_movie=db.get(Movie,id)
        if db_movie:
            db.delete(db_movie)
            db.commit()
            return db_movie
        else:
            raise HTTPException(status_code=404,detail="Movie not found")

app=FastAPI(title="get_settings")
@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie:MovieCreate,db:Session=Depends(get_db)):
    return MovieService.create_movie(movie=movie,db=db)

@app.get("/movies",response_model=MoviePage)
def get_movies(
    db=Depends(get_db),
    page_info=Depends(pagation),
    keywords:Annotated[str| None,'']=None

):
    page=page_info['page']
    page_size=page_info['page_size']
    total,items=MovieService.get_movies(db=db,page=page,page_size=page_size,keywords=keywords)
    return MoviePage(page=page,page_size=page_size,total=total,items=items)

@app.get("/movies/{id}")
def get_movie(id:int,db:Session=Depends(get_db)):
    return MovieService.get_movie(id=id,db=db)

@app.put("/movies/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_movie(id:int,movie:MovieUpdate,db:Session=Depends(get_db)):
    return MovieService.update_movie(id=id,movie=movie,db=db)
        
@app.delete("/movies/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id:int,db:Session=Depends(get_db)):
    return MovieService.delete_movie(id=id,db=db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)


        

