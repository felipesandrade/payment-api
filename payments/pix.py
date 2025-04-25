import uuid
import qrcode

class Pix():
    def __init__(self):
        pass

    def create_payment(self):
        # Create the payment at the bank
        bank_payment_id = str(uuid.uuid4())

        # Copie and paste pix
        hash_payment = f"hash_payment_{bank_payment_id}"

        # Qr Code
        img = qrcode.make(hash_payment)
        # Save qrcode image as png
        img.save(f"static/img/qr_code_payment_{bank_payment_id}.png")
        
        return {
                "payment_bank_id": bank_payment_id,
                "qr_code_path": f"qr_code_payment_{bank_payment_id}" 
                }