# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from application import db


class Operation(db.Model):
    __tablename__ = 'operation'

    id = db.Column(db.Integer, primary_key=True, info='主键-操作id')
    user_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='用户id')
    type = db.Column(db.String(255), nullable=False, server_default=db.FetchedValue(), info='操作类型')
    commodity_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue(), info='商品id')
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue(), info='操作时间')
