from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/your_database'
db = SQLAlchemy(app)

class Registration(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    DateOfBirth = db.Column(db.Date, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())
    UpdatedAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

@app.route('/register', methods=['POST'])
def create_registration():
    data = request.get_json()
    new_registration = Registration(Name=data['Name'], Email=data['Email'], DateOfBirth=data['DateOfBirth'])
    db.session.add(new_registration)
    db.session.commit()
    return jsonify({'message': 'Registration successful!'}), 201

@app.route('/registrations', methods=['GET'])
def read_registrations():
    registrations = Registration.query.all()
    return jsonify([{'ID': reg.ID, 'Name': reg.Name, 'Email': reg.Email, 'DateOfBirth': reg.DateOfBirth} for reg in registrations])

@app.route('/register/<int:id>', methods=['PUT'])
def update_registration(id):
    data = request.get_json()
    registration = Registration.query.get(id)
    if registration:
        registration.Name = data['Name']
        registration.Email = data['Email']
        registration.DateOfBirth = data['DateOfBirth']
        db.session.commit()
        return jsonify({'message': 'Registration updated!'})
    return jsonify({'message': 'Registration not found!'}), 404

@app.route('/register/<int:id>', methods=['DELETE'])
def delete_registration(id):
    registration = Registration.query.get(id)
    if registration:
        db.session.delete(registration)
        db.session.commit()
        return jsonify({'message': 'Registration deleted!'})
    return jsonify({'message': 'Registration not found!'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
