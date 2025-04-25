from flask import Flask, jsonify, request, send_file, render_template
from repository.database import db
from models.payment import Payment
from payments.pix import Pix
from datetime import datetime, timedelta
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

# Load dotenv
load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SECRET_KEY']= os.getenv('FLASK_SECRET_KEY')

db.init_app(app)

# Inicializing SocketIO
socketio = SocketIO(app)

# Create pix payment
@app.route('/payments/pix', methods=['POST'])
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "Invalid value."}), 400
    
    # Get the actual datetime and add 30 minutes
    expiration_date = datetime.now() + timedelta(minutes=30) 

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['payment_bank_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has been created.",
                    "payment": new_payment.to_dict()})

# Create Qr Code
@app.route('/payments/pix/qr_code/<file_name>', methods=['GET'])
def get_image(file_name):
    return send_file(f"static/img/{file_name}.png", mimetype="image/png")

# Recieve payment confirmation (Webhook)
@app.route('/payments/pix/confirmation', methods=['POST'])
def pix_confirmation():
    data = request.get_json()

    if "bank_payment_id" not in data and "value" not in data:
        return jsonify({"message": "Invalid payment data"}), 400

    payment = Payment.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment or payment.paid:
        return jsonify({"message": "Payment not founded"}), 404
    
    if data.get("value") != payment.value:
        return jsonify({"message": "Invalid payment data"})
    
    payment.paid = True
    db.session.commit()

    # Send notification to connected clients
    socketio.emit(f"payment-confirmed-{payment.id}")

    return jsonify({"message": "The payment has been confirmed."})

# Show payment has been confirmed (Websocket)
@app.route('/payments/pix/<int:payment_id>', methods=['GET'])
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)

    # Payment not found
    if not payment:
        return render_template("404.html")

    # Confirmed payment page
    if payment.paid:

       return render_template("confirmed_payment.html", 
                           payment_id=payment.id, 
                           value=payment.value)
    
    # Payment page
    else:

        return render_template("payment.html", 
                            payment_id=payment.id, 
                            value=payment.value,
                            host=os.getenv('HOST'), 
                            qr_code=payment.qr_code)

@app.route('/', methods=['GET'])
def initial_page():
    return "Payment API"

# Implementing connected server Websockets
@socketio.on('connect')
def handle_connect():
    print("Client connected to the server.")

# Implementing disconnected server Websockets
@socketio.on('disconnect')
def handle_disconnect():
    print("Client has disconnected to the server.")

if __name__ == '__main__':
    socketio.run(app, debug=True)