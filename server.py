from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initiailize DB
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self, name, desc, price, qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price', 'desc', 'qty')

# Initialize Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(strict=True, many=True)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
