# coding: utf-8
from sqlalchemy import Column, DateTime, Index, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

Base.to_dict = to_dict


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True)
    name = Column(String(20))
    description = Column(String(500), server_default=text("''"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class FetchResult(Base):
    __tablename__ = 'fetch_result'
    __table_args__ = (
        Index('idx_platform_author_id', 'platform_id', 'article_author_id'),
        Index('idx_platform_article_id', 'platform_id', 'article_id', unique=True)
    )

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False, index=True)
    platform_id = Column(Integer, server_default=text("'0'"))
    platform_name = Column(String(50), server_default=text("''"))
    channel_id = Column(Integer, server_default=text("'0'"))
    channel_name = Column(String(50), server_default=text("''"))
    article_id = Column(String(50), server_default=text("''"))
    article_url = Column(String(512), server_default=text("''"))
    article_title = Column(String(100), server_default=text("''"))
    article_author_id = Column(String(100), server_default=text("''"))
    article_author_name = Column(String(100), server_default=text("''"))
    article_tags = Column(String(100), server_default=text("''"))
    article_abstract = Column(String(500), server_default=text("''"))
    article_content = Column(String)
    article_pub_time = Column(DateTime, index=True, server_default=text("'1000-01-01 00:00:00'"))
    create_time = Column(DateTime, nullable=False, index=True, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, index=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class FetchTask(Base):
    __tablename__ = 'fetch_task'
    __table_args__ = (
        Index('idx_platform_follow_id', 'platform_id', 'follow_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, server_default=text("'0'"))
    channel_id = Column(Integer, server_default=text("'0'"))
    follow_id = Column(String(45), server_default=text("''"))
    follow_name = Column(String(45), server_default=text("''"))
    avatar_url = Column(String(512), server_default=text("''"))
    fetch_url = Column(String(512), server_default=text("''"))
    flag_enabled = Column(Integer, server_default=text("'0'"))
    description = Column(String(500), server_default=text("''"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class LogTaskScheduling(Base):
    __tablename__ = 'log_task_scheduling'

    id = Column(Integer, primary_key=True)
    platform_id = Column(Integer, server_default=text("'0'"))
    platform_name = Column(String(50), server_default=text("''"))
    spider_name = Column(String(45), server_default=text("''"))
    task_quantity = Column(Integer, server_default=text("'0'"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
