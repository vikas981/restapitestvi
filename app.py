from flask import Flask, render_template, url_for, request, redirect, flash, session, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teststep = db.Column(db.String(20), nullable=False)
    testcase = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __init__(self, teststep, testcase, description):
        self.teststep = teststep
        self.testcase = testcase
        self.description = description


# Test Schema
class TestSchema(ma.Schema):
    class Meta:
        fields = ('id', 'teststep', 'testcase', 'description')


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
        new_test = Test(teststep, testcase, description)
        db.session.add(new_test)
        db.session.commit()
        return redirect('/rest')
    else:
        all_products = Test.query.all()
        result = tests_schema.dump(all_products)
        return jsonify(result)


# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


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
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
