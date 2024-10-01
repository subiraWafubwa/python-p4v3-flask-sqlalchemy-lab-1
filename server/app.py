# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
    else:
        return jsonify({
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
        })
        
@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude)

    quake_list = []
    
    for earthquake in earthquakes:
        quake_list.append({
            "id": earthquake.id,
            "magnitude": earthquake.magnitude,
            "location": earthquake.location,
            "year": earthquake.year
        })
    return jsonify({
        "count": len(quake_list),
        "quakes": quake_list

    })
     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
