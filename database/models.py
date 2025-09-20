from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.config import Base

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, unique=True, index=True)
    title = Column(String)
    username = Column(String)
    added_date = Column(DateTime, default=datetime.utcnow)
    
    schedules = relationship("Schedule", back_populates="channel")

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    newspaper = Column(String, index=True)
    category = Column(String, index=True)
    rss_url = Column(String, unique=True)
    title = Column(String)
    description = Column(Text)
    link = Column(String)
    added_date = Column(DateTime, default=datetime.utcnow)
    
    articles = relationship("Article", back_populates="source")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"))
    title = Column(String)
    link = Column(String, unique=True)
    published = Column(DateTime)
    summary = Column(Text)
    content = Column(Text)
    fetched_date = Column(DateTime, default=datetime.utcnow)
    
    source = relationship("Source", back_populates="articles")
    posted_articles = relationship("PostedArticle", back_populates="article")

class Ad(Base):
    __tablename__ = "ads"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    image_path = Column(String)
    schedule = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    times_posted = Column(Integer, default=0)

class Schedule(Base):
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(String, ForeignKey("channels.channel_id"))
    interval_seconds = Column(Integer)
    enabled = Column(Boolean, default=True)
    last_run = Column(DateTime)
    next_run = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    channel = relationship("Channel", back_populates="schedules")

class PostedArticle(Base):
    __tablename__ = "posted_articles"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"))
    channel_id = Column(String)
    posted_at = Column(DateTime, default=datetime.utcnow)
    
    article = relationship("Article", back_populates="posted_articles")