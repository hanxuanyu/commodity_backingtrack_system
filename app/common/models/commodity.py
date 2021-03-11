# coding: utf-8
from sqlalchemy import Column, Integer, String
from application import db


class Commodity(db.Model):
    __tablename__ = 'commodity'

    id = db.Column(db.Integer, primary_key=True, info='主键-商品id')
    name = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='商品名称')
    origin = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='商品产地')
    seller = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='卖家')
    trans = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='运输')
    warehouse = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='仓库')
    buyer = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='买家')
    status = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue(), info='商品状态')
