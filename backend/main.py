from typing import Annotated,Optional
from datetime import datetime
from fastapi import Depends, FastAPI, Query, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker,Session,selectinload
from sqlalchemy import String, Integer, DateTime, create_engine, func, select
from app.database import get_db, Memo
from app.settings import settings
from fastapi.responses import JSONResponse

def get_settings():
    return settings.TITLE

def pagation(page: int = 1, page_size: int = 10):
    return {"page": page, "page_size": page_size}

class MemoCreate(BaseModel):
    title: str
    sort: str
    body: str

class MemoUpdate(BaseModel):
    title: str | None
    sort: str | None
    body: str | None

class MemoRead(BaseModel):
    id: int
    title: str
    sort: str
    body: str
    model_config = ConfigDict(from_attributes=True)

class MemoPage(BaseModel):
    page: int
    page_size: int
    total: int
    items: list[MemoRead]

class MemoService:
    @staticmethod
    def create_memo(db: Session, memo: MemoCreate):
        db_memo = Memo(**memo.dict())
        db.add(db_memo)
        db.commit()
        db.refresh(db_memo)
        return db_memo

    @staticmethod
    def get_memos(page,page_size,db: Session,keywords: str = None):
        stmt=select(Memo)
        if keywords:
            stmt=stmt.where(Memo.title.contains(keywords))
        # total= db.query(func.count(Memo.id)).scalar()
        total=db.scalar(select(func.count(Memo.id)).select_from(stmt.subquery()))

        offset=(page-1)*page_size
        stmt=stmt.limit(page_size).offset(offset)
        items=db.scalars(stmt).all()
        return total,items

    @staticmethod
    def get_memo(db: Session, memo_id: int):
        # return db.query(Memo).filter(Memo.id == memo_id).first()
        return db.scalars(select(Memo).where(Memo.id == memo_id)).first()
    @staticmethod
    def update_memo(db: Session, memo_id: int, memo: MemoUpdate):
        db_memo=db.get(Memo,memo_id)
        if db_memo:
            for key,value in memo.dict(exclude_unset=True).items():
                setattr(db_memo,key,value)
            db.commit()
            db.refresh(db_memo)
            return db_memo
        else:
            raise HTTPException(status_code=404,detail="Memo not found")
        
    @staticmethod
    def delete_memo(db: Session, memo_id: int):
        db_memo=db.get(Memo,memo_id)
        if db_memo:
            db.delete(db_memo)
            db.commit()
            return db_memo
        else:
            raise HTTPException(status_code=404,detail="Memo not found")

app=FastAPI(title=get_settings())

@app.post("/memos",status_code=201)
def create_memo(memo: MemoCreate,db: Session = Depends(get_db)):
    return MemoService.create_memo(db=db,memo=memo)

@app.get("/memos")
def get_all_memos(
    db: Session = Depends(get_db),
    pageinfo=Depends(pagation),
    keywords: Annotated[str| None,'']=None
):
    page=pageinfo['page']
    page_size=pageinfo['page_size']
    total,items=MemoService.get_memos(db=db,page=page,page_size=page_size,keywords=keywords)
    return MemoPage(page=page,page_size=page_size,total=total,items=items)

@app.get("/memos/{memo_id}")
def get_memo(memo_id: int,db: Session = Depends(get_db)):
    return MemoService.get_memo(db=db,memo_id=memo_id)

@app.delete("/memos/{memo_id}",status_code=204)
def delete_memo(memo_id: int,db: Session = Depends(get_db)):
    return MemoService.delete_memo(db=db,memo_id=memo_id)
@app.put("/memos/{memo_id}",status_code=200)
def update_memo(memo_id: int,memo: MemoUpdate,db: Session = Depends(get_db)):
    return MemoService.update_memo(db=db,memo_id=memo_id,memo=memo)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app',host="127.0.0.1",port=8000,reload=True)
        

