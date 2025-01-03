from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from session_manage import SessionManager

from models import *
import asyncio
import sys


class App:
    def __init__(self):
        self.session = None
        self.request = None

    async def init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def register(self):
        checker = 0
        while checker < 3:
            username = input('Username: ')
            email = input('Email: ')
            password = input('Password: ')
            password2 = input('Repeat password: ')

            if password and password2 and password == password2:
                try:
                    async with async_session() as session:
                        new_user = User(username=username,email=email,password=password)
                        session.add(new_user)
                        await session.commit()
                        print("User successfully created")
                        self.request = SessionManager(username=username,email=email)
                except IntegrityError:
                    print('Username or email already taken')
                    checker += 1
                    await session.rollback()
            else:
                checker += 1
                print('Passwords do not match')
                await session.rollback()


    async def login(self):
        checker = 0
        while checker < 3:
            email = input('Email: ')
            password = input('Password: ')

            async with async_session() as session:
                result = await session.execute(select(User).where(User.email == email))
                user = result.scalars().first()
                if user is None:
                    print('User not found')
                    checker += 1
                else:
                    if user.password == password and user.email == email:
                        await session.commit()
                        self.request = SessionManager(username=user.username, email=user.email)
                        print('Login successful')
                        await self.categories()
                        break
                    else:
                        print('Password or email is incorrect')



    async def start(self):
        await self.init_db()


        login_choice = int(input('Choose 1 for login, 2 for register: '))
        if login_choice == 1:
            await self.login()
        else:
            await self.register()




    async def categories(self):
        while True:
            async with async_session() as session:
                categories_request = await session.execute(select(Category))
                categories = categories_request.scalars().all()
                for category in categories:
                    print(f'{category.id}: {category.cat_title} ')
                action = int(input(f'Hello,{self.request.username} choose category by number, if you want to exit enter 101: '))

                if action!=101 and action > 4:
                    await session.rollback()
                    print('Invalid choice')
                if action == 101:
                    sys.exit()
                else:
                    await self.posts_by_category(action)

    async def posts_by_category(self, category_id):
        async with async_session() as session:
            posts_request = await session.execute(select(Post).where(Post.category_id == category_id))
            posts = posts_request.scalars().all()

            print(f'There we go {self.request.username}!,all the posts bellow! \n')
            for post in posts:
                print(f'{post.id}: {post.title} \n{post.content} ')






async def main():
    app = App()
    await app.start()

asyncio.run(main())
