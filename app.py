from flask import Flask, render_template, url_for, request, redirect, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json

# Init app
app = Flask(__name__)
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'vikash'
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teststep = db.Column(db.String(20), nullable=False)
    testcase = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    authkey = db.Column(db.String(100), nullable=False)

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


# Create a Product
@app.route('/rest', methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        teststep = request.form['teststep']
        testcase = request.form['testcase']
        description = request.form['description']
        url = request.form['url']
        print(url)
        status = request.form['status']
        print(status)
        authkey = request.form['key']
        new_test = Test(teststep, testcase, description, url, status, authkey)
        db.session.add(new_test)
        db.session.commit()
        flash("Data added to database.", "success")
        return redirect(request.referrer)
    else:
        all_products = Test.query.all()
        result = tests_schema.dump(all_products)
        return render_template('response.html', result=json.dumps(result), sort_keys=True,
                               indent=4)


# Get Single Products
@app.route('/update/<id>', methods=['POST', 'GET'])
def get_product(id):
    test = Test.query.get_or_404(id)
    if request.method == 'POST':
        test.teststep = request.form['teststep']
        test.testcase = request.form['testcase']
        test.description = request.form['description']
        test.url = request.form['url']
        test.status = request.form['status']
        test.authkey = request.form['key']
        db.session.commit()
        flash("Your data has been updated!", "success")
        return redirect(request.referrer)
    else:
        return render_template('update.html', test=test)


# Update a Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']
    product.name = name
    product.description = description
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)
# Delete Product
@app.route('/delete/<id>', methods=['DELETE'])
def delete_product(id):
    test = Test.query.get(id)
    db.session.delete(test)
    db.session.commit()
    return product_schema.jsonify(test)

# Run Server
if __name__ == '__main__':
    app.run(debug=True)
