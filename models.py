from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String,select,ForeignKey
from sqlalchemy.exc import IntegrityError
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    category_id = Column(Integer,ForeignKey('categories.id',ondelete='CASCADE'),nullable=False)

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    cat_title = Column(String,nullable=False)





DATABASE_URL = 'postgresql+asyncpg://postgres:root@localhost:5432/AsyncPost'
engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(engine, class_ = AsyncSession,expire_on_commit=False)



async def model_create():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


