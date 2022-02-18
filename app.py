from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Marathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    country = db.Column(db.String(200))
    date = db.Column(db.String(200))

    def __init__(self, name, country, date):
        self.name = name
        self.country = country
        self.date = date

class MarathonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'country', 'date')

marathon_schema = MarathonSchema()
marathons_schema = MarathonSchema(many=True)

@app.route('/marathon', methods = ['POST'])
def add_marathon():
    name = request.json['name']
    country = request.json['country']
    date = request.json['date']

    new_marathon = Marathon(name,country,date)

    db.session.add(new_marathon)
    db.session.commit()

    return marathon_schema.jsonify(new_marathon)

@app.route('/marathon', methods = ['GET'])
def get_marathons():
    all_marathons = Marathon.query.all()
    result = marathon_schema.dump(all_marathons, many=True)
    return jsonify(result)

@app.route('/marathon/delete/<id>', methods = ['DELETE'])
def delete_marathon(id):
    marathon = Marathon.query.get(id)
    db.session.delete(marathon)
    db.session.commit()
    return marathon_schema.jsonify(marathon)

@app.route('/', methods = ['GET'])
def get():
    return jsonify({'msg':'Hello World'})

if __name__ == '__main__':
    app.run(debug=True)