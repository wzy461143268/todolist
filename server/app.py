from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import click
import datetime
import os
import sys

app = Flask(__name__)
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(
    app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app=app)
db = SQLAlchemy(app)


class TodoList(db.Model):
    __tablename__ = 'todolist'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    content = db.Column(db.TEXT, nullable=False, default='')
    c_time = db.Column(db.DATETIME, default=datetime.datetime.now)


db.drop_all()
db.create_all()

todos = ['学习到天亮', '学习到天黑', '学习到天亮再天黑']
for td in todos:
    db.session.add(TodoList(content=td))

db.session.commit()
click.echo("数据库创建完成")


@app.route('/add-todolist', methods=['POST'])
def add_todolist():
    content = request.json.get('text')
    tl = TodoList(content=content)
    db.session.add(tl)
    db.session.commit()
    return jsonify({'code': 200, 'msg': '添加成功!', 'id': tl.id})


@app.route('/remove-todolist', methods=['POST'])
def remove_todolist():
    tl_id = request.json.get('id')
    tl = TodoList.query.filter_by(id=tl_id).first()
    if tl:
        db.session.delete(tl)
        db.session.commit()
        return jsonify({'code': 200, 'msg': '删除成功！'})
    else:
        return jsonify({'code': 404, 'msg': '未找到todolist!'})


@app.route('/get-todolist')
def get_todolist():
    result = []
    todolists = TodoList.query.all()
    for todolist in todolists:
        dic = {'id': todolist.id, 'text': todolist.content}
        result.append(dic)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000)
