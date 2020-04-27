from flask import Flask, render_template, url_for, request, redirect, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json


app = Flask(__name__)

ENV ='prod'

if ENV=='dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vikash:Vikas98@a@127.0.0.1:5432/db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ywurgnrqkapoaz:9bea09f133b1fc6b659bda06556aed79e7ea82088d17a6dbde0fea2f5e82c936@ec2-52-207-25-133.compute-1.amazonaws.com:5432/d824a65a7tvvva'
# Init app

# Database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



app.secret_key = 'vikash'
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    teststep = db.Column(db.String(20))
    testcase = db.Column(db.String(20))
    description = db.Column(db.Text())
    url = db.Column(db.String(100))
    status = db.Column(db.Integer)
    authkey = db.Column(db.String(100))

    def __init__(self, teststep, testcase, description, url, status, authkey):
        self.teststep = teststep
        self.testcase = testcase
        self.description = description
        self.url = url
        self.status = status
        self.authkey = authkey


# Test Schema
class TestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'teststep', 'testcase', 'description', 'url', 'status', 'authkey')


test_schema = TestSchema()
tests_schema = TestSchema(many=True)


@app.route('/')
def form():
    return render_template('form.html')


def to_pretty_json(value):
    return json.dumps(value, sort_keys=False,
                      indent=4, separators=(',', ': '))


app.jinja_env.filters['tojson_pretty'] = to_pretty_json


# Create a Product
@app.route('/rest', methods=['POST', 'GET'])
def get_product():
    if request.method == 'POST':
        teststep = request.form['teststep']
        testcase = request.form['testcase']
        description = request.form['description']
        url = request.form['url']
        status = request.form.get('status')
        authkey = request.form['key']
        new_test = Test(teststep, testcase, description, url, status, authkey)
        db.session.add(new_test)
        db.session.commit()
        flash("Data added to database.", "success")
        return redirect(request.referrer)
    else:
        all_products = Test.query.all()
        result = tests_schema.dump(all_products)
        return render_template('response.html', result=to_pretty_json(result))


# Get Single Products
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update_product(id):
    test = Test.query.get_or_404(id)
    if request.method == 'POST':
        try:
            test.teststep = request.form['teststep']
            test.testcase = request.form['testcase']
            test.description = request.form['description']
            test.url = request.form['url']
            test.status = request.form['status']
            test.authkey = request.form['key']
            db.session.commit()
            flash("Data updated successfully!", "success")
        except Exception:
            return 'There is an issue updating your data'
        return redirect(request.referrer)
    else:
        return render_template('update.html', test=test)


@app.route('/delete/<int:id>')
def delete_product(id):
    try:
        test = Test.query.get_or_404(id)
        db.session.delete(test)
        db.session.commit()
        return redirect('/rest')
    except Exception:
        return 'The data you want to detele already deleted by someone.'


@app.route('/all', methods=['POST', 'GET'])
def show():
    all_products = Test.query.all()
    return render_template("detail.html", data=all_products)


# Run Server
if __name__ == '__main__':
    app.run()
