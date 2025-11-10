from flask import request
from flask_restx import Resource, fields
from database import db
from models import Task

def init_routes(api):
    # Swagger 모델 정의
    task_model = api.model('Task', {
        'id': fields.Integer(readonly=True, description='게시글 ID'),
        'title': fields.String(required=True, description='제목'),
        'content': fields.String(required=True, description='내용'),
    })

    @api.route('/board')
    class Boards(Resource):
        @api.marshal_list_with(task_model)
        def get(self):
            """모든 게시글 조회"""
            return Task.query.all()

        @api.expect(task_model)
        @api.marshal_with(task_model, code=201)
        def post(self):
            """게시글 추가"""
            data = request.json
            task = Task(title=data['title'], content=data['content'])
            db.session.add(task)
            db.session.commit()
            return task, 201

    @api.route('/board/<int:pk>')
    @api.response(404, 'Board Not Found')
    class Board(Resource):
        @api.marshal_with(task_model)
        def get(self, pk):
            """특정 게시글 조회"""
            task = Task.query.get(pk)
            if not task:
                api.abort(404, "Board Not Found")
            return task

        @api.expect(task_model)
        @api.marshal_with(task_model)
        def patch(self, pk):
            """게시글 수정"""
            task = Task.query.get(pk)
            if not task:
                api.abort(404, "Board Not Found")

            data = request.json
            if 'title' in data:
                task.title = data['title']
            if 'content' in data:
                task.content = data['content']
            db.session.commit()
            return task

        @api.marshal_with(task_model)
        def delete(self, pk):
            """게시글 삭제"""
            task = Task.query.get(pk)
            if not task:
                api.abort(404, "Board Not Found")
            db.session.delete(task)
            db.session.commit()
            return task, 204
