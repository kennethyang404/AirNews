from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
import os
import random
import bisect
import bayes

app = Flask(__name__)
app.debug = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/posts.db"

db = SQLAlchemy(app)


class posts(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    text = db.Column(db.String(1000))
    score = db.Column(db.Integer)
    date = db.Column(db.DateTime())

    def __init__(self, title, text, score):
        self.title = title
        self.text = text
        self.score = score
        self.date = datetime.utcnow()

db.create_all()


def createTitle(text):
    if (text != None) and (len(text) <= 400):
        return text
    else:
        return None


def createText(text):
    if (text != None) and (len(text) <= 100000):
        return text
    else:
        return None


def weighted_choice_b(weights):
    s = 0.0
    n = len(weights)
    for i in xrange(n):
        s = s + 1 / float(weights[i])
    c = (n - 1) / s
    for i in xrange(n):
        weights[i] = 1 - c / weights[i]
    totals = []
    running_total = 0
    # source for binary random below: http://eli.thegreenplace.net/
    for w in weights:
        running_total += w
        totals.append(running_total)
    rnd = random.random() * running_total
    return bisect.bisect_right(totals, rnd)


@app.route("/")
def home():
    random.seed()
    allPost = posts.query.all()
    allScore = [allPost[i].score for i in xrange(len(allPost))]
    theOne = allPost[weighted_choice_b(allScore)]
    return render_template("index.html", theOne=theOne)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/detail/<int:post_id>")
def detail(post_id):
    theOne = posts.query.get(post_id)
    theOne.score = theOne.score + 1
    db.session.commit()
    return render_template("detail.html", theOne=theOne)


@app.route("/newpost", methods=["POST"])
def newpost():
    newtitle = createTitle(request.form["post-title"])
    newtext = createText(request.form["post-text"])
    newlist = ["bayes.py", "classify", newtext, "spam", "valid"]
    c = bayes.main(newlist)
    if not(c > 0.9):
        db.session.add(posts(newtitle, newtext, 20))
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
