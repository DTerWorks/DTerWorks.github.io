import click
from flask_sqlalchemy import SQLAlchemy
import sys
import os
from flask import Flask, render_template
from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/<names>')
def user_page(names):
    return '提示："/'+names + '" 页面不存在。请让畅神赶快写代码！'


name = 'DTer'
movies = [
    {'title': 'Pyside6', 'year': '3月'},
    {'title': 'Python', 'year': '4月'},
    {'title': 'Pandas', 'year': '5月'},
    {'title': 'Requests', 'year': '6月'},
    {'title': 'Dash', 'year': '7月'},
    {'title': 'VBA', 'year': '8月'},
    {'title': 'SPL', 'year': '9月'},
    {'title': 'DAX', 'year': '10月'},
    {'title': 'C++', 'year': '11月'},
    {'title': 'Flask', 'year': '12月'},
]


@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.first()
    return render_template('404.html', user=user), 404  # 返回模板和状态码


###########


WIN = sys.platform.startswith('win')
print(WIN)
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
# print(db)


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', name=name, user=user, movies=movies)


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'DTer'
    movies = [
        {'title': '畅神', 'year': '牛逼'},
        {'title': '篮球哥', 'year': '牛逼'},
        {'title': '冬哥', 'year': '牛逼'},
        {'title': '景哥', 'year': '牛逼'},
        {'title': 'DTer', 'year': '吹牛逼'}

    ]

    user = User(name=name)
    db.session.add(user)

    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# 开启此项并执行则可以向数据库添加数据，但网页刷新会报错。
# 开启后服务器将关闭，需要关闭此项并重启服务器。
# forge()
