#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/15 下午2:46
# @Author  : allenwu
# @File    : api.py
import os
from flask import Flask, jsonify, abort, request
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask import url_for

'''
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
'''

# initialization
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


class Post(db.Model):
    # table name in db
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    author = db.Column(db.String(20))
    content = db.Column(db.String(50))
    date = db.Column(db.DateTime)

    def __init__(self,title,author,content,date=None):
        #self.id = id
        self.title = title
        self.author = author
        self.content = content
        if date is None:
            date = datetime.utcnow()
        self.date = date


@app.route('/api/v1.0/diary/', methods = ['GET'])
#@auth.login_required
def index():
    # the type of post is list
    posts = Post.query.all()
    if len(posts) == 0:
        abort(404)
    diarys = []
    for post in posts:
        diary = {
            'id':post.id,
            'title': post.title,
            'date':post.date,
            'author': post.author,
            'content': post.content
        }
        diarys.append(diary)
    return jsonify({'posts': diarys})


'''
404错误处理好 400 or 404 ?
'''
@app.route('/api/v1.0/diary/<int:id>/')
def get_post(id):
    # post is a model
    post = Post.query.get(id)
    if not post:
        abort(404)
    diary = {
        'id':post.id,
        'title': post.title,
        'date': post.date,
        'author': post.author,
        'content': post.content
    }
    #print type(post)
    return jsonify({'post': diary})


@app.route('/api/v1.0/diary/', methods = ['POST'])
def create_post():
    if not request.json or not 'title' in request.json:
        abort(400)
    # json to dict
    diary = {
        'title': request.json['title'],
        'author': request.json['author'],
        'content': request.json['content']
    }
    post = Post(diary['title'],diary['author'],diary['content'])
    #post = Post(request.json.title, request.json.get('author'), request.json.get('content'))
    db.session.add(post)
    db.session.commit()
    return jsonify({'post':diary}), 201


@app.route('/api/v1.0/diary/<int:id>', methods = ['DELETE'])
@auth.login_required
def delete_post(id):
    db.session.delete(Post.query.get(id))
    db.session.commit()
    return jsonify({ 'result': True })


@app.route('/api/v1.0/diary/<int:id>', methods = ['PUT'])
@auth.login_required
def update_post(id):
    post = Post.query.get(id)
    post.name = request.json.get('title', post.title)
    post.author = request.json.get('author', post.author)
    post.content = request.json.get('content', post.content)
    db.session.commit()
    return jsonify( { 'post': post } )


'''
def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task
'''


'''
更加友善的 404 错误显示
'''
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


'''
权限认证，修改或者添加数据，需要认证
目前是最简单的固定的用户名和密码
'''
@auth.get_password
def get_password(username):
    if username == 'allen':
        return '12345'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    if not os.path.exists('db.sqlite'):
        db.create_all()
    app.run(debug=True)
