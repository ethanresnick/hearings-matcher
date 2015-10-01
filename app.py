from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import tokenizer
from datetime import datetime
import requests

app = Flask(__name__)

def get_article_info(url):
    new_url = "https://www.readability.com/api/content/v1/parser?url=" + url + "&token=f6b04483b9e3f605ce40fc73858b3522ef7869b9"
    response_dict = requests.get(new_url).json()
    text = BeautifulSoup(response_dict["content"]).get_text()
    date = response_dict["date_published"]
    return {"text": text, "date_published": date}

def get_matching_hearings(text, date_published):
    tokens = tokenizer.tokenize(text)
    return {
        "data": [{
            "attributes": {
                "agency": "MTA",
                "shortTitle": "MTA Hearing",
                "description": "Hearing description.",
                "date": datetime.now()
            },
            "meta": {
                "confidence": ".1"
            }
        }]
    }


@app.route('/matches')
def matches():
    url = request.args.get('for')
    article = get_article_info(url)
    matches = get_matching_hearings(article["text"], article["date_published"])
    return jsonify(matches)

if __name__ == '__main__':
    app.run(debug=True)
