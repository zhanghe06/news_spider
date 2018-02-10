#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: client_db.py
@time: 2018-02-10 17:34
"""


from sqlalchemy import create_engine
from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import redis

from config import current_config

SQLALCHEMY_DATABASE_URI_MYSQL = current_config.SQLALCHEMY_DATABASE_URI_MYSQL
SQLALCHEMY_POOL_SIZE = current_config.SQLALCHEMY_POOL_SIZE
REDIS = current_config.REDIS


engine_mysql = create_engine(SQLALCHEMY_DATABASE_URI_MYSQL, pool_size=SQLALCHEMY_POOL_SIZE, max_overflow=0)
db_session_mysql = sessionmaker(bind=engine_mysql, autocommit=True)


redis_client = redis.Redis(**REDIS)


def get_item(model_class, pk_id):
    session = db_session_mysql()
    try:
        result = session.query(model_class).get(pk_id)
        return result
    finally:
        session.close()


def get_all(model_class, *args, **kwargs):
    session = db_session_mysql()
    try:
        result = session.query(model_class).filter(*args).filter_by(**kwargs).all()
        return result
    finally:
        session.close()


def get_distinct(model_class, field, *args, **kwargs):
    session = db_session_mysql()
    try:
        result = session.query(distinct(getattr(model_class, field)).label(field)).filter(*args).filter_by(**kwargs).all()
        return result
    finally:
        session.close()


def get_group(model_class, field, min_count=0, *args, **kwargs):
    field_obj = getattr(model_class, field)
    session = db_session_mysql()
    try:
        result = session.query(field_obj, func.count(field_obj).label('c')).filter(*args).filter_by(
            **kwargs).group_by(field_obj).having(func.count(field_obj) >= min_count).all()
        return result
    finally:
        session.close()
