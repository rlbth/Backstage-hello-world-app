from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///truckrental.db'
db = SQLAlchemy(app)

class Truck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

@app.route('/trucks', methods=['GET'])
def list_trucks():
    trucks = Truck.query.filter_by(is_available=True).all()
    return jsonify([{'make': truck.make, 'model': truck.model} for truck in trucks])

@app.route('/trucks', methods=['POST'])
def add_truck():
    data = request.json
    new_truck = Truck(make=data['make'], model=data['model'], is_available=True)
    db.session.add(new_truck)
    db.session.commit()
    return jsonify({'message': 'Truck added successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)