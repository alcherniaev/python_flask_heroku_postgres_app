from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)


ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://qhwdwjyfjfbwat:61ea2c7db09109be3676124c2d6d2127e3300190531c5812e1c85afcb0821fcf@ec2-35-174-127-63.compute-1.amazonaws.com/d3lmcbisdoj6s4"
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://qhwdwjyfjfbwat:61ea2c7db09109be3676124c2d6d2127e3300190531c5812e1c85afcb0821fcf@ec2-35-174-127-63.compute-1.amazonaws.com/d3lmcbisdoj6s4"
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__='feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Float)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"]
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        #print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message="Please fill the form")

        if db.session.query(Feedback).filter(Feedback.customer==customer).count()==0:
            data = Feedback(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template("success.html")
        return render_template('index.html', message="Sorry, you've already submited feedback.")


if __name__ == '__main__':
    app.debug = True
    app.run()