# app.py


from flask import Flask
from flask import request, render_template
#from flask.ext.sqlalchemy import SQLAlchemy
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)


#from models import *


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        post = Post(text)
        db.session.add(post)
        db.session.commit()
    return '1'
    #posts = Post.query.order_by(Post.date_posted.desc()).all()
    #return render_template('index.html', posts=posts)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
