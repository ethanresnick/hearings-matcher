from flask import Flask, jsonify, request, Markup
from bs4 import BeautifulSoup
import requests
app = Flask(__name__)

def get_article_text(url):
    new_url = "https://www.readability.com/api/content/v1/parser?url=" + url + "&token=f6b04483b9e3f605ce40fc73858b3522ef7869b9"
    response_dict = requests.get(new_url).json()
    text = BeautifulSoup(response_dict["content"]).get_text()
    date = response_dict["date_published"]
    return {"text": text, "date_published": date}

@app.route('/matches')
def matches():
    url = request.args.get('for')
    text = get_article_text(url)
    # matches = match(text)
    return jsonify(text)

if __name__ == '__main__':
    app.run(debug=True)