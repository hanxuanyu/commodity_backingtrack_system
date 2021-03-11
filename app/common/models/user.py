# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from application import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True, server_default=db.FetchedValue())
    type = db.Column(db.String(10), nullable=False, server_default=db.FetchedValue())
    password = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())
    regist_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
