from flask import Flask, url_for, request
from flask import render_template

app = Flask(__name__)


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()

# @app.route('/')
# def index(): pass

# @app.route('/login')
# def login(): pass

# @app.route('/user/<username>')
# def profile(username): pass

# with app.test_request_context():
#     print url_for('index')
#     print url_for('login')
#     print url_for('login', next='/')
#     print url_for('profile', username='John Doe')




# @app.route('/')
# def index():
#    return 'Index Page'

# @app.route('/hello')
# def hello():
#    return 'Hello, World'


if __name__ == "__main__":
    app.run(host="0.0.0.0")
