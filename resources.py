from flask import request
from flask_restx import Resource, fields
from database import db
from models import Board as BoardModel, Comment as CommentModel
from datetime import datetime

def init_routes(api):
    # Swagger 모델 정의
    board_write_model = api.model('BoardWrite', {
        'title': fields.String(required=True, description='제목'),
        'content': fields.String(required=True, description='내용'),
    })
    
    board_read_model = api.model('BoardRead', {
        'id': fields.Integer(readonly=True, description='게시글 ID'),
        'title': fields.String(required=True, description='제목'),
        'content': fields.String(required=True, description='내용'),
        'likes': fields.Integer(required=True, description='좋아요 수')
    })
    
    comment_write_model = api.model('CommentWrite', {
        'content': fields.String(required=True, description='댓글 내용'),
    })
    
    comment_read_model = api.model('CommentRead', {
        'id': fields.Integer(readonly=True, description='댓글 ID'),
        'content': fields.String(required=True, description='댓글 내용'),
        'likes': fields.Integer(description='좋아요 수'),
        'created_at': fields.DateTime(description='댓글 작성 시간')
    })
    
    def serialize_comment(comment):
        return {
            'id': comment.id,
            'content': comment.content,
            'likes': comment.likes,
            'created_at': comment.created_at.isoformat(),
            'replies': [serialize_comment(reply) for reply in comment.replies]
        }


    def serialize_board(board):
        parent_comments = CommentModel.query.filter_by(board_id=board.id, parent_comment_id=None).all()

        return {
            'id': board.id,
            'title': board.title,
            'content': board.content,
            'likes': board.likes,
            'comments': [serialize_comment(c) for c in parent_comments]
        }

    @api.route('/boards')
    class Boards(Resource):
        @api.marshal_list_with(board_read_model)
        def get(self):
            """모든 게시글 조회"""
            return BoardModel.query.all()

        @api.expect(board_write_model)
        @api.marshal_with(board_read_model, code=201)
        def post(self):
            """게시글 추가"""
            data = request.json
            board = BoardModel(title=data['title'], content=data['content'], likes=0)
            db.session.add(board)
            db.session.commit()
            return board, 201

    @api.route('/boards/<int:pk>')
    class BoardDetail(Resource):
    
        def get(self, pk):
            """특정 게시글 조회"""
            board = BoardModel.query.get_or_404(pk)
            return serialize_board(board)

        @api.expect(board_write_model)
        @api.marshal_with(board_read_model)
        def patch(self, pk):
            """게시글 수정"""
            board = BoardModel.query.get(pk)
            if not board:
                api.abort(404, "Board Not Found")

            data = request.json
            if 'title' in data:
                board.title = data['title']
            if 'content' in data:
                board.content = data['content']
            db.session.commit()
            return board

        @api.marshal_with(board_read_model, 204)
        def delete(self, pk):
            """게시글 삭제"""
            board = BoardModel.query.get(pk)
            if not board:
                api.abort(404, "Board Not Found")
            db.session.delete(board)
            db.session.commit()
            return '', 204
    
    @api.route('/boards/<int:pk>/like')
    class BoardLike(Resource):
        @api.marshal_with(board_read_model)
        def post(self, pk):
            """게시글 좋아요"""
            board = BoardModel.query.get(pk)
            if not board:
                api.abort(404, "Board Not Found")
            
            board.likes += 1
            db.session.commit()
            return board

    @api.route('/comments/<int:board_id>')
    class Comments(Resource):
        @api.expect(comment_write_model)
        @api.marshal_with(comment_read_model, code=201)
        def post(self, board_id):
            """게시글 댓글 달기"""
            data = request.json
            
            board = BoardModel.query.get(board_id)
            if not board:
                api.abort(404, "Board Not Found")
            
            now = datetime.now()
            
            comment = CommentModel(
                content=data['content'],
                likes=0,
                parent_comment_id=None,
                created_at=now,
                board_id=board_id
            )
            db.session.add(comment)
            db.session.commit()
            return comment, 201
        
    @api.route('/comments/<int:comment_id>/like')
    class CommentLike(Resource):
        @api.marshal_with(comment_read_model)
        def post(self, comment_id):
            """댓글/대댓글 좋아요"""
            comment = CommentModel.query.get(comment_id)
            if not comment:
                api.abort(404, "Comment Not Found")
            
            comment.likes += 1
            db.session.commit()
            return comment
        
        
    @api.route('/comments/<int:comment_id>/replies')
    class CommentOfComments(Resource):
        @api.expect(comment_write_model)
        @api.marshal_with(comment_read_model, code=201)
        def post(self, comment_id):
            """대댓글 작성"""
            data = request.json
            
            # 부모 댓글 존재 확인
            find_comment = CommentModel.query.get(comment_id)
            if not find_comment:
                api.abort(404, "Parent Comment Not Found")
            
            now = datetime.now()
            
            comment = CommentModel(
                content=data['content'],
                likes=0,
                parent_comment_id=find_comment.id,
                created_at=now,
                board_id=find_comment.board_id
            )
            db.session.add(comment)
            db.session.commit()
            return comment, 201