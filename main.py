from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    # return render_template('pages/placeholder.home.html')
    return "hello, world"

@app.route('/signup')
def signup():
    # return render_template('pages/placeholder.home.html')
    return "signup"

@app.route('/login')
def login():
    # return render_template('pages/placeholder.home.html')
    return "hello, world"

@app.route('/dashboard')
def dashboard():
    # return render_template('pages/placeholder.home.html')
    return "hello, world"


if __name__ == '__main__':
    app.run()