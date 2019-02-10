import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

# Init app
app = Flask(__name__, static_url_path='')
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

# User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    def __init__(self, firstName, lastName, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desc', 'price', 'qty')

# User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password')

# Initialize Schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(strict=True, many=True)
user_schema = UserSchema(strict=True)

# File serving routes

# METHOD: GET
# ROUTE:  /
# ACCESS: PUBLIC
# DESC:   Root
@app.route('/', methods=['GET'])
def root():
    return app.send_static_file('index.html')

# METHOD: GET
# ROUTE:  /login
# ACCESS: PUBLIC
# DESC:   Serve login page
@app.route('/login', methods=['GET'])
def serve_login():
    return app.send_static_file('login.html')

# METHOD: GET
# ROUTE:  /register
# ACCESS: PUBLIC
# DESC:   Serve register page
@app.route('/register', methods=['GET'])
def serve_register():
    return app.send_static_file('register.html')

# METHOD: GET
# ROUTE:  /catalogue
# ACCESS: PUBLIC
# DESC:   Serve catalogue page
@app.route('/catalogue', methods=['GET'])
def serve_catalogue():
    return app.send_static_file('catalogue.html')

# METHOD: None
# ROUTE:  Any
# ACCESS: PUBLIC
# DESC:   404 Handler
@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('404.html')


# Routes

# METHOD: GET
# ROUTE:  /products
# ACCESS: PUBLIC
# DESC:   Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    result = products_schema.dump(products)
    return products_schema.jsonify(result)

# METHOD: GET
# ROUTE:  /products/<id>
# ACCESS: PUBLIC
# DESC:   Get single product via ID
@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

# METHOD: POST
# ROUTE:  /products
# ACCESS: PRIVATE
# DESC:   Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    new_product = Product(name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

# METHOD: PUT
# ROUTE:  /products/<id>
# ACCESS: PRIVATE
# DESC:   Edit a product
@app.route('/products/<id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']
    product.name = name
    product.desc = desc
    product.price = price
    product.qty = qty
    db.session.commit()
    return product_schema.jsonify(product)

# METHOD: DELETE
# ROUTE:  /products/<id>
# ACCESS: PRIVATE
# DESC:   Delete a product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.remove(product)
    db.session.commit()
    return product_schema.jsonify(product)

# METHOD: POST
# ROUTE:  /register
# ACCESS: PUBLIC
# DESC:   Register a new user
@app.route('/register', methods=['POST'])
def register_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    email = request.json['email']
    password = generate_password_hash(request.json['password'])
    new_user = User(firstName, lastName, email, password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

# METHOD: POST
# ROUTE:  /login
# ACCESS: PUBLIC
# DESC:   Login a new user
@app.route('/login', methods=['POST'])
def login_user():
    user = User.query.filter_by(email = request.json['email']).first()
    if user:
        if check_password_hash(user.password, request.json['password']) == True:
            return user_schema.jsonify(user)
        else:
            return 'Incorrect Password.'    
    else:
        return 'User does not exist.'

# Run server
if __name__ == '__main__':
    app.run(debug=True)
