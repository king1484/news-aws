from flask import Flask,request,jsonify
from newspaper import Article
from googletrans import Translator

app = Flask(__name__)

@app.route("/", methods=["POST"])
def get():
    url = request.form.get("url")
    lang = request.form.get("lang")
    article = Article(url)
    article.download()
    article.parse()
    title=""
    text=""
    if lang!="en":
        translator = Translator()
        translated = translator.translate([article.title, article.text], dest=lang)
        title = translated[0].text
        text = translated[1].text
    else:
        title = article.title
        text = article.text
    data = {
        "title" : title,
        "img_url" : article.top_image,
        "keywords" : article.meta_keywords,
        "authors" : article.authors,
        "text" : text
    }
    return jsonify(data)


if __name__ == "__main__":
    app.run()