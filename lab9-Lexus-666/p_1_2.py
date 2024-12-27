from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


def db_create():
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/laba_9_2"

    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True, autoincrement=True)
        username = Column(String, unique=True, nullable=False)
        email = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)

        posts = relationship("Post", back_populates="user")

    class Post(Base):
        __tablename__ = 'posts'

        id = Column(Integer, primary_key=True, autoincrement=True)
        title = Column(String, nullable=False)
        content = Column(Text, nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

        user = relationship("User", back_populates="posts")

    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    user1 = User(username="Dasha", email="dasha@yandex.ru", password="fghsdhst")
    user2 = User(username="Sveta", email="sveta@gmail.com", password="tfhrshtaerfhtds")
    user3 = User(username="Kostya", email="kstyan@mail.com", password="hsderthsert")
    user4 = User(username="Bubun", email="Bubun@yahoo.com", password="hrsththt")

    session.add_all([user1, user2, user3, user4])
    session.commit()

    post1 = Post(title="First", content="Sueta...", user_id=user1.id)
    post2 = Post(title="Second", content="Ne sueta.", user_id=user1.id)
    post3 = Post(title="qwe", content="Hello!", user_id=user2.id)
    post4 = Post(title="Post", content="Post...", user_id=user4.id)

    session.add_all([post1, post2, post3, post4])
    session.commit()

    users = session.query(User).all()
    for user in users:
        print(f"id-{user.id}, username-{user.username}, email-{user.email}, password-{user.password}")
    print()

    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id-{post.id}, title-{post.title}, content-{post.content}, user_id-{post.user_id}\n"
              f"author-{post.user.username}")
    print()

    user_posts = session.query(Post).filter(Post.user_id == user2.id).all()
    for post in user_posts:
        print(f"title-{post.title}, content-{post.content}")
    print()

    user_to_update = session.query(User).filter(User.id == 3).first()
    print(f"id-{user_to_update.id}, username-{user_to_update.username}, email-{user_to_update.email}, password-"
          f"{user_to_update.password}")
    if user_to_update:
        user_to_update.email = "kstyan@mail.com"
        session.commit()
    session.refresh(user_to_update)
    print(f"id-{user_to_update.id}, username-{user_to_update.username}, email-{user_to_update.email}, password-"
          f"{user_to_update.password}")
    print()

    post_to_update = session.query(Post).filter(Post.id == 1).first()
    print(f"id-{post_to_update.id}, title-{post_to_update.title}, content-{post_to_update.content}, user_id-"
          f"{post_to_update.user_id}")
    if post_to_update:
        post_to_update.content += " updated"
        session.commit()
    session.refresh(post_to_update)
    print(f"id-{post_to_update.id}, title-{post_to_update.title}, content-{post_to_update.content}, user_id-"
          f"{post_to_update.user_id}")
    print()

    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id-{post.id}, title-{post.title}, content-{post.content}, user_id-{post.user_id}\n"
              f"author-{post.user.username}")
    print()
    post_to_delete = session.query(Post).filter(Post.id == 3).first()
    if post_to_delete:
        session.delete(post_to_delete)
        session.commit()
    posts = session.query(Post).join(User).all()
    for post in posts:
        print(f"id-{post.id}, title-{post.title}, content-{post.content}, user_id-{post.user_id}\n"
              f"author-{post.user.username}")
    print()

    users = session.query(User).all()
    for user in users:
        print(f"id-{user.id}, username-{user.username}, email-{user.email}, password-{user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title-{post.title}, content-{post.content}")
    print()
    user_to_delete = session.query(User).filter(User.id == 1).first()
    if user_to_delete:
        session.query(Post).filter(Post.user_id == user_to_delete.id).delete()
        session.delete(user_to_delete)
        session.commit()
    users = session.query(User).all()
    for user in users:
        print(f"id-{user.id}, username-{user.username}, email-{user.email}, password-{user.password}")
    user_posts = session.query(Post).filter(Post.user_id == user1.id).all()
    for post in user_posts:
        print(f"title-{post.title}, content-{post.content}")
    print()


if __name__ == '__main__':
    db_create()
