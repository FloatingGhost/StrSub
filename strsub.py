from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sub")
def sub():
    url = request.args.get("url")
    if not url.startswith("http://"):
        url = "http://{}".format(url)    
    try:
        html = requests.get(url).text
    except Exception as ex:
        return str(ex)
    
    cleaner = Cleaner()
    cleaner.javascript = True
    html = lxml.html.tostring(cleaner.clean_html(lxml.html.fromstring(html, url))).decode("utf-8")

    soup = BeautifulSoup(html, "lxml")
    for link in soup.find_all("img"):
        if "src" in link.attrs:
            u = link.attrs.get("src")
            if not u.startswith("http"):
                html = html.replace(u, "{}/{}".format(url, u))
    for arg in request.args:
        if arg.startswith("from"):
            from_ = request.args.get(arg)
            number = arg.replace("from", "")
            to = request.args.get("to{}".format(number))

            from_ = BeautifulSoup(from_, "lxml").text
            to    = BeautifulSoup(to, "lxml").text
           
            print("FROM {} TO {}".format(from_, to)) 
            concat = (from_ + to).lower()
            naughty = ["http://", "src=", "<script"]
            for i in naughty:
                if i in concat:
                    return "OY STOP BEING NAUGHTY"
            html = html.replace(from_, to)
            html = html.replace(from_.lower(), to)
            html = html.replace(from_.upper(), to)
            html = html.replace(from_.title(), to)
    
    return html

if __name__ == "__main__":
    app.run()    
