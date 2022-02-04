from flask import Flask,request,jsonify
from newspaper import Article
from deep_translator import GoogleTranslator

application = Flask(__name__)

@application.route("/", methods=["POST"])
def get():
    url = request.form.get("url")
    lang = request.form.get("lang")
    article = Article(url)
    article.download()
    article.parse()
    title=""
    text=""
    if lang!="en":
        translated = GoogleTranslator(target=lang).translate_batch([article.title, article.text])
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
