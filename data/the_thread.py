import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


def create_thread_table(name):
    class TheThread(SqlAlchemyBase, UserMixin, SerializerMixin):
        def __init__(self):
            __tablename__ = name
            id = sqlalchemy.Column(sqlalchemy.Integer,
                                   primary_key=True, autoincrement=True)
            author = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
            text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
            photo = sqlalchemy.Column(sqlalchemy.BLOB)