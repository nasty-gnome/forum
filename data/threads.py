import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Threads(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'threads'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    author = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.BLOB)
    first_answer = sqlalchemy.Column(sqlalchemy.String)
    first_author = sqlalchemy.Column(sqlalchemy.Integer)
    second_answer = sqlalchemy.Column(sqlalchemy.String)
    second_author = sqlalchemy.Column(sqlalchemy.Integer)
    third_answer = sqlalchemy.Column(sqlalchemy.String)
    third_author = sqlalchemy.Column(sqlalchemy.Integer)
    forth_answer = sqlalchemy.Column(sqlalchemy.String)
    forth_author = sqlalchemy.Column(sqlalchemy.Integer)
    all_answers = sqlalchemy.Column(sqlalchemy.JSON)
