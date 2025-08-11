from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

favorite_table = Table(
    "favorites",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("post_id", ForeignKey("post.id")),
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    favorites: Mapped[List["Post"]] = relationship(
        "Post",
        secondary=favorite_table,
        back_populates="favorite_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites": [post.serialize() for post in self.favorites]
        }


class Post(db.Model):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    favorite_by: Mapped[List["User"]] = relationship(
        "User",
        secondary=favorite_table,
        back_populates="favorites"
    )

    def serialize(self):
        return {
            "id": self.id,
            "image": self.image,
            "description": self.description
        }
