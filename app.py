from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from databaseCode import theString

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database

ENV = 'prod'



if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = databaseCode.theString


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)

# Dessert List
class Dessert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    culture = db.Column(db.String(15))
    popularity = db.Column(db.Integer)
    dairy = db.Column(db.Boolean)
    nuts = db.Column(db.Boolean)
    egg = db.Column(db.Boolean)
    meat = db.Column(db.Boolean)
    url = db.Column(db.String(500))

    def __init__(self, name, culture, popularity, dairy, nuts, egg, meat, url):
        self.name = name
        self.culture = culture
        self.popularity = popularity
        self.dairy = dairy
        self.nuts = nuts
        self.egg = egg
        self.meat = meat
        self.url = url

# Dessert Schema
class DessertSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'culture', 'popularity', 'dairy', 'nuts', 'egg', 'meat', 'url')

# Init schema
dessert_schema = DessertSchema()
desserts_schema = DessertSchema(many=True)

# CRUD Options:

# Create Dessert
@app.route('/dessert', methods=['POST'])
def add_dessert():
    name = request.json['name']
    culture = request.json['culture']
    popularity = request.json['[popularity]']
    dairy = request.json['dairy']
    nuts = request.json['nuts']
    egg = request.json['egg']
    meat = request.json['meat']
    url = request.json['url']

    new_dessert = Dessert(name, culture, popularity, dairy, nuts, egg, meat, url)

    db.session.add(new_dessert)

    db.session.commit()

    return dessert_schema.jsonify(new_dessert)


# Read (Get) all desserts
@app.route('/dessert', methods=['GET'])
def get_desserts():
    all_desserts = Dessert.query.all()
    result = desserts_schema.dump(all_desserts)
    return jsonify(result)

# Read (Get) one dessert
@app.route('/dessert/<id>', methods=['GET'])
def get_dessert(id):
    dessert = Dessert.query.get(id)
    return dessert_schema.jsonify(dessert)

# Update a dessert
@app.route('/dessert/<id>', methods=['PUT'])
def update_dessert(id):
    dessert = Dessert.query.get(id)

    name = request.json['name']
    culture = request.json['culture']
    popularity = request.json['[popularity]']
    dairy = request.json['dairy']
    nuts = request.json['nuts']
    egg = request.json['egg']
    meat = request.json['meat']
    url = request.json['url']

    dessert.name = name
    dessert.culture = culture
    dessert.popularity = popularity
    dessert.dairy = dairy
    dessert.nuts = nuts
    dessert.egg = egg
    dessert.meat = meat
    dessert.url = url

    db.session.commit()

    return dessert_schema.jsonify(dessert)

# Delete one dessert
@app.route('/dessert/<id>', methods=['DELETE'])
def delete_dessert(id):
    dessert = Dessert.query.get(id)

    db.session.delete(dessert)
    db.session.commit()

    return dessert_schema.jsonify(dessert)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
