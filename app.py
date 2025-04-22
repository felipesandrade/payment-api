from flask import Flask, jsonify
from repository.database import db
from models.payment import Payment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =''
app.config['SECRET_KEY']= ''

db.init_app(app)

# Pix payments route
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    return jsonify({"message": "The payment has been created."})

# Recieve payment confirmation (Webhook)
@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    return jsonify({"message": "The payment has been confirmed"})

# Show payment has been confirmed (Websocket)
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    return jsonify({"message": "Pix payment."})

@app.route('/', methods=['GET'])
def initial_page():
    return "Payment API"

if __name__ == '__main__':
    app.run(debug=True)