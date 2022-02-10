from flask_sqlalchemy import SQLAlchemy, Model
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class Novel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    cover = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    preview = db.Column(db.String(), nullable=False)
    hot = db.Column(db.Integer, nullable=False)

class Scroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    novel_id = db.Column(db.Integer, nullable=True)
    scroll_name = db.Column(db.String(255), nullable=True)
    # chapters = relationship("Chapter", back_populates="scroll")
    chapters = relationship("Chapter")

    def __repr__(self) -> str:
        return "<scroll id=%s, novel_id=%s, scroll_name=%s>" % (self.id, self.novel_id, self.scroll_name)

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scroll_id = db.Column(db.Integer, ForeignKey('scroll.id'))
    chapter_name = db.Column(db.String(255), nullable=True)
    # txt = db.Column(db.Text, nullable=False)
    # chatu = db.Column(db.String(), nullable=False)
    # scroll = relationship("Scroll", back_populates="chapters")
    def __str__(self) -> str:
        return "Chapter: id:%s, chapter_name: %s" %(self.id, self.chapter_name)

class ChapterContent(db.Model):
    __tablename__ = 'chapter'
    __table_args__ = {"extend_existing":True}
    
    id = db.Column(db.Integer, primary_key=True)
    scroll_id = db.Column(db.Integer, ForeignKey('scroll.id'))
    chapter_name = db.Column(db.String(255), nullable=True)
    txt = db.Column(db.Text, nullable=False)
    chatu = db.Column(db.String(), nullable=False)
    scroll = relationship("Scroll")
