from database import db
from datetime import datetime

class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    content = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return self.title
    
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(100), nullable=False)
    likes=db.Column(db.Integer, default=0, nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    board_id=db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)