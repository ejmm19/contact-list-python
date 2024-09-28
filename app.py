from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# init configs
app = Flask(__name__)
app.config.from_mapping(
    DEBUG=True,
    SECRET_KEY='prod_987928392',
    SQLALCHEMY_DATABASE_URI='sqlite:///api_contact.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@mysql:3309/api_contact'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_password@localhost:3309/api_contact'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# create models
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(11), unique=True, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

#migrate apply
with app.app_context():
    db.create_all()

# Routes
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify({'contacts': [contact.serialize() for contact in contacts]})

@app.route('/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'data is empty'}), 400
    is_exist = Contact.query.filter_by(name=data['name']).first()
    if is_exist:
        return jsonify({'message': 'Contact with this data already exists.'}), 400
    contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(contact)
    db.session.commit()
    return jsonify({'contact': contact.serialize()}), 201

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    return jsonify({'contact': contact.serialize()})

@app.route('/contacts/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    data = request.get_json()
    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']

    db.session.commit()
    return jsonify({'message': 'item updated successful', 'contact': contact.serialize()}), 200

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return not_found()
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'item delete successful'}), 200

def not_found():
    return jsonify({'message': 'not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
