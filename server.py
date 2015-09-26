from flask import Flask
from flask import request
app = Flask(__name__)

def get_article_text(url):
    return 'Hello World!'

def match():
    return 'Hello World!'

@app.route('/matches')
def hello_world():
    url = request.args.get('for')
    text = get_article_text(url)
    matches = match(text)

if __name__ == '__main__':
    app.run()


# new comment