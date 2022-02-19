from flask import Flask,request,jsonify
from newspaper import Article
from deep_translator import GoogleTranslator
from newspaper import Config

application = Flask(__name__)

@application.route("/", methods=["GET"])
def data():
    return "ok"

@application.route("/", methods=["POST"])
def get():
    url = request.form.get("url")
    lang = request.form.get("lang")
    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    config.request_timeout = 10
    article = Article(url,config=config)
    
    article.download()
    article.parse()
    title=""
    text=""
    if lang!="en":
        translated = GoogleTranslator(target=lang).translate_batch([article.title, (article.text[:4900]+"...") if len(article.text)>5000 else article.text])
        title = translated[0]
        text = translated[1]
    else:
        title = article.title
        text = article.text
    data = {
        "title" : title,
        "img_url" : article.top_image,
        "publish_date" : article.publish_date,
        "keywords" : article.meta_keywords,
        "authors" : article.authors,
        "text" : text
    }
    return jsonify(data)


if __name__ == "__main__":
    application.run()
