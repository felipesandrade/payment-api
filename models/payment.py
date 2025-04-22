from repository.database import db

class Payment(db.Model):
    # id, value, paid, bank_payment_id, qr_code, expiration_date
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    bank_payment_id = db.Column(db.Integer, nullable=True)
    qr_code = db.Column(db.String, nullable=True)
    expiration_date = db.Column(db.DateTime, nullable=True)